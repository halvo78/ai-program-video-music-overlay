"""
Tests for Taj Chat Agents
"""

import pytest
import asyncio
from pathlib import Path

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents.base_agent import AgentType, AgentTask, AgentPriority
from app.agents.video_agent import VideoGenerationAgent
from app.agents.music_agent import MusicGenerationAgent
from app.agents.image_agent import ImageGenerationAgent
from app.agents.content_agent import ContentAnalysisAgent
from app.agents.orchestrator import Orchestrator, WorkflowMode


class TestBaseAgent:
    """Test base agent functionality."""

    def test_video_agent_init(self):
        agent = VideoGenerationAgent()
        assert agent.agent_type == AgentType.VIDEO_GENERATION
        assert agent.priority == AgentPriority.CRITICAL
        assert agent.parallel_capable == True
        assert agent.name == "Video Generation Agent"

    def test_music_agent_init(self):
        agent = MusicGenerationAgent()
        assert agent.agent_type == AgentType.MUSIC_GENERATION
        assert agent.name == "Music Generation Agent"

    def test_image_agent_init(self):
        agent = ImageGenerationAgent()
        assert agent.agent_type == AgentType.IMAGE_GENERATION
        assert agent.name == "Image Generation Agent"

    def test_content_agent_init(self):
        agent = ContentAnalysisAgent()
        assert agent.agent_type == AgentType.CONTENT_ANALYSIS
        assert agent.parallel_capable == False  # Runs first


class TestOrchestrator:
    """Test orchestrator functionality."""

    def test_orchestrator_init(self):
        orchestrator = Orchestrator()
        assert orchestrator.agents == {}
        assert orchestrator.active_workflows == {}

    def test_register_agent(self):
        orchestrator = Orchestrator()
        agent = VideoGenerationAgent()
        orchestrator.register_agent(agent)
        assert AgentType.VIDEO_GENERATION in orchestrator.agents

    def test_get_registered_agents(self):
        orchestrator = Orchestrator()
        orchestrator.register_agent(VideoGenerationAgent())
        orchestrator.register_agent(MusicGenerationAgent())
        agents = orchestrator.get_registered_agents()
        assert "video_generation" in agents
        assert "music_generation" in agents


class TestAgentTask:
    """Test agent task creation."""

    def test_task_creation(self):
        task = AgentTask(
            task_id="test_001",
            task_type="video_generation",
            prompt="Create a test video",
        )
        assert task.task_id == "test_001"
        assert task.prompt == "Create a test video"
        assert task.priority == AgentPriority.MEDIUM
        assert task.timeout_seconds == 300


@pytest.mark.asyncio
class TestAgentExecution:
    """Test agent execution (async)."""

    async def test_video_agent_execute(self):
        agent = VideoGenerationAgent()
        task = AgentTask(
            task_id="test_video",
            task_type="video_generation",
            prompt="Test video prompt",
            parameters={"video_type": "text-to-video"},
        )

        result = await agent.run(task)
        assert result.task_id == "test_video"
        assert result.agent_type == AgentType.VIDEO_GENERATION

    async def test_content_agent_execute(self):
        agent = ContentAnalysisAgent()
        task = AgentTask(
            task_id="test_content",
            task_type="content_analysis",
            prompt="Create a motivational video",
            context={"platforms": ["tiktok"]},
        )

        result = await agent.run(task)
        assert result.task_id == "test_content"
        assert result.status in ["success", "error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
