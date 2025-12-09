"""
YouTube Complete Integration
============================

Full integration with YouTube APIs:
- YouTube Data API v3
- YouTube Analytics API
- YouTube Reporting API
- YouTube Live Streaming API

Documentation: https://developers.google.com/youtube/v3
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
class YouTubeCredentials:
    """YouTube API credentials"""
    api_key: str
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: Optional[str] = None
    channel_id: Optional[str] = None


class YouTubeClient:
    """
    Complete YouTube Platform Integration

    Capabilities:
    1. OAuth 2.0 Authentication
    2. Video Upload & Management
    3. YouTube Shorts Publishing
    4. Channel Management
    5. Playlists & Collections
    6. Comments & Community
    7. Live Streaming
    8. Analytics & Reporting
    9. Captions & Subtitles
    10. Monetization & Memberships
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3"
    UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3"
    ANALYTICS_URL = "https://youtubeanalytics.googleapis.com/v2"
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"

    def __init__(self, credentials: YouTubeCredentials):
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
        base_url: str = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to YouTube API"""
        url = f"{base_url or self.BASE_URL}/{endpoint}"

        params = params or {}
        params["key"] = self.credentials.api_key

        headers = {
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Content-Type": "application/json",
        }

        async with self.session.request(
            method,
            url,
            headers=headers,
            params=params,
            json=data,
        ) as response:
            result = await response.json()

            if "error" in result:
                logger.error(f"YouTube API Error: {result['error']}")
                raise Exception(f"YouTube API Error: {result['error']['message']}")

            return result

    # ==========================================
    # 1. AUTHENTICATION
    # ==========================================

    def get_authorization_url(
        self,
        redirect_uri: str,
        scope: str = "https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly",
        state: str = None,
    ) -> str:
        """Generate OAuth authorization URL"""
        params = {
            "client_id": self.credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
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
            data={
                "client_id": self.credentials.client_id,
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

            return result

    async def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh access token"""
        async with self.session.post(
            self.TOKEN_URL,
            data={
                "client_id": self.credentials.client_id,
                "client_secret": self.credentials.client_secret,
                "refresh_token": self.credentials.refresh_token,
                "grant_type": "refresh_token",
            }
        ) as response:
            result = await response.json()

            if "access_token" in result:
                self.credentials.access_token = result["access_token"]

            return result

    # ==========================================
    # 2. VIDEO UPLOAD & MANAGEMENT
    # ==========================================

    async def upload_video(
        self,
        video_file: bytes,
        title: str,
        description: str,
        tags: List[str] = None,
        category_id: str = "22",  # People & Blogs
        privacy_status: str = "private",
        made_for_kids: bool = False,
        notify_subscribers: bool = True,
        thumbnail_file: bytes = None,
    ) -> Dict[str, Any]:
        """Upload a video to YouTube"""
        # Create video metadata
        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": made_for_kids,
            },
            "notifySubscribers": notify_subscribers,
        }

        # Resumable upload
        url = f"{self.UPLOAD_URL}/videos"

        headers = {
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Content-Type": "application/json",
            "X-Upload-Content-Type": "video/*",
            "X-Upload-Content-Length": str(len(video_file)),
        }

        # Initialize upload
        async with self.session.post(
            url,
            headers=headers,
            params={"uploadType": "resumable", "part": "snippet,status"},
            json=metadata,
        ) as response:
            upload_url = response.headers.get("Location")

        # Upload video content
        async with self.session.put(
            upload_url,
            headers={
                "Authorization": f"Bearer {self.credentials.access_token}",
                "Content-Type": "video/*",
            },
            data=video_file,
        ) as response:
            result = await response.json()

        # Upload thumbnail if provided
        if thumbnail_file and "id" in result:
            await self.set_thumbnail(result["id"], thumbnail_file)

        return result

    async def upload_video_from_url(
        self,
        video_url: str,
        title: str,
        description: str,
        tags: List[str] = None,
        category_id: str = "22",
        privacy_status: str = "private",
    ) -> Dict[str, Any]:
        """Download video from URL and upload to YouTube"""
        # Download video
        async with self.session.get(video_url) as response:
            video_file = await response.read()

        return await self.upload_video(
            video_file=video_file,
            title=title,
            description=description,
            tags=tags,
            category_id=category_id,
            privacy_status=privacy_status,
        )

    async def update_video(
        self,
        video_id: str,
        title: str = None,
        description: str = None,
        tags: List[str] = None,
        category_id: str = None,
        privacy_status: str = None,
    ) -> Dict[str, Any]:
        """Update video metadata"""
        # Get current video data
        current = await self.get_video(video_id)
        snippet = current["items"][0]["snippet"]
        status = current["items"][0]["status"]

        # Update fields
        if title:
            snippet["title"] = title
        if description:
            snippet["description"] = description
        if tags:
            snippet["tags"] = tags
        if category_id:
            snippet["categoryId"] = category_id
        if privacy_status:
            status["privacyStatus"] = privacy_status

        return await self._request(
            "PUT",
            "videos",
            params={"part": "snippet,status"},
            data={
                "id": video_id,
                "snippet": snippet,
                "status": status,
            }
        )

    async def delete_video(self, video_id: str) -> Dict[str, Any]:
        """Delete a video"""
        return await self._request(
            "DELETE",
            "videos",
            params={"id": video_id}
        )

    async def get_video(
        self,
        video_id: str,
        parts: str = "snippet,contentDetails,statistics,status",
    ) -> Dict[str, Any]:
        """Get video details"""
        return await self._request(
            "GET",
            "videos",
            params={
                "id": video_id,
                "part": parts,
            }
        )

    # ==========================================
    # 3. YOUTUBE SHORTS
    # ==========================================

    async def upload_short(
        self,
        video_file: bytes,
        title: str,
        description: str = "",
        tags: List[str] = None,
        privacy_status: str = "public",
    ) -> Dict[str, Any]:
        """Upload a YouTube Short (vertical video < 60s)"""
        # Shorts are identified by #Shorts in title/description
        if "#Shorts" not in title and "#Shorts" not in description:
            title = f"{title} #Shorts"

        return await self.upload_video(
            video_file=video_file,
            title=title,
            description=description,
            tags=tags or [],
            privacy_status=privacy_status,
        )

    # ==========================================
    # 4. CHANNEL MANAGEMENT
    # ==========================================

    async def get_my_channel(
        self,
        parts: str = "snippet,contentDetails,statistics,brandingSettings",
    ) -> Dict[str, Any]:
        """Get authenticated user's channel"""
        return await self._request(
            "GET",
            "channels",
            params={
                "mine": "true",
                "part": parts,
            }
        )

    async def get_channel(
        self,
        channel_id: str,
        parts: str = "snippet,contentDetails,statistics",
    ) -> Dict[str, Any]:
        """Get channel by ID"""
        return await self._request(
            "GET",
            "channels",
            params={
                "id": channel_id,
                "part": parts,
            }
        )

    async def update_channel_branding(
        self,
        channel_id: str,
        banner_image: bytes = None,
        keywords: List[str] = None,
        description: str = None,
    ) -> Dict[str, Any]:
        """Update channel branding settings"""
        data = {
            "id": channel_id,
            "brandingSettings": {
                "channel": {}
            }
        }

        if keywords:
            data["brandingSettings"]["channel"]["keywords"] = " ".join(keywords)
        if description:
            data["brandingSettings"]["channel"]["description"] = description

        return await self._request(
            "PUT",
            "channels",
            params={"part": "brandingSettings"},
            data=data
        )

    async def get_channel_videos(
        self,
        channel_id: str = None,
        max_results: int = 25,
        page_token: str = None,
        order: str = "date",
    ) -> Dict[str, Any]:
        """Get videos from a channel"""
        params = {
            "part": "snippet",
            "maxResults": max_results,
            "order": order,
            "type": "video",
        }

        if channel_id:
            params["channelId"] = channel_id
        else:
            params["forMine"] = "true"

        if page_token:
            params["pageToken"] = page_token

        return await self._request("GET", "search", params=params)

    # ==========================================
    # 5. PLAYLISTS & COLLECTIONS
    # ==========================================

    async def create_playlist(
        self,
        title: str,
        description: str = "",
        privacy_status: str = "public",
    ) -> Dict[str, Any]:
        """Create a new playlist"""
        return await self._request(
            "POST",
            "playlists",
            params={"part": "snippet,status"},
            data={
                "snippet": {
                    "title": title,
                    "description": description,
                },
                "status": {
                    "privacyStatus": privacy_status,
                }
            }
        )

    async def get_playlists(
        self,
        channel_id: str = None,
        max_results: int = 25,
    ) -> Dict[str, Any]:
        """Get playlists"""
        params = {
            "part": "snippet,contentDetails",
            "maxResults": max_results,
        }

        if channel_id:
            params["channelId"] = channel_id
        else:
            params["mine"] = "true"

        return await self._request("GET", "playlists", params=params)

    async def add_video_to_playlist(
        self,
        playlist_id: str,
        video_id: str,
        position: int = None,
    ) -> Dict[str, Any]:
        """Add video to playlist"""
        data = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                }
            }
        }

        if position is not None:
            data["snippet"]["position"] = position

        return await self._request(
            "POST",
            "playlistItems",
            params={"part": "snippet"},
            data=data
        )

    async def get_playlist_items(
        self,
        playlist_id: str,
        max_results: int = 50,
    ) -> Dict[str, Any]:
        """Get items in a playlist"""
        return await self._request(
            "GET",
            "playlistItems",
            params={
                "playlistId": playlist_id,
                "part": "snippet,contentDetails",
                "maxResults": max_results,
            }
        )

    # ==========================================
    # 6. COMMENTS & COMMUNITY
    # ==========================================

    async def get_comments(
        self,
        video_id: str,
        max_results: int = 20,
        order: str = "relevance",
    ) -> Dict[str, Any]:
        """Get comments on a video"""
        return await self._request(
            "GET",
            "commentThreads",
            params={
                "videoId": video_id,
                "part": "snippet,replies",
                "maxResults": max_results,
                "order": order,
            }
        )

    async def post_comment(
        self,
        video_id: str,
        text: str,
    ) -> Dict[str, Any]:
        """Post a comment on a video"""
        return await self._request(
            "POST",
            "commentThreads",
            params={"part": "snippet"},
            data={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": text,
                        }
                    }
                }
            }
        )

    async def reply_to_comment(
        self,
        parent_id: str,
        text: str,
    ) -> Dict[str, Any]:
        """Reply to a comment"""
        return await self._request(
            "POST",
            "comments",
            params={"part": "snippet"},
            data={
                "snippet": {
                    "parentId": parent_id,
                    "textOriginal": text,
                }
            }
        )

    async def create_community_post(
        self,
        text: str,
        image_url: str = None,
    ) -> Dict[str, Any]:
        """Create a community post (requires channel membership)"""
        # Note: Community posts API has limited availability
        data = {
            "snippet": {
                "description": text,
            }
        }

        return await self._request(
            "POST",
            "activities",
            params={"part": "snippet"},
            data=data
        )

    # ==========================================
    # 7. LIVE STREAMING
    # ==========================================

    async def create_broadcast(
        self,
        title: str,
        description: str = "",
        scheduled_start_time: str = None,
        privacy_status: str = "public",
    ) -> Dict[str, Any]:
        """Create a live broadcast"""
        data = {
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": privacy_status,
            },
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": True,
            }
        }

        if scheduled_start_time:
            data["snippet"]["scheduledStartTime"] = scheduled_start_time

        return await self._request(
            "POST",
            "liveBroadcasts",
            params={"part": "snippet,status,contentDetails"},
            data=data
        )

    async def create_stream(
        self,
        title: str,
        resolution: str = "1080p",
        frame_rate: str = "30fps",
    ) -> Dict[str, Any]:
        """Create a live stream"""
        return await self._request(
            "POST",
            "liveStreams",
            params={"part": "snippet,cdn"},
            data={
                "snippet": {
                    "title": title,
                },
                "cdn": {
                    "frameRate": frame_rate,
                    "resolution": resolution,
                    "ingestionType": "rtmp",
                }
            }
        )

    async def bind_broadcast_to_stream(
        self,
        broadcast_id: str,
        stream_id: str,
    ) -> Dict[str, Any]:
        """Bind a broadcast to a stream"""
        return await self._request(
            "POST",
            "liveBroadcasts/bind",
            params={
                "id": broadcast_id,
                "part": "id,contentDetails",
                "streamId": stream_id,
            }
        )

    async def transition_broadcast(
        self,
        broadcast_id: str,
        status: str,  # testing, live, complete
    ) -> Dict[str, Any]:
        """Transition broadcast status"""
        return await self._request(
            "POST",
            "liveBroadcasts/transition",
            params={
                "id": broadcast_id,
                "broadcastStatus": status,
                "part": "status",
            }
        )

    # ==========================================
    # 8. ANALYTICS & REPORTING
    # ==========================================

    async def get_channel_analytics(
        self,
        start_date: str,
        end_date: str,
        metrics: str = "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost",
        dimensions: str = "day",
    ) -> Dict[str, Any]:
        """Get channel analytics"""
        return await self._request(
            "GET",
            "reports",
            params={
                "ids": f"channel=={self.credentials.channel_id}",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": metrics,
                "dimensions": dimensions,
            },
            base_url=self.ANALYTICS_URL
        )

    async def get_video_analytics(
        self,
        video_id: str,
        start_date: str,
        end_date: str,
        metrics: str = "views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments",
    ) -> Dict[str, Any]:
        """Get analytics for a specific video"""
        return await self._request(
            "GET",
            "reports",
            params={
                "ids": f"channel=={self.credentials.channel_id}",
                "filters": f"video=={video_id}",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": metrics,
            },
            base_url=self.ANALYTICS_URL
        )

    async def get_demographics(
        self,
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        """Get audience demographics"""
        return await self._request(
            "GET",
            "reports",
            params={
                "ids": f"channel=={self.credentials.channel_id}",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": "viewerPercentage",
                "dimensions": "ageGroup,gender",
            },
            base_url=self.ANALYTICS_URL
        )

    # ==========================================
    # 9. CAPTIONS & SUBTITLES
    # ==========================================

    async def get_captions(self, video_id: str) -> Dict[str, Any]:
        """Get captions for a video"""
        return await self._request(
            "GET",
            "captions",
            params={
                "videoId": video_id,
                "part": "snippet",
            }
        )

    async def upload_caption(
        self,
        video_id: str,
        language: str,
        name: str,
        caption_file: bytes,
        is_draft: bool = False,
    ) -> Dict[str, Any]:
        """Upload caption track"""
        url = f"{self.UPLOAD_URL}/captions"

        headers = {
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Content-Type": "application/octet-stream",
        }

        async with self.session.post(
            url,
            headers=headers,
            params={
                "uploadType": "media",
                "part": "snippet",
                "videoId": video_id,
            },
            data=caption_file,
        ) as response:
            return await response.json()

    async def set_thumbnail(
        self,
        video_id: str,
        thumbnail_file: bytes,
    ) -> Dict[str, Any]:
        """Set video thumbnail"""
        url = f"{self.UPLOAD_URL}/thumbnails/set"

        headers = {
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Content-Type": "image/jpeg",
        }

        async with self.session.post(
            url,
            headers=headers,
            params={"videoId": video_id},
            data=thumbnail_file,
        ) as response:
            return await response.json()

    # ==========================================
    # 10. MONETIZATION & MEMBERSHIPS
    # ==========================================

    async def get_monetization_status(self) -> Dict[str, Any]:
        """Get channel monetization status"""
        return await self._request(
            "GET",
            "channels",
            params={
                "mine": "true",
                "part": "status",
            }
        )

    async def get_members(
        self,
        max_results: int = 50,
        page_token: str = None,
    ) -> Dict[str, Any]:
        """Get channel members (requires membership enabled)"""
        params = {
            "part": "snippet",
            "maxResults": max_results,
        }

        if page_token:
            params["pageToken"] = page_token

        return await self._request("GET", "members", params=params)

    async def get_membership_levels(self) -> Dict[str, Any]:
        """Get membership levels"""
        return await self._request(
            "GET",
            "membershipsLevels",
            params={"part": "snippet"}
        )


# Convenience function
def create_youtube_client(
    api_key: str,
    client_id: str,
    client_secret: str,
    access_token: str,
    channel_id: str = None,
) -> YouTubeClient:
    """Create a YouTube client with credentials"""
    credentials = YouTubeCredentials(
        api_key=api_key,
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        channel_id=channel_id,
    )
    return YouTubeClient(credentials)
