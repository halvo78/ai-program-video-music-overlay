"""
Core Swarm Infrastructure
=========================

Base classes and utilities for the AI Agent Swarm system.
"""

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Type
import json
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class AgentPriority(Enum):
    """Agent execution priority"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5


class FindingSeverity(Enum):
    """Severity level for findings"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingCategory(Enum):
    """Category of findings"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"
    MAINTAINABILITY = "maintainability"
    USABILITY = "usability"
    COMPLIANCE = "compliance"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    ARCHITECTURE = "architecture"
    CONFIGURATION = "configuration"


@dataclass
class AgentFinding:
    """A finding/issue discovered by an agent"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    agent_name: str = ""
    category: FindingCategory = FindingCategory.TESTING
    severity: FindingSeverity = FindingSeverity.INFO
    title: str = ""
    description: str = ""
    location: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""
    auto_fixable: bool = False
    fix_script: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "auto_fixable": self.auto_fixable,
            "fix_script": self.fix_script,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class AgentMetrics:
    """Metrics collected during agent execution"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    items_processed: int = 0
    items_passed: int = 0
    items_failed: int = 0
    findings_count: int = 0
    critical_findings: int = 0
    high_findings: int = 0
    medium_findings: int = 0
    low_findings: int = 0
    info_findings: int = 0
    memory_used_mb: float = 0.0
    cpu_percent: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "items_processed": self.items_processed,
            "items_passed": self.items_passed,
            "items_failed": self.items_failed,
            "findings_count": self.findings_count,
            "critical_findings": self.critical_findings,
            "high_findings": self.high_findings,
            "medium_findings": self.medium_findings,
            "low_findings": self.low_findings,
            "info_findings": self.info_findings,
            "memory_used_mb": self.memory_used_mb,
            "cpu_percent": self.cpu_percent,
        }


@dataclass
class AgentReport:
    """Complete report from an agent execution"""
    agent_id: str
    agent_name: str
    agent_type: str
    status: AgentStatus
    metrics: AgentMetrics
    findings: List[AgentFinding] = field(default_factory=list)
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    raw_output: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "metrics": self.metrics.to_dict(),
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary,
            "recommendations": self.recommendations,
            "raw_output": self.raw_output,
        }

    @property
    def passed(self) -> bool:
        """Check if agent passed (no critical/high findings)"""
        return self.metrics.critical_findings == 0 and self.metrics.high_findings == 0


class BaseSwarmAgent(ABC):
    """
    Base class for all swarm agents.

    Each agent is a specialist that performs a specific validation,
    testing, or verification task.
    """

    def __init__(
        self,
        name: str,
        description: str,
        priority: AgentPriority = AgentPriority.MEDIUM,
        timeout_seconds: int = 300,
        retry_count: int = 3,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.priority = priority
        self.timeout_seconds = timeout_seconds
        self.retry_count = retry_count
        self.status = AgentStatus.IDLE
        self.metrics = AgentMetrics()
        self.findings: List[AgentFinding] = []
        self._callbacks: List[Callable] = []

    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the type of agent"""
        pass

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> AgentReport:
        """Execute the agent's task"""
        pass

    def add_finding(
        self,
        category: FindingCategory,
        severity: FindingSeverity,
        title: str,
        description: str,
        location: str = "",
        evidence: Dict[str, Any] = None,
        recommendation: str = "",
        auto_fixable: bool = False,
        fix_script: Optional[str] = None,
    ) -> AgentFinding:
        """Add a finding to the agent's results"""
        finding = AgentFinding(
            agent_id=self.id,
            agent_name=self.name,
            category=category,
            severity=severity,
            title=title,
            description=description,
            location=location,
            evidence=evidence or {},
            recommendation=recommendation,
            auto_fixable=auto_fixable,
            fix_script=fix_script,
        )
        self.findings.append(finding)

        # Update metrics
        self.metrics.findings_count += 1
        if severity == FindingSeverity.CRITICAL:
            self.metrics.critical_findings += 1
        elif severity == FindingSeverity.HIGH:
            self.metrics.high_findings += 1
        elif severity == FindingSeverity.MEDIUM:
            self.metrics.medium_findings += 1
        elif severity == FindingSeverity.LOW:
            self.metrics.low_findings += 1
        else:
            self.metrics.info_findings += 1

        return finding

    def on_status_change(self, callback: Callable):
        """Register a callback for status changes"""
        self._callbacks.append(callback)

    def _set_status(self, status: AgentStatus):
        """Update status and notify callbacks"""
        self.status = status
        for callback in self._callbacks:
            try:
                callback(self, status)
            except Exception as e:
                logger.error(f"Callback error: {e}")

    async def run(self, context: Dict[str, Any]) -> AgentReport:
        """Run the agent with proper lifecycle management"""
        self._set_status(AgentStatus.INITIALIZING)
        self.metrics.start_time = datetime.now()
        self.findings = []

        try:
            self._set_status(AgentStatus.RUNNING)

            # Execute with timeout
            report = await asyncio.wait_for(
                self.execute(context),
                timeout=self.timeout_seconds
            )

            self._set_status(AgentStatus.COMPLETED)

        except asyncio.TimeoutError:
            self._set_status(AgentStatus.FAILED)
            report = self._create_error_report("Agent execution timed out")

        except Exception as e:
            self._set_status(AgentStatus.FAILED)
            report = self._create_error_report(str(e))
            logger.exception(f"Agent {self.name} failed")

        finally:
            self.metrics.end_time = datetime.now()
            self.metrics.duration_seconds = (
                self.metrics.end_time - self.metrics.start_time
            ).total_seconds()

        return report

    def _create_error_report(self, error: str) -> AgentReport:
        """Create an error report"""
        return AgentReport(
            agent_id=self.id,
            agent_name=self.name,
            agent_type=self.agent_type,
            status=AgentStatus.FAILED,
            metrics=self.metrics,
            findings=self.findings,
            summary=f"Agent failed: {error}",
            recommendations=["Investigate and fix the error", "Re-run the agent"],
        )

    def _create_success_report(
        self,
        summary: str,
        recommendations: List[str] = None,
        raw_output: Dict[str, Any] = None,
    ) -> AgentReport:
        """Create a success report"""
        return AgentReport(
            agent_id=self.id,
            agent_name=self.name,
            agent_type=self.agent_type,
            status=AgentStatus.COMPLETED,
            metrics=self.metrics,
            findings=self.findings,
            summary=summary,
            recommendations=recommendations or [],
            raw_output=raw_output or {},
        )


