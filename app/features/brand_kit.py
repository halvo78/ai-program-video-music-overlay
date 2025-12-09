"""
Brand Kit System - NEW FEATURE

Like Lumen5/Pictory brand presets:
- Save brand colors, fonts, logos
- Watermark management
- Intro/outro templates
- Consistent styling across all videos
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, field, asdict
import json
import os

logger = logging.getLogger(__name__)


@dataclass
class BrandColors:
    """Brand color palette."""
    primary: str = "#6366F1"  # Indigo
    secondary: str = "#EC4899"  # Pink
    accent: str = "#10B981"  # Emerald
    background: str = "#0F172A"  # Slate 900
    text: str = "#F8FAFC"  # Slate 50
    text_secondary: str = "#94A3B8"  # Slate 400
    gradient_start: str = "#6366F1"
    gradient_end: str = "#EC4899"


@dataclass
class BrandFonts:
    """Brand typography settings."""
    heading: str = "Inter"
    body: str = "Inter"
    accent: str = "Space Grotesk"
    caption: str = "Inter"
    heading_weight: str = "bold"
    body_weight: str = "normal"
    caption_style: str = "normal"  # normal, italic


@dataclass
class BrandLogo:
    """Brand logo settings."""
    path: Optional[str] = None
    position: str = "bottom-right"  # top-left, top-right, bottom-left, bottom-right, center
    size: str = "small"  # small, medium, large
    opacity: float = 0.8
    padding: int = 20  # pixels from edge


@dataclass
class BrandWatermark:
    """Brand watermark settings."""
    enabled: bool = True
    text: Optional[str] = None  # Text watermark (alternative to logo)
    logo_path: Optional[str] = None
    position: str = "bottom-right"
    opacity: float = 0.5
    size: str = "small"


@dataclass
class BrandIntroOutro:
    """Brand intro/outro templates."""
    intro_enabled: bool = True
    intro_video_path: Optional[str] = None
    intro_duration: float = 3.0  # seconds
    intro_animation: str = "fade"  # fade, zoom, slide
    
    outro_enabled: bool = True
    outro_video_path: Optional[str] = None
    outro_duration: float = 3.0
    outro_animation: str = "fade"
    
    # Auto-generated intro/outro settings
    auto_intro_text: str = ""
    auto_outro_text: str = "Follow for more!"
    auto_outro_cta: str = "Subscribe"


@dataclass
class BrandCaptionStyle:
    """Brand caption/subtitle styling."""
    enabled: bool = True
    font: str = "Inter"
    font_size: int = 48
    font_weight: str = "bold"
    color: str = "#FFFFFF"
    background_color: str = "#000000"
    background_opacity: float = 0.7
    position: str = "bottom"  # top, center, bottom
    animation: str = "word-by-word"  # none, word-by-word, line-by-line, karaoke
    highlight_color: str = "#FFD700"  # For keyword highlighting
    outline_enabled: bool = True
    outline_color: str = "#000000"
    outline_width: int = 2


@dataclass
class BrandKit:
    """Complete brand kit configuration."""
    name: str = "Default Brand"
    description: str = ""
    
    # Core brand elements
    colors: BrandColors = field(default_factory=BrandColors)
    fonts: BrandFonts = field(default_factory=BrandFonts)
    logo: BrandLogo = field(default_factory=BrandLogo)
    watermark: BrandWatermark = field(default_factory=BrandWatermark)
    intro_outro: BrandIntroOutro = field(default_factory=BrandIntroOutro)
    caption_style: BrandCaptionStyle = field(default_factory=BrandCaptionStyle)
    
    # Platform-specific overrides
    platform_overrides: Dict[str, Dict] = field(default_factory=dict)
    
    # Metadata
    created_at: str = ""
    updated_at: str = ""
    is_default: bool = False

    def to_dict(self) -> Dict:
        """Convert brand kit to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "colors": asdict(self.colors),
            "fonts": asdict(self.fonts),
            "logo": asdict(self.logo),
            "watermark": asdict(self.watermark),
            "intro_outro": asdict(self.intro_outro),
            "caption_style": asdict(self.caption_style),
            "platform_overrides": self.platform_overrides,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_default": self.is_default,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BrandKit":
        """Create brand kit from dictionary."""
        return cls(
            name=data.get("name", "Default Brand"),
            description=data.get("description", ""),
            colors=BrandColors(**data.get("colors", {})),
            fonts=BrandFonts(**data.get("fonts", {})),
            logo=BrandLogo(**data.get("logo", {})),
            watermark=BrandWatermark(**data.get("watermark", {})),
            intro_outro=BrandIntroOutro(**data.get("intro_outro", {})),
            caption_style=BrandCaptionStyle(**data.get("caption_style", {})),
            platform_overrides=data.get("platform_overrides", {}),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            is_default=data.get("is_default", False),
        )


