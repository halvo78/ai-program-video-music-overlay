"""
Instagram Complete Integration
==============================

Full integration with Instagram Graph API:
- Content Publishing (Feed, Reels, Stories, Carousels)
- Instagram Shopping
- Insights & Analytics
- Comments & Messaging
- Hashtag Discovery

Documentation: https://developers.facebook.com/docs/instagram-api
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
class InstagramCredentials:
    """Instagram API credentials (via Meta Graph API)"""
    access_token: str
    instagram_account_id: str
    facebook_page_id: Optional[str] = None


class InstagramClient:
    """
    Complete Instagram Platform Integration

    Capabilities:
    1. OAuth & Authentication
    2. Feed Post Publishing
    3. Reels Publishing
    4. Stories Publishing
    5. Carousel Posts
    6. Insights & Analytics
    7. Comments Management
    8. Hashtag Discovery
    9. Shopping & Products
    10. Messaging (Instagram Direct)
    """

    GRAPH_API_VERSION = "v18.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    def __init__(self, credentials: InstagramCredentials):
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
    ) -> Dict[str, Any]:
        """Make authenticated request to Instagram Graph API"""
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
                logger.error(f"Instagram API Error: {result['error']}")
                raise Exception(f"Instagram API Error: {result['error']['message']}")

            return result

    # ==========================================
    # 1. ACCOUNT INFORMATION
    # ==========================================

    async def get_account_info(
        self,
        fields: str = "id,username,name,biography,followers_count,follows_count,media_count,profile_picture_url,website",
    ) -> Dict[str, Any]:
        """Get Instagram Business Account information"""
        return await self._request(
            "GET",
            self.credentials.instagram_account_id,
            params={"fields": fields}
        )

    # ==========================================
    # 2. FEED POST PUBLISHING
    # ==========================================

    async def create_image_post(
        self,
        image_url: str,
        caption: str,
        location_id: str = None,
        user_tags: List[Dict] = None,
    ) -> Dict[str, Any]:
        """Create a single image post"""
        # Step 1: Create media container
        data = {
            "image_url": image_url,
            "caption": caption,
        }

        if location_id:
            data["location_id"] = location_id

        if user_tags:
            data["user_tags"] = user_tags

        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

        # Step 2: Publish the container
        return await self._publish_media(container["id"])

    async def create_video_post(
        self,
        video_url: str,
        caption: str,
        cover_url: str = None,
        location_id: str = None,
        thumb_offset: int = None,
    ) -> Dict[str, Any]:
        """Create a video post (non-Reel)"""
        data = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "VIDEO",
        }

        if cover_url:
            data["cover_url"] = cover_url
        if location_id:
            data["location_id"] = location_id
        if thumb_offset:
            data["thumb_offset"] = thumb_offset

        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

        # Wait for processing
        await self._wait_for_container(container["id"])

        return await self._publish_media(container["id"])

    # ==========================================
    # 3. REELS PUBLISHING
    # ==========================================

    async def create_reel(
        self,
        video_url: str,
        caption: str,
        cover_url: str = None,
        share_to_feed: bool = True,
        audio_name: str = None,
        collaborators: List[str] = None,
    ) -> Dict[str, Any]:
        """Create and publish an Instagram Reel"""
        data = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS",
            "share_to_feed": share_to_feed,
        }

        if cover_url:
            data["cover_url"] = cover_url
        if audio_name:
            data["audio_name"] = audio_name
        if collaborators:
            data["collaborators"] = collaborators

        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

        # Wait for video processing
        await self._wait_for_container(container["id"])

        return await self._publish_media(container["id"])

    # ==========================================
    # 4. STORIES PUBLISHING
    # ==========================================

    async def create_image_story(
        self,
        image_url: str,
    ) -> Dict[str, Any]:
        """Create an image story"""
        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data={
                "image_url": image_url,
                "media_type": "STORIES",
            }
        )

        return await self._publish_media(container["id"])

    async def create_video_story(
        self,
        video_url: str,
    ) -> Dict[str, Any]:
        """Create a video story"""
        container = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data={
                "video_url": video_url,
                "media_type": "STORIES",
            }
        )

        await self._wait_for_container(container["id"])

        return await self._publish_media(container["id"])

    async def get_stories(self) -> Dict[str, Any]:
        """Get current stories"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/stories",
            params={"fields": "id,media_type,media_url,timestamp"}
        )

    # ==========================================
    # 5. CAROUSEL POSTS
    # ==========================================

    async def create_carousel_post(
        self,
        media_items: List[Dict],  # [{"type": "IMAGE", "url": "..."}, {"type": "VIDEO", "url": "..."}]
        caption: str,
        location_id: str = None,
    ) -> Dict[str, Any]:
        """Create a carousel post with multiple images/videos"""
        # Step 1: Create child containers
        children_ids = []

        for item in media_items:
            if item["type"] == "IMAGE":
                child = await self._request(
                    "POST",
                    f"{self.credentials.instagram_account_id}/media",
                    data={
                        "image_url": item["url"],
                        "is_carousel_item": True,
                    }
                )
            else:  # VIDEO
                child = await self._request(
                    "POST",
                    f"{self.credentials.instagram_account_id}/media",
                    data={
                        "video_url": item["url"],
                        "media_type": "VIDEO",
                        "is_carousel_item": True,
                    }
                )
                await self._wait_for_container(child["id"])

            children_ids.append(child["id"])

        # Step 2: Create carousel container
        data = {
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "caption": caption,
        }

        if location_id:
            data["location_id"] = location_id

        carousel = await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media",
            data=data
        )

        # Step 3: Publish
        return await self._publish_media(carousel["id"])

    # ==========================================
    # 6. INSIGHTS & ANALYTICS
    # ==========================================

    async def get_account_insights(
        self,
        metrics: str = "impressions,reach,profile_views",
        period: str = "day",
    ) -> Dict[str, Any]:
        """Get account-level insights"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/insights",
            params={
                "metric": metrics,
                "period": period,
            }
        )

    async def get_media_insights(
        self,
        media_id: str,
        metrics: str = "impressions,reach,engagement,saved,video_views",
    ) -> Dict[str, Any]:
        """Get insights for specific media"""
        return await self._request(
            "GET",
            f"{media_id}/insights",
            params={"metric": metrics}
        )

    async def get_story_insights(
        self,
        story_id: str,
        metrics: str = "impressions,reach,replies,taps_forward,taps_back,exits",
    ) -> Dict[str, Any]:
        """Get insights for a story"""
        return await self._request(
            "GET",
            f"{story_id}/insights",
            params={"metric": metrics}
        )

    async def get_reel_insights(
        self,
        reel_id: str,
        metrics: str = "plays,reach,likes,comments,shares,saved,total_interactions",
    ) -> Dict[str, Any]:
        """Get insights for a Reel"""
        return await self._request(
            "GET",
            f"{reel_id}/insights",
            params={"metric": metrics}
        )

    async def get_audience_demographics(self) -> Dict[str, Any]:
        """Get audience demographics"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/insights",
            params={
                "metric": "audience_city,audience_country,audience_gender_age,audience_locale",
                "period": "lifetime",
            }
        )

    # ==========================================
    # 7. COMMENTS MANAGEMENT
    # ==========================================

    async def get_comments(
        self,
        media_id: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get comments on a media"""
        return await self._request(
            "GET",
            f"{media_id}/comments",
            params={
                "fields": "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}",
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
            f"{comment_id}/replies",
            data={"message": message}
        )

    async def hide_comment(self, comment_id: str) -> Dict[str, Any]:
        """Hide a comment"""
        return await self._request(
            "POST",
            comment_id,
            data={"hide": True}
        )

    async def delete_comment(self, comment_id: str) -> Dict[str, Any]:
        """Delete a comment"""
        return await self._request("DELETE", comment_id)

    # ==========================================
    # 8. HASHTAG DISCOVERY
    # ==========================================

    async def search_hashtag(self, hashtag: str) -> Dict[str, Any]:
        """Search for a hashtag ID"""
        return await self._request(
            "GET",
            "ig_hashtag_search",
            params={
                "user_id": self.credentials.instagram_account_id,
                "q": hashtag,
            }
        )

    async def get_hashtag_recent_media(
        self,
        hashtag_id: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get recent media for a hashtag"""
        return await self._request(
            "GET",
            f"{hashtag_id}/recent_media",
            params={
                "user_id": self.credentials.instagram_account_id,
                "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
                "limit": limit,
            }
        )

    async def get_hashtag_top_media(
        self,
        hashtag_id: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Get top media for a hashtag"""
        return await self._request(
            "GET",
            f"{hashtag_id}/top_media",
            params={
                "user_id": self.credentials.instagram_account_id,
                "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
                "limit": limit,
            }
        )

    # ==========================================
    # 9. SHOPPING & PRODUCTS
    # ==========================================

    async def get_product_catalog(self) -> Dict[str, Any]:
        """Get connected product catalog"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/catalog_product_search",
            params={"catalog_id": "auto"}
        )

    async def tag_products_in_media(
        self,
        media_id: str,
        product_tags: List[Dict],  # [{"product_id": "...", "x": 0.5, "y": 0.5}]
    ) -> Dict[str, Any]:
        """Tag products in a media post"""
        return await self._request(
            "POST",
            f"{media_id}",
            data={"product_tags": product_tags}
        )

    # ==========================================
    # 10. MESSAGING (INSTAGRAM DIRECT)
    # ==========================================

    async def get_conversations(
        self,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get Instagram Direct conversations"""
        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/conversations",
            params={
                "platform": "instagram",
                "fields": "id,participants,messages{id,message,from,created_time}",
                "limit": limit,
            }
        )

    async def send_message(
        self,
        recipient_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """Send a direct message"""
        return await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/messages",
            data={
                "recipient": {"id": recipient_id},
                "message": {"text": message},
            }
        )

    async def send_media_message(
        self,
        recipient_id: str,
        media_url: str,
        media_type: str = "image",
    ) -> Dict[str, Any]:
        """Send a media message"""
        return await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/messages",
            data={
                "recipient": {"id": recipient_id},
                "message": {
                    "attachment": {
                        "type": media_type,
                        "payload": {"url": media_url},
                    }
                },
            }
        )

    # ==========================================
    # HELPER METHODS
    # ==========================================

    async def _publish_media(self, creation_id: str) -> Dict[str, Any]:
        """Publish a media container"""
        return await self._request(
            "POST",
            f"{self.credentials.instagram_account_id}/media_publish",
            data={"creation_id": creation_id}
        )

    async def _wait_for_container(
        self,
        container_id: str,
        max_wait: int = 300,
        check_interval: int = 5,
    ) -> Dict[str, Any]:
        """Wait for media container to finish processing"""
        for _ in range(max_wait // check_interval):
            status = await self._request(
                "GET",
                container_id,
                params={"fields": "status_code,status"}
            )

            if status.get("status_code") == "FINISHED":
                return status
            elif status.get("status_code") == "ERROR":
                raise Exception(f"Media processing failed: {status.get('status')}")

            await asyncio.sleep(check_interval)

        raise Exception("Media processing timed out")

    async def get_media(
        self,
        limit: int = 25,
        after: str = None,
    ) -> Dict[str, Any]:
        """Get account's media"""
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,thumbnail_url",
            "limit": limit,
        }

        if after:
            params["after"] = after

        return await self._request(
            "GET",
            f"{self.credentials.instagram_account_id}/media",
            params=params
        )


# Convenience function
def create_instagram_client(
    access_token: str,
    instagram_account_id: str,
) -> InstagramClient:
    """Create an Instagram client with credentials"""
    credentials = InstagramCredentials(
        access_token=access_token,
        instagram_account_id=instagram_account_id,
    )
    return InstagramClient(credentials)
