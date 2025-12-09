#!/usr/bin/env python
"""
Run AI Agent Swarm Commissioning
================================

This script runs the full commissioning process with 60+ AI agents
across 6 phases to validate the Taj Chat system.
"""

import asyncio
import json
from datetime import datetime
from app.swarm.orchestrator import SwarmOrchestrator


async def main():
    print("=" * 70)
    print("  TAJ CHAT - AI AGENT SWARM COMMISSIONING SYSTEM")
    print("=" * 70)
    print()

    # Initialize orchestrator
    orchestrator = SwarmOrchestrator(project_path=".")

    # Display phase information
    print(f"Total Agents: {orchestrator.get_agent_count()}")
    print()

    print("COMMISSIONING PHASES:")
    print("-" * 50)

    for phase in orchestrator.get_phase_info():
        print(f"\nPhase {phase['order']}: {phase['name']}")
        print(f"  Agents: {phase['agent_count']}")
        for agent in phase['agents']:
            print(f"    - {agent['name']} [{agent['priority']}]")

    print()
    print("=" * 70)
    print("  RUNNING QUICK HEALTH CHECK")
    print("=" * 70)
    print()

    # Run quick check
    result = await orchestrator.run_quick_check()

    print(f"Status: {result['status'].upper()}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Checks Run: {len(result['checks'])}")
    print()

    passed = sum(1 for c in result['checks'] if c['status'] == 'passed')
    failed = sum(1 for c in result['checks'] if c['status'] == 'failed')

    print(f"Results: {passed} passed, {failed} failed")
    print()

    print("Check Details:")
    for check in result['checks']:
        status_icon = "✓" if check['status'] == 'passed' else "✗"
        print(f"  {status_icon} {check['agent']} ({check['phase']})")
        if check.get('findings', 0) > 0:
            print(f"      Findings: {check['findings']}")

    print()
    print("=" * 70)
    print("  RUNNING FULL COMMISSION")
    print("=" * 70)
    print()

    # Run full commission
    report = await orchestrator.run_commission()

    print(f"\nCOMMISSIONING COMPLETE")
    print(f"Status: {report.status.upper()}")
    print(f"Duration: {(report.end_time - report.start_time).total_seconds():.2f}s")
    print()

    print("SUMMARY:")
    print(f"  Total Agents: {report.total_agents}")
    print(f"  Passed: {report.agents_passed}")
    print(f"  Failed: {report.agents_failed}")
    print(f"  Pass Rate: {report.agents_passed/report.total_agents*100:.1f}%")
    print()

    print("FINDINGS:")
    print(f"  Critical: {report.critical_findings}")
    print(f"  High: {report.high_findings}")
    print(f"  Medium: {report.medium_findings}")
    print(f"  Low: {report.low_findings}")
    print(f"  Info: {report.info_findings}")
    print()

    print("PHASE RESULTS:")
    for phase in report.phases:
        status = "✓" if phase['summary']['overall_status'] == 'PASSED' else "✗"
        print(f"  {status} {phase['name']}: {phase['summary']['agents_passed']}/{phase['summary']['total_agents']} passed")
    print()

    print("RECOMMENDATIONS:")
    for rec in report.recommendations:
        print(f"  • {rec}")
    print()

    # Save report
    report_file = f"commission_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        f.write(report.to_json())
    print(f"Full report saved to: {report_file}")

    print()
    print("=" * 70)
    overall = "PASSED ✓" if report.critical_findings == 0 and report.high_findings == 0 else "FAILED ✗"
    print(f"  OVERALL RESULT: {overall}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
