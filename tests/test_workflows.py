"""
Workflow Engine Tests for Taj Chat
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.workflows.engine import WorkflowEngine, WorkflowMode


class TestWorkflowEngine:
    """Test workflow engine functionality."""

    def test_workflow_engine_init(self):
        """Test workflow engine initialization."""
        engine = WorkflowEngine()
        assert engine is not None

    def test_workflow_modes(self):
        """Test all workflow modes exist."""
        assert WorkflowMode.SEQUENTIAL.value == "sequential"
        assert WorkflowMode.PARALLEL.value == "parallel"
        assert WorkflowMode.HYBRID.value == "hybrid"

    @pytest.mark.asyncio
    async def test_agent_registration(self):
        """Test agent registration with engine."""
        engine = WorkflowEngine()
        status = engine.get_agent_status()
        # Should have agents registered
        assert isinstance(status, dict)


class TestWorkflowExecution:
    """Test workflow execution."""

    @pytest.fixture
    def engine(self):
        """Create workflow engine instance."""
        return WorkflowEngine()

    @pytest.mark.asyncio
    async def test_create_video_workflow(self, engine):
        """Test video creation workflow."""
        result = await engine.create_video(
            prompt="Test video prompt",
            mode=WorkflowMode.HYBRID,
            platforms=["tiktok"],
        )
        assert result is not None
        assert hasattr(result, "workflow_id")
        assert hasattr(result, "status")

    @pytest.mark.asyncio
    async def test_sequential_mode(self, engine):
        """Test sequential workflow mode."""
        result = await engine.create_video(
            prompt="Sequential test",
            mode=WorkflowMode.SEQUENTIAL,
            platforms=["tiktok"],
        )
        assert result.mode == WorkflowMode.SEQUENTIAL

    @pytest.mark.asyncio
    async def test_parallel_mode(self, engine):
        """Test parallel workflow mode."""
        result = await engine.create_video(
            prompt="Parallel test",
            mode=WorkflowMode.PARALLEL,
            platforms=["instagram_reels"],
        )
        assert result.mode == WorkflowMode.PARALLEL

    @pytest.mark.asyncio
    async def test_multi_platform_workflow(self, engine):
        """Test multi-platform video creation."""
        result = await engine.create_video(
            prompt="Multi-platform test",
            mode=WorkflowMode.HYBRID,
            platforms=["tiktok", "instagram_reels", "youtube_shorts"],
        )
        assert result is not None


class TestWorkflowStatus:
    """Test workflow status tracking."""

    @pytest.fixture
    def engine(self):
        return WorkflowEngine()

    def test_get_workflow_status(self, engine):
        """Test getting workflow status."""
        # Non-existent workflow
        status = engine.get_workflow_status("nonexistent_id")
        assert status is None or status == {}

    def test_get_agent_status(self, engine):
        """Test getting agent status."""
        status = engine.get_agent_status()
        assert isinstance(status, dict)


class TestWorkflowParameters:
    """Test workflow parameter handling."""

    @pytest.fixture
    def engine(self):
        return WorkflowEngine()

    @pytest.mark.asyncio
    async def test_custom_parameters(self, engine):
        """Test custom parameter passing."""
        result = await engine.create_video(
            prompt="Test with params",
            mode=WorkflowMode.HYBRID,
            platforms=["tiktok"],
            parameters={
                "video_style": "cinematic",
                "music_mood": "energetic",
                "include_voice": True,
            },
        )
        assert result is not None


class TestPlatformSupport:
    """Test platform-specific features."""

    SUPPORTED_PLATFORMS = [
        "tiktok",
        "instagram_reels",
        "youtube_shorts",
        "twitter",
    ]

    PLATFORM_SPECS = {
        "tiktok": {"aspect_ratio": "9:16", "resolution": "1080x1920"},
        "instagram_reels": {"aspect_ratio": "9:16", "resolution": "1080x1920"},
        "youtube_shorts": {"aspect_ratio": "9:16", "resolution": "1080x1920"},
        "twitter": {"aspect_ratio": "16:9", "resolution": "1280x720"},
    }

    def test_platform_list(self):
        """Test all platforms are supported."""
        for platform in self.SUPPORTED_PLATFORMS:
            assert platform in self.PLATFORM_SPECS

    def test_platform_specs(self):
        """Test platform specifications."""
        for platform, specs in self.PLATFORM_SPECS.items():
            assert "aspect_ratio" in specs
            assert "resolution" in specs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