class AgentRegistry:
    """
    Registry for all available agents.
    Manages agent types and instantiation.
    """

    _agents: Dict[str, Type[BaseSwarmAgent]] = {}
    _instances: Dict[str, BaseSwarmAgent] = {}

    @classmethod
    def register(cls, agent_type: str):
        """Decorator to register an agent type"""
        def decorator(agent_class: Type[BaseSwarmAgent]):
            cls._agents[agent_type] = agent_class
            return agent_class
        return decorator

    @classmethod
    def get_agent_class(cls, agent_type: str) -> Optional[Type[BaseSwarmAgent]]:
        """Get an agent class by type"""
        return cls._agents.get(agent_type)

    @classmethod
    def create_agent(cls, agent_type: str, **kwargs) -> Optional[BaseSwarmAgent]:
        """Create an agent instance"""
        agent_class = cls._agents.get(agent_type)
        if agent_class:
            agent = agent_class(**kwargs)
            cls._instances[agent.id] = agent
            return agent
        return None

    @classmethod
    def get_instance(cls, agent_id: str) -> Optional[BaseSwarmAgent]:
        """Get an agent instance by ID"""
        return cls._instances.get(agent_id)

    @classmethod
    def list_agent_types(cls) -> List[str]:
        """List all registered agent types"""
        return list(cls._agents.keys())

    @classmethod
    def list_instances(cls) -> List[BaseSwarmAgent]:
        """List all agent instances"""
        return list(cls._instances.values())


