"""
Element Library System for Taj Chat

Inspired by Kling O1's Element Library and Runway's character consistency.
Store and reuse characters, objects, and styles across videos.
"""

import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ElementType(Enum):
    """Types of elements that can be stored."""
    CHARACTER = "character"
    OBJECT = "object"
    STYLE = "style"
    ENVIRONMENT = "environment"
    BRAND = "brand"
    MOTION = "motion"
    VOICE = "voice"
    MUSIC = "music"


class ElementCategory(Enum):
    """Element categories for organization."""
    PERSON = "person"
    ANIMAL = "animal"
    VEHICLE = "vehicle"
    BUILDING = "building"
    NATURE = "nature"
    PRODUCT = "product"
    CUSTOM = "custom"


@dataclass
class ElementReference:
    """Reference material for an element."""
    reference_id: str
    url: str
    reference_type: str  # image, video, audio
    description: Optional[str] = None
    is_primary: bool = False


@dataclass
class Element:
    """
    Stored element for consistent generation.
    Like Kling O1's Element Library.
    """
    element_id: str
    name: str
    element_type: ElementType
    category: ElementCategory = ElementCategory.CUSTOM

    # Reference materials
    references: List[ElementReference] = field(default_factory=list)

    # Extracted features (for AI consistency)
    features: Dict = field(default_factory=dict)  # AI-extracted features
    embeddings: Optional[List[float]] = None  # Vector embedding

    # Metadata
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    use_count: int = 0
    owner_id: Optional[str] = None

    # Generation settings
    default_settings: Dict = field(default_factory=dict)


@dataclass
class ElementCollection:
    """Collection of related elements."""
    collection_id: str
    name: str
    description: Optional[str] = None
    elements: List[str] = field(default_factory=list)  # Element IDs
    is_public: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class BrandKit:
    """
    Brand kit for consistent branding.
    Like Synthesia and Pictory brand kits.
    """
    brand_id: str
    name: str

    # Visual branding
    primary_color: str = "#7C3AED"
    secondary_color: str = "#06B6D4"
    accent_color: str = "#F472B6"
    logo_url: Optional[str] = None
    font_family: str = "Inter"
    font_heading: str = "Inter"

    # Audio branding
    intro_audio_url: Optional[str] = None
    outro_audio_url: Optional[str] = None
    default_music_style: Optional[str] = None
    default_voice_id: Optional[str] = None

    # Watermark
    watermark_url: Optional[str] = None
    watermark_position: str = "bottom_right"
    watermark_opacity: float = 0.5

    # Templates
    intro_template_id: Optional[str] = None
    outro_template_id: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    owner_id: Optional[str] = None


