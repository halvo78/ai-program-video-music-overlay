"""
Workflow Engine

Main entry point for video creation workflows.
"""

import logging
from enum import Enum
from typing import Optional

from ..agents.orchestrator import Orchestrator, WorkflowMode, WorkflowResult
from ..agents import (
    VideoGenerationAgent,
    MusicGenerationAgent,
    ImageGenerationAgent,
    VoiceSpeechAgent,
    ContentAnalysisAgent,
    EditingAgent,
    OptimizationAgent,
    AnalyticsAgent,
    SafetyComplianceAgent,
    SocialMediaAgent,
)

logger = logging.getLogger(__name__)

# Re-export WorkflowMode
WorkflowMode = WorkflowMode


class WorkflowEngine:
    """
    Main workflow engine for Taj Chat.

    Initializes all 10 specialist agents and coordinates
    video creation through the orchestrator.
    """

    def __init__(self):
        """Initialize workflow engine with all agents."""

        logger.info("Initializing Taj Chat Workflow Engine...")

        # Create orchestrator
        self.orchestrator = Orchestrator()

        # Initialize and register all 10 agents
        agents = [
            VideoGenerationAgent(),
            MusicGenerationAgent(),
            ImageGenerationAgent(),
            VoiceSpeechAgent(),
            ContentAnalysisAgent(),
            EditingAgent(),
            OptimizationAgent(),
            AnalyticsAgent(),
            SafetyComplianceAgent(),
            SocialMediaAgent(),
        ]

        for agent in agents:
            self.orchestrator.register_agent(agent)

        logger.info(f"Registered {len(agents)} specialist agents")

    async def create_video(
        self,
        prompt: str,
        mode: WorkflowMode = WorkflowMode.HYBRID,
        platforms: Optional[list[str]] = None,
        parameters: Optional[dict] = None,
    ) -> WorkflowResult:
        """
        Create a video using the 10x agent system.

        Args:
            prompt: Description of the video to create
            mode: Workflow mode (SEQUENTIAL, PARALLEL, HYBRID)
            platforms: Target platforms (tiktok, instagram_reels, youtube_shorts, twitter)
            parameters: Additional parameters

        Returns:
            WorkflowResult with output files and status
        """
        platforms = platforms or ["tiktok"]
        parameters = parameters or {}

        logger.info(f"Creating video: {prompt[:50]}...")
        logger.info(f"Mode: {mode.value}, Platforms: {platforms}")

        return await self.orchestrator.create_video(
            prompt=prompt,
            mode=mode,
            parameters=parameters,
            platforms=platforms,
        )

    async def create_video_sequential(
        self,
        prompt: str,
        platforms: Optional[list[str]] = None,
        **kwargs,
    ) -> WorkflowResult:
        """Create video using sequential workflow (highest quality)."""
        return await self.create_video(
            prompt=prompt,
            mode=WorkflowMode.SEQUENTIAL,
            platforms=platforms,
            parameters=kwargs,
        )

    async def create_video_parallel(
        self,
        prompt: str,
        platforms: Optional[list[str]] = None,
        **kwargs,
    ) -> WorkflowResult:
        """Create video using parallel workflow (fastest)."""
        return await self.create_video(
            prompt=prompt,
            mode=WorkflowMode.PARALLEL,
            platforms=platforms,
            parameters=kwargs,
        )

    async def create_video_hybrid(
        self,
        prompt: str,
        platforms: Optional[list[str]] = None,
        **kwargs,
    ) -> WorkflowResult:
        """Create video using hybrid workflow (balanced)."""
        return await self.create_video(
            prompt=prompt,
            mode=WorkflowMode.HYBRID,
            platforms=platforms,
            parameters=kwargs,
        )

    def get_agent_status(self) -> dict:
        """Get status of all agents."""
        return self.orchestrator.get_all_agent_status()

    def get_workflow_status(self, workflow_id: str) -> Optional[dict]:
        """Get status of a specific workflow."""
        return self.orchestrator.get_workflow_status(workflow_id)
