"""
Taj Chat - 15x Specialist AI Agents
===================================

Multi-agent architecture for video creation:

Core Agents (10):
1. Video Generation Agent - AI video creation
2. Music Generation Agent - AI music/soundtrack
3. Image Generation Agent - Thumbnails, overlays
4. Voice & Speech Agent - TTS, transcription
5. Content Analysis Agent - Script, SEO
6. Editing Agent - Composition, effects
7. Optimization Agent - Platform encoding
8. Analytics Agent - Performance prediction
9. Safety & Compliance Agent - Content moderation
10. Social Media Agent - Publishing, scheduling

NEW - Competitor-Parity Agents (5):
11. Virality Agent - Viral score prediction (Opus Clip)
12. Voice Clone Agent - Voice cloning (ElevenLabs/Descript)
13. Avatar Agent - AI avatars (Synthesia/HeyGen)
14. Text Editing Agent - Text-based editing (Descript)
15. B-Roll Agent - Auto B-roll insertion (Opus Clip/Kapwing)

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

# NEW - Competitor-Parity Agents
from .virality_agent import ViralityAgent, ViralityReport, Platform as ViralityPlatform
from .voice_clone_agent import VoiceCloneAgent, VoiceProfile, VoiceSettings, create_voice_agent
from .avatar_agent import AIAvatarAgent, AvatarProfile, AvatarVideoSettings, create_avatar_agent
from .text_editing_agent import TextBasedEditingAgent, Transcript, create_text_editing_agent
from .broll_agent import AIBRollAgent, BRollPlan, BRollClip, create_broll_agent

__all__ = [
    # Base
    "BaseAgent",
    "AgentType",
    "AgentResult",
    "AgentTask",
    "Orchestrator",
    # Core Agents
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
    # NEW - Competitor-Parity Agents
    "ViralityAgent",
    "ViralityReport",
    "ViralityPlatform",
    "VoiceCloneAgent",
    "VoiceProfile",
    "VoiceSettings",
    "create_voice_agent",
    "AIAvatarAgent",
    "AvatarProfile",
    "AvatarVideoSettings",
    "create_avatar_agent",
    "TextBasedEditingAgent",
    "Transcript",
    "create_text_editing_agent",
    "AIBRollAgent",
    "BRollPlan",
    "BRollClip",
    "create_broll_agent",
]
