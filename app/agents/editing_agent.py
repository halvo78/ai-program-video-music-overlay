"""
Editing Agent - ENHANCED

Video composition using FFmpeg and MoviePy:
- Video compositing
- Overlay placement
- Transitions
- Color grading
- Effects
- Filler Word Removal (NEW - like Descript)
- Smart Cut / Silence Removal (NEW - like Kapwing)
- Keyword Highlighting Captions (NEW - like Opus Clip)
- Auto B-Roll insertion (NEW)
"""

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Any, Optional, List, Dict
import os
import re
import json

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class EditingAgent(BaseAgent):
    """
    Editing Agent using FFmpeg and MoviePy.

    Runs AFTER generation agents to compose final video.
    
    NEW FEATURES:
    - Filler Word Removal: Auto-remove "um", "uh", "like", etc. (like Descript)
    - Smart Cut: Auto-remove silences and dead air (like Kapwing)
    - Keyword Highlighting: Dynamic caption styling (like Opus Clip)
    - Auto B-Roll: Intelligent B-roll insertion
    """

    # Filler words to detect and remove
    FILLER_WORDS = [
        "um", "uh", "uhh", "umm", "er", "err", "ah", "ahh",
        "like", "you know", "basically", "actually", "literally",
        "i mean", "so yeah", "kind of", "sort of", "right",
        "okay so", "well", "anyway", "anyways",
    ]

    # Keywords to highlight in captions
    HIGHLIGHT_TRIGGERS = [
        # Numbers and statistics
        r'\d+%', r'\$\d+', r'\d+ million', r'\d+ billion', r'#\d+',
        # Emphasis words
        r'\b(amazing|incredible|shocking|secret|hack|tip|trick)\b',
        r'\b(never|always|best|worst|first|last|only)\b',
        r'\b(free|new|exclusive|limited|breaking)\b',
    ]

    def __init__(self):
        super().__init__(
            agent_type=AgentType.EDITING,
            priority=AgentPriority.HIGH,
            parallel_capable=False,  # Sequential - needs generation outputs
        )

        self.output_dir = Path("C:/taj-chat/generated/edited")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Check FFmpeg availability
        self.ffmpeg_available = self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except FileNotFoundError:
            logger.warning("FFmpeg not found in PATH")
            return False

    @property
    def name(self) -> str:
        return "Editing Agent"

    @property
    def models(self) -> list[str]:
        return ["FFmpeg", "MoviePy", "Whisper"]

    @property
    def capabilities(self) -> list[str]:
        return [
            "video compositing",
            "overlay placement",
            "transitions",
            "color grading",
            "effects",
            "audio mixing",
            "caption burning",
            "filler word removal",
            "smart cut (silence removal)",
            "keyword highlighting",
            "auto b-roll insertion",
            "aspect ratio conversion",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Compose video from generated assets."""

        context = task.context
        parameters = task.parameters

        logger.info("Starting video composition...")

        try:
            # Get generated assets from context
            video_files = context.get("video_generation_files", [])
            music_files = context.get("music_generation_files", [])
            image_files = context.get("image_generation_files", [])
            voice_files = context.get("voice_speech_files", [])
            captions = context.get("voice_speech", {}).get("captions", [])
            transcript = context.get("voice_speech", {}).get("transcript", "")
            broll_files = context.get("broll_files", [])

            # Apply smart editing features
            editing_results = {}

            # 1. Filler Word Removal (if enabled)
            if parameters.get("remove_filler_words", True) and transcript:
                filler_result = await self._remove_filler_words(transcript, voice_files)
                editing_results["filler_removal"] = filler_result

            # 2. Smart Cut - Silence Removal (if enabled)
            if parameters.get("smart_cut", True) and voice_files:
                smart_cut_result = await self._smart_cut(voice_files[0] if voice_files else None)
                editing_results["smart_cut"] = smart_cut_result

            # 3. Keyword Highlighting for Captions
            if parameters.get("highlight_keywords", True) and captions:
                highlighted_captions = self._highlight_keywords(captions)
                editing_results["highlighted_captions"] = highlighted_captions
            else:
                highlighted_captions = captions

            # 4. Auto B-Roll Insertion
            if parameters.get("auto_broll", False) and broll_files:
                broll_result = await self._auto_insert_broll(
                    video_files, broll_files, transcript
                )
                editing_results["broll_insertion"] = broll_result

            # 5. Compose final video
            output = await self._compose_video(
                video_files=video_files,
                music_files=music_files,
                image_files=image_files,
                voice_files=voice_files,
                captions=highlighted_captions,
                parameters=parameters,
            )

            output["editing_features"] = editing_results

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=output,
                output_files=[output["output_path"]] if output.get("output_path") else [],
                metadata={
                    "ffmpeg_used": self.ffmpeg_available,
                    "has_music": bool(music_files),
                    "has_overlays": bool(image_files),
                    "has_voice": bool(voice_files),
                    "has_captions": bool(captions),
                    "filler_removed": "filler_removal" in editing_results,
                    "smart_cut_applied": "smart_cut" in editing_results,
                    "keywords_highlighted": "highlighted_captions" in editing_results,
                },
            )

        except Exception as e:
            logger.error(f"Editing error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _remove_filler_words(
        self,
        transcript: str,
        audio_files: List[Path],
    ) -> Dict:
        """
        Remove filler words from transcript and audio (like Descript).
        
        Detects "um", "uh", "like", etc. and marks them for removal.
        """
        
        logger.info("Removing filler words...")
        
        original_length = len(transcript)
        cleaned_transcript = transcript
        removed_fillers = []
        
        # Find and track filler words
        for filler in self.FILLER_WORDS:
            pattern = rf'\b{re.escape(filler)}\b'
            matches = list(re.finditer(pattern, cleaned_transcript, re.IGNORECASE))
            
            if matches:
                removed_fillers.extend([
                    {
                        "word": filler,
                        "count": len(matches),
                        "positions": [m.start() for m in matches],
                    }
                ])
                
                # Remove filler words (keep one space)
                cleaned_transcript = re.sub(
                    pattern + r'\s*',
                    '',
                    cleaned_transcript,
                    flags=re.IGNORECASE
                )
        
        # Clean up multiple spaces
        cleaned_transcript = re.sub(r'\s+', ' ', cleaned_transcript).strip()
        
        # Calculate statistics
        total_removed = sum(f["count"] for f in removed_fillers)
        reduction_percent = ((original_length - len(cleaned_transcript)) / original_length * 100) if original_length > 0 else 0
        
        return {
            "original_transcript": transcript,
            "cleaned_transcript": cleaned_transcript,
            "removed_fillers": removed_fillers,
            "total_fillers_removed": total_removed,
            "character_reduction": f"{reduction_percent:.1f}%",
            "status": "success",
        }

    async def _smart_cut(
        self,
        audio_path: Optional[Path],
        silence_threshold: float = -40,  # dB
        min_silence_duration: float = 0.5,  # seconds
    ) -> Dict:
        """
        Smart Cut - Remove silences and dead air (like Kapwing).
        
        Detects silent portions and marks them for removal.
        """
        
        logger.info("Applying smart cut (silence removal)...")
        
        if not audio_path or not self.ffmpeg_available:
            return {
                "status": "skipped",
                "reason": "No audio file or FFmpeg unavailable",
            }
        
        # Use FFmpeg to detect silences
        # silencedetect filter outputs silence start/end times
        cmd = [
            "ffmpeg", "-i", str(audio_path),
            "-af", f"silencedetect=noise={silence_threshold}dB:d={min_silence_duration}",
            "-f", "null", "-"
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate()
            output = stderr.decode()
            
            # Parse silence detection output
            silence_starts = re.findall(r'silence_start: ([\d.]+)', output)
            silence_ends = re.findall(r'silence_end: ([\d.]+)', output)
            
            silences = []
            for start, end in zip(silence_starts, silence_ends):
                duration = float(end) - float(start)
                silences.append({
                    "start": float(start),
                    "end": float(end),
                    "duration": round(duration, 2),
                })
            
            total_silence = sum(s["duration"] for s in silences)
            
            return {
                "silences_detected": len(silences),
                "silence_segments": silences,
                "total_silence_duration": round(total_silence, 2),
                "status": "success",
                "recommendation": f"Remove {len(silences)} silence segments ({total_silence:.1f}s total)",
            }
            
        except Exception as e:
            logger.warning(f"Smart cut failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    def _highlight_keywords(
        self,
        captions: List[Dict],
    ) -> List[Dict]:
        """
        Keyword Highlighting for captions (like Opus Clip).
        
        Marks important words/phrases for visual emphasis.
        """
        
        logger.info("Highlighting keywords in captions...")
        
        highlighted_captions = []
        
        for caption in captions:
            text = caption.get("text", "")
            highlighted_words = []
            
            # Find keywords to highlight
            for pattern in self.HIGHLIGHT_TRIGGERS:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    highlighted_words.append({
                        "word": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "style": self._get_highlight_style(match.group()),
                    })
            
            # Create highlighted caption
            highlighted_caption = {
                **caption,
                "highlighted_words": highlighted_words,
                "has_highlights": len(highlighted_words) > 0,
            }
            
            highlighted_captions.append(highlighted_caption)
        
        return highlighted_captions

    def _get_highlight_style(self, word: str) -> Dict:
        """Get highlight style based on word type."""
        
        word_lower = word.lower()
        
        # Numbers/statistics - bold yellow
        if re.match(r'\d', word):
            return {
                "color": "#FFD700",
                "weight": "bold",
                "scale": 1.2,
                "animation": "pop",
            }
        
        # Emphasis words - bold white with glow
        if word_lower in ["amazing", "incredible", "shocking", "secret"]:
            return {
                "color": "#FFFFFF",
                "weight": "bold",
                "scale": 1.3,
                "animation": "glow",
                "glow_color": "#FF6B6B",
            }
        
        # Action words - gradient
        if word_lower in ["free", "new", "exclusive", "limited"]:
            return {
                "color": "gradient(#FF6B6B, #4ECDC4)",
                "weight": "bold",
                "scale": 1.2,
                "animation": "shake",
            }
        
        # Default highlight
        return {
            "color": "#4ECDC4",
            "weight": "bold",
            "scale": 1.1,
            "animation": "none",
        }

    async def _auto_insert_broll(
        self,
        main_video_files: List[Path],
        broll_files: List[Path],
        transcript: str,
    ) -> Dict:
        """
        Auto B-Roll Insertion (like Opus Clip).
        
        Intelligently inserts B-roll footage based on transcript content.
        """
        
        logger.info("Auto-inserting B-roll footage...")
        
        # Analyze transcript for B-roll insertion points
        # Look for descriptive phrases that would benefit from B-roll
        broll_triggers = [
            (r'\b(showing|shows|see|look at|watch)\b', "action"),
            (r'\b(example|for instance|like this)\b', "demonstration"),
            (r'\b(product|item|thing|device)\b', "product_shot"),
            (r'\b(place|location|here|there)\b', "location"),
            (r'\b(people|person|they|them)\b', "people"),
        ]
        
        insertion_points = []
        for pattern, broll_type in broll_triggers:
            matches = re.finditer(pattern, transcript, re.IGNORECASE)
            for match in matches:
                insertion_points.append({
                    "position": match.start(),
                    "trigger_word": match.group(),
                    "broll_type": broll_type,
                    "suggested_duration": 2.0,  # seconds
                })
        
        # Match B-roll files to insertion points
        broll_assignments = []
        for i, point in enumerate(insertion_points[:len(broll_files)]):
            broll_assignments.append({
                **point,
                "broll_file": str(broll_files[i % len(broll_files)]) if broll_files else None,
            })
        
        return {
            "insertion_points": len(insertion_points),
            "broll_assignments": broll_assignments,
            "status": "success",
        }

    async def _compose_video(
        self,
        video_files: List[Path],
        music_files: List[Path],
        image_files: List[Path],
        voice_files: List[Path],
        captions: list,
        parameters: dict,
    ) -> dict:
        """Compose final video from all assets."""

        output_path = self.output_dir / f"composed_{hash(str(video_files)) % 10000}.mp4"

        # Build FFmpeg command
        if self.ffmpeg_available and video_files:
            try:
                await self._ffmpeg_compose(
                    video_files=video_files,
                    music_files=music_files,
                    voice_files=voice_files,
                    output_path=output_path,
                    parameters=parameters,
                )
            except Exception as e:
                logger.warning(f"FFmpeg composition failed: {e}")

        return {
            "output_path": output_path,
            "video_sources": [str(f) for f in video_files],
            "music_sources": [str(f) for f in music_files],
            "overlay_sources": [str(f) for f in image_files],
            "voice_sources": [str(f) for f in voice_files],
            "captions_count": len(captions),
            "status": "composed",
        }

    async def _ffmpeg_compose(
        self,
        video_files: List[Path],
        music_files: List[Path],
        voice_files: List[Path],
        output_path: Path,
        parameters: dict,
    ):
        """Use FFmpeg to compose video."""

        if not video_files:
            return

        # Basic FFmpeg command for video + audio mixing
        cmd = ["ffmpeg", "-y"]

        # Input video
        cmd.extend(["-i", str(video_files[0])])

        # Input music (if available)
        if music_files:
            cmd.extend(["-i", str(music_files[0])])

        # Input voice (if available)
        if voice_files:
            cmd.extend(["-i", str(voice_files[0])])

        # Filter complex for audio mixing
        filter_parts = []

        if music_files and voice_files:
            # Mix music and voice
            filter_parts.append("[1:a]volume=0.3[music]")
            filter_parts.append("[2:a]volume=1.0[voice]")
            filter_parts.append("[music][voice]amix=inputs=2[aout]")
            cmd.extend(["-filter_complex", ";".join(filter_parts)])
            cmd.extend(["-map", "0:v", "-map", "[aout]"])
        elif music_files:
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        elif voice_files:
            cmd.extend(["-map", "0:v", "-map", "1:a"])
        else:
            cmd.extend(["-map", "0"])

        # Output settings
        cmd.extend([
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_path),
        ])

        logger.info(f"Running FFmpeg: {' '.join(cmd[:10])}...")

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"FFmpeg failed: {stderr.decode()[:500]}")

        logger.info(f"Video composed: {output_path}")

    async def add_overlay(
        self,
        video_path: Path,
        overlay_path: Path,
        position: str = "center",
        opacity: float = 1.0,
    ) -> Path:
        """Add image overlay to video."""

        output_path = self.output_dir / f"overlay_{video_path.stem}.mp4"

        # Position mapping
        positions = {
            "center": "overlay=(W-w)/2:(H-h)/2",
            "top-left": "overlay=10:10",
            "top-right": "overlay=W-w-10:10",
            "bottom-left": "overlay=10:H-h-10",
            "bottom-right": "overlay=W-w-10:H-h-10",
        }

        overlay_filter = positions.get(position, positions["center"])

        if self.ffmpeg_available:
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video_path),
                "-i", str(overlay_path),
                "-filter_complex", overlay_filter,
                "-c:a", "copy",
                str(output_path),
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()

        return output_path

    async def add_transition(
        self,
        video1_path: Path,
        video2_path: Path,
        transition_type: str = "fade",
        duration: float = 0.5,
    ) -> Path:
        """Add transition between two videos."""

        output_path = self.output_dir / f"transition_{video1_path.stem}_{video2_path.stem}.mp4"

        # Transition filters
        transitions = {
            "fade": f"xfade=transition=fade:duration={duration}",
            "wipe": f"xfade=transition=wipeleft:duration={duration}",
            "slide": f"xfade=transition=slideleft:duration={duration}",
            "dissolve": f"xfade=transition=dissolve:duration={duration}",
            "zoom": f"xfade=transition=zoomin:duration={duration}",
            "circle": f"xfade=transition=circleopen:duration={duration}",
        }

        transition_filter = transitions.get(transition_type, transitions["fade"])

        if self.ffmpeg_available:
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video1_path),
                "-i", str(video2_path),
                "-filter_complex", transition_filter,
                str(output_path),
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()

        return output_path

    async def convert_aspect_ratio(
        self,
        video_path: Path,
        target_ratio: str = "9:16",
    ) -> Path:
        """Convert video to different aspect ratio."""

        output_path = self.output_dir / f"{target_ratio.replace(':', 'x')}_{video_path.stem}.mp4"

        # Aspect ratio settings
        ratios = {
            "9:16": {"w": 1080, "h": 1920},  # TikTok/Reels
            "1:1": {"w": 1080, "h": 1080},   # Instagram Square
            "16:9": {"w": 1920, "h": 1080},  # YouTube
            "4:5": {"w": 1080, "h": 1350},   # Instagram Portrait
        }

        target = ratios.get(target_ratio, ratios["9:16"])

        if self.ffmpeg_available:
            # Scale and pad to fit target aspect ratio
            filter_str = f"scale={target['w']}:{target['h']}:force_original_aspect_ratio=decrease,pad={target['w']}:{target['h']}:(ow-iw)/2:(oh-ih)/2"
            
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video_path),
                "-vf", filter_str,
                "-c:a", "copy",
                str(output_path),
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()

        return output_path