class SwarmCoordinator:
    """
    Coordinates multiple agents in a swarm.
    Manages parallel and sequential execution.
    """

    def __init__(
        self,
        name: str = "SwarmCoordinator",
        max_parallel: int = 10,
        use_processes: bool = False,
    ):
        self.name = name
        self.max_parallel = max_parallel
        self.use_processes = use_processes
        self.agents: List[BaseSwarmAgent] = []
        self.reports: List[AgentReport] = []
        self._status_callbacks: List[Callable] = []

    def add_agent(self, agent: BaseSwarmAgent):
        """Add an agent to the swarm"""
        self.agents.append(agent)

    def add_agents(self, agents: List[BaseSwarmAgent]):
        """Add multiple agents to the swarm"""
        self.agents.extend(agents)

    def on_agent_status(self, callback: Callable):
        """Register callback for agent status changes"""
        self._status_callbacks.append(callback)

    async def run_sequential(self, context: Dict[str, Any]) -> List[AgentReport]:
        """Run all agents sequentially"""
        self.reports = []

        # Sort by priority
        sorted_agents = sorted(self.agents, key=lambda a: a.priority.value)

        for agent in sorted_agents:
            for callback in self._status_callbacks:
                agent.on_status_change(callback)

            report = await agent.run(context)
            self.reports.append(report)

            # Stop on critical failure if configured
            if report.metrics.critical_findings > 0:
                logger.warning(f"Critical findings in {agent.name}, continuing...")

        return self.reports

    async def run_parallel(self, context: Dict[str, Any]) -> List[AgentReport]:
        """Run all agents in parallel with concurrency limit"""
        self.reports = []

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.max_parallel)

        async def run_with_semaphore(agent: BaseSwarmAgent) -> AgentReport:
            async with semaphore:
                for callback in self._status_callbacks:
                    agent.on_status_change(callback)
                return await agent.run(context)

        # Run all agents
        tasks = [run_with_semaphore(agent) for agent in self.agents]
        self.reports = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        for i, report in enumerate(self.reports):
            if isinstance(report, Exception):
                self.reports[i] = AgentReport(
                    agent_id=self.agents[i].id,
                    agent_name=self.agents[i].name,
                    agent_type=self.agents[i].agent_type,
                    status=AgentStatus.FAILED,
                    metrics=AgentMetrics(),
                    summary=f"Exception: {str(report)}",
                )

        return self.reports

    async def run_hybrid(
        self,
        context: Dict[str, Any],
        parallel_groups: List[List[str]] = None,
    ) -> List[AgentReport]:
        """
        Run agents in a hybrid mode:
        - Groups run sequentially
        - Agents within groups run in parallel
        """
        self.reports = []

        if not parallel_groups:
            # Default: group by priority
            priority_groups = {}
            for agent in self.agents:
                priority = agent.priority.value
                if priority not in priority_groups:
                    priority_groups[priority] = []
                priority_groups[priority].append(agent)

            # Run each priority group
            for priority in sorted(priority_groups.keys()):
                group_agents = priority_groups[priority]

                # Create temporary coordinator for parallel execution
                group_coordinator = SwarmCoordinator(
                    name=f"Priority-{priority}",
                    max_parallel=self.max_parallel,
                )
                group_coordinator.add_agents(group_agents)

                group_reports = await group_coordinator.run_parallel(context)
                self.reports.extend(group_reports)
        else:
            # Use provided groups
            agent_map = {agent.id: agent for agent in self.agents}

            for group_ids in parallel_groups:
                group_agents = [agent_map[aid] for aid in group_ids if aid in agent_map]

                group_coordinator = SwarmCoordinator(
                    name="CustomGroup",
                    max_parallel=self.max_parallel,
                )
                group_coordinator.add_agents(group_agents)

                group_reports = await group_coordinator.run_parallel(context)
                self.reports.extend(group_reports)

        return self.reports

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all agent reports"""
        total_findings = sum(r.metrics.findings_count for r in self.reports)
        critical = sum(r.metrics.critical_findings for r in self.reports)
        high = sum(r.metrics.high_findings for r in self.reports)
        medium = sum(r.metrics.medium_findings for r in self.reports)
        low = sum(r.metrics.low_findings for r in self.reports)
        info = sum(r.metrics.info_findings for r in self.reports)

        passed = sum(1 for r in self.reports if r.passed)
        failed = len(self.reports) - passed

        total_duration = sum(r.metrics.duration_seconds for r in self.reports)

        return {
            "swarm_name": self.name,
            "total_agents": len(self.reports),
            "agents_passed": passed,
            "agents_failed": failed,
            "pass_rate": passed / len(self.reports) if self.reports else 0,
            "total_findings": total_findings,
            "critical_findings": critical,
            "high_findings": high,
            "medium_findings": medium,
            "low_findings": low,
            "info_findings": info,
            "total_duration_seconds": total_duration,
            "overall_status": "PASSED" if critical == 0 and high == 0 else "FAILED",
        }