class ElementLibrary:
    """
    Element Library for storing and managing reusable elements.

    Features inspired by:
    - Kling O1: Element Library for character consistency
    - Runway: Character and object references
    - Synthesia/Pictory: Brand kits
    """

    def __init__(self):
        self._elements: Dict[str, Element] = {}
        self._collections: Dict[str, ElementCollection] = {}
        self._brand_kits: Dict[str, BrandKit] = {}

    # Element Management

    async def create_element(
        self,
        name: str,
        element_type: ElementType,
        references: List[str],  # URLs
        description: Optional[str] = None,
        category: ElementCategory = ElementCategory.CUSTOM,
    ) -> Element:
        """
        Create a new element from reference materials.
        Extracts features for consistent generation.
        """
        import uuid

        element_id = f"elem_{uuid.uuid4().hex[:8]}"

        # Create reference objects
        ref_objects = []
        for i, url in enumerate(references):
            ref_type = "image"
            if url.endswith((".mp4", ".mov", ".webm")):
                ref_type = "video"
            elif url.endswith((".mp3", ".wav", ".m4a")):
                ref_type = "audio"

            ref_objects.append(ElementReference(
                reference_id=f"ref_{i}",
                url=url,
                reference_type=ref_type,
                is_primary=(i == 0),
            ))

        # Extract features (in production, would use AI)
        features = await self._extract_features(ref_objects)

        element = Element(
            element_id=element_id,
            name=name,
            element_type=element_type,
            category=category,
            references=ref_objects,
            features=features,
            description=description,
        )

        self._elements[element_id] = element
        logger.info(f"Created element: {name} ({element_id})")

        return element

    async def _extract_features(
        self,
        references: List[ElementReference],
    ) -> Dict:
        """Extract AI features from references."""
        # In production, would use vision models to extract:
        # - Facial features for characters
        # - Object characteristics
        # - Style attributes

        return {
            "extracted": True,
            "reference_count": len(references),
            "feature_vector_size": 512,
        }

    def get_element(self, element_id: str) -> Optional[Element]:
        """Get element by ID."""
        return self._elements.get(element_id)

    def search_elements(
        self,
        query: Optional[str] = None,
        element_type: Optional[ElementType] = None,
        category: Optional[ElementCategory] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Element]:
        """Search elements by criteria."""
        results = list(self._elements.values())

        if element_type:
            results = [e for e in results if e.element_type == element_type]

        if category:
            results = [e for e in results if e.category == category]

        if tags:
            results = [e for e in results if any(t in e.tags for t in tags)]

        if query:
            query_lower = query.lower()
            results = [
                e for e in results
                if query_lower in e.name.lower()
                or (e.description and query_lower in e.description.lower())
            ]

        return results

    def delete_element(self, element_id: str) -> bool:
        """Delete an element."""
        if element_id in self._elements:
            del self._elements[element_id]
            return True
        return False

    # Collection Management

    def create_collection(
        self,
        name: str,
        element_ids: List[str],
        description: Optional[str] = None,
    ) -> ElementCollection:
        """Create a collection of elements."""
        import uuid

        collection_id = f"coll_{uuid.uuid4().hex[:8]}"

        collection = ElementCollection(
            collection_id=collection_id,
            name=name,
            description=description,
            elements=element_ids,
        )

        self._collections[collection_id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[ElementCollection]:
        """Get collection by ID."""
        return self._collections.get(collection_id)

    # Brand Kit Management

    def create_brand_kit(
        self,
        name: str,
        primary_color: str = "#7C3AED",
        secondary_color: str = "#06B6D4",
        logo_url: Optional[str] = None,
    ) -> BrandKit:
        """Create a brand kit."""
        import uuid

        brand_id = f"brand_{uuid.uuid4().hex[:8]}"

        brand = BrandKit(
            brand_id=brand_id,
            name=name,
            primary_color=primary_color,
            secondary_color=secondary_color,
            logo_url=logo_url,
        )

        self._brand_kits[brand_id] = brand
        return brand

    def get_brand_kit(self, brand_id: str) -> Optional[BrandKit]:
        """Get brand kit by ID."""
        return self._brand_kits.get(brand_id)

    # Generation with Elements

    async def generate_with_element(
        self,
        element_id: str,
        prompt: str,
        duration_seconds: float = 5.0,
    ) -> Dict:
        """
        Generate video using stored element for consistency.
        Like Kling O1's element-based generation.
        """
        import uuid

        element = self.get_element(element_id)
        if not element:
            return {"error": f"Element not found: {element_id}"}

        # Increment use count
        element.use_count += 1
        element.updated_at = datetime.now()

        video_id = f"elem_gen_{uuid.uuid4().hex[:8]}"

        return {
            "video_id": video_id,
            "status": "completed",
            "video_url": f"/generated/elements/{video_id}.mp4",
            "element_used": element.name,
            "duration_seconds": duration_seconds,
        }

    async def generate_with_brand(
        self,
        brand_id: str,
        prompt: str,
        content: str,
    ) -> Dict:
        """
        Generate video using brand kit for consistent branding.
        """
        import uuid

        brand = self.get_brand_kit(brand_id)
        if not brand:
            return {"error": f"Brand kit not found: {brand_id}"}

        video_id = f"brand_gen_{uuid.uuid4().hex[:8]}"

        return {
            "video_id": video_id,
            "status": "completed",
            "video_url": f"/generated/branded/{video_id}.mp4",
            "brand_applied": brand.name,
            "has_logo": brand.logo_url is not None,
            "has_watermark": brand.watermark_url is not None,
        }


class CharacterManager:
    """
    Specialized character management.
    Ensures consistent character appearance across shots.
    """

    def __init__(self, library: ElementLibrary):
        self.library = library

    async def create_character(
        self,
        name: str,
        reference_images: List[str],
        voice_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Element:
        """Create a character element."""
        character = await self.library.create_element(
            name=name,
            element_type=ElementType.CHARACTER,
            references=reference_images,
            description=description,
            category=ElementCategory.PERSON,
        )

        # Store voice reference
        if voice_id:
            character.default_settings["voice_id"] = voice_id

        return character

    async def generate_character_shot(
        self,
        character_id: str,
        action: str,
        setting: str,
        camera_angle: str = "medium",
    ) -> Dict:
        """
        Generate a shot of a character with consistent appearance.
        """
        character = self.library.get_element(character_id)
        if not character:
            return {"error": "Character not found"}

        prompt = f"{character.name} {action} in {setting}, {camera_angle} shot"

        return await self.library.generate_with_element(
            character_id,
            prompt,
        )


# Global instances
element_library = ElementLibrary()
character_manager = CharacterManager(element_library)
