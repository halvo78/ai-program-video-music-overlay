"""
Swarm Orchestrator
==================

Master orchestrator for coordinating all agent swarms.
Manages execution order, dependencies, and reporting.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import logging

from .core import (
    SwarmCoordinator,
    AgentReport,
    AgentStatus,
    FindingSeverity,
)
from .research_agents import ResearchAgentSwarm
from .engineering_agents import EngineeringAgentSwarm
from .testing_agents import TestingAgentSwarm
from .production_agents import ProductionAgentSwarm
from .proof_agents import ProofAgentSwarm

logger = logging.getLogger(__name__)


@dataclass
class SwarmPhase:
    """Represents a phase in the commissioning process"""
    name: str
    swarm: SwarmCoordinator
    order: int
    required: bool = True
    depends_on: List[str] = field(default_factory=list)
    status: str = "pending"
    reports: List[AgentReport] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def duration_seconds(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


@dataclass
class CommissionReport:
    """Complete commissioning report"""
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "running"
    phases: List[Dict[str, Any]] = field(default_factory=list)
    total_agents: int = 0
    agents_passed: int = 0
    agents_failed: int = 0
    total_findings: int = 0
    critical_findings: int = 0
    high_findings: int = 0
    medium_findings: int = 0
    low_findings: int = 0
    info_findings: int = 0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "duration_seconds": (self.end_time - self.start_time).total_seconds() if self.end_time else 0,
            "phases": self.phases,
            "summary": {
                "total_agents": self.total_agents,
                "agents_passed": self.agents_passed,
                "agents_failed": self.agents_failed,
                "pass_rate": self.agents_passed / self.total_agents if self.total_agents else 0,
                "total_findings": self.total_findings,
                "critical_findings": self.critical_findings,
                "high_findings": self.high_findings,
                "medium_findings": self.medium_findings,
                "low_findings": self.low_findings,
                "info_findings": self.info_findings,
            },
            "recommendations": self.recommendations,
            "overall_result": "PASSED" if self.critical_findings == 0 and self.high_findings == 0 else "FAILED",
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class SwarmOrchestrator:
    """
    Master orchestrator for all agent swarms.

    Coordinates 60+ agents across 6 phases:
    1. Research & Analysis (10 agents)
    2. Engineering Validation (10 agents)
    3. Testing (10 agents)
    4. Production Readiness (10 agents)
    5. Proof & Verification (10 agents)
    6. Final Validation (all agents re-run critical checks)
    """

    def __init__(
        self,
        project_path: str = ".",
        parallel_phases: bool = False,
        max_parallel_agents: int = 10,
    ):
        self.project_path = project_path
        self.parallel_phases = parallel_phases
        self.max_parallel_agents = max_parallel_agents

        # Initialize phases
        self.phases: List[SwarmPhase] = [
            SwarmPhase(
                name="Research & Analysis",
                swarm=ResearchAgentSwarm.create_swarm(),
                order=1,
                required=True,
            ),
            SwarmPhase(
                name="Engineering Validation",
                swarm=EngineeringAgentSwarm.create_swarm(),
                order=2,
                required=True,
                depends_on=["Research & Analysis"],
            ),
            SwarmPhase(
                name="Testing",
                swarm=TestingAgentSwarm.create_swarm(),
                order=3,
                required=True,
                depends_on=["Engineering Validation"],
            ),
            SwarmPhase(
                name="Production Readiness",
                swarm=ProductionAgentSwarm.create_swarm(),
                order=4,
                required=True,
                depends_on=["Testing"],
            ),
            SwarmPhase(
                name="Proof & Verification",
                swarm=ProofAgentSwarm.create_swarm(),
                order=5,
                required=True,
                depends_on=["Production Readiness"],
            ),
        ]

        self._status_callbacks: List = []
        self._current_report: Optional[CommissionReport] = None

    def on_status_change(self, callback):
        """Register callback for status updates"""
        self._status_callbacks.append(callback)

    def _notify_status(self, phase: str, agent: str, status: str, progress: float):
        """Notify all callbacks of status change"""
        for callback in self._status_callbacks:
            try:
                callback({
                    "phase": phase,
                    "agent": agent,
                    "status": status,
                    "progress": progress,
                    "timestamp": datetime.now().isoformat(),
                })
            except Exception as e:
                logger.error(f"Callback error: {e}")

    async def run_commission(
        self,
        context: Optional[Dict[str, Any]] = None,
        phases_to_run: Optional[List[str]] = None,
    ) -> CommissionReport:
        """
        Run the full commissioning process.

        Args:
            context: Additional context for agents
            phases_to_run: Optional list of phase names to run (runs all if None)

        Returns:
            CommissionReport with all results
        """
        # Initialize report
        report = CommissionReport(
            id=f"commission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            start_time=datetime.now(),
        )
        self._current_report = report

        # Build context
        ctx = {
            "project_path": self.project_path,
            "commission_id": report.id,
            **(context or {}),
        }

        # Filter phases if specified
        phases = self.phases
        if phases_to_run:
            phases = [p for p in phases if p.name in phases_to_run]

        logger.info(f"Starting commissioning with {len(phases)} phases")

        if self.parallel_phases:
            # Run all phases in parallel
            await self._run_phases_parallel(phases, ctx, report)
        else:
            # Run phases sequentially
            await self._run_phases_sequential(phases, ctx, report)

        # Finalize report
        report.end_time = datetime.now()
        report.status = "completed"

        # Determine overall status
        if report.critical_findings > 0:
            report.status = "failed_critical"
        elif report.high_findings > 0:
            report.status = "failed_high"
        else:
            report.status = "passed"

        # Generate recommendations
        report.recommendations = self._generate_recommendations(report)

        logger.info(f"Commissioning completed: {report.status}")

        return report

    async def _run_phases_sequential(
        self,
        phases: List[SwarmPhase],
        context: Dict[str, Any],
        report: CommissionReport,
    ):
        """Run phases sequentially"""
        for phase in sorted(phases, key=lambda p: p.order):
            logger.info(f"Starting phase: {phase.name}")
            phase.start_time = datetime.now()
            phase.status = "running"

            self._notify_status(phase.name, "", "started", 0)

            try:
                # Run the swarm
                phase.reports = await phase.swarm.run_parallel(context)
                phase.status = "completed"

            except Exception as e:
                logger.error(f"Phase {phase.name} failed: {e}")
                phase.status = "failed"

            finally:
                phase.end_time = datetime.now()

            # Update report
            self._update_report_from_phase(report, phase)

            self._notify_status(phase.name, "", "completed", 100)

            # Check for blocking failures
            if phase.required and phase.status == "failed":
                logger.error(f"Required phase {phase.name} failed, stopping commissioning")
                break

    async def _run_phases_parallel(
        self,
        phases: List[SwarmPhase],
        context: Dict[str, Any],
        report: CommissionReport,
    ):
        """Run phases in parallel"""

        async def run_phase(phase: SwarmPhase):
            logger.info(f"Starting phase: {phase.name}")
            phase.start_time = datetime.now()
            phase.status = "running"

            try:
                phase.reports = await phase.swarm.run_parallel(context)
                phase.status = "completed"
            except Exception as e:
                logger.error(f"Phase {phase.name} failed: {e}")
                phase.status = "failed"
            finally:
                phase.end_time = datetime.now()

            return phase

        # Run all phases
        tasks = [run_phase(phase) for phase in phases]
        completed_phases = await asyncio.gather(*tasks, return_exceptions=True)

        # Update report
        for phase in completed_phases:
            if isinstance(phase, SwarmPhase):
                self._update_report_from_phase(report, phase)

    def _update_report_from_phase(self, report: CommissionReport, phase: SwarmPhase):
        """Update commission report from phase results"""
        phase_summary = phase.swarm.get_summary()

        report.phases.append({
            "name": phase.name,
            "status": phase.status,
            "duration_seconds": phase.duration_seconds,
            "summary": phase_summary,
        })

        report.total_agents += phase_summary["total_agents"]
        report.agents_passed += phase_summary["agents_passed"]
        report.agents_failed += phase_summary["agents_failed"]
        report.total_findings += phase_summary["total_findings"]
        report.critical_findings += phase_summary["critical_findings"]
        report.high_findings += phase_summary["high_findings"]
        report.medium_findings += phase_summary["medium_findings"]
        report.low_findings += phase_summary["low_findings"]
        report.info_findings += phase_summary["info_findings"]

    def _generate_recommendations(self, report: CommissionReport) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []

        if report.critical_findings > 0:
            recommendations.append(
                f"URGENT: Address {report.critical_findings} critical findings immediately"
            )

        if report.high_findings > 0:
            recommendations.append(
                f"HIGH PRIORITY: Fix {report.high_findings} high-severity findings before production"
            )

        if report.medium_findings > 0:
            recommendations.append(
                f"MEDIUM: Plan to address {report.medium_findings} medium-severity findings"
            )

        if report.agents_failed > 0:
            recommendations.append(
                f"Review {report.agents_failed} failed agent checks and fix underlying issues"
            )

        pass_rate = report.agents_passed / report.total_agents if report.total_agents else 0
        if pass_rate < 0.9:
            recommendations.append(
                f"Overall pass rate is {pass_rate*100:.1f}%, target is 90%+"
            )

        if not recommendations:
            recommendations.append("System is ready for production deployment!")

        return recommendations

    async def run_quick_check(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a quick health check with critical agents only"""
        ctx = {
            "project_path": self.project_path,
            **(context or {}),
        }

        # Run only critical agents from each phase
        results = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "checks": [],
        }

        for phase in self.phases:
            critical_agents = [
                a for a in phase.swarm.agents
                if a.priority.value <= 2  # CRITICAL or HIGH
            ][:3]  # Top 3 per phase

            for agent in critical_agents:
                try:
                    report = await agent.run(ctx)
                    results["checks"].append({
                        "agent": agent.name,
                        "phase": phase.name,
                        "status": "passed" if report.passed else "failed",
                        "findings": report.metrics.findings_count,
                    })

                    if not report.passed:
                        results["status"] = "unhealthy"

                except Exception as e:
                    results["checks"].append({
                        "agent": agent.name,
                        "phase": phase.name,
                        "status": "error",
                        "error": str(e),
                    })
                    results["status"] = "unhealthy"

        return results

    def get_agent_count(self) -> int:
        """Get total number of agents across all phases"""
        return sum(len(phase.swarm.agents) for phase in self.phases)

    def get_phase_info(self) -> List[Dict[str, Any]]:
        """Get information about all phases"""
        return [
            {
                "name": phase.name,
                "order": phase.order,
                "required": phase.required,
                "depends_on": phase.depends_on,
                "agent_count": len(phase.swarm.agents),
                "agents": [
                    {
                        "name": agent.name,
                        "type": agent.agent_type,
                        "priority": agent.priority.name,
                    }
                    for agent in phase.swarm.agents
                ],
            }
            for phase in self.phases
        ]


