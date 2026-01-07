"""
Facebook Client
===============

Specialized Facebook client for page management, video uploads, and engagement.
Wraps Meta Graph API with Facebook-specific functionality.
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
class FacebookCredentials:
    """Facebook API credentials"""
    app_id: str
    app_secret: str
    access_token: str
    page_access_token: Optional[str] = None
    page_id: Optional[str] = None


class FacebookClient:
    """
    Facebook Page & Video Client

    Capabilities:
    1. Page Management
    2. Post Creation & Publishing
    3. Video Upload (Standard & Reels)
    4. Live Video Streaming
    5. Insights & Analytics
    6. Comments & Engagement
    7. Ads & Boosting
    8. Story Publishing
    9. Scheduled Publishing
    10. Audience Management
    """

    GRAPH_API_VERSION = "v18.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    def __init__(
        self,
        app_id: str = None,
        app_secret: str = None,
        access_token: str = None,
        page_access_token: str = None,
        page_id: str = None,
        credentials: FacebookCredentials = None,
    ):
        if credentials:
            self.credentials = credentials
        else:
            self.credentials = FacebookCredentials(
                app_id=app_id or "",
                app_secret=app_secret or "",
                access_token=access_token or "",
                page_access_token=page_access_token,
                page_id=page_id,
            )
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_token(self) -> str:
        """Get the appropriate access token"""
        return self.credentials.page_access_token or self.credentials.access_token

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Graph API"""
        url = f"{self.BASE_URL}/{endpoint}"

        params = params or {}
        params["access_token"] = self._get_token()

        if not self.session:
            self.session = aiohttp.ClientSession()

        async with self.session.request(
            method,
            url,
            params=params,
            json=data,
        ) as response:
            result = await response.json()

            if "error" in result:
                logger.error(f"Facebook API Error: {result['error']}")
                raise Exception(f"Facebook API Error: {result['error'].get('message', str(result['error']))}")

            return result

    # ==========================================
    # PAGE MANAGEMENT
    # ==========================================

    async def get_page_info(self, page_id: str = None) -> Dict[str, Any]:
        """Get Facebook page information"""
        page_id = page_id or self.credentials.page_id
        return await self._request(
            "GET",
            page_id,
            params={
                "fields": "id,name,about,category,fan_count,followers_count,link,picture,cover,website,location"
            }
        )

    async def get_pages(self) -> Dict[str, Any]:
        """Get all pages managed by the user"""
        return await self._request(
            "GET",
            "me/accounts",
            params={
                "fields": "id,name,access_token,category,fan_count"
            }
        )

    # ==========================================
    # POST MANAGEMENT
    # ==========================================

    async def create_post(
        self,
        message: str,
        link: str = None,
        page_id: str = None,
        scheduled_publish_time: int = None,
    ) -> Dict[str, Any]:
        """Create a new page post"""
        page_id = page_id or self.credentials.page_id
        data = {"message": message}

        if link:
            data["link"] = link

        if scheduled_publish_time:
            data["scheduled_publish_time"] = scheduled_publish_time
            data["published"] = False

        return await self._request(
            "POST",
            f"{page_id}/feed",
            data=data
        )

    async def get_posts(
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

    async def delete_post(self, post_id: str) -> Dict[str, Any]:
        """Delete a post"""
        return await self._request("DELETE", post_id)

    # ==========================================
    # VIDEO UPLOAD
    # ==========================================

    async def upload_video(
        self,
        video_url: str,
        title: str,
        description: str,
        page_id: str = None,
        scheduled_publish_time: int = None,
        thumb_url: str = None,
    ) -> Dict[str, Any]:
        """Upload video to Facebook page"""
        page_id = page_id or self.credentials.page_id

        data = {
            "file_url": video_url,
            "title": title,
            "description": description,
        }

        if thumb_url:
            data["thumb"] = thumb_url

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

    async def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """Get video upload/processing status"""
        return await self._request(
            "GET",
            video_id,
            params={
                "fields": "id,title,description,status,length,source,picture,permalink_url"
            }
        )

    # ==========================================
    # LIVE VIDEO
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

    async def end_live_video(self, video_id: str) -> Dict[str, Any]:
        """End a live video broadcast"""
        return await self._request(
            "POST",
            video_id,
            data={"end_live_video": True}
        )

    # ==========================================
    # STORIES
    # ==========================================

    async def create_story(
        self,
        media_url: str,
        media_type: str = "photo",
        page_id: str = None,
    ) -> Dict[str, Any]:
        """Create a Facebook Story"""
        page_id = page_id or self.credentials.page_id

        data = {}
        if media_type == "photo":
            data["photo_url"] = media_url
        else:
            data["video_url"] = media_url

        return await self._request(
            "POST",
            f"{page_id}/stories",
            data=data
        )

    # ==========================================
    # INSIGHTS & ANALYTICS
    # ==========================================

    async def get_page_insights(
        self,
        page_id: str = None,
        metrics: str = "page_impressions,page_engaged_users,page_fan_adds,page_views_total",
        period: str = "day",
    ) -> Dict[str, Any]:
        """Get page insights"""
        page_id = page_id or self.credentials.page_id
        return await self._request(
            "GET",
            f"{page_id}/insights",
            params={
                "metric": metrics,
                "period": period,
            }
        )

    async def get_post_insights(
        self,
        post_id: str,
        metrics: str = "post_impressions,post_engaged_users,post_reactions_by_type_total",
    ) -> Dict[str, Any]:
        """Get insights for a specific post"""
        return await self._request(
            "GET",
            f"{post_id}/insights",
            params={"metric": metrics}
        )

    async def get_video_insights(
        self,
        video_id: str,
        metrics: str = "total_video_views,total_video_impressions,total_video_avg_time_watched",
    ) -> Dict[str, Any]:
        """Get video insights"""
        return await self._request(
            "GET",
            f"{video_id}/video_insights",
            params={"metric": metrics}
        )

    # ==========================================
    # COMMENTS & ENGAGEMENT
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

    async def like(self, object_id: str) -> Dict[str, Any]:
        """Like a post/comment"""
        return await self._request("POST", f"{object_id}/likes")

    async def unlike(self, object_id: str) -> Dict[str, Any]:
        """Unlike a post/comment"""
        return await self._request("DELETE", f"{object_id}/likes")

    # ==========================================
    # AUDIENCE
    # ==========================================

    async def get_page_fans(self, page_id: str = None) -> Dict[str, Any]:
        """Get page fan demographics"""
        page_id = page_id or self.credentials.page_id
        return await self._request(
            "GET",
            f"{page_id}/insights",
            params={
                "metric": "page_fans,page_fans_city,page_fans_country,page_fans_gender_age",
                "period": "lifetime",
            }
        )

    # ==========================================
    # ADS & BOOSTING
    # ==========================================

    async def boost_post(
        self,
        post_id: str,
        budget: int,
        duration_days: int = 7,
        targeting: Dict = None,
    ) -> Dict[str, Any]:
        """Boost a Facebook post"""
        # Get ad account
        accounts = await self._request("GET", "me/adaccounts")
        if not accounts.get("data"):
            raise Exception("No ad account found")

        ad_account_id = accounts["data"][0]["id"]

        return await self._request(
            "POST",
            f"{ad_account_id}/ads",
            data={
                "creative": {"object_story_id": post_id},
                "targeting": targeting or {"geo_locations": {"countries": ["US"]}},
                "lifetime_budget": budget * 100,
                "status": "ACTIVE",
            }
        )


# Convenience function
def create_facebook_client(
    app_id: str,
    app_secret: str,
    access_token: str,
    page_id: str = None,
    page_access_token: str = None,
) -> FacebookClient:
    """Create a Facebook client with credentials"""
    return FacebookClient(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        page_id=page_id,
        page_access_token=page_access_token,
    )
