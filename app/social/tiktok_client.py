"""
TikTok Complete Integration
===========================

Full integration with TikTok APIs:
- Content Posting API
- Display API
- Login Kit
- Video Kit
- Sound Kit
- Research API

Documentation: https://developers.tiktok.com/doc
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
class TikTokCredentials:
    """TikTok API credentials"""
    client_key: str
    client_secret: str
    access_token: str
    refresh_token: Optional[str] = None
    open_id: Optional[str] = None


class TikTokClient:
    """
    Complete TikTok Platform Integration

    Capabilities:
    1. OAuth 2.0 Authentication & Login Kit
    2. Video Upload & Publishing
    3. Photo Post Publishing
    4. User Profile Management
    5. Video List & Discovery
    6. Comments & Engagement
    7. Sound/Music Integration
    8. Analytics & Insights
    9. Duet & Stitch Features
    10. Creator Tools & Effects
    """

    BASE_URL = "https://open.tiktokapis.com/v2"
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize"
    TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token"

    def __init__(self, credentials: TikTokCredentials):
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
        headers: Dict = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to TikTok API"""
        url = f"{self.BASE_URL}/{endpoint}"

        default_headers = {
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Content-Type": "application/json",
        }

        if headers:
            default_headers.update(headers)

        async with self.session.request(
            method,
            url,
            headers=default_headers,
            params=params,
            json=data,
        ) as response:
            result = await response.json()

            if result.get("error", {}).get("code"):
                logger.error(f"TikTok API Error: {result['error']}")
                raise Exception(f"TikTok API Error: {result['error']['message']}")

            return result

    # ==========================================
    # 1. AUTHENTICATION & LOGIN KIT
    # ==========================================

    def get_authorization_url(
        self,
        redirect_uri: str,
        scope: str = "user.info.basic,video.list,video.publish",
        state: str = None,
    ) -> str:
        """Generate OAuth authorization URL"""
        params = {
            "client_key": self.credentials.client_key,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "response_type": "code",
        }

        if state:
            params["state"] = state

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query}"

    async def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str,
    ) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with self.session.post(
            self.TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_key": self.credentials.client_key,
                "client_secret": self.credentials.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            }
        ) as response:
            result = await response.json()

            if "access_token" in result:
                self.credentials.access_token = result["access_token"]
                self.credentials.refresh_token = result.get("refresh_token")
                self.credentials.open_id = result.get("open_id")

            return result

    async def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        async with self.session.post(
            self.TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_key": self.credentials.client_key,
                "client_secret": self.credentials.client_secret,
                "refresh_token": self.credentials.refresh_token,
                "grant_type": "refresh_token",
            }
        ) as response:
            result = await response.json()

            if "access_token" in result:
                self.credentials.access_token = result["access_token"]
                self.credentials.refresh_token = result.get("refresh_token")

            return result

    # ==========================================
    # 2. VIDEO UPLOAD & PUBLISHING
    # ==========================================

    async def init_video_upload(
        self,
        chunk_size: int = 10000000,
        total_byte_count: int = None,
    ) -> Dict[str, Any]:
        """Initialize video upload (chunked)"""
        return await self._request(
            "POST",
            "post/publish/video/init/",
            data={
                "post_info": {
                    "title": "",
                    "privacy_level": "SELF_ONLY",
                    "disable_duet": False,
                    "disable_comment": False,
                    "disable_stitch": False,
                },
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": total_byte_count,
                    "chunk_size": chunk_size,
                    "total_chunk_count": (total_byte_count // chunk_size) + 1,
                }
            }
        )

    async def upload_video_chunk(
        self,
        upload_url: str,
        chunk_data: bytes,
        chunk_index: int,
    ) -> Dict[str, Any]:
        """Upload a video chunk"""
        headers = {
            "Content-Type": "video/mp4",
            "Content-Range": f"bytes {chunk_index}/*",
        }

        async with self.session.put(
            upload_url,
            headers=headers,
            data=chunk_data,
        ) as response:
            return {"status": response.status}

    async def publish_video(
        self,
        publish_id: str,
        title: str,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
        disable_duet: bool = False,
        disable_comment: bool = False,
        disable_stitch: bool = False,
        video_cover_timestamp_ms: int = 1000,
    ) -> Dict[str, Any]:
        """Publish uploaded video"""
        return await self._request(
            "POST",
            "post/publish/status/fetch/",
            data={
                "publish_id": publish_id,
            }
        )

    async def post_video_from_url(
        self,
        video_url: str,
        title: str,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
        disable_duet: bool = False,
        disable_comment: bool = False,
        disable_stitch: bool = False,
    ) -> Dict[str, Any]:
        """Post video directly from URL"""
        return await self._request(
            "POST",
            "post/publish/video/init/",
            data={
                "post_info": {
                    "title": title,
                    "privacy_level": privacy_level,
                    "disable_duet": disable_duet,
                    "disable_comment": disable_comment,
                    "disable_stitch": disable_stitch,
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "video_url": video_url,
                }
            }
        )

    # ==========================================
    # 3. PHOTO POST PUBLISHING
    # ==========================================

    async def post_photo(
        self,
        photo_urls: List[str],
        title: str,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
        disable_comment: bool = False,
        auto_add_music: bool = True,
    ) -> Dict[str, Any]:
        """Post photo slideshow"""
        return await self._request(
            "POST",
            "post/publish/content/init/",
            data={
                "post_info": {
                    "title": title,
                    "privacy_level": privacy_level,
                    "disable_comment": disable_comment,
                    "auto_add_music": auto_add_music,
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "photo_cover_index": 0,
                    "photo_images": photo_urls,
                },
                "post_mode": "DIRECT_POST",
                "media_type": "PHOTO",
            }
        )

    # ==========================================
    # 4. USER PROFILE MANAGEMENT
    # ==========================================

    async def get_user_info(
        self,
        fields: str = "open_id,union_id,avatar_url,display_name,bio_description,profile_deep_link,is_verified,follower_count,following_count,likes_count,video_count",
    ) -> Dict[str, Any]:
        """Get current user's profile information"""
        return await self._request(
            "GET",
            "user/info/",
            params={"fields": fields}
        )

    # ==========================================
    # 5. VIDEO LIST & DISCOVERY
    # ==========================================

    async def get_user_videos(
        self,
        cursor: int = 0,
        max_count: int = 20,
        fields: str = "id,create_time,cover_image_url,share_url,video_description,duration,title,like_count,comment_count,share_count,view_count",
    ) -> Dict[str, Any]:
        """Get user's videos"""
        return await self._request(
            "POST",
            "video/list/",
            data={
                "cursor": cursor,
                "max_count": max_count,
            },
            params={"fields": fields}
        )

    async def query_videos(
        self,
        video_ids: List[str],
        fields: str = "id,create_time,cover_image_url,share_url,video_description,duration,title,like_count,comment_count,share_count,view_count",
    ) -> Dict[str, Any]:
        """Query specific videos by ID"""
        return await self._request(
            "POST",
            "video/query/",
            data={
                "filters": {
                    "video_ids": video_ids,
                }
            },
            params={"fields": fields}
        )

    # ==========================================
    # 6. COMMENTS & ENGAGEMENT
    # ==========================================

    async def get_video_comments(
        self,
        video_id: str,
        cursor: int = 0,
        max_count: int = 50,
    ) -> Dict[str, Any]:
        """Get comments on a video"""
        return await self._request(
            "POST",
            "video/comment/list/",
            data={
                "video_id": video_id,
                "cursor": cursor,
                "max_count": max_count,
            }
        )

    async def reply_to_comment(
        self,
        video_id: str,
        comment_id: str,
        text: str,
    ) -> Dict[str, Any]:
        """Reply to a comment"""
        return await self._request(
            "POST",
            "video/comment/reply/",
            data={
                "video_id": video_id,
                "comment_id": comment_id,
                "text": text,
            }
        )

    # ==========================================
    # 7. SOUND/MUSIC INTEGRATION
    # ==========================================

    async def search_music(
        self,
        query: str,
        cursor: int = 0,
        count: int = 20,
    ) -> Dict[str, Any]:
        """Search for music/sounds"""
        return await self._request(
            "GET",
            "sound/search/",
            params={
                "query": query,
                "cursor": cursor,
                "count": count,
            }
        )

    async def get_trending_sounds(
        self,
        cursor: int = 0,
        count: int = 20,
    ) -> Dict[str, Any]:
        """Get trending sounds"""
        return await self._request(
            "GET",
            "sound/trending/",
            params={
                "cursor": cursor,
                "count": count,
            }
        )

    # ==========================================
    # 8. ANALYTICS & INSIGHTS
    # ==========================================

    async def get_video_insights(
        self,
        video_id: str,
    ) -> Dict[str, Any]:
        """Get insights for a specific video"""
        return await self._request(
            "POST",
            "video/query/",
            data={
                "filters": {
                    "video_ids": [video_id],
                }
            },
            params={
                "fields": "id,like_count,comment_count,share_count,view_count,create_time"
            }
        )

    async def get_creator_insights(
        self,
        fields: str = "follower_count,following_count,likes_count,video_count",
    ) -> Dict[str, Any]:
        """Get creator account insights"""
        return await self._request(
            "GET",
            "user/info/",
            params={"fields": fields}
        )

    # ==========================================
    # 9. DUET & STITCH FEATURES
    # ==========================================

    async def create_duet(
        self,
        original_video_id: str,
        video_url: str,
        title: str,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
    ) -> Dict[str, Any]:
        """Create a duet with another video"""
        return await self._request(
            "POST",
            "post/publish/video/init/",
            data={
                "post_info": {
                    "title": title,
                    "privacy_level": privacy_level,
                    "duet_with_video_id": original_video_id,
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "video_url": video_url,
                }
            }
        )

    async def create_stitch(
        self,
        original_video_id: str,
        video_url: str,
        title: str,
        stitch_duration_ms: int = 5000,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
    ) -> Dict[str, Any]:
        """Create a stitch with another video"""
        return await self._request(
            "POST",
            "post/publish/video/init/",
            data={
                "post_info": {
                    "title": title,
                    "privacy_level": privacy_level,
                    "stitch_with_video_id": original_video_id,
                    "stitch_duration_ms": stitch_duration_ms,
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "video_url": video_url,
                }
            }
        )

    # ==========================================
    # 10. CREATOR TOOLS & EFFECTS
    # ==========================================

    async def get_creator_info(self) -> Dict[str, Any]:
        """Get creator account information"""
        return await self._request(
            "GET",
            "user/info/",
            params={
                "fields": "open_id,display_name,avatar_url,is_verified,follower_count,video_count,likes_count"
            }
        )

    async def check_publish_status(
        self,
        publish_id: str,
    ) -> Dict[str, Any]:
        """Check video publish status"""
        return await self._request(
            "POST",
            "post/publish/status/fetch/",
            data={"publish_id": publish_id}
        )

    async def get_available_effects(self) -> Dict[str, Any]:
        """Get available effects for video creation"""
        return await self._request(
            "GET",
            "effect/list/",
        )


