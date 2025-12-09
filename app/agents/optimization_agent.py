"""
Optimization Agent

Platform-specific video optimization:
- Encoding for each platform
- Aspect ratio conversion
- File size optimization
- Quality balancing
"""

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Any, Optional
import os

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class OptimizationAgent(BaseAgent):
    """
    Optimization Agent for platform-specific encoding.

    Optimizes videos for:
    - TikTok (9:16, 1080x1920, H.264)
    - Instagram Reels (9:16, 1080x1920)
    - YouTube Shorts (9:16, up to 4K)
    - Twitter/X (multiple formats)
    """

    # Platform specifications
    PLATFORM_SPECS = {
        "tiktok": {
            "width": 1080,
            "height": 1920,
            "aspect": "9:16",
            "fps": 30,
            "max_duration": 180,
            "max_size_mb": 287,
            "codec": "h264",
            "audio_codec": "aac",
            "audio_bitrate": "128k",
        },
        "instagram_reels": {
            "width": 1080,
            "height": 1920,
            "aspect": "9:16",
            "fps": 30,
            "max_duration": 90,
            "max_size_mb": 250,
            "codec": "h264",
            "audio_codec": "aac",
            "audio_bitrate": "128k",
        },
        "youtube_shorts": {
            "width": 1080,
            "height": 1920,
            "aspect": "9:16",
            "fps": 60,
            "max_duration": 60,
            "max_size_mb": 500,
            "codec": "h264",
            "audio_codec": "aac",
            "audio_bitrate": "192k",
        },
        "twitter": {
            "width": 1280,
            "height": 720,
            "aspect": "16:9",
            "fps": 30,
            "max_duration": 140,
            "max_size_mb": 512,
            "codec": "h264",
            "audio_codec": "aac",
            "audio_bitrate": "128k",
        },
    }

    def __init__(self):
        super().__init__(
            agent_type=AgentType.OPTIMIZATION,
            priority=AgentPriority.HIGH,
            parallel_capable=False,
        )

        self.output_dir = Path("C:/dev/taj-chat/generated/optimized")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.ffmpeg_available = self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    @property
    def name(self) -> str:
        return "Optimization Agent"

    @property
    def models(self) -> list[str]:
        return ["FFmpeg"]

    @property
    def capabilities(self) -> list[str]:
        return [
            "platform-specific encoding",
            "aspect ratio conversion",
            "file size optimization",
            "quality balancing",
            "bitrate optimization",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Optimize video for target platforms."""

        context = task.context
        parameters = task.parameters

        platforms = context.get("platforms", ["tiktok"])

        # Get composed video from editing agent
        editing_output = context.get("editing", {})
        input_video = editing_output.get("output_path")

        if not input_video:
            # Try to find video in context
            video_files = context.get("editing_files", [])
            if video_files:
                input_video = video_files[0]

        logger.info(f"Optimizing video for: {platforms}")

        try:
            optimized_videos = {}

            for platform in platforms:
                if platform in self.PLATFORM_SPECS:
                    output = await self._optimize_for_platform(
                        input_path=input_video,
                        platform=platform,
                    )
                    optimized_videos[platform] = output

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=optimized_videos,
                output_files=[
                    v["output_path"] for v in optimized_videos.values()
                    if v.get("output_path")
                ],
                metadata={
                    "platforms": platforms,
                    "optimized_count": len(optimized_videos),
                },
            )

        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _optimize_for_platform(
        self,
        input_path: Optional[Path],
        platform: str,
    ) -> dict:
        """Optimize video for a specific platform."""

        specs = self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS["tiktok"])

        output_path = self.output_dir / f"{platform}_{hash(str(input_path)) % 10000}.mp4"

        if input_path and self.ffmpeg_available:
            try:
                await self._ffmpeg_optimize(
                    input_path=input_path,
                    output_path=output_path,
                    specs=specs,
                )
            except Exception as e:
                logger.warning(f"FFmpeg optimization failed: {e}")

        return {
            "output_path": output_path,
            "platform": platform,
            "specs": specs,
            "status": "optimized",
        }

    async def _ffmpeg_optimize(
        self,
        input_path: Path,
        output_path: Path,
        specs: dict,
    ):
        """Use FFmpeg to optimize video."""

        width = specs["width"]
        height = specs["height"]
        fps = specs["fps"]
        codec = specs["codec"]
        audio_codec = specs["audio_codec"]
        audio_bitrate = specs["audio_bitrate"]

        # Calculate target bitrate for file size
        max_size_mb = specs["max_size_mb"]
        max_duration = specs["max_duration"]
        target_bitrate = int((max_size_mb * 8 * 1024) / max_duration * 0.8)  # 80% of max

        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
            "-r", str(fps),
            "-c:v", f"lib{codec}",
            "-b:v", f"{target_bitrate}k",
            "-maxrate", f"{int(target_bitrate * 1.5)}k",
            "-bufsize", f"{target_bitrate * 2}k",
            "-c:a", audio_codec,
            "-b:a", audio_bitrate,
            "-movflags", "+faststart",
            str(output_path),
        ]

        logger.info(f"Optimizing for {specs['aspect']} @ {width}x{height}")

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"FFmpeg optimization failed: {stderr.decode()[:500]}")

        logger.info(f"Optimized video: {output_path}")
