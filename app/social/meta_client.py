"""
Meta Platform Complete Integration
==================================

Full integration with Meta's ecosystem:
- Facebook Graph API
- Instagram Graph API
- Threads API
- Facebook Pages API
- Marketing API
- Live Video API
- Webhooks

Documentation: https://developers.facebook.com/docs/
"""

import asyncio
import aiohttp
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class MetaCredentials:
    """Meta API credentials"""
    app_id: str
    app_secret: str
    access_token: str
    page_access_token: Optional[str] = None
    instagram_account_id: Optional[str] = None
    page_id: Optional[str] = None


class MetaClient:
    """
    Complete Meta Platform Integration

    Capabilities:
    1. Authentication & OAuth 2.0
    2. Facebook Page Management
    3. Instagram Content Publishing
    4. Threads API Integration
    5. Video & Reels Upload
    6. Stories Publishing
    7. Live Video Streaming
    8. Analytics & Insights
    9. Audience Management
    10. Marketing & Ads API
    """

    GRAPH_API_VERSION = "v18.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    def __init__(self, credentials: MetaCredentials):
        self.credentials = credentials
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
        files: Dict = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Graph API"""
        url = f"{self.BASE_URL}/{endpoint}"

        params = params or {}
        params["access_token"] = self.credentials.access_token

        async with self.session.request(
            method,
            url,
            params=params,
            json=data,
        ) as response:
            result = await response.json()

            if "error" in result:
                logger.error(f"Meta API Error: {result['error']}")
                raise Exception(f"Meta API Error: {result['error']['message']}")

            return result

    # ==========================================
    # 1. AUTHENTICATION & OAUTH
    # ==========================================

    async def get_long_lived_token(self, short_lived_token: str) -> Dict[str, Any]:
        """Exchange short-lived token for long-lived token"""
        return await self._request(
            "GET",
            "oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": self.credentials.app_id,
                "client_secret": self.credentials.app_secret,
                "fb_exchange_token": short_lived_token,
            }
        )

    async def get_page_access_token(self, page_id: str) -> Dict[str, Any]:
        """Get page access token"""
        return await self._request(
            "GET",
            f"{page_id}",
            params={"fields": "access_token"}
        )

    async def debug_token(self, token: str) -> Dict[str, Any]:
        """Debug and inspect access token"""
        return await self._request(
            "GET",
            "debug_token",
            params={"input_token": token}
        )

    # ==========================================
    # 2. FACEBOOK PAGE MANAGEMENT
    # ==========================================

    async def get_page_info(self, page_id: str = None) -> Dict[str, Any]:
        """Get Facebook page information"""
        page_id = page_id or self.credentials.page_id
        return await self._request(
            "GET",
            page_id,
            params={
                "fields": "id,name,about,category,fan_count,followers_count,link,picture,cover,website"
            }
        )

    async def get_page_posts(
        self,
        page_id: str = None,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Get page posts"""
        page_id = page_id or self.credentials.page_id
        return await self._request(
            "GET",
            f"{page_id}/posts",
            params={
                "fields": "id,message,created_time,permalink_url,shares,reactions.summary(true),comments.summary(true)",
                "limit": limit,
            }
        )

    async def create_page_post(
        self,
        message: str,
        link: str = None,
        page_id: str = None,
    ) -> Dict[str, Any]:
        """Create a new page post"""
        page_id = page_id or self.credentials.page_id
        data = {"message": message}
        if link:
            data["link"] = link

        return await self._request(
            "POST",
            f"{page_id}/feed",
            data=data
        )

    # ==========================================
    # 3. FACEBOOK VIDEO UPLOAD
    # ==========================================

    async def upload_video(
        self,
        video_url: str,
        title: str,
        description: str,
        page_id: str = None,
        scheduled_publish_time: int = None,
    ) -> Dict[str, Any]:
        """Upload video to Facebook page"""
        page_id = page_id or self.credentials.page_id

        data = {
            "file_url": video_url,
            "title": title,
            "description": description,
        }

        if scheduled_publish_time:
            data["scheduled_publish_time"] = scheduled_publish_time
            data["published"] = False

        return await self._request(
            "POST",
            f"{page_id}/videos",
            data=data
        )

    async def upload_reel(
        self,
        video_url: str,
        description: str,
        page_id: str = None,
    ) -> Dict[str, Any]:
        """Upload Facebook Reel"""
        page_id = page_id or self.credentials.page_id

        return await self._request(
            "POST",
            f"{page_id}/video_reels",
            data={
                "video_url": video_url,
                "description": description,
            }
        )

    # ==========================================
    # 4. INSTAGRAM CONTENT PUBLISHING
    # ==========================================

    async def get_instagram_account(self) -> Dict[str, Any]:
        """Get Instagram Business Account info"""
        return await self._request(
            "GET",
            self.credentials.instagram_account_id,
            params={
                "fields": "id,username,name,biography,followers_count,follows_count,media_count,profile_picture_url"
            }
        )

    async def create_instagram_media_container(
        self,
        image_url: str = None,
        video_url: str = None,
        caption: str = "",
        media_type: str = "IMAGE",
        is_carousel_item: bool = False,
    ) -> Dict[str, Any]:
        """Create Instagram media container"""
        data = {"caption": caption}

        if media_type == "IMAGE":
            data["image_url"] = image_url
        elif media_type == "VIDEO":
            data["video_url"] = video_url
            data["media_type"] = "VIDEO"
        elif media_type == "REELS":
            data["video_url"] = video_url
            data["media_type"] = "REELS"
        elif media_type == "STORIES":
            data["video_url"] = video_url if video_url else image_url
            data["media_type"] = "STORIES"

        if is_carousel_item:
            data["is_carousel_item"] = True

        return await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

    async def publish_instagram_media(
        self,
        creation_id: str,
    ) -> Dict[str, Any]:
        """Publish Instagram media from container"""
        return await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media_publish",
            data={"creation_id": creation_id}
        )

    async def create_instagram_carousel(
        self,
        children: List[str],
        caption: str,
    ) -> Dict[str, Any]:
        """Create Instagram carousel post"""
        # First create the carousel container
        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data={
                "media_type": "CAROUSEL",
                "children": ",".join(children),
                "caption": caption,
            }
        )

        # Then publish it
        return await self.publish_instagram_media(container["id"])

    async def create_instagram_reel(
        self,
        video_url: str,
        caption: str,
        cover_url: str = None,
        share_to_feed: bool = True,
    ) -> Dict[str, Any]:
        """Create and publish Instagram Reel"""
        data = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS",
            "share_to_feed": share_to_feed,
        }

        if cover_url:
            data["cover_url"] = cover_url

        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

        # Wait for processing
        await asyncio.sleep(10)

        return await self.publish_instagram_media(container["id"])

    async def create_instagram_story(
        self,
        media_url: str,
        media_type: str = "IMAGE",
    ) -> Dict[str, Any]:
        """Create Instagram Story"""
        data = {
            "media_type": "STORIES",
        }

        if media_type == "IMAGE":
            data["image_url"] = media_url
        else:
            data["video_url"] = media_url

        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

        return await self.publish_instagram_media(container["id"])

    # ==========================================
    # 5. INSTAGRAM INSIGHTS & ANALYTICS
    # ==========================================

    async def get_instagram_insights(
        self,
        metric: str = "impressions,reach,profile_views",
        period: str = "day",
    ) -> Dict[str, Any]:
        """Get Instagram account insights"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/insights",
            params={
                "metric": metric,
                "period": period,
            }
        )

    async def get_media_insights(
        self,
        media_id: str,
        metric: str = "impressions,reach,engagement,saved",
    ) -> Dict[str, Any]:
        """Get insights for specific media"""
        return await self._request(
            "GET",
            f"{media_id}/insights",
            params={"metric": metric}
        )

    # ==========================================
    # 6. THREADS API INTEGRATION
    # ==========================================

    async def create_threads_post(
        self,
        text: str,
        media_url: str = None,
        media_type: str = "TEXT",
        reply_to_id: str = None,
    ) -> Dict[str, Any]:
        """Create a Threads post"""
        data = {
            "text": text,
            "media_type": media_type,
        }

        if media_url:
            if media_type == "IMAGE":
                data["image_url"] = media_url
            elif media_type == "VIDEO":
                data["video_url"] = media_url

        if reply_to_id:
            data["reply_to_id"] = reply_to_id

        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/threads",
            data=data
        )

        return await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/threads_publish",
            data={"creation_id": container["id"]}
        )

    # ==========================================
    # 7. LIVE VIDEO API
    # ==========================================

    async def create_live_video(
        self,
        title: str,
        description: str,
        page_id: str = None,
    ) -> Dict[str, Any]:
        """Create a live video broadcast"""
        page_id = page_id or self.credentials.page_id

        return await self._request(
            "POST",
            f"{page_id}/live_videos",
            data={
                "title": title,
                "description": description,
                "status": "LIVE_NOW",
            }
        )

    async def end_live_video(
        self,
        video_id: str,
    ) -> Dict[str, Any]:
        """End a live video broadcast"""
        return await self._request(
            "POST",
            video_id,
            data={"end_live_video": True}
        )

    # ==========================================
    # 8. COMMENTS & ENGAGEMENT
    # ==========================================

    async def get_comments(
        self,
        object_id: str,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Get comments on a post/video"""
        return await self._request(
            "GET",
            f"{object_id}/comments",
            params={
                "fields": "id,message,from,created_time,like_count",
                "limit": limit,
            }
        )

    async def reply_to_comment(
        self,
        comment_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """Reply to a comment"""
        return await self._request(
            "POST",
            f"{comment_id}/comments",
            data={"message": message}
        )

    async def like_object(self, object_id: str) -> Dict[str, Any]:
        """Like a post/comment"""
        return await self._request("POST", f"{object_id}/likes")

    # ==========================================
    # 9. AUDIENCE & FOLLOWERS
    # ==========================================

    async def get_page_fans(
        self,
        page_id: str = None,
    ) -> Dict[str, Any]:
        """Get page fan count and demographics"""
        page_id = page_id or self.credentials.page_id
        return await self._request(
            "GET",
            f"{page_id}/insights",
            params={
                "metric": "page_fans,page_fans_city,page_fans_country,page_fans_gender_age",
                "period": "lifetime",
            }
        )

    async def get_instagram_followers(self) -> Dict[str, Any]:
        """Get Instagram follower demographics"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/insights",
            params={
                "metric": "follower_count,follower_demographics",
                "period": "lifetime",
            }
        )

    # ==========================================
    # 10. MARKETING & ADS API
    # ==========================================

    async def get_ad_accounts(self) -> Dict[str, Any]:
        """Get associated ad accounts"""
        return await self._request(
            "GET",
            "me/adaccounts",
            params={"fields": "id,name,account_status,amount_spent,balance"}
        )

    async def create_ad_campaign(
        self,
        ad_account_id: str,
        name: str,
        objective: str,
        status: str = "PAUSED",
    ) -> Dict[str, Any]:
        """Create an ad campaign"""
        return await self._request(
            "POST",
            f"act_{ad_account_id}/campaigns",
            data={
                "name": name,
                "objective": objective,
                "status": status,
                "special_ad_categories": [],
            }
        )

    async def boost_post(
        self,
        post_id: str,
        ad_account_id: str,
        budget: int,
        duration_days: int,
        targeting: Dict = None,
    ) -> Dict[str, Any]:
        """Boost a Facebook/Instagram post"""
        return await self._request(
            "POST",
            f"act_{ad_account_id}/ads",
            data={
                "creative": {"object_story_id": post_id},
                "targeting": targeting or {"geo_locations": {"countries": ["US"]}},
                "lifetime_budget": budget * 100,  # In cents
                "status": "ACTIVE",
            }
        )


# Convenience function for creating client
def create_meta_client(
    app_id: str,
    app_secret: str,
    access_token: str,
    page_id: str = None,
    instagram_account_id: str = None,
) -> MetaClient:
    """Create a Meta client with credentials"""
    credentials = MetaCredentials(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        page_id=page_id,
        instagram_account_id=instagram_account_id,
    )
    return MetaClient(credentials)
