"""
Taj Chat Database Models

Pydantic models for the AI Video Creation Platform.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field


# ============================================
# ENUMS
# ============================================

class UserPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class VideoStatus(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PUBLISHED = "published"


class AssetType(str, Enum):
    MUSIC = "music"
    IMAGE = "image"
    OVERLAY = "overlay"
    VOICEOVER = "voiceover"
    B_ROLL = "b-roll"


class TrackType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    OVERLAY = "overlay"
    TEXT = "text"


class JobType(str, Enum):
    SCRIPT = "script"
    MUSIC = "music"
    IMAGE = "image"
    VOICE = "voice"
    VIDEO = "video"
    OPTIMIZE = "optimize"


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentType(str, Enum):
    CONTENT = "content"
    VIDEO = "video"
    MUSIC = "music"
    IMAGE = "image"
    VOICE = "voice"
    EDITING = "editing"
    OPTIMIZATION = "optimization"
    ANALYTICS = "analytics"
    SAFETY = "safety"
    SOCIAL = "social"


class AgentStatus(str, Enum):
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    THREADS = "threads"


class PostStatus(str, Enum):
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================
# USER MODELS
# ============================================

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    plan: UserPlan = UserPlan.FREE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserSettings(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    theme: str = "dark"
    notifications_enabled: bool = True
    auto_publish: bool = False
    default_platform: Platform = Platform.TIKTOK
    default_aspect_ratio: str = "9:16"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# VIDEO MODELS
# ============================================

class Video(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    title: str
    description: Optional[str] = None
    prompt: Optional[str] = None
    script: Optional[str] = None

    # Video specs
    duration_seconds: Optional[int] = None
    width: int = 1080
    height: int = 1920
    fps: int = 30
    aspect_ratio: str = "9:16"

    # File paths
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None

    # Status
    status: VideoStatus = VideoStatus.DRAFT
    processing_progress: int = 0
    error_message: Optional[str] = None

    # Metadata
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None


class VideoAsset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    video_id: UUID
    asset_type: AssetType
    name: Optional[str] = None
    file_url: str
    duration_seconds: Optional[float] = None
    start_time: float = 0
    end_time: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VideoTrack(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    video_id: UUID
    track_type: TrackType
    track_index: int = 0
    name: Optional[str] = None
    is_muted: bool = False
    is_locked: bool = False
    volume: float = 1.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VideoClip(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    track_id: UUID
    asset_id: Optional[UUID] = None
    start_time: float
    end_time: float
    position_x: float = 0
    position_y: float = 0
    scale: float = 1.0
    rotation: float = 0
    opacity: float = 1.0
    effects: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# AI GENERATION MODELS
# ============================================

class GenerationJob(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    video_id: UUID
    job_type: JobType
    provider: Optional[str] = None
    model: Optional[str] = None
    input_prompt: Optional[str] = None
    input_params: Dict[str, Any] = Field(default_factory=dict)
    output_url: Optional[str] = None
    output_data: Dict[str, Any] = Field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    tokens_used: Optional[int] = None
    cost_usd: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AIAgent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    agent_type: AgentType
    description: Optional[str] = None
    status: AgentStatus = AgentStatus.READY
    current_task: Optional[str] = None
    tasks_completed: int = 0
    avg_duration_ms: Optional[int] = None
    success_rate: float = 1.0
    config: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# SOCIAL MEDIA MODELS
# ============================================

class SocialAccount(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    platform: Platform
    platform_user_id: Optional[str] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    followers_count: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    is_connected: bool = True
    last_sync_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ScheduledPost(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    video_id: UUID
    scheduled_at: datetime
    timezone: str = "UTC"
    platforms: List[Platform]
    caption: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)
    status: PostStatus = PostStatus.SCHEDULED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PublishedPost(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    scheduled_post_id: Optional[UUID] = None
    video_id: UUID
    social_account_id: UUID
    platform: Platform
    platform_post_id: Optional[str] = None
    post_url: Optional[str] = None
    status: str = "published"
    published_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# ANALYTICS MODELS
# ============================================

class VideoAnalytics(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    video_id: UUID
    platform: Optional[Platform] = None
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    watch_time_seconds: int = 0
    avg_watch_percentage: Optional[float] = None
    engagement_rate: Optional[float] = None
    demographics: Dict[str, Any] = Field(default_factory=dict)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)


class PlatformAnalytics(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    platform: Platform
    followers_count: int = 0
    followers_gained: int = 0
    followers_lost: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    recorded_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================
# TEMPLATE & MUSIC MODELS
# ============================================

class Template(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    template_data: Dict[str, Any]
    uses_count: int = 0
    rating: float = 0
    tags: List[str] = Field(default_factory=list)
    is_featured: bool = False
    is_trending: bool = False
    is_new: bool = True
    author_name: Optional[str] = None
    author_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MusicTrack(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    artist: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    file_url: str
    duration_seconds: Optional[int] = None
    bpm: Optional[int] = None
    key: Optional[str] = None
    license_type: str = "royalty-free"
    attribution_required: bool = False
    uses_count: int = 0
    is_ai_generated: bool = False
    generation_prompt: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
