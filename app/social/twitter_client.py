"""
Twitter/X Complete Integration
==============================

Full integration with Twitter API v2:
- Tweet Management
- Media Upload
- User Management
- Spaces (Audio)
- Lists
- Direct Messages
- Analytics
- Ads API

Documentation: https://developer.twitter.com/en/docs
"""

import asyncio
import aiohttp
import json
import base64
import hashlib
import hmac
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)


@dataclass
class TwitterCredentials:
    """Twitter API credentials"""
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str
    bearer_token: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class TwitterClient:
    """
    Complete Twitter/X Platform Integration

    Capabilities:
    1. OAuth 1.0a & 2.0 Authentication
    2. Tweet Creation & Management
    3. Media Upload (Images, Videos, GIFs)
    4. User Profile Management
    5. Followers & Following
    6. Lists Management
    7. Direct Messages
    8. Twitter Spaces
    9. Analytics & Metrics
    10. Ads API Integration
    """

    API_V2_BASE = "https://api.twitter.com/2"
    API_V1_BASE = "https://api.twitter.com/1.1"
    UPLOAD_BASE = "https://upload.twitter.com/1.1"

    def __init__(self, credentials: TwitterCredentials):
        self.credentials = credentials
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _generate_oauth_signature(
        self,
        method: str,
        url: str,
        params: Dict,
    ) -> str:
        """Generate OAuth 1.0a signature"""
        # Create signature base string
        sorted_params = "&".join(
            f"{quote(k, safe='')}={quote(str(v), safe='')}"
            for k, v in sorted(params.items())
        )

        base_string = f"{method.upper()}&{quote(url, safe='')}&{quote(sorted_params, safe='')}"

        # Create signing key
        signing_key = f"{quote(self.credentials.api_secret, safe='')}&{quote(self.credentials.access_token_secret, safe='')}"

        # Generate signature
        signature = base64.b64encode(
            hmac.new(
                signing_key.encode(),
                base_string.encode(),
                hashlib.sha1
            ).digest()
        ).decode()

        return signature

    def _get_oauth_header(self, method: str, url: str, params: Dict = None) -> str:
        """Generate OAuth 1.0a Authorization header"""
        oauth_params = {
            "oauth_consumer_key": self.credentials.api_key,
            "oauth_token": self.credentials.access_token,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_nonce": base64.b64encode(str(time.time()).encode()).decode()[:32],
            "oauth_version": "1.0",
        }

        all_params = {**oauth_params, **(params or {})}
        oauth_params["oauth_signature"] = self._generate_oauth_signature(method, url, all_params)

        header = "OAuth " + ", ".join(
            f'{k}="{quote(str(v), safe="")}"'
            for k, v in sorted(oauth_params.items())
        )

        return header

    async def _request_v2(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ) -> Dict[str, Any]:
        """Make request to Twitter API v2"""
        url = f"{self.API_V2_BASE}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.credentials.bearer_token}",
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

            if "errors" in result:
                logger.error(f"Twitter API Error: {result['errors']}")
                raise Exception(f"Twitter API Error: {result['errors']}")

            return result

    async def _request_v1(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ) -> Dict[str, Any]:
        """Make OAuth 1.0a request to Twitter API v1.1"""
        url = f"{self.API_V1_BASE}/{endpoint}"

        headers = {
            "Authorization": self._get_oauth_header(method, url, params),
            "Content-Type": "application/json",
        }

        async with self.session.request(
            method,
            url,
            headers=headers,
            params=params,
            json=data,
        ) as response:
            return await response.json()

    # ==========================================
    # 1. AUTHENTICATION
    # ==========================================

    async def verify_credentials(self) -> Dict[str, Any]:
        """Verify OAuth credentials and get user info"""
        return await self._request_v2("GET", "users/me", params={
            "user.fields": "id,name,username,description,profile_image_url,public_metrics,verified"
        })

    async def get_oauth2_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for OAuth 2.0 token"""
        url = "https://api.twitter.com/2/oauth2/token"

        auth = base64.b64encode(
            f"{self.credentials.client_id}:{self.credentials.client_secret}".encode()
        ).decode()

        async with self.session.post(
            url,
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
                "code_verifier": "challenge",
            }
        ) as response:
            return await response.json()

    # ==========================================
    # 2. TWEET MANAGEMENT
    # ==========================================

    async def create_tweet(
        self,
        text: str,
        media_ids: List[str] = None,
        reply_to: str = None,
        quote_tweet_id: str = None,
        poll_options: List[str] = None,
        poll_duration_minutes: int = None,
    ) -> Dict[str, Any]:
        """Create a new tweet"""
        data = {"text": text}

        if media_ids:
            data["media"] = {"media_ids": media_ids}

        if reply_to:
            data["reply"] = {"in_reply_to_tweet_id": reply_to}

        if quote_tweet_id:
            data["quote_tweet_id"] = quote_tweet_id

        if poll_options:
            data["poll"] = {
                "options": poll_options,
                "duration_minutes": poll_duration_minutes or 1440,
            }

        return await self._request_v2("POST", "tweets", data=data)

    async def delete_tweet(self, tweet_id: str) -> Dict[str, Any]:
        """Delete a tweet"""
        return await self._request_v2("DELETE", f"tweets/{tweet_id}")

    async def get_tweet(
        self,
        tweet_id: str,
        expansions: str = "author_id,attachments.media_keys",
    ) -> Dict[str, Any]:
        """Get tweet by ID"""
        return await self._request_v2(
            "GET",
            f"tweets/{tweet_id}",
            params={
                "expansions": expansions,
                "tweet.fields": "created_at,public_metrics,entities,attachments",
                "media.fields": "url,preview_image_url,duration_ms,public_metrics",
            }
        )

    async def get_user_tweets(
        self,
        user_id: str,
        max_results: int = 10,
        pagination_token: str = None,
    ) -> Dict[str, Any]:
        """Get tweets from a user"""
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,entities",
        }

        if pagination_token:
            params["pagination_token"] = pagination_token

        return await self._request_v2("GET", f"users/{user_id}/tweets", params=params)

    async def search_tweets(
        self,
        query: str,
        max_results: int = 10,
        start_time: str = None,
        end_time: str = None,
    ) -> Dict[str, Any]:
        """Search recent tweets"""
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "created_at,public_metrics,author_id",
        }

        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time

        return await self._request_v2("GET", "tweets/search/recent", params=params)

    # ==========================================
    # 3. MEDIA UPLOAD
    # ==========================================

    async def upload_media(
        self,
        media_data: bytes,
        media_type: str = "image/jpeg",
        media_category: str = "tweet_image",
    ) -> Dict[str, Any]:
        """Upload media (image/video/gif) for tweets"""
        url = f"{self.UPLOAD_BASE}/media/upload.json"

        # For images, use simple upload
        if media_category == "tweet_image":
            headers = {
                "Authorization": self._get_oauth_header("POST", url),
            }

            data = aiohttp.FormData()
            data.add_field("media", media_data)

            async with self.session.post(url, headers=headers, data=data) as response:
                return await response.json()

        # For videos, use chunked upload
        return await self._chunked_upload(media_data, media_type, media_category)

    async def _chunked_upload(
        self,
        media_data: bytes,
        media_type: str,
        media_category: str,
    ) -> Dict[str, Any]:
        """Chunked upload for large media files"""
        url = f"{self.UPLOAD_BASE}/media/upload.json"
        total_bytes = len(media_data)

        # INIT
        init_params = {
            "command": "INIT",
            "total_bytes": total_bytes,
            "media_type": media_type,
            "media_category": media_category,
        }

        headers = {"Authorization": self._get_oauth_header("POST", url, init_params)}

        async with self.session.post(url, headers=headers, params=init_params) as response:
            init_result = await response.json()
            media_id = init_result["media_id_string"]

        # APPEND chunks
        chunk_size = 5 * 1024 * 1024  # 5MB chunks
        segment_index = 0

        for i in range(0, total_bytes, chunk_size):
            chunk = media_data[i:i + chunk_size]

            append_params = {
                "command": "APPEND",
                "media_id": media_id,
                "segment_index": segment_index,
            }

            headers = {"Authorization": self._get_oauth_header("POST", url, append_params)}

            data = aiohttp.FormData()
            data.add_field("media", chunk)

            async with self.session.post(
                url,
                headers=headers,
                params=append_params,
                data=data
            ) as response:
                pass  # APPEND returns empty response

            segment_index += 1

        # FINALIZE
        finalize_params = {
            "command": "FINALIZE",
            "media_id": media_id,
        }

        headers = {"Authorization": self._get_oauth_header("POST", url, finalize_params)}

        async with self.session.post(url, headers=headers, params=finalize_params) as response:
            finalize_result = await response.json()

        # Check processing status for videos
        if "processing_info" in finalize_result:
            await self._wait_for_processing(media_id)

        return {"media_id": media_id, "media_id_string": media_id}

    async def _wait_for_processing(self, media_id: str, max_wait: int = 300):
        """Wait for media processing to complete"""
        url = f"{self.UPLOAD_BASE}/media/upload.json"

        for _ in range(max_wait // 5):
            status_params = {
                "command": "STATUS",
                "media_id": media_id,
            }

            headers = {"Authorization": self._get_oauth_header("GET", url, status_params)}

            async with self.session.get(url, headers=headers, params=status_params) as response:
                result = await response.json()

            if "processing_info" not in result:
                return

            state = result["processing_info"]["state"]

            if state == "succeeded":
                return
            elif state == "failed":
                raise Exception(f"Media processing failed: {result}")

            await asyncio.sleep(5)

    # ==========================================
    # 4. USER MANAGEMENT
    # ==========================================

    async def get_user(
        self,
        user_id: str = None,
        username: str = None,
    ) -> Dict[str, Any]:
        """Get user by ID or username"""
        if user_id:
            endpoint = f"users/{user_id}"
        else:
            endpoint = f"users/by/username/{username}"

        return await self._request_v2(
            "GET",
            endpoint,
            params={
                "user.fields": "id,name,username,description,profile_image_url,public_metrics,verified,created_at"
            }
        )

    async def update_profile(
        self,
        name: str = None,
        description: str = None,
        location: str = None,
        url: str = None,
    ) -> Dict[str, Any]:
        """Update user profile"""
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if location:
            data["location"] = location
        if url:
            data["url"] = url

        return await self._request_v1(
            "POST",
            "account/update_profile.json",
            data=data
        )

    # ==========================================
    # 5. FOLLOWERS & FOLLOWING
    # ==========================================

    async def get_followers(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: str = None,
    ) -> Dict[str, Any]:
        """Get user's followers"""
        params = {
            "max_results": max_results,
            "user.fields": "id,name,username,profile_image_url,public_metrics",
        }

        if pagination_token:
            params["pagination_token"] = pagination_token

        return await self._request_v2("GET", f"users/{user_id}/followers", params=params)

    async def get_following(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: str = None,
    ) -> Dict[str, Any]:
        """Get users that user is following"""
        params = {
            "max_results": max_results,
            "user.fields": "id,name,username,profile_image_url,public_metrics",
        }

        if pagination_token:
            params["pagination_token"] = pagination_token

        return await self._request_v2("GET", f"users/{user_id}/following", params=params)

    async def follow_user(self, user_id: str, target_user_id: str) -> Dict[str, Any]:
        """Follow a user"""
        return await self._request_v2(
            "POST",
            f"users/{user_id}/following",
            data={"target_user_id": target_user_id}
        )

    async def unfollow_user(self, user_id: str, target_user_id: str) -> Dict[str, Any]:
        """Unfollow a user"""
        return await self._request_v2(
            "DELETE",
            f"users/{user_id}/following/{target_user_id}"
        )

    # ==========================================
    # 6. LISTS MANAGEMENT
    # ==========================================

    async def create_list(
        self,
        name: str,
        description: str = "",
        private: bool = False,
    ) -> Dict[str, Any]:
        """Create a new list"""
        return await self._request_v2(
            "POST",
            "lists",
            data={
                "name": name,
                "description": description,
                "private": private,
            }
        )

    async def get_list(self, list_id: str) -> Dict[str, Any]:
        """Get list by ID"""
        return await self._request_v2(
            "GET",
            f"lists/{list_id}",
            params={"list.fields": "id,name,description,member_count,follower_count,owner_id"}
        )

    async def add_list_member(self, list_id: str, user_id: str) -> Dict[str, Any]:
        """Add member to list"""
        return await self._request_v2(
            "POST",
            f"lists/{list_id}/members",
            data={"user_id": user_id}
        )

    # ==========================================
    # 7. DIRECT MESSAGES
    # ==========================================

    async def send_dm(
        self,
        recipient_id: str,
        text: str,
        media_id: str = None,
    ) -> Dict[str, Any]:
        """Send direct message"""
        data = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {"recipient_id": recipient_id},
                    "message_data": {"text": text},
                }
            }
        }

        if media_id:
            data["event"]["message_create"]["message_data"]["attachment"] = {
                "type": "media",
                "media": {"id": media_id}
            }

        return await self._request_v1("POST", "direct_messages/events/new.json", data=data)

    async def get_dm_events(self, count: int = 50) -> Dict[str, Any]:
        """Get direct message events"""
        return await self._request_v1(
            "GET",
            "direct_messages/events/list.json",
            params={"count": count}
        )

    # ==========================================
    # 8. TWITTER SPACES
    # ==========================================

    async def get_space(self, space_id: str) -> Dict[str, Any]:
        """Get Space by ID"""
        return await self._request_v2(
            "GET",
            f"spaces/{space_id}",
            params={
                "space.fields": "id,state,title,host_ids,participant_count,scheduled_start,started_at"
            }
        )

    async def search_spaces(
        self,
        query: str,
        state: str = "live",
    ) -> Dict[str, Any]:
        """Search for Spaces"""
        return await self._request_v2(
            "GET",
            "spaces/search",
            params={
                "query": query,
                "state": state,
                "space.fields": "id,state,title,host_ids,participant_count",
            }
        )

    # ==========================================
    # 9. ANALYTICS & METRICS
    # ==========================================

    async def get_tweet_metrics(
        self,
        tweet_ids: List[str],
    ) -> Dict[str, Any]:
        """Get engagement metrics for tweets"""
        return await self._request_v2(
            "GET",
            "tweets",
            params={
                "ids": ",".join(tweet_ids),
                "tweet.fields": "public_metrics,organic_metrics,non_public_metrics",
            }
        )

    async def get_user_metrics(self, user_id: str) -> Dict[str, Any]:
        """Get user public metrics"""
        return await self._request_v2(
            "GET",
            f"users/{user_id}",
            params={"user.fields": "public_metrics"}
        )

    # ==========================================
    # 10. ADS API
    # ==========================================

    async def get_ad_accounts(self) -> Dict[str, Any]:
        """Get advertising accounts"""
        return await self._request_v1("GET", "accounts.json")

    async def create_promoted_tweet(
        self,
        account_id: str,
        tweet_id: str,
        line_item_id: str,
    ) -> Dict[str, Any]:
        """Create a promoted tweet"""
        return await self._request_v1(
            "POST",
            f"accounts/{account_id}/promoted_tweets.json",
            data={
                "tweet_ids": [tweet_id],
                "line_item_id": line_item_id,
            }
        )


# Convenience function
def create_twitter_client(
    api_key: str,
    api_secret: str,
    access_token: str,
    access_token_secret: str,
    bearer_token: str,
) -> TwitterClient:
    """Create a Twitter client with credentials"""
    credentials = TwitterCredentials(
        api_key=api_key,
        api_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        bearer_token=bearer_token,
    )
    return TwitterClient(credentials)
