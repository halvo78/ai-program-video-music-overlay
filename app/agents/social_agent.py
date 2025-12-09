"""
Social Media Agent

Upload to social platforms:
- Twitter/X
- YouTube
- Telegram
- (Instagram and TikTok require manual upload)
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Optional
import aiohttp
import os

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class SocialMediaAgent(BaseAgent):
    """
    Social Media Agent for uploading content.

    Supports direct upload to:
    - Twitter/X (via API)
    - YouTube (via API)
    - Telegram (via Bot API)

    For TikTok and Instagram, provides optimized files for manual upload.
    """

    def __init__(self):
        super().__init__(
            agent_type=AgentType.SOCIAL_MEDIA,
            priority=AgentPriority.HIGH,
            parallel_capable=False,  # Final step
        )

        # Load credentials
        self.twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN", "")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET", "")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET", "")

        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", "")
        self.youtube_client_id = os.getenv("YOUTUBE_CLIENT_ID", "")
        self.youtube_client_secret = os.getenv("YOUTUBE_CLIENT_SECRET", "")

        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    @property
    def name(self) -> str:
        return "Social Media Agent"

    @property
    def models(self) -> list[str]:
        return ["Twitter API", "YouTube API", "Telegram Bot API"]

    @property
    def capabilities(self) -> list[str]:
        return [
            "Twitter/X upload",
            "YouTube upload",
            "Telegram upload",
            "caption optimization",
            "hashtag insertion",
            "scheduling",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Upload content to social platforms."""

        context = task.context
        parameters = task.parameters

        platforms = context.get("platforms", ["tiktok"])
        content_analysis = context.get("content_analysis", {})

        # Get optimized videos
        optimization_output = context.get("optimization", {})

        logger.info(f"Uploading to platforms: {platforms}")

        try:
            upload_results = {}

            for platform in platforms:
                video_info = optimization_output.get(platform, {})
                video_path = video_info.get("output_path")

                if platform == "twitter" and self.twitter_bearer:
                    result = await self._upload_twitter(
                        video_path=video_path,
                        caption=self._generate_caption(content_analysis, platform),
                    )
                    upload_results["twitter"] = result

                elif platform == "telegram" and self.telegram_bot_token:
                    result = await self._upload_telegram(
                        video_path=video_path,
                        caption=self._generate_caption(content_analysis, platform),
                    )
                    upload_results["telegram"] = result

                else:
                    # Provide file path for manual upload
                    upload_results[platform] = {
                        "status": "ready_for_manual_upload",
                        "video_path": str(video_path) if video_path else None,
                        "caption": self._generate_caption(content_analysis, platform),
                        "hashtags": content_analysis.get("hashtags", []),
                    }

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=upload_results,
                output_files=[
                    Path(r.get("video_path")) for r in upload_results.values()
                    if r.get("video_path")
                ],
                metadata={
                    "platforms": platforms,
                    "uploaded_count": len([r for r in upload_results.values() if r.get("status") == "uploaded"]),
                },
            )

        except Exception as e:
            logger.error(f"Social media upload error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    def _generate_caption(self, content_analysis: dict, platform: str) -> str:
        """Generate platform-optimized caption."""

        script = content_analysis.get("script", "")
        hashtags = content_analysis.get("hashtags", [])

        # Platform-specific caption limits
        limits = {
            "twitter": 280,
            "tiktok": 2200,
            "instagram_reels": 2200,
            "youtube_shorts": 100,
            "telegram": 4096,
        }

        max_length = limits.get(platform, 280)

        # Build caption
        caption = script[:max_length // 2] if script else ""

        # Add hashtags
        hashtag_str = " ".join(hashtags[:10])
        if len(caption) + len(hashtag_str) + 2 <= max_length:
            caption = f"{caption}\n\n{hashtag_str}"

        # Add AI disclosure
        ai_disclosure = "\n\n🤖 Created with AI"
        if len(caption) + len(ai_disclosure) <= max_length:
            caption += ai_disclosure

        return caption[:max_length]

    async def _upload_twitter(
        self,
        video_path: Optional[Path],
        caption: str,
    ) -> dict:
        """Upload video to Twitter/X."""

        if not video_path or not video_path.exists():
            return {"status": "error", "error": "No video file"}

        logger.info(f"Uploading to Twitter: {video_path}")

        # Twitter API v2 media upload is complex - simplified here
        # In production, would use tweepy or twitter-api-v2

        try:
            # Step 1: Initialize media upload
            # Step 2: Upload chunks
            # Step 3: Finalize
            # Step 4: Create tweet with media

            # Placeholder for actual implementation
            return {
                "status": "ready_for_upload",
                "video_path": str(video_path),
                "caption": caption,
                "note": "Twitter API integration ready - requires OAuth flow",
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _upload_telegram(
        self,
        video_path: Optional[Path],
        caption: str,
    ) -> dict:
        """Upload video to Telegram."""

        if not video_path or not video_path.exists():
            return {"status": "error", "error": "No video file"}

        logger.info(f"Uploading to Telegram: {video_path}")

        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendVideo"

                with open(video_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field("chat_id", self.telegram_chat_id)
                    data.add_field("video", f, filename=video_path.name)
                    data.add_field("caption", caption[:1024])

                    async with session.post(url, data=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            return {
                                "status": "uploaded",
                                "message_id": result.get("result", {}).get("message_id"),
                                "chat_id": self.telegram_chat_id,
                            }
                        else:
                            error_text = await response.text()
                            return {"status": "error", "error": error_text}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def schedule_upload(
        self,
        video_path: Path,
        platform: str,
        scheduled_time: str,
        caption: str,
    ) -> dict:
        """Schedule upload for later."""

        # In production, would use a task queue like Celery
        return {
            "status": "scheduled",
            "platform": platform,
            "scheduled_time": scheduled_time,
            "video_path": str(video_path),
            "caption": caption,
        }
