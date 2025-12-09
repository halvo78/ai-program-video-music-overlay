"""
Orchestrator Agent - Master Coordinator

Coordinates all 10 specialist agents using:
- Sequential workflows (full quality)
- Parallel workflows (fast mode)
- Hybrid workflows (balanced)

Pattern adapted from UTS multi-agent validator.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from enum import Enum
import uuid

from .base_agent import (
    BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult
)

logger = logging.getLogger(__name__)


class WorkflowMode(Enum):
    """Workflow execution modes."""
    SEQUENTIAL = "sequential"  # Full quality, step by step
    PARALLEL = "parallel"      # Fast mode, concurrent generation
    HYBRID = "hybrid"          # Balanced approach


@dataclass
class WorkflowStep:
    """A step in a workflow."""
    step_id: str
    agent_type: AgentType
    task: AgentTask
    depends_on: list[str] = field(default_factory=list)
    result: Optional[AgentResult] = None


@dataclass
class WorkflowResult:
    """Result of a complete workflow execution."""
    workflow_id: str
    mode: WorkflowMode
    status: str  # success, partial, error
    steps: list[WorkflowStep] = field(default_factory=list)
    final_output: Any = None
    output_files: list = field(default_factory=list)
    total_execution_time_ms: float = 0
    agent_results: dict[str, AgentResult] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class Orchestrator:
    """
    Master Orchestrator for Taj Chat.

    Coordinates 10 specialist agents:
    1. Content Analysis (first - informs others)
    2. Video Generation (parallel)
    3. Music Generation (parallel)
    4. Image Generation (parallel)
    5. Voice & Speech (parallel)
    6. Editing (sequential - needs generation outputs)
    7. Optimization (sequential)
    8. Analytics (can run parallel)
    9. Safety (sequential - must check before export)
    10. Social Media (last - uploads final product)
    """

    def __init__(self):
        self.agents: dict[AgentType, BaseAgent] = {}
        self.active_workflows: dict[str, WorkflowResult] = {}

        logger.info("Orchestrator initialized")

    def register_agent(self, agent: BaseAgent):
        """Register a specialist agent."""
        self.agents[agent.agent_type] = agent
        logger.info(f"Registered agent: {agent.name}")

    def get_registered_agents(self) -> list[str]:
        """Get list of registered agent types."""
        return [a.value for a in self.agents.keys()]

    async def run_sequential(
        self,
        prompt: str,
        parameters: dict = None,
        platforms: list[str] = None,
    ) -> WorkflowResult:
        """
        Run full sequential workflow for maximum quality.

        Order:
        1. Content Analysis → Analyze prompt, generate script
        2. Video Generation → Generate base video
        3. Music Generation → Generate matching music
        4. Image Generation → Generate overlays
        5. Voice Agent → Generate narration (if needed)
        6. Editing Agent → Compose all elements
        7. Optimization Agent → Platform-specific optimization
        8. Safety Agent → Content moderation check
        9. Social Media Agent → Upload to platforms
        """
        workflow_id = f"seq_{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()

        logger.info(f"Starting sequential workflow: {workflow_id}")

        result = WorkflowResult(
            workflow_id=workflow_id,
            mode=WorkflowMode.SEQUENTIAL,
            status="running",
        )
        self.active_workflows[workflow_id] = result

        parameters = parameters or {}
        platforms = platforms or ["tiktok"]

        # Define sequential order
        sequential_order = [
            AgentType.CONTENT_ANALYSIS,
            AgentType.VIDEO_GENERATION,
            AgentType.MUSIC_GENERATION,
            AgentType.IMAGE_GENERATION,
            AgentType.VOICE_SPEECH,
            AgentType.EDITING,
            AgentType.OPTIMIZATION,
            AgentType.SAFETY,
            AgentType.SOCIAL_MEDIA,
        ]

        context = {"prompt": prompt, "parameters": parameters, "platforms": platforms}

        for agent_type in sequential_order:
            if agent_type not in self.agents:
                logger.warning(f"Agent {agent_type.value} not registered, skipping")
                continue

            agent = self.agents[agent_type]

            task = AgentTask(
                task_id=f"{workflow_id}_{agent_type.value}",
                task_type=agent_type.value,
                prompt=prompt,
                parameters=parameters,
                context=context,
            )

            agent_result = await agent.run(task)
            result.agent_results[agent_type.value] = agent_result

            # Update context with result for next agent
            if agent_result.status == "success":
                context[agent_type.value] = agent_result.output
                if agent_result.output_files:
                    context[f"{agent_type.value}_files"] = agent_result.output_files
            else:
                result.errors.append(f"{agent_type.value}: {agent_result.error}")
                # Continue with warnings for non-critical agents
                if agent_type in [AgentType.SAFETY, AgentType.CONTENT_ANALYSIS]:
                    logger.error(f"Critical agent {agent_type.value} failed, stopping workflow")
                    break

        # Finalize
        result.total_execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        result.status = "success" if not result.errors else "partial" if len(result.errors) < 3 else "error"

        # Get final output files from social media agent
        if AgentType.SOCIAL_MEDIA.value in result.agent_results:
            social_result = result.agent_results[AgentType.SOCIAL_MEDIA.value]
            result.output_files = social_result.output_files
            result.final_output = social_result.output

        logger.info(
            f"Sequential workflow {workflow_id} completed: {result.status} "
            f"in {result.total_execution_time_ms:.0f}ms"
        )

        return result

    async def run_parallel(
        self,
        prompt: str,
        parameters: dict = None,
        platforms: list[str] = None,
    ) -> WorkflowResult:
        """
        Run parallel workflow for speed.

        Phase 1 (Parallel):
        - Content Analysis
        - Video Generation
        - Music Generation
        - Image Generation
        - Voice & Speech

        Phase 2 (Sequential):
        - Editing → Optimization → Safety → Social Media
        """
        workflow_id = f"par_{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()

        logger.info(f"Starting parallel workflow: {workflow_id}")

        result = WorkflowResult(
            workflow_id=workflow_id,
            mode=WorkflowMode.PARALLEL,
            status="running",
        )
        self.active_workflows[workflow_id] = result

        parameters = parameters or {}
        platforms = platforms or ["tiktok"]
        context = {"prompt": prompt, "parameters": parameters, "platforms": platforms}

        # Phase 1: Parallel generation
        parallel_agents = [
            AgentType.CONTENT_ANALYSIS,
            AgentType.VIDEO_GENERATION,
            AgentType.MUSIC_GENERATION,
            AgentType.IMAGE_GENERATION,
            AgentType.VOICE_SPEECH,
        ]

        parallel_tasks = []
        for agent_type in parallel_agents:
            if agent_type in self.agents:
                agent = self.agents[agent_type]
                task = AgentTask(
                    task_id=f"{workflow_id}_{agent_type.value}",
                    task_type=agent_type.value,
                    prompt=prompt,
                    parameters=parameters,
                    context=context,
                )
                parallel_tasks.append((agent_type, agent.run(task)))

        # Run all parallel tasks
        logger.info(f"Running {len(parallel_tasks)} agents in parallel...")
        parallel_results = await asyncio.gather(
            *[task for _, task in parallel_tasks],
            return_exceptions=True
        )

        # Collect parallel results
        for i, (agent_type, _) in enumerate(parallel_tasks):
            agent_result = parallel_results[i]
            if isinstance(agent_result, AgentResult):
                result.agent_results[agent_type.value] = agent_result
                if agent_result.status == "success":
                    context[agent_type.value] = agent_result.output
                    if agent_result.output_files:
                        context[f"{agent_type.value}_files"] = agent_result.output_files
                else:
                    result.errors.append(f"{agent_type.value}: {agent_result.error}")
            else:
                result.errors.append(f"{agent_type.value}: {str(agent_result)}")

        # Phase 2: Sequential processing
        sequential_agents = [
            AgentType.EDITING,
            AgentType.OPTIMIZATION,
            AgentType.SAFETY,
            AgentType.SOCIAL_MEDIA,
        ]

        for agent_type in sequential_agents:
            if agent_type not in self.agents:
                continue

            agent = self.agents[agent_type]
            task = AgentTask(
                task_id=f"{workflow_id}_{agent_type.value}",
                task_type=agent_type.value,
                prompt=prompt,
                parameters=parameters,
                context=context,
            )

            agent_result = await agent.run(task)
            result.agent_results[agent_type.value] = agent_result

            if agent_result.status == "success":
                context[agent_type.value] = agent_result.output
                if agent_result.output_files:
                    context[f"{agent_type.value}_files"] = agent_result.output_files
            else:
                result.errors.append(f"{agent_type.value}: {agent_result.error}")

        # Finalize
        result.total_execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        result.status = "success" if not result.errors else "partial" if len(result.errors) < 3 else "error"

        if AgentType.SOCIAL_MEDIA.value in result.agent_results:
            social_result = result.agent_results[AgentType.SOCIAL_MEDIA.value]
            result.output_files = social_result.output_files
            result.final_output = social_result.output

        logger.info(
            f"Parallel workflow {workflow_id} completed: {result.status} "
            f"in {result.total_execution_time_ms:.0f}ms"
        )

        return result

    async def run_hybrid(
        self,
        prompt: str,
        parameters: dict = None,
        platforms: list[str] = None,
    ) -> WorkflowResult:
        """
        Run hybrid workflow for balance.

        Phase 1 (Sequential): Content Analysis first
        Phase 2 (Parallel): Video + Music + Image + Voice
        Phase 3 (Sequential): Editing → Optimization → Safety → Social
        """
        workflow_id = f"hyb_{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()

        logger.info(f"Starting hybrid workflow: {workflow_id}")

        result = WorkflowResult(
            workflow_id=workflow_id,
            mode=WorkflowMode.HYBRID,
            status="running",
        )
        self.active_workflows[workflow_id] = result

        parameters = parameters or {}
        platforms = platforms or ["tiktok"]
        context = {"prompt": prompt, "parameters": parameters, "platforms": platforms}

        # Phase 1: Content Analysis first (informs other agents)
        if AgentType.CONTENT_ANALYSIS in self.agents:
            agent = self.agents[AgentType.CONTENT_ANALYSIS]
            task = AgentTask(
                task_id=f"{workflow_id}_content_analysis",
                task_type="content_analysis",
                prompt=prompt,
                parameters=parameters,
                context=context,
            )
            content_result = await agent.run(task)
            result.agent_results["content_analysis"] = content_result

            if content_result.status == "success":
                context["content_analysis"] = content_result.output
                # Use content analysis to enhance prompts for other agents
                if isinstance(content_result.output, dict):
                    context["script"] = content_result.output.get("script", prompt)
                    context["keywords"] = content_result.output.get("keywords", [])
                    context["mood"] = content_result.output.get("mood", "neutral")

        # Phase 2: Parallel generation with enhanced context
        parallel_agents = [
            AgentType.VIDEO_GENERATION,
            AgentType.MUSIC_GENERATION,
            AgentType.IMAGE_GENERATION,
            AgentType.VOICE_SPEECH,
        ]

        parallel_tasks = []
        for agent_type in parallel_agents:
            if agent_type in self.agents:
                agent = self.agents[agent_type]
                task = AgentTask(
                    task_id=f"{workflow_id}_{agent_type.value}",
                    task_type=agent_type.value,
                    prompt=context.get("script", prompt),  # Use enhanced script
                    parameters=parameters,
                    context=context,
                )
                parallel_tasks.append((agent_type, agent.run(task)))

        parallel_results = await asyncio.gather(
            *[task for _, task in parallel_tasks],
            return_exceptions=True
        )

        for i, (agent_type, _) in enumerate(parallel_tasks):
            agent_result = parallel_results[i]
            if isinstance(agent_result, AgentResult):
                result.agent_results[agent_type.value] = agent_result
                if agent_result.status == "success":
                    context[agent_type.value] = agent_result.output
                    if agent_result.output_files:
                        context[f"{agent_type.value}_files"] = agent_result.output_files
                else:
                    result.errors.append(f"{agent_type.value}: {agent_result.error}")

        # Phase 3: Sequential processing
        sequential_agents = [
            AgentType.EDITING,
            AgentType.OPTIMIZATION,
            AgentType.SAFETY,
            AgentType.SOCIAL_MEDIA,
        ]

        for agent_type in sequential_agents:
            if agent_type not in self.agents:
                continue

            agent = self.agents[agent_type]
            task = AgentTask(
                task_id=f"{workflow_id}_{agent_type.value}",
                task_type=agent_type.value,
                prompt=prompt,
                parameters=parameters,
                context=context,
            )

            agent_result = await agent.run(task)
            result.agent_results[agent_type.value] = agent_result

            if agent_result.status == "success":
                context[agent_type.value] = agent_result.output
                if agent_result.output_files:
                    context[f"{agent_type.value}_files"] = agent_result.output_files
            else:
                result.errors.append(f"{agent_type.value}: {agent_result.error}")

        # Finalize
        result.total_execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        result.status = "success" if not result.errors else "partial" if len(result.errors) < 3 else "error"

        if AgentType.SOCIAL_MEDIA.value in result.agent_results:
            social_result = result.agent_results[AgentType.SOCIAL_MEDIA.value]
            result.output_files = social_result.output_files
            result.final_output = social_result.output

        logger.info(
            f"Hybrid workflow {workflow_id} completed: {result.status} "
            f"in {result.total_execution_time_ms:.0f}ms"
        )

        return result

    async def create_video(
        self,
        prompt: str,
        mode: WorkflowMode = WorkflowMode.HYBRID,
        parameters: dict = None,
        platforms: list[str] = None,
    ) -> WorkflowResult:
        """
        Main entry point for video creation.

        Args:
            prompt: Description of the video to create
            mode: Workflow mode (sequential, parallel, hybrid)
            parameters: Additional parameters
            platforms: Target platforms (tiktok, instagram_reels, youtube_shorts, twitter)

        Returns:
            WorkflowResult with output files and status
        """
        if mode == WorkflowMode.SEQUENTIAL:
            return await self.run_sequential(prompt, parameters, platforms)
        elif mode == WorkflowMode.PARALLEL:
            return await self.run_parallel(prompt, parameters, platforms)
        else:
            return await self.run_hybrid(prompt, parameters, platforms)

    def get_workflow_status(self, workflow_id: str) -> Optional[dict]:
        """Get status of a workflow."""
        if workflow_id in self.active_workflows:
            result = self.active_workflows[workflow_id]
            return {
                "workflow_id": result.workflow_id,
                "mode": result.mode.value,
                "status": result.status,
                "agents_completed": list(result.agent_results.keys()),
                "errors": result.errors,
                "execution_time_ms": result.total_execution_time_ms,
            }
        return None

    def get_all_agent_status(self) -> dict:
        """Get status of all registered agents."""
        return {
            agent_type.value: agent.get_status()
            for agent_type, agent in self.agents.items()
        }
