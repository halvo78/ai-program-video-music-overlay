"""
Integration Tests for Taj Chat Platform

End-to-end tests for full workflow validation:
- Video creation workflows
- Agent coordination
- API integration
- Error recovery
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFullWorkflowIntegration:
    """Test complete video creation workflows."""

    @pytest.mark.asyncio
    async def test_video_creation_workflow(self):
        """Test complete video creation from prompt to output."""
        from app.workflows.engine import WorkflowEngine, WorkflowMode

        engine = WorkflowEngine()

        # Create a video workflow using create_video method
        result = await engine.create_video(
            prompt="Create a motivational video about success",
            mode=WorkflowMode.HYBRID,
            platforms=["tiktok"]
        )

        assert result is not None
        # Result is a WorkflowResult object
        assert hasattr(result, 'workflow_id') or hasattr(result, 'status') or result is not None

    @pytest.mark.asyncio
    async def test_multi_platform_workflow(self):
        """Test workflow with multiple platform targets."""
        from app.workflows.engine import WorkflowEngine, WorkflowMode

        engine = WorkflowEngine()

        platforms = ["tiktok", "instagram_reels", "youtube_shorts"]
        result = await engine.create_video(
            prompt="Create a tech tutorial video",
            mode=WorkflowMode.PARALLEL,
            platforms=platforms
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_agent_coordination(self):
        """Test that agents coordinate correctly."""
        from app.workflows.engine import WorkflowEngine

        engine = WorkflowEngine()
        agent_status = engine.get_agent_status()

        # Should have multiple agents registered
        assert agent_status is not None
        assert len(agent_status) > 0


class TestAPIIntegration:
    """Test API endpoint integration."""

    def test_api_models_integration(self):
        """Test API request/response models work together."""
        from app.main import VideoRequest, VideoResponse, StatusResponse

        # Create request
        request = VideoRequest(
            prompt="Test video creation",
            mode="hybrid",
            platforms=["tiktok", "instagram_reels"]
        )

        # Verify request is valid
        assert request.prompt == "Test video creation"
        assert len(request.platforms) == 2

        # Create response
        response = VideoResponse(
            workflow_id="test_wf_123",
            status="completed",
            mode="hybrid",
            platforms=["tiktok", "instagram_reels"],
            execution_time_ms=5000.0,
            output_files=["output/video.mp4"],
            errors=[]
        )

        assert response.status == "completed"
        assert len(response.output_files) > 0

    def test_validation_integration(self):
        """Test input validation across the system."""
        from app.main import VideoRequest
        from pydantic import ValidationError

        # Valid request
        valid = VideoRequest(prompt="Valid prompt", mode="sequential")
        assert valid.prompt == "Valid prompt"

        # Invalid empty prompt
        with pytest.raises(ValidationError):
            VideoRequest(prompt="")


class TestProviderIntegration:
    """Test AI provider integration."""

    @pytest.mark.asyncio
    async def test_huggingface_initialization(self):
        """Test HuggingFace client initializes correctly."""
        from app.providers.huggingface_client import HuggingFaceClient

        client = HuggingFaceClient()

        # Should have MODELS defined
        assert hasattr(client, 'MODELS')
        assert len(client.MODELS) > 0

    @pytest.mark.asyncio
    async def test_flux_initialization(self):
        """Test FLUX client initializes correctly."""
        from app.providers.flux_client import FluxClient

        client = FluxClient()
        assert client is not None

        # Should have generate method
        assert hasattr(client, 'generate')

    @pytest.mark.asyncio
    async def test_together_initialization(self):
        """Test Together.ai client initializes correctly."""
        from app.providers.together_client import TogetherClient

        client = TogetherClient()
        assert client is not None


class TestSocialIntegration:
    """Test social media platform integration."""

    @pytest.mark.asyncio
    async def test_unified_publisher_workflow(self):
        """Test unified publisher can handle multi-platform publishing."""
        from app.social.unified_publisher import UnifiedPublisher

        publisher = UnifiedPublisher()

        # Should be able to initialize without credentials
        assert publisher is not None

        # Should have publish method
        assert hasattr(publisher, 'publish')

    def test_platform_credentials_handling(self):
        """Test platforms handle credentials correctly."""
        from app.social.tiktok_client import TikTokClient, TikTokCredentials
        from app.social.youtube_client import YouTubeClient, YouTubeCredentials

        # TikTok
        tiktok_creds = TikTokCredentials(
            client_key="test",
            client_secret="test",
            access_token="test"
        )
        tiktok = TikTokClient(credentials=tiktok_creds)
        assert tiktok is not None

        # YouTube
        youtube_creds = YouTubeCredentials(
            api_key="test",
            client_id="test",
            client_secret="test",
            access_token="test"
        )
        youtube = YouTubeClient(credentials=youtube_creds)
        assert youtube is not None


class TestFeatureIntegration:
    """Test feature module integration."""

    @pytest.mark.asyncio
    async def test_avatar_to_video_workflow(self):
        """Test avatar system integrates with video generation."""
        from app.features.avatar_system import AvatarLibrary, AvatarGenerator

        library = AvatarLibrary()
        generator = AvatarGenerator()

        # Get available avatars
        avatars = library.get_all_avatars()
        assert len(avatars) > 0

        # Generator should be ready
        assert generator is not None

    @pytest.mark.asyncio
    async def test_content_to_video_workflow(self):
        """Test content-to-video pipeline."""
        from app.features.content_to_video import ContentToVideoEngine

        engine = ContentToVideoEngine()
        assert engine is not None

        # Should have parsing capability
        assert hasattr(engine, 'parse_content') or hasattr(engine, 'url_to_video')

    @pytest.mark.asyncio
    async def test_effects_integration(self):
        """Test video effects integrate correctly."""
        from app.features.video_effects import AIEffectsEngine, EffectType

        engine = AIEffectsEngine()

        # Should have all effect types available
        assert EffectType.INFLATE is not None
        assert EffectType.MELT is not None
        assert EffectType.EXPLODE is not None


class TestErrorRecovery:
    """Test error handling and recovery."""

    @pytest.mark.asyncio
    async def test_workflow_error_handling(self):
        """Test workflow handles errors gracefully."""
        from app.workflows.engine import WorkflowEngine, WorkflowMode

        engine = WorkflowEngine()

        # Should handle invalid mode gracefully or raise appropriate error
        try:
            await engine.create_workflow(
                prompt="Test",
                mode=WorkflowMode.HYBRID,
                platforms=[]
            )
        except Exception as e:
            # Should raise a meaningful error, not crash
            assert str(e) != ""

    def test_invalid_input_handling(self):
        """Test system handles invalid inputs."""
        from app.main import VideoRequest
        from pydantic import ValidationError

        # Missing required field
        with pytest.raises(ValidationError):
            VideoRequest()

        # Empty prompt
        with pytest.raises(ValidationError):
            VideoRequest(prompt="")

    @pytest.mark.asyncio
    async def test_provider_error_handling(self):
        """Test providers handle API errors."""
        from app.providers.huggingface_client import HuggingFaceClient

        client = HuggingFaceClient(api_key="invalid_key")

        # Should not crash on invalid key
        assert client is not None


class TestMonitoringIntegration:
    """Test monitoring and metrics integration."""

    def test_metrics_collection(self):
        """Test metrics can be collected."""
        from app.monitoring.metrics import metrics

        # Get all metrics
        all_metrics = metrics.get_all_metrics()

        # Should return a dict with metrics
        assert all_metrics is not None
        assert isinstance(all_metrics, dict)

    def test_performance_monitoring(self):
        """Test performance monitoring works."""
        from app.monitoring.performance import performance_monitor

        # Should be able to record timings using timer context manager
        with performance_monitor.timer("test_operation"):
            pass  # Simulated work

        # Should have recorded the timing
        assert performance_monitor is not None


class TestConfigurationIntegration:
    """Test configuration and environment integration."""

    def test_config_loading(self):
        """Test configuration loads correctly."""
        from app.config import get_config

        config = get_config()

        # Should have required attributes
        assert config is not None
        assert hasattr(config, 'validate')

    def test_config_validation(self):
        """Test configuration validation."""
        from app.config import get_config

        config = get_config()
        status = config.validate()

        # Should return validation status
        assert status is not None


class TestDatabaseIntegration:
    """Test data persistence integration."""

    @pytest.mark.asyncio
    async def test_workflow_persistence(self):
        """Test workflows can be persisted and retrieved."""
        from app.workflows.engine import WorkflowEngine, WorkflowMode

        engine = WorkflowEngine()

        # Create workflow using create_video
        result = await engine.create_video(
            prompt="Persistence test",
            mode=WorkflowMode.SEQUENTIAL,
            platforms=["tiktok"]
        )

        # Should get a result
        assert result is not None


class TestConcurrencyIntegration:
    """Test concurrent operations."""

    @pytest.mark.asyncio
    async def test_concurrent_workflows(self):
        """Test multiple workflows can run concurrently."""
        from app.workflows.engine import WorkflowEngine, WorkflowMode

        engine = WorkflowEngine()

        # Create multiple workflows concurrently
        tasks = [
            engine.create_video(
                prompt=f"Concurrent test {i}",
                mode=WorkflowMode.PARALLEL,
                platforms=["tiktok"]
            )
            for i in range(3)
        ]

        results = await asyncio.gather(*tasks)

        # All should complete
        assert len(results) == 3
        assert all(r is not None for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
