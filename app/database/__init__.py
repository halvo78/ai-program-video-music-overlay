"""
Taj Chat Database Module

Database models and utilities for the AI Video Creation Platform.
"""

from .models import (
    User,
    UserSettings,
    Video,
    VideoAsset,
    VideoTrack,
    VideoClip,
    GenerationJob,
    AIAgent,
    SocialAccount,
    ScheduledPost,
    PublishedPost,
    VideoAnalytics,
    PlatformAnalytics,
    Template,
    MusicTrack,
)
from .connection import get_db, init_db

__all__ = [
    # Models
    "User",
    "UserSettings",
    "Video",
    "VideoAsset",
    "VideoTrack",
    "VideoClip",
    "GenerationJob",
    "AIAgent",
    "SocialAccount",
    "ScheduledPost",
    "PublishedPost",
    "VideoAnalytics",
    "PlatformAnalytics",
    "Template",
    "MusicTrack",
    # Connection
    "get_db",
    "init_db",
]
