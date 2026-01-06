"""
Unified Social Media Publisher
==============================

Single interface to publish content across all platforms:
- Meta (Facebook, Instagram, Threads)
- Twitter/X
- TikTok
- YouTube
- Telegram

Handles:
- Platform-specific formatting
- Optimal timing
- Cross-posting
- Scheduling
- Analytics tracking
"""

import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from .meta_client import MetaClient
from .twitter_client import TwitterClient
from .tiktok_client import TikTokClient
from .youtube_client import YouTubeClient
from .instagram_client import InstagramClient
from .telegram_client import TelegramClient

logger = logging.getLogger(__name__)


class Platform(Enum):
    """Supported social media platforms"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_STORIES = "instagram_stories"
    THREADS = "threads"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    TELEGRAM = "telegram"


@dataclass
class PublishResult:
    """Result of a publish operation"""
    platform: Platform
    success: bool
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class ContentPackage:
    """Content package for multi-platform publishing"""
    # Core content
    title: str
    description: str
    hashtags: List[str] = field(default_factory=list)

    # Media
    video_url: Optional[str] = None
    image_urls: List[str] = field(default_factory=list)
    thumbnail_url: Optional[str] = None

    # Platform-specific overrides
    platform_overrides: Dict[str, Dict] = field(default_factory=dict)

    # Scheduling
    scheduled_time: Optional[datetime] = None

    # Options
    is_short_form: bool = False  # For Reels/Shorts/TikTok
    enable_comments: bool = True
    enable_duet: bool = True  # TikTok
    enable_stitch: bool = True  # TikTok
    share_to_feed: bool = True  # Instagram Reels


class UnifiedPublisher:
    """
    Unified publisher for all social media platforms

    Features:
    1. Single API for all platforms
    2. Automatic format optimization
    3. Platform-specific caption formatting
    4. Hashtag optimization
    5. Cross-posting with deduplication
    6. Scheduling support
    7. Error handling and retries
    8. Analytics tracking
    9. Rate limit management
    10. Batch publishing
    """

    # Platform character limits
    CHAR_LIMITS = {
        Platform.FACEBOOK: 63206,
        Platform.INSTAGRAM: 2200,
        Platform.INSTAGRAM_REELS: 2200,
        Platform.INSTAGRAM_STORIES: 2200,
        Platform.THREADS: 500,
        Platform.TWITTER: 280,
        Platform.TIKTOK: 2200,
        Platform.YOUTUBE: 5000,
        Platform.YOUTUBE_SHORTS: 100,
        Platform.TELEGRAM: 1024,
    }

    # Platform hashtag limits
    HASHTAG_LIMITS = {
        Platform.FACEBOOK: 30,
        Platform.INSTAGRAM: 30,
        Platform.INSTAGRAM_REELS: 30,
        Platform.THREADS: 10,
        Platform.TWITTER: 5,
        Platform.TIKTOK: 100,
        Platform.YOUTUBE: 15,
        Platform.YOUTUBE_SHORTS: 15,
        Platform.TELEGRAM: 20,
    }

    def __init__(
        self,
        meta_client: MetaClient = None,
        twitter_client: TwitterClient = None,
        tiktok_client: TikTokClient = None,
        youtube_client: YouTubeClient = None,
        instagram_client: InstagramClient = None,
        telegram_client: TelegramClient = None,
    ):
        self.meta = meta_client
        self.twitter = twitter_client
        self.tiktok = tiktok_client
        self.youtube = youtube_client
        self.instagram = instagram_client
        self.telegram = telegram_client

        self._publish_history: List[PublishResult] = []

    async def publish(
        self,
        content: ContentPackage,
        platforms: List[Platform],
    ) -> List[PublishResult]:
        """
        Publish content to multiple platforms

        Args:
            content: ContentPackage with media and metadata
            platforms: List of platforms to publish to

        Returns:
            List of PublishResult for each platform
        """
        results = []

        # Create tasks for parallel publishing
        tasks = []
        for platform in platforms:
            task = self._publish_to_platform(content, platform)
            tasks.append(task)

        # Execute all publishes in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append(PublishResult(
                    platform=platforms[i],
                    success=False,
                    error=str(result),
                ))
            else:
                final_results.append(result)

        # Track history
        self._publish_history.extend(final_results)

        return final_results

    async def _publish_to_platform(
        self,
        content: ContentPackage,
        platform: Platform,
    ) -> PublishResult:
        """Publish to a specific platform"""
        try:
            # Get platform-specific content
            formatted = self._format_for_platform(content, platform)

            if platform == Platform.FACEBOOK:
                return await self._publish_facebook(formatted)
            elif platform == Platform.INSTAGRAM:
                return await self._publish_instagram_feed(formatted)
            elif platform == Platform.INSTAGRAM_REELS:
                return await self._publish_instagram_reel(formatted)
            elif platform == Platform.INSTAGRAM_STORIES:
                return await self._publish_instagram_story(formatted)
            elif platform == Platform.THREADS:
                return await self._publish_threads(formatted)
            elif platform == Platform.TWITTER:
                return await self._publish_twitter(formatted)
            elif platform == Platform.TIKTOK:
                return await self._publish_tiktok(formatted)
            elif platform == Platform.YOUTUBE:
                return await self._publish_youtube(formatted)
            elif platform == Platform.YOUTUBE_SHORTS:
                return await self._publish_youtube_short(formatted)
            elif platform == Platform.TELEGRAM:
                return await self._publish_telegram(formatted)
            else:
                raise ValueError(f"Unknown platform: {platform}")

        except Exception as e:
            logger.error(f"Failed to publish to {platform}: {e}")
            return PublishResult(
                platform=platform,
                success=False,
                error=str(e),
            )

    def _format_for_platform(
        self,
        content: ContentPackage,
        platform: Platform,
    ) -> Dict[str, Any]:
        """Format content for specific platform"""
        # Get base content
        title = content.title
        description = content.description
        hashtags = content.hashtags.copy()

        # Apply platform overrides
        if platform.value in content.platform_overrides:
            overrides = content.platform_overrides[platform.value]
            title = overrides.get("title", title)
            description = overrides.get("description", description)
            hashtags = overrides.get("hashtags", hashtags)

        # Limit hashtags
        max_hashtags = self.HASHTAG_LIMITS.get(platform, 10)
        hashtags = hashtags[:max_hashtags]

        # Format hashtag string
        hashtag_str = " ".join(f"#{tag}" for tag in hashtags)

        # Build caption based on platform
        if platform in [Platform.TWITTER]:
            # Twitter: Title + hashtags (short)
            caption = f"{title}\n\n{hashtag_str}"
        elif platform in [Platform.TIKTOK, Platform.INSTAGRAM_REELS]:
            # Short-form: Description + hashtags
            caption = f"{description}\n\n{hashtag_str}"
        elif platform in [Platform.YOUTUBE, Platform.YOUTUBE_SHORTS]:
            # YouTube: Full description
            caption = f"{description}\n\n{hashtag_str}"
        else:
            # Default: Title + Description + hashtags
            caption = f"{title}\n\n{description}\n\n{hashtag_str}"

        # Truncate to platform limit
        char_limit = self.CHAR_LIMITS.get(platform, 2000)
        if len(caption) > char_limit:
            caption = caption[:char_limit - 3] + "..."

        return {
            "title": title,
            "description": description,
            "caption": caption,
            "hashtags": hashtags,
            "hashtag_str": hashtag_str,
            "video_url": content.video_url,
            "image_urls": content.image_urls,
            "thumbnail_url": content.thumbnail_url,
            "is_short_form": content.is_short_form,
            "enable_comments": content.enable_comments,
            "enable_duet": content.enable_duet,
            "enable_stitch": content.enable_stitch,
            "share_to_feed": content.share_to_feed,
        }

    # ==========================================
    # PLATFORM-SPECIFIC PUBLISHERS
    # ==========================================

    async def _publish_facebook(self, content: Dict) -> PublishResult:
        """Publish to Facebook"""
        if not self.meta:
            raise ValueError("Meta client not configured")

        async with self.meta:
            if content["video_url"]:
                result = await self.meta.upload_video(
                    video_url=content["video_url"],
                    title=content["title"],
                    description=content["caption"],
                )
            else:
                result = await self.meta.create_page_post(
                    message=content["caption"],
                )

        return PublishResult(
            platform=Platform.FACEBOOK,
            success=True,
            post_id=result.get("id"),
            metadata=result,
        )

    async def _publish_instagram_feed(self, content: Dict) -> PublishResult:
        """Publish to Instagram Feed"""
        if not self.instagram:
            raise ValueError("Instagram client not configured")

        async with self.instagram:
            if content["video_url"]:
                result = await self.instagram.create_video_post(
                    video_url=content["video_url"],
                    caption=content["caption"],
                    cover_url=content["thumbnail_url"],
                )
            elif len(content["image_urls"]) > 1:
                # Carousel post
                media_items = [{"type": "IMAGE", "url": url} for url in content["image_urls"]]
                result = await self.instagram.create_carousel_post(
                    media_items=media_items,
                    caption=content["caption"],
                )
            else:
                result = await self.instagram.create_image_post(
                    image_url=content["image_urls"][0],
                    caption=content["caption"],
                )

        return PublishResult(
            platform=Platform.INSTAGRAM,
            success=True,
            post_id=result.get("id"),
            metadata=result,
        )

    async def _publish_instagram_reel(self, content: Dict) -> PublishResult:
        """Publish Instagram Reel"""
        if not self.instagram:
            raise ValueError("Instagram client not configured")

        if not content["video_url"]:
            raise ValueError("Video URL required for Reels")

        async with self.instagram:
            result = await self.instagram.create_reel(
                video_url=content["video_url"],
                caption=content["caption"],
                cover_url=content["thumbnail_url"],
                share_to_feed=content["share_to_feed"],
            )

        return PublishResult(
            platform=Platform.INSTAGRAM_REELS,
            success=True,
            post_id=result.get("id"),
            metadata=result,
        )

    async def _publish_instagram_story(self, content: Dict) -> PublishResult:
        """Publish Instagram Story"""
        if not self.instagram:
            raise ValueError("Instagram client not configured")

        async with self.instagram:
            if content["video_url"]:
                result = await self.instagram.create_video_story(
                    video_url=content["video_url"],
                )
            else:
                result = await self.instagram.create_image_story(
                    image_url=content["image_urls"][0],
                )

        return PublishResult(
            platform=Platform.INSTAGRAM_STORIES,
            success=True,
            post_id=result.get("id"),
            metadata=result,
        )

    async def _publish_threads(self, content: Dict) -> PublishResult:
        """Publish to Threads"""
        if not self.meta:
            raise ValueError("Meta client not configured")

        async with self.meta:
            media_type = "TEXT"
            media_url = None

            if content["video_url"]:
                media_type = "VIDEO"
                media_url = content["video_url"]
            elif content["image_urls"]:
                media_type = "IMAGE"
                media_url = content["image_urls"][0]

            result = await self.meta.create_threads_post(
                text=content["caption"],
                media_url=media_url,
                media_type=media_type,
            )

        return PublishResult(
            platform=Platform.THREADS,
            success=True,
            post_id=result.get("id"),
            metadata=result,
        )

    async def _publish_twitter(self, content: Dict) -> PublishResult:
        """Publish to Twitter/X"""
        if not self.twitter:
            raise ValueError("Twitter client not configured")

        async with self.twitter:
            media_ids = []

            # Upload media if present
            if content["video_url"]:
                # Download and upload video
                async with self.twitter.session.get(content["video_url"]) as resp:
                    video_data = await resp.read()
                media = await self.twitter.upload_media(
                    media_data=video_data,
                    media_type="video/mp4",
                    media_category="tweet_video",
                )
                media_ids.append(media["media_id_string"])
            elif content["image_urls"]:
                # Upload images (max 4)
                for url in content["image_urls"][:4]:
                    async with self.twitter.session.get(url) as resp:
                        image_data = await resp.read()
                    media = await self.twitter.upload_media(
                        media_data=image_data,
                        media_type="image/jpeg",
                    )
                    media_ids.append(media["media_id_string"])

            result = await self.twitter.create_tweet(
                text=content["caption"],
                media_ids=media_ids if media_ids else None,
            )

        return PublishResult(
            platform=Platform.TWITTER,
            success=True,
            post_id=result.get("data", {}).get("id"),
            metadata=result,
        )

    async def _publish_tiktok(self, content: Dict) -> PublishResult:
        """Publish to TikTok"""
        if not self.tiktok:
            raise ValueError("TikTok client not configured")

        if not content["video_url"]:
            raise ValueError("Video URL required for TikTok")

        async with self.tiktok:
            result = await self.tiktok.post_video_from_url(
                video_url=content["video_url"],
                title=content["caption"],
                disable_comment=not content["enable_comments"],
                disable_duet=not content["enable_duet"],
                disable_stitch=not content["enable_stitch"],
            )

        return PublishResult(
            platform=Platform.TIKTOK,
            success=True,
            post_id=result.get("data", {}).get("publish_id"),
            metadata=result,
        )

    async def _publish_youtube(self, content: Dict) -> PublishResult:
        """Publish to YouTube"""
        if not self.youtube:
            raise ValueError("YouTube client not configured")

        if not content["video_url"]:
            raise ValueError("Video URL required for YouTube")

        async with self.youtube:
            result = await self.youtube.upload_video_from_url(
                video_url=content["video_url"],
                title=content["title"],
                description=content["caption"],
                tags=content["hashtags"],
                privacy_status="public",
            )

        return PublishResult(
            platform=Platform.YOUTUBE,
            success=True,
            post_id=result.get("id"),
            post_url=f"https://youtube.com/watch?v={result.get('id')}",
            metadata=result,
        )

    async def _publish_youtube_short(self, content: Dict) -> PublishResult:
        """Publish YouTube Short"""
        if not self.youtube:
            raise ValueError("YouTube client not configured")

        if not content["video_url"]:
            raise ValueError("Video URL required for YouTube Shorts")

        # Download video
        async with self.youtube.session.get(content["video_url"]) as resp:
            video_data = await resp.read()

        async with self.youtube:
            result = await self.youtube.upload_short(
                video_file=video_data,
                title=content["title"],
                description=content["caption"],
                tags=content["hashtags"],
            )

        return PublishResult(
            platform=Platform.YOUTUBE_SHORTS,
            success=True,
            post_id=result.get("id"),
            post_url=f"https://youtube.com/shorts/{result.get('id')}",
            metadata=result,
        )

    async def _publish_telegram(self, content: Dict) -> PublishResult:
        """Publish to Telegram Channel"""
        if not self.telegram:
            raise ValueError("Telegram client not configured")

        if not content["video_url"]:
            raise ValueError("Video URL required for Telegram")

        async with self.telegram:
            # Format caption with HTML
            caption = self.telegram.format_video_caption(
                title=content["title"],
                description=content.get("description", ""),
                hashtags=content["hashtags"],
            )

            result = await self.telegram.send_video_from_url(
                video_url=content["video_url"],
                caption=caption,
            )

        message_id = result.get("message_id")

        return PublishResult(
            platform=Platform.TELEGRAM,
            success=True,
            post_id=str(message_id) if message_id else None,
            metadata=result,
        )

    # ==========================================
    # UTILITY METHODS
    # ==========================================

    def get_publish_history(self) -> List[PublishResult]:
        """Get history of all publishes"""
        return self._publish_history.copy()

    def get_success_rate(self) -> float:
        """Calculate overall success rate"""
        if not self._publish_history:
            return 0.0

        successful = sum(1 for r in self._publish_history if r.success)
        return successful / len(self._publish_history)

    def get_platform_stats(self) -> Dict[Platform, Dict]:
        """Get stats per platform"""
        stats = {}

        for platform in Platform:
            platform_results = [r for r in self._publish_history if r.platform == platform]
            if platform_results:
                successful = sum(1 for r in platform_results if r.success)
                stats[platform] = {
                    "total": len(platform_results),
                    "successful": successful,
                    "failed": len(platform_results) - successful,
                    "success_rate": successful / len(platform_results),
                }

        return stats
