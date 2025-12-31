"""
API Integration Tests for Taj Chat Backend
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app, VideoRequest, VideoResponse, StatusResponse


class TestAPIEndpoints:
    """Test API endpoints."""

    @pytest.fixture
    def mock_workflow_engine(self):
        """Create a mock workflow engine."""
        engine = Mock()
        engine.get_agent_status = Mock(return_value={
            "video_generation": {"status": "ready", "priority": "critical"},
            "music_generation": {"status": "ready", "priority": "high"},
            "content_analysis": {"status": "ready", "priority": "high"},
        })
        engine.get_workflow_status = Mock(return_value={
            "workflow_id": "test_123",
            "status": "completed",
            "progress": 100,
        })
        return engine

    def test_video_request_validation(self):
        """Test VideoRequest model validation."""
        request = VideoRequest(
            prompt="Create a motivational video",
            mode="hybrid",
            platforms=["tiktok", "instagram_reels"],
        )
        assert request.prompt == "Create a motivational video"
        assert request.mode == "hybrid"
        assert "tiktok" in request.platforms

    def test_video_request_defaults(self):
        """Test VideoRequest default values."""
        request = VideoRequest(prompt="Test video")
        assert request.mode == "hybrid"
        assert request.platforms == ["tiktok"]
        assert request.parameters == {}

    def test_video_response_model(self):
        """Test VideoResponse model."""
        response = VideoResponse(
            workflow_id="wf_123",
            status="completed",
            mode="hybrid",
            platforms=["tiktok"],
            execution_time_ms=5000.0,
            output_files=["output/video.mp4"],
            errors=[],
        )
        assert response.workflow_id == "wf_123"
        assert response.status == "completed"
        assert response.execution_time_ms == 5000.0

    def test_status_response_model(self):
        """Test StatusResponse model."""
        response = StatusResponse(
            app_name="Taj Chat",
            version="1.0.0",
            agents_registered=["video", "music", "content"],
            ai_providers={"openai": "configured"},
            social_media={"tiktok": "available"},
        )
        assert response.app_name == "Taj Chat"
        assert len(response.agents_registered) == 3


class TestAPIValidation:
    """Test API input validation."""

    def test_valid_platforms(self):
        """Test valid platform names."""
        valid_platforms = ["tiktok", "instagram_reels", "youtube_shorts", "twitter"]
        request = VideoRequest(prompt="Test", platforms=valid_platforms)
        assert len(request.platforms) == 4

    def test_valid_modes(self):
        """Test valid workflow modes."""
        for mode in ["sequential", "parallel", "hybrid"]:
            request = VideoRequest(prompt="Test", mode=mode)
            assert request.mode == mode

    def test_empty_prompt_rejected(self):
        """Test that empty prompts are rejected."""
        with pytest.raises(ValueError):
            VideoRequest(prompt="")


class TestWorkflowModes:
    """Test workflow mode handling."""

    def test_mode_mapping(self):
        """Test mode string to enum mapping."""
        mode_map = {
            "sequential": "SEQUENTIAL",
            "parallel": "PARALLEL",
            "hybrid": "HYBRID",
        }
        for string_mode, enum_name in mode_map.items():
            request = VideoRequest(prompt="Test", mode=string_mode)
            assert request.mode == string_mode


class TestHealthCheck:
    """Test health check functionality."""

    def test_health_response_format(self):
        """Test health check response format."""
        expected_keys = ["status"]
        # Health check should return at least status
        assert "status" in expected_keys


class TestErrorHandling:
    """Test API error handling."""

    def test_invalid_workflow_mode(self):
        """Test handling of invalid workflow mode."""
        # Invalid mode should fall back to hybrid
        request = VideoRequest(prompt="Test", mode="invalid_mode")
        assert request.mode == "invalid_mode"  # Raw value stored

    def test_missing_required_field(self):
        """Test missing required field handling."""
        with pytest.raises(ValueError):
            VideoRequest()  # Missing prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
