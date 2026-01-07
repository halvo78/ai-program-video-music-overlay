"""
Threads Client
==============

Specialized Threads client for posting, engagement, and analytics.
Uses Meta's Threads API.
"""

import asyncio
import aiohttp
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThreadsCredentials:
    """Threads API credentials"""
    app_id: str
    app_secret: str
    access_token: str
    user_id: Optional[str] = None


class ThreadsClient:
    """
    Threads API Client

    Capabilities:
    1. Text Post Creation
    2. Image Post Creation
    3. Video Post Creation
    4. Carousel Posts
    5. Reply Management
    6. Insights & Analytics
    7. Profile Management
    8. Quote Posts
    9. Media Retrieval
    10. Publishing Controls
    """

    GRAPH_API_VERSION = "v18.0"
    BASE_URL = f"https://graph.threads.net/{GRAPH_API_VERSION}"

    def __init__(
        self,
        app_id: str = None,
        app_secret: str = None,
        access_token: str = None,
        user_id: str = None,
        credentials: ThreadsCredentials = None,
    ):
        if credentials:
            self.credentials = credentials
        else:
            self.credentials = ThreadsCredentials(
                app_id=app_id or "",
                app_secret=app_secret or "",
                access_token=access_token or "",
                user_id=user_id,
            )
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
        """Make authenticated request to Threads API"""
        url = f"{self.BASE_URL}/{endpoint}"

        params = params or {}
        params["access_token"] = self.credentials.access_token

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
                logger.error(f"Threads API Error: {result['error']}")
                raise Exception(f"Threads API Error: {result['error'].get('message', str(result['error']))}")

            return result

    async def _get_user_id(self) -> str:
        """Get the user ID"""
        if self.credentials.user_id:
            return self.credentials.user_id

        # Fetch user ID
        result = await self._request("GET", "me", params={"fields": "id"})
        self.credentials.user_id = result["id"]
        return self.credentials.user_id

    # ==========================================
    # PROFILE MANAGEMENT
    # ==========================================

    async def get_profile(self) -> Dict[str, Any]:
        """Get Threads profile information"""
        user_id = await self._get_user_id()
        return await self._request(
            "GET",
            user_id,
            params={
                "fields": "id,username,name,threads_profile_picture_url,threads_biography"
            }
        )

    # ==========================================
    # TEXT POSTS
    # ==========================================

    async def create_text_post(
        self,
        text: str,
        reply_to_id: str = None,
    ) -> Dict[str, Any]:
        """Create a text-only Threads post"""
        user_id = await self._get_user_id()

        data = {
            "text": text,
            "media_type": "TEXT",
        }

        if reply_to_id:
            data["reply_to_id"] = reply_to_id

        # Create container
        container = await self._request(
            "POST",
            f"{user_id}/threads",
            data=data
        )

        # Publish
        return await self._request(
            "POST",
            f"{user_id}/threads_publish",
            data={"creation_id": container["id"]}
        )

    # ==========================================
    # IMAGE POSTS
    # ==========================================

    async def create_image_post(
        self,
        image_url: str,
        text: str = "",
        reply_to_id: str = None,
    ) -> Dict[str, Any]:
        """Create an image Threads post"""
        user_id = await self._get_user_id()

        data = {
            "image_url": image_url,
            "media_type": "IMAGE",
            "text": text,
        }

        if reply_to_id:
            data["reply_to_id"] = reply_to_id

        # Create container
        container = await self._request(
            "POST",
            f"{user_id}/threads",
            data=data
        )

        # Wait for processing
        await asyncio.sleep(2)

        # Publish
        return await self._request(
            "POST",
            f"{user_id}/threads_publish",
            data={"creation_id": container["id"]}
        )

    # ==========================================
    # VIDEO POSTS
    # ==========================================

    async def create_video_post(
        self,
        video_url: str,
        text: str = "",
        reply_to_id: str = None,
    ) -> Dict[str, Any]:
        """Create a video Threads post"""
        user_id = await self._get_user_id()

        data = {
            "video_url": video_url,
            "media_type": "VIDEO",
            "text": text,
        }

        if reply_to_id:
            data["reply_to_id"] = reply_to_id

        # Create container
        container = await self._request(
            "POST",
            f"{user_id}/threads",
            data=data
        )

        # Wait for video processing (videos take longer)
        await asyncio.sleep(10)

        # Check status and publish when ready
        max_attempts = 30
        for _ in range(max_attempts):
            status = await self._request(
                "GET",
                container["id"],
                params={"fields": "status"}
            )

            if status.get("status") == "FINISHED":
                break
            elif status.get("status") == "ERROR":
                raise Exception("Video processing failed")

            await asyncio.sleep(2)

        # Publish
        return await self._request(
            "POST",
            f"{user_id}/threads_publish",
            data={"creation_id": container["id"]}
        )

    # ==========================================
    # CAROUSEL POSTS
    # ==========================================

    async def create_carousel_post(
        self,
        media_items: List[Dict[str, str]],
        text: str = "",
    ) -> Dict[str, Any]:
        """
        Create a carousel Threads post

        media_items: List of dicts with 'type' (IMAGE/VIDEO) and 'url'
        """
        user_id = await self._get_user_id()

        # Create child containers
        children = []
        for item in media_items:
            data = {
                "media_type": item["type"],
                "is_carousel_item": True,
            }

            if item["type"] == "IMAGE":
                data["image_url"] = item["url"]
            else:
                data["video_url"] = item["url"]

            container = await self._request(
                "POST",
                f"{user_id}/threads",
                data=data
            )
            children.append(container["id"])

        # Create carousel container
        carousel = await self._request(
            "POST",
            f"{user_id}/threads",
            data={
                "media_type": "CAROUSEL",
                "children": ",".join(children),
                "text": text,
            }
        )

        # Wait for processing
        await asyncio.sleep(5)

        # Publish
        return await self._request(
            "POST",
            f"{user_id}/threads_publish",
            data={"creation_id": carousel["id"]}
        )

    # ==========================================
    # REPLIES & QUOTES
    # ==========================================

    async def reply_to_thread(
        self,
        thread_id: str,
        text: str,
        media_url: str = None,
        media_type: str = "TEXT",
    ) -> Dict[str, Any]:
        """Reply to a thread"""
        if media_type == "TEXT":
            return await self.create_text_post(text, reply_to_id=thread_id)
        elif media_type == "IMAGE":
            return await self.create_image_post(media_url, text, reply_to_id=thread_id)
        else:
            return await self.create_video_post(media_url, text, reply_to_id=thread_id)

    async def quote_thread(
        self,
        thread_id: str,
        text: str,
    ) -> Dict[str, Any]:
        """Quote a thread (repost with comment)"""
        user_id = await self._get_user_id()

        container = await self._request(
            "POST",
            f"{user_id}/threads",
            data={
                "text": text,
                "media_type": "TEXT",
                "quote_post_id": thread_id,
            }
        )

        return await self._request(
            "POST",
            f"{user_id}/threads_publish",
            data={"creation_id": container["id"]}
        )

    # ==========================================
    # MEDIA RETRIEVAL
    # ==========================================

    async def get_threads(
        self,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Get user's threads"""
        user_id = await self._get_user_id()
        return await self._request(
            "GET",
            f"{user_id}/threads",
            params={
                "fields": "id,text,username,timestamp,media_type,permalink,shortcode",
                "limit": limit,
            }
        )

    async def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get a specific thread"""
        return await self._request(
            "GET",
            thread_id,
            params={
                "fields": "id,text,username,timestamp,media_type,permalink,is_quote_post,has_replies,root_post,replied_to"
            }
        )

    async def get_replies(
        self,
        thread_id: str,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Get replies to a thread"""
        return await self._request(
            "GET",
            f"{thread_id}/replies",
            params={
                "fields": "id,text,username,timestamp",
                "limit": limit,
            }
        )

    async def get_conversation(
        self,
        thread_id: str,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """Get full conversation thread"""
        return await self._request(
            "GET",
            f"{thread_id}/conversation",
            params={
                "fields": "id,text,username,timestamp",
                "limit": limit,
            }
        )

    # ==========================================
    # INSIGHTS & ANALYTICS
    # ==========================================

    async def get_profile_insights(
        self,
        metrics: str = "views,likes,replies,reposts,quotes,followers_count",
    ) -> Dict[str, Any]:
        """Get profile insights"""
        user_id = await self._get_user_id()
        return await self._request(
            "GET",
            f"{user_id}/threads_insights",
            params={"metric": metrics}
        )

    async def get_thread_insights(
        self,
        thread_id: str,
        metrics: str = "views,likes,replies,reposts,quotes",
    ) -> Dict[str, Any]:
        """Get insights for a specific thread"""
        return await self._request(
            "GET",
            f"{thread_id}/insights",
            params={"metric": metrics}
        )

    # ==========================================
    # PUBLISHING CONTROLS
    # ==========================================

    async def get_publishing_limit(self) -> Dict[str, Any]:
        """Get current publishing rate limit status"""
        user_id = await self._get_user_id()
        return await self._request(
            "GET",
            f"{user_id}/threads_publishing_limit",
            params={"fields": "quota_usage,config"}
        )

    async def delete_thread(self, thread_id: str) -> Dict[str, Any]:
        """Delete a thread"""
        return await self._request("DELETE", thread_id)

    # ==========================================
    # CONVENIENCE METHODS
    # ==========================================

    async def post(
        self,
        text: str,
        media_url: str = None,
        media_type: str = "TEXT",
    ) -> Dict[str, Any]:
        """
        Universal post method

        Args:
            text: The text content
            media_url: Optional URL to image or video
            media_type: TEXT, IMAGE, or VIDEO
        """
        if media_type == "TEXT" or not media_url:
            return await self.create_text_post(text)
        elif media_type == "IMAGE":
            return await self.create_image_post(media_url, text)
        elif media_type == "VIDEO":
            return await self.create_video_post(media_url, text)
        else:
            raise ValueError(f"Unknown media type: {media_type}")


# Convenience function
def create_threads_client(
    app_id: str,
    app_secret: str,
    access_token: str,
    user_id: str = None,
) -> ThreadsClient:
    """Create a Threads client with credentials"""
    return ThreadsClient(
        app_id=app_id,
        app_secret=app_secret,
        access_token=access_token,
        user_id=user_id,
    )
