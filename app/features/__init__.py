"""
Taj Chat Features Module

Advanced features for AI video creation:
- Brand Kit management
- AI Avatars integration
- Screen Recording (future)
- Real-time Collaboration (future)
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
    # AI Avatars
    "AIAvatar",
    "AIAvatarManager",
    "avatar_manager",
]

