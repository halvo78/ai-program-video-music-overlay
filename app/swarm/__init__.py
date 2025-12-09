"""
Taj Chat AI Agent Swarm System
==============================

A comprehensive multi-agent orchestration system for:
- Commissioning & Validation
- Deep Research & Analysis
- Engineering Verification
- Testing (All Phases)
- Production Readiness
- Proof & Verification

Architecture:
- 60+ Specialist Agents across 6 layers
- 10x agents per domain for comprehensive coverage
- Parallel & Sequential execution modes
- Real-time reporting & dashboards
"""

from .core import SwarmCoordinator, AgentRegistry
from .research_agents import ResearchAgentSwarm
from .engineering_agents import EngineeringAgentSwarm
from .testing_agents import TestingAgentSwarm
from .production_agents import ProductionAgentSwarm
from .proof_agents import ProofAgentSwarm
from .orchestrator import SwarmOrchestrator

__all__ = [
    'SwarmCoordinator',
    'AgentRegistry',
    'ResearchAgentSwarm',
    'EngineeringAgentSwarm',
    'TestingAgentSwarm',
    'ProductionAgentSwarm',
    'ProofAgentSwarm',
    'SwarmOrchestrator',
]

__version__ = '1.0.0'
