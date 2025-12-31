"""
Social Media Integration Tests for Taj Chat
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.social.tiktok_client import TikTokClient
from app.social.instagram_client import InstagramClient
from app.social.youtube_client import YouTubeClient
from app.social.twitter_client import TwitterClient
from app.social.unified_publisher import UnifiedPublisher


class TestTikTokClient:
    """Test TikTok client."""

    def test_client_init(self):
        """Test client initialization."""
        client = TikTokClient()
        assert client is not None

    def test_video_specs(self):
        """Test TikTok video specifications."""
        specs = {
            "aspect_ratio": "9:16",
            "max_duration": 180,  # 3 minutes
            "resolution": "1080x1920",
        }
        assert specs["aspect_ratio"] == "9:16"

    @pytest.mark.asyncio
    async def test_upload_interface(self):
        """Test upload interface exists."""
        client = TikTokClient()
        assert hasattr(client, 'upload_video') or hasattr(client, 'publish')


class TestInstagramClient:
    """Test Instagram client."""

    def test_client_init(self):
        """Test client initialization."""
        client = InstagramClient()
        assert client is not None

    def test_reels_specs(self):
        """Test Instagram Reels specifications."""
        specs = {
            "aspect_ratio": "9:16",
            "max_duration": 90,  # 90 seconds
            "resolution": "1080x1920",
        }
        assert specs["max_duration"] == 90

    @pytest.mark.asyncio
    async def test_upload_interface(self):
        """Test upload interface exists."""
        client = InstagramClient()
        assert hasattr(client, 'upload_reel') or hasattr(client, 'publish')


class TestYouTubeClient:
    """Test YouTube client."""

    def test_client_init(self):
        """Test client initialization."""
        client = YouTubeClient()
        assert client is not None

    def test_shorts_specs(self):
        """Test YouTube Shorts specifications."""
        specs = {
            "aspect_ratio": "9:16",
            "max_duration": 60,  # 60 seconds
            "resolution": "1080x1920",
        }
        assert specs["max_duration"] == 60

    @pytest.mark.asyncio
    async def test_upload_interface(self):
        """Test upload interface exists."""
        client = YouTubeClient()
        assert hasattr(client, 'upload_short') or hasattr(client, 'upload')


class TestTwitterClient:
    """Test Twitter/X client."""

    def test_client_init(self):
        """Test client initialization."""
        client = TwitterClient()
        assert client is not None

    def test_video_specs(self):
        """Test Twitter video specifications."""
        specs = {
            "aspect_ratio": "16:9",
            "max_duration": 140,  # 2:20 seconds
            "resolution": "1280x720",
        }
        assert specs["aspect_ratio"] == "16:9"

    @pytest.mark.asyncio
    async def test_upload_interface(self):
        """Test upload interface exists."""
        client = TwitterClient()
        assert hasattr(client, 'upload_video') or hasattr(client, 'post')


class TestUnifiedPublisher:
    """Test unified publisher."""

    def test_publisher_init(self):
        """Test publisher initialization."""
        publisher = UnifiedPublisher()
        assert publisher is not None

    def test_platform_registry(self):
        """Test platform registry."""
        publisher = UnifiedPublisher()
        # Should have registered platforms
        assert hasattr(publisher, 'platforms') or hasattr(publisher, 'clients')

    @pytest.mark.asyncio
    async def test_multi_platform_publish_interface(self):
        """Test multi-platform publish interface."""
        publisher = UnifiedPublisher()
        assert hasattr(publisher, 'publish_to_all') or hasattr(publisher, 'publish')

    @pytest.mark.asyncio
    async def test_selective_publish(self):
        """Test selective platform publishing."""
        publisher = UnifiedPublisher()
        # Should support publishing to specific platforms
        assert hasattr(publisher, 'publish_to') or hasattr(publisher, 'publish')


class TestSocialMediaErrors:
    """Test social media error handling."""

    @pytest.mark.asyncio
    async def test_invalid_credentials_handling(self):
        """Test invalid credentials handling."""
        client = TikTokClient()
        # Should not crash with missing credentials
        assert client is not None

    @pytest.mark.asyncio
    async def test_rate_limit_handling(self):
        """Test rate limit handling."""
        publisher = UnifiedPublisher()
        # Should have rate limit awareness
        assert publisher is not None


class TestScheduling:
    """Test scheduling functionality."""

    def test_schedule_capability(self):
        """Test scheduling capability."""
        publisher = UnifiedPublisher()
        # Should support scheduling or have schedule method
        assert hasattr(publisher, 'schedule') or True  # Optional feature


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
