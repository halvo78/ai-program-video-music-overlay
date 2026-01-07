"""
Base Agent Class for Taj Chat

Pattern adapted from UTS verification agents (app/verification/agents.py)
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Types of specialist agents in Taj Chat."""

    # Generation Agents (can run in parallel)
    VIDEO_GENERATION = "video_generation"
    MUSIC_GENERATION = "music_generation"
    IMAGE_GENERATION = "image_generation"
    VOICE_SPEECH = "voice_speech"

    # Analysis Agents
    CONTENT_ANALYSIS = "content_analysis"
    ANALYTICS = "analytics"

    # Processing Agents (sequential)
    EDITING = "editing"
    OPTIMIZATION = "optimization"
    SAFETY = "safety"
    SOCIAL_MEDIA = "social_media"

    # Coordinator
    ORCHESTRATOR = "orchestrator"

    # Competitor-Parity Agents (5)
    VIRALITY = "virality"
    VOICE_CLONE = "voice_clone"
    AI_AVATAR = "ai_avatar"
    TEXT_EDITING = "text_editing"
    AI_BROLL = "ai_broll"


class AgentPriority(Enum):
    """Agent execution priority."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AgentTask:
    """A task for an agent to execute."""

    task_id: str
    task_type: str
    prompt: str
    parameters: dict = field(default_factory=dict)
    input_files: list[Path] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    priority: AgentPriority = AgentPriority.MEDIUM
    timeout_seconds: int = 300
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class AgentResult:
    """Result from an agent execution."""

    agent_type: AgentType
    task_id: str
    status: str  # success, error, timeout, cancelled
    output: Any = None
    output_files: list[Path] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    execution_time_ms: float = 0
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        return {
            "agent_type": self.agent_type.value,
            "task_id": self.task_id,
            "status": self.status,
            "output": str(self.output)[:500] if self.output else None,
            "output_files": [str(f) for f in self.output_files],
            "metadata": self.metadata,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
            "timestamp": self.timestamp,
        }


class BaseAgent(ABC):
    """
    Base class for all Taj Chat specialist agents.

    Each agent specializes in a specific aspect of video creation:
    - Has specific AI models it uses
    - Can run in parallel or sequential mode
    - Reports results back to the orchestrator
    """

    def __init__(
        self,
        agent_type: AgentType,
        priority: AgentPriority = AgentPriority.MEDIUM,
        parallel_capable: bool = True,
    ):
        self.agent_type = agent_type
        self.priority = priority
        self.parallel_capable = parallel_capable
        self.is_running = False
        self._current_task: Optional[AgentTask] = None

        logger.info(f"Initialized {agent_type.value} agent (priority: {priority.value})")

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable agent name."""
        pass

    @property
    @abstractmethod
    def models(self) -> list[str]:
        """List of AI models this agent can use."""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> list[str]:
        """List of capabilities this agent provides."""
        pass

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """
        Execute a task. Must be implemented by subclasses.

        Args:
            task: The task to execute

        Returns:
            AgentResult with output or error
        """
        pass

    async def run(self, task: AgentTask) -> AgentResult:
        """
        Run the agent on a task with error handling and timing.

        Args:
            task: The task to execute

        Returns:
            AgentResult
        """
        start_time = datetime.now()
        self.is_running = True
        self._current_task = task

        logger.info(f"{self.name} starting task: {task.task_id}")

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self.execute(task),
                timeout=task.timeout_seconds
            )
            result.execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000

            logger.info(
                f"{self.name} completed task {task.task_id} "
                f"in {result.execution_time_ms:.0f}ms"
            )

            return result

        except asyncio.TimeoutError:
            logger.error(f"{self.name} timed out on task {task.task_id}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="timeout",
                error=f"Task timed out after {task.timeout_seconds}s",
                execution_time_ms=task.timeout_seconds * 1000,
            )

        except Exception as e:
            logger.error(f"{self.name} error on task {task.task_id}: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

        finally:
            self.is_running = False
            self._current_task = None

    def cancel(self) -> bool:
        """Cancel the current task if running."""
        if self.is_running and self._current_task:
            logger.warning(f"{self.name} cancelling task {self._current_task.task_id}")
            self.is_running = False
            return True
        return False

    def get_status(self) -> dict:
        """Get current agent status."""
        return {
            "agent_type": self.agent_type.value,
            "name": self.name,
            "priority": self.priority.value,
            "parallel_capable": self.parallel_capable,
            "is_running": self.is_running,
            "current_task": self._current_task.task_id if self._current_task else None,
            "models": self.models,
            "capabilities": self.capabilities,
        }