# Convenience function for running commissioning
async def run_full_commission(
    project_path: str = ".",
    parallel: bool = False,
) -> CommissionReport:
    """Run a full system commissioning"""
    orchestrator = SwarmOrchestrator(
        project_path=project_path,
        parallel_phases=parallel,
    )
    return await orchestrator.run_commission()


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run AI Agent Swarm Commissioning")
    parser.add_argument("--path", default=".", help="Project path")
    parser.add_argument("--parallel", action="store_true", help="Run phases in parallel")
    parser.add_argument("--quick", action="store_true", help="Run quick check only")
    parser.add_argument("--output", default="commission_report.json", help="Output file")

    args = parser.parse_args()

    async def main():
        orchestrator = SwarmOrchestrator(
            project_path=args.path,
            parallel_phases=args.parallel,
        )

        if args.quick:
            result = await orchestrator.run_quick_check()
            print(json.dumps(result, indent=2))
        else:
            report = await orchestrator.run_commission()

            # Save report
            with open(args.output, "w") as f:
                f.write(report.to_json())

            print(f"\n{'='*60}")
            print(f"COMMISSIONING REPORT: {report.status.upper()}")
            print(f"{'='*60}")
            print(f"Total Agents: {report.total_agents}")
            print(f"Passed: {report.agents_passed}")
            print(f"Failed: {report.agents_failed}")
            print(f"Pass Rate: {report.agents_passed/report.total_agents*100:.1f}%")
            print(f"\nFindings:")
            print(f"  Critical: {report.critical_findings}")
            print(f"  High: {report.high_findings}")
            print(f"  Medium: {report.medium_findings}")
            print(f"  Low: {report.low_findings}")
            print(f"  Info: {report.info_findings}")
            print(f"\nRecommendations:")
            for rec in report.recommendations:
                print(f"  - {rec}")
            print(f"\nFull report saved to: {args.output}")

    asyncio.run(main())