class BrandKitManager:
    """
    Manage brand kits for users.
    
    Features:
    - Create, update, delete brand kits
    - Apply brand kit to video projects
    - Platform-specific overrides
    - Import/export brand kits
    """

    def __init__(self, storage_path: str = "C:/taj-chat/data/brand_kits"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.brand_kits: Dict[str, BrandKit] = {}
        self._load_brand_kits()

    def _load_brand_kits(self):
        """Load all brand kits from storage."""
        for file_path in self.storage_path.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    kit = BrandKit.from_dict(data)
                    self.brand_kits[kit.name] = kit
            except Exception as e:
                logger.warning(f"Failed to load brand kit {file_path}: {e}")

    def create_brand_kit(
        self,
        name: str,
        description: str = "",
        **kwargs,
    ) -> BrandKit:
        """Create a new brand kit."""
        from datetime import datetime
        
        kit = BrandKit(
            name=name,
            description=description,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        
        # Apply any provided settings
        if "colors" in kwargs:
            kit.colors = BrandColors(**kwargs["colors"])
        if "fonts" in kwargs:
            kit.fonts = BrandFonts(**kwargs["fonts"])
        if "logo" in kwargs:
            kit.logo = BrandLogo(**kwargs["logo"])
        if "watermark" in kwargs:
            kit.watermark = BrandWatermark(**kwargs["watermark"])
        if "intro_outro" in kwargs:
            kit.intro_outro = BrandIntroOutro(**kwargs["intro_outro"])
        if "caption_style" in kwargs:
            kit.caption_style = BrandCaptionStyle(**kwargs["caption_style"])
        
        self.brand_kits[name] = kit
        self._save_brand_kit(kit)
        
        logger.info(f"Created brand kit: {name}")
        return kit

    def update_brand_kit(
        self,
        name: str,
        **kwargs,
    ) -> Optional[BrandKit]:
        """Update an existing brand kit."""
        from datetime import datetime
        
        kit = self.brand_kits.get(name)
        if not kit:
            logger.warning(f"Brand kit not found: {name}")
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(kit, key):
                if key == "colors" and isinstance(value, dict):
                    kit.colors = BrandColors(**value)
                elif key == "fonts" and isinstance(value, dict):
                    kit.fonts = BrandFonts(**value)
                elif key == "logo" and isinstance(value, dict):
                    kit.logo = BrandLogo(**value)
                elif key == "watermark" and isinstance(value, dict):
                    kit.watermark = BrandWatermark(**value)
                elif key == "intro_outro" and isinstance(value, dict):
                    kit.intro_outro = BrandIntroOutro(**value)
                elif key == "caption_style" and isinstance(value, dict):
                    kit.caption_style = BrandCaptionStyle(**value)
                else:
                    setattr(kit, key, value)
        
        kit.updated_at = datetime.now().isoformat()
        self._save_brand_kit(kit)
        
        logger.info(f"Updated brand kit: {name}")
        return kit

    def delete_brand_kit(self, name: str) -> bool:
        """Delete a brand kit."""
        if name not in self.brand_kits:
            return False
        
        del self.brand_kits[name]
        
        file_path = self.storage_path / f"{name.lower().replace(' ', '_')}.json"
        if file_path.exists():
            file_path.unlink()
        
        logger.info(f"Deleted brand kit: {name}")
        return True

    def get_brand_kit(self, name: str) -> Optional[BrandKit]:
        """Get a brand kit by name."""
        return self.brand_kits.get(name)

    def list_brand_kits(self) -> List[Dict]:
        """List all brand kits."""
        return [
            {
                "name": kit.name,
                "description": kit.description,
                "is_default": kit.is_default,
                "created_at": kit.created_at,
                "updated_at": kit.updated_at,
            }
            for kit in self.brand_kits.values()
        ]

    def set_default_brand_kit(self, name: str) -> bool:
        """Set a brand kit as the default."""
        if name not in self.brand_kits:
            return False
        
        # Unset current default
        for kit in self.brand_kits.values():
            kit.is_default = False
        
        # Set new default
        self.brand_kits[name].is_default = True
        self._save_brand_kit(self.brand_kits[name])
        
        return True

    def get_default_brand_kit(self) -> Optional[BrandKit]:
        """Get the default brand kit."""
        for kit in self.brand_kits.values():
            if kit.is_default:
                return kit
        
        # Return first kit if no default set
        if self.brand_kits:
            return list(self.brand_kits.values())[0]
        
        return None

    def apply_brand_kit_to_video(
        self,
        brand_kit: BrandKit,
        video_settings: Dict,
        platform: str = None,
    ) -> Dict:
        """Apply brand kit settings to video configuration."""
        
        settings = video_settings.copy()
        
        # Apply base brand settings
        settings["colors"] = asdict(brand_kit.colors)
        settings["fonts"] = asdict(brand_kit.fonts)
        settings["watermark"] = asdict(brand_kit.watermark)
        settings["captions"] = asdict(brand_kit.caption_style)
        
        # Apply intro/outro
        if brand_kit.intro_outro.intro_enabled:
            settings["intro"] = {
                "enabled": True,
                "video_path": brand_kit.intro_outro.intro_video_path,
                "duration": brand_kit.intro_outro.intro_duration,
                "animation": brand_kit.intro_outro.intro_animation,
                "text": brand_kit.intro_outro.auto_intro_text,
            }
        
        if brand_kit.intro_outro.outro_enabled:
            settings["outro"] = {
                "enabled": True,
                "video_path": brand_kit.intro_outro.outro_video_path,
                "duration": brand_kit.intro_outro.outro_duration,
                "animation": brand_kit.intro_outro.outro_animation,
                "text": brand_kit.intro_outro.auto_outro_text,
                "cta": brand_kit.intro_outro.auto_outro_cta,
            }
        
        # Apply platform-specific overrides
        if platform and platform in brand_kit.platform_overrides:
            overrides = brand_kit.platform_overrides[platform]
            for key, value in overrides.items():
                if key in settings:
                    if isinstance(settings[key], dict) and isinstance(value, dict):
                        settings[key].update(value)
                    else:
                        settings[key] = value
        
        return settings

    def _save_brand_kit(self, kit: BrandKit):
        """Save brand kit to storage."""
        file_path = self.storage_path / f"{kit.name.lower().replace(' ', '_')}.json"
        with open(file_path, "w") as f:
            json.dump(kit.to_dict(), f, indent=2)

    def export_brand_kit(self, name: str) -> Optional[str]:
        """Export brand kit as JSON string."""
        kit = self.brand_kits.get(name)
        if not kit:
            return None
        return json.dumps(kit.to_dict(), indent=2)

    def import_brand_kit(self, json_str: str) -> Optional[BrandKit]:
        """Import brand kit from JSON string."""
        try:
            data = json.loads(json_str)
            kit = BrandKit.from_dict(data)
            self.brand_kits[kit.name] = kit
            self._save_brand_kit(kit)
            return kit
        except Exception as e:
            logger.error(f"Failed to import brand kit: {e}")
            return None


# Pre-built brand kit templates
BRAND_KIT_TEMPLATES = {
    "modern_dark": BrandKit(
        name="Modern Dark",
        description="Sleek dark theme with vibrant accents",
        colors=BrandColors(
            primary="#6366F1",
            secondary="#EC4899",
            accent="#10B981",
            background="#0F172A",
            text="#F8FAFC",
        ),
        fonts=BrandFonts(
            heading="Inter",
            body="Inter",
            accent="Space Grotesk",
        ),
        caption_style=BrandCaptionStyle(
            font="Inter",
            font_size=48,
            color="#FFFFFF",
            background_opacity=0.8,
            animation="word-by-word",
            highlight_color="#FFD700",
        ),
    ),
    "clean_minimal": BrandKit(
        name="Clean Minimal",
        description="Clean and minimal aesthetic",
        colors=BrandColors(
            primary="#000000",
            secondary="#666666",
            accent="#FF6B6B",
            background="#FFFFFF",
            text="#000000",
        ),
        fonts=BrandFonts(
            heading="Helvetica Neue",
            body="Helvetica Neue",
            accent="Helvetica Neue",
        ),
        caption_style=BrandCaptionStyle(
            font="Helvetica Neue",
            font_size=42,
            color="#000000",
            background_color="#FFFFFF",
            background_opacity=0.9,
            animation="line-by-line",
        ),
    ),
    "vibrant_creator": BrandKit(
        name="Vibrant Creator",
        description="Bold and colorful for content creators",
        colors=BrandColors(
            primary="#FF6B6B",
            secondary="#4ECDC4",
            accent="#FFE66D",
            background="#2C3E50",
            text="#FFFFFF",
        ),
        fonts=BrandFonts(
            heading="Poppins",
            body="Poppins",
            accent="Bebas Neue",
        ),
        caption_style=BrandCaptionStyle(
            font="Poppins",
            font_size=52,
            font_weight="bold",
            color="#FFFFFF",
            background_opacity=0.0,
            animation="karaoke",
            highlight_color="#FFE66D",
            outline_enabled=True,
            outline_width=3,
        ),
    ),
    "corporate_professional": BrandKit(
        name="Corporate Professional",
        description="Professional look for business content",
        colors=BrandColors(
            primary="#1E40AF",
            secondary="#3B82F6",
            accent="#F59E0B",
            background="#F1F5F9",
            text="#1E293B",
        ),
        fonts=BrandFonts(
            heading="Roboto",
            body="Roboto",
            accent="Roboto Condensed",
        ),
        caption_style=BrandCaptionStyle(
            font="Roboto",
            font_size=44,
            color="#1E293B",
            background_color="#FFFFFF",
            background_opacity=0.95,
            animation="none",
        ),
    ),
}

