"""
Taj Chat Features Module

Advanced features for AI video creation inspired by top competitors:
- Avatar System (Synthesia, HeyGen)
- Keyframe & Transitions (Pika Labs, Luma AI)
- Voice Cloning (Descript, HeyGen)
- Motion Control (Kling AI)
- Multi-modal Generation (Veo 3, Kling 2.6)
- Video Effects (Pika Labs, Kapwing)
- Content-to-Video (Pictory, InVideo)
- Element Library (Kling O1, Runway)
- Brand Kit management
"""

from .brand_kit import (
    BrandKit,
    BrandKitManager,
    BrandColors,
    BrandFonts,
    BrandLogo,
    BrandWatermark,
    BrandIntroOutro,
    BrandCaptionStyle,
    BRAND_KIT_TEMPLATES,
)

from .ai_avatars import (
    AIAvatar,
    AIAvatarManager,
    avatar_manager,
)

# New competitor-inspired features
from .avatar_system import (
    AvatarGenerator,
    AvatarLibrary,
    Avatar,
    AvatarVideoRequest,
    AvatarVideoResult,
    avatar_generator,
)

from .keyframe_system import (
    KeyframeInterpolator,
    MotionPathEditor,
    Keyframe,
    KeyframeSequence,
    KeyframeVideoRequest,
    CameraMotion,
    TransitionType,
    keyframe_interpolator,
    motion_editor,
)

from .voice_cloning import (
    VoiceCloningEngine,
    VoiceLibrary,
    VoiceProfile,
    VoiceCloneRequest,
    TextToSpeechRequest,
    OverdubRequest,
    voice_engine,
)

from .motion_control import (
    MotionControlEngine,
    MotionLibrary,
    PhysicsSimulator,
    MotionType,
    MotionControlRequest,
    motion_engine,
    physics_simulator,
)

from .multimodal_generation import (
    MultiModalEngine,
    CharacterConsistencyEngine,
    MultiModalRequest,
    MultiModalResult,
    multimodal_engine,
    character_engine,
)

from .video_effects import (
    AIEffectsEngine,
    EffectType,
    EffectIntensity,
    EffectRequest,
    EffectPresets,
    effects_engine,
)

from .content_to_video import (
    ContentToVideoEngine,
    ContentParser,
    ScriptGenerator,
    BRollEngine,
    HighlightExtractor,
    ContentSource,
    ContentType,
    VideoFormat,
    content_to_video,
)

from .element_library import (
    ElementLibrary,
    CharacterManager,
    Element,
    ElementType,
    ElementCollection,
    element_library,
    character_manager,
)

__all__ = [
    # Brand Kit
    "BrandKit",
    "BrandKitManager",
    "BrandColors",
    "BrandFonts",
    "BrandLogo",
    "BrandWatermark",
    "BrandIntroOutro",
    "BrandCaptionStyle",
    "BRAND_KIT_TEMPLATES",
    # AI Avatars (original)
    "AIAvatar",
    "AIAvatarManager",
    "avatar_manager",
    # Avatar System (Synthesia/HeyGen)
    "AvatarGenerator",
    "AvatarLibrary",
    "Avatar",
    "AvatarVideoRequest",
    "AvatarVideoResult",
    "avatar_generator",
    # Keyframe System (Pika/Luma)
    "KeyframeInterpolator",
    "MotionPathEditor",
    "Keyframe",
    "KeyframeSequence",
    "KeyframeVideoRequest",
    "CameraMotion",
    "TransitionType",
    "keyframe_interpolator",
    "motion_editor",
    # Voice Cloning (Descript/HeyGen)
    "VoiceCloningEngine",
    "VoiceLibrary",
    "VoiceProfile",
    "VoiceCloneRequest",
    "TextToSpeechRequest",
    "OverdubRequest",
    "voice_engine",
    # Motion Control (Kling AI)
    "MotionControlEngine",
    "MotionLibrary",
    "PhysicsSimulator",
    "MotionType",
    "MotionControlRequest",
    "motion_engine",
    "physics_simulator",
    # Multi-modal Generation (Veo 3)
    "MultiModalEngine",
    "CharacterConsistencyEngine",
    "MultiModalRequest",
    "MultiModalResult",
    "multimodal_engine",
    "character_engine",
    # Video Effects (Pika/Kapwing)
    "AIEffectsEngine",
    "EffectType",
    "EffectIntensity",
    "EffectRequest",
    "EffectPresets",
    "effects_engine",
    # Content-to-Video (Pictory)
    "ContentToVideoEngine",
    "ContentParser",
    "ScriptGenerator",
    "BRollEngine",
    "HighlightExtractor",
    "ContentSource",
    "ContentType",
    "VideoFormat",
    "content_to_video",
    # Element Library (Kling/Runway)
    "ElementLibrary",
    "CharacterManager",
    "Element",
    "ElementType",
    "ElementCollection",
    "element_library",
    "character_manager",
]

