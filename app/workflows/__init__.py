"""
Workflow Engine for Taj Chat

Supports three processing modes:
- Sequential: Full quality, step by step
- Parallel: Fast mode, concurrent generation
- Hybrid: Balanced approach
"""

from .engine import WorkflowEngine, WorkflowMode

__all__ = ["WorkflowEngine", "WorkflowMode"]
