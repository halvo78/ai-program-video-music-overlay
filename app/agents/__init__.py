"""
Taj Chat - 10x Specialist AI Agents

Multi-agent architecture for video creation:
1. Video Generation Agent
2. Music Generation Agent
3. Image Generation Agent
4. Voice & Speech Agent
5. Content Analysis Agent
6. Editing Agent
7. Optimization Agent
8. Analytics Agent
9. Safety & Compliance Agent
10. Social Media Agent

Plus: Orchestrator Agent (Master Coordinator)
"""

from .base_agent import BaseAgent, AgentType, AgentResult, AgentTask
from .orchestrator import Orchestrator
from .video_agent import VideoGenerationAgent
from .music_agent import MusicGenerationAgent
from .image_agent import ImageGenerationAgent
from .voice_agent import VoiceSpeechAgent
from .content_agent import ContentAnalysisAgent
from .editing_agent import EditingAgent
from .optimization_agent import OptimizationAgent
from .analytics_agent import AnalyticsAgent
from .safety_agent import SafetyComplianceAgent
from .social_agent import SocialMediaAgent

__all__ = [
    "BaseAgent",
    "AgentType",
    "AgentResult",
    "AgentTask",
    "Orchestrator",
    "VideoGenerationAgent",
    "MusicGenerationAgent",
    "ImageGenerationAgent",
    "VoiceSpeechAgent",
    "ContentAnalysisAgent",
    "EditingAgent",
    "OptimizationAgent",
    "AnalyticsAgent",
    "SafetyComplianceAgent",
    "SocialMediaAgent",
]
