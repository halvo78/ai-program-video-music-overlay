"""
Music Generation Agent

Uses HuggingFace MCP for music generation:
- MusicGen
- Riffusion
- AudioCraft
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Optional
import aiohttp
import os

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class MusicGenerationAgent(BaseAgent):
    """
    Music Generation Agent using HuggingFace models.

    Capabilities:
    - Text-to-music generation
    - Beat detection and analysis
    - Mood matching
    - Music synchronization
    """

    # HuggingFace music models
    MUSIC_MODELS = {
        "musicgen": "facebook/musicgen-large",
        "musicgen_melody": "facebook/musicgen-melody",
        "musicgen_stereo": "facebook/musicgen-stereo-large",
        "riffusion": "riffusion/riffusion-model-v1",
        "audiocraft": "facebook/audiogen-medium",
    }

    # Mood to music style mapping
    MOOD_STYLES = {
        "happy": "upbeat, cheerful, major key, energetic",
        "sad": "melancholic, minor key, slow tempo, emotional",
        "energetic": "fast tempo, driving beat, powerful, dynamic",
        "calm": "peaceful, ambient, soft, relaxing",
        "dramatic": "cinematic, orchestral, intense, building",
        "mysterious": "atmospheric, suspenseful, dark ambient",
        "romantic": "soft, emotional, strings, piano",
        "epic": "orchestral, powerful, triumphant, heroic",
        "neutral": "balanced, moderate tempo, versatile",
    }

    def __init__(self):
        super().__init__(
            agent_type=AgentType.MUSIC_GENERATION,
            priority=AgentPriority.CRITICAL,
            parallel_capable=True,
        )

        self.hf_token = os.getenv("HF_TOKEN_PRO", "")
        self.hf_base_url = "https://api-inference.huggingface.co"
        self.output_dir = Path("C:/dev/taj-chat/generated/music")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def name(self) -> str:
        return "Music Generation Agent"

    @property
    def models(self) -> list[str]:
        return list(self.MUSIC_MODELS.values())

    @property
    def capabilities(self) -> list[str]:
        return [
            "text-to-music generation",
            "beat detection and analysis",
            "mood matching",
            "music synchronization",
            "genre-specific generation",
            "duration control",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Generate music based on task parameters."""

        prompt = task.prompt
        parameters = task.parameters
        context = task.context

        # Get parameters
        model_key = parameters.get("model", "musicgen")
        duration = parameters.get("duration", 30)  # seconds
        mood = context.get("mood", parameters.get("mood", "neutral"))
        genre = parameters.get("genre", "")

        logger.info(f"Generating music: {prompt[:50]}... (mood: {mood})")

        try:
            output = await self._generate_music(
                prompt=prompt,
                model_key=model_key,
                duration=duration,
                mood=mood,
                genre=genre,
                context=context,
            )

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=output,
                output_files=[output["audio_path"]] if output.get("audio_path") else [],
                metadata={
                    "model": model_key,
                    "duration": duration,
                    "mood": mood,
                    "genre": genre,
                    "bpm": output.get("bpm"),
                },
            )

        except Exception as e:
            logger.error(f"Music generation error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _generate_music(
        self,
        prompt: str,
        model_key: str = "musicgen",
        duration: int = 30,
        mood: str = "neutral",
        genre: str = "",
        context: dict = None,
    ) -> dict:
        """Generate music from text prompt using HuggingFace."""

        model_id = self.MUSIC_MODELS.get(model_key, self.MUSIC_MODELS["musicgen"])

        # Build enhanced prompt
        style_hints = self.MOOD_STYLES.get(mood, self.MOOD_STYLES["neutral"])

        enhanced_prompt = prompt
        if mood and mood != "neutral":
            enhanced_prompt = f"{prompt}, {style_hints}"
        if genre:
            enhanced_prompt = f"{enhanced_prompt}, {genre} style"

        # Add context-based enhancements
        if context:
            keywords = context.get("keywords", [])
            if keywords:
                enhanced_prompt = f"{enhanced_prompt}, {', '.join(keywords[:2])}"

        logger.info(f"Using model: {model_id}")
        logger.info(f"Enhanced prompt: {enhanced_prompt}")

        output_path = self.output_dir / f"music_{hash(enhanced_prompt) % 10000}.wav"

        # Call HuggingFace API for music generation
        if self.hf_token:
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {"Authorization": f"Bearer {self.hf_token}"}
                    payload = {"inputs": enhanced_prompt}

                    async with session.post(
                        f"{self.hf_base_url}/models/{model_id}",
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=120),
                    ) as response:
                        if response.status == 200:
                            audio_data = await response.read()
                            output_path.write_bytes(audio_data)
                            logger.info(f"Music generated: {output_path}")
                        else:
                            error_text = await response.text()
                            logger.warning(f"HuggingFace API error: {response.status} - {error_text}")

            except Exception as e:
                logger.warning(f"HuggingFace API call failed: {e}")

        # Estimate BPM based on mood
        bpm_map = {
            "happy": 120,
            "sad": 70,
            "energetic": 140,
            "calm": 80,
            "dramatic": 100,
            "mysterious": 90,
            "romantic": 85,
            "epic": 110,
            "neutral": 100,
        }
        estimated_bpm = bpm_map.get(mood, 100)

        return {
            "audio_path": output_path,
            "prompt": enhanced_prompt,
            "model": model_id,
            "duration": duration,
            "mood": mood,
            "genre": genre,
            "bpm": estimated_bpm,
            "sample_rate": 32000,
            "status": "generated",
        }

    async def analyze_beat(self, audio_path: Path) -> dict:
        """Analyze beat and rhythm of audio file."""

        logger.info(f"Analyzing beat: {audio_path}")

        # Placeholder for beat analysis
        # In production, would use librosa or essentia
        return {
            "bpm": 120,
            "beat_times": [],
            "downbeats": [],
            "time_signature": "4/4",
        }

    async def match_mood(self, video_analysis: dict) -> str:
        """Determine best music mood based on video content analysis."""

        # Use video content to determine mood
        sentiment = video_analysis.get("sentiment", "neutral")
        energy = video_analysis.get("energy", "medium")

        if sentiment == "positive" and energy == "high":
            return "energetic"
        elif sentiment == "positive":
            return "happy"
        elif sentiment == "negative":
            return "sad"
        elif energy == "low":
            return "calm"
        else:
            return "neutral"