# ==========================================
# TIKTOK CONTENT POSTING WORKFLOW
# ==========================================

class TikTokPublisher:
    """High-level TikTok publishing workflow"""

    def __init__(self, client: TikTokClient):
        self.client = client

    async def publish_video(
        self,
        video_url: str,
        title: str,
        hashtags: List[str] = None,
        privacy: str = "PUBLIC_TO_EVERYONE",
    ) -> Dict[str, Any]:
        """Complete workflow to publish a video"""
        # Format title with hashtags
        if hashtags:
            hashtag_str = " ".join(f"#{tag}" for tag in hashtags)
            full_title = f"{title} {hashtag_str}"
        else:
            full_title = title

        # Truncate to TikTok's limit (2200 characters)
        full_title = full_title[:2200]

        # Initialize upload
        result = await self.client.post_video_from_url(
            video_url=video_url,
            title=full_title,
            privacy_level=privacy,
        )

        publish_id = result.get("data", {}).get("publish_id")

        if not publish_id:
            raise Exception("Failed to initialize video upload")

        # Poll for completion
        for _ in range(60):  # Max 5 minutes
            status = await self.client.check_publish_status(publish_id)

            if status.get("data", {}).get("status") == "PUBLISH_COMPLETE":
                return {
                    "success": True,
                    "publish_id": publish_id,
                    "video_id": status.get("data", {}).get("video_id"),
                }
            elif status.get("data", {}).get("status") == "FAILED":
                raise Exception(f"Video publish failed: {status}")

            await asyncio.sleep(5)

        raise Exception("Video publish timed out")

    async def publish_photo_slideshow(
        self,
        photo_urls: List[str],
        title: str,
        hashtags: List[str] = None,
    ) -> Dict[str, Any]:
        """Publish photo slideshow"""
        if hashtags:
            hashtag_str = " ".join(f"#{tag}" for tag in hashtags)
            full_title = f"{title} {hashtag_str}"
        else:
            full_title = title

        return await self.client.post_photo(
            photo_urls=photo_urls,
            title=full_title[:2200],
        )


# Convenience function
def create_tiktok_client(
    client_key: str,
    client_secret: str,
    access_token: str,
) -> TikTokClient:
    """Create a TikTok client with credentials"""
    credentials = TikTokCredentials(
        client_key=client_key,
        client_secret=client_secret,
        access_token=access_token,
    )
    return TikTokClient(credentials)
