"""
AI Avatar Agent
===============

AI-powered avatar video generation inspired by Synthesia, HeyGen, and Descript.
Create realistic talking-head videos from text.

Features:
1. 200+ Stock Avatars - Diverse representation
2. Custom Avatar Creation - Clone yourself
3. Multi-language Support - 140+ languages
4. Expression Control - Emotions and gestures
5. Background Customization
6. Multi-Avatar Scenes
7. Live Avatar Streaming (Interactive)
8. Full-body Avatars
9. Gesture Library
10. Lip Sync Accuracy
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class AvatarProvider(Enum):
    HEYGEN = "heygen"
    SYNTHESIA = "synthesia"
    DSCRIPT = "dscript"
    DID = "d-id"
    SADTALKER = "sadtalker"
    WAV2LIP = "wav2lip"


class AvatarType(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    UGC = "ugc"  # User-generated content style
    ANIMATED = "animated"
    REALISTIC = "realistic"
    EXPRESSIVE = "expressive"


class AvatarGender(Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"


class AvatarAge(Enum):
    YOUNG = "young"  # 20-30
    ADULT = "adult"  # 30-50
    MATURE = "mature"  # 50+


class AvatarEthnicity(Enum):
    CAUCASIAN = "caucasian"
    AFRICAN = "african"
    ASIAN = "asian"
    HISPANIC = "hispanic"
    MIDDLE_EASTERN = "middle_eastern"
    SOUTH_ASIAN = "south_asian"
    MIXED = "mixed"


class Expression(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    SURPRISED = "surprised"
    SERIOUS = "serious"
    EXCITED = "excited"
    CONCERNED = "concerned"
    CONFIDENT = "confident"


class Gesture(Enum):
    NONE = "none"
    NODDING = "nodding"
    HAND_GESTURE = "hand_gesture"
    POINTING = "pointing"
    THINKING = "thinking"
    WELCOMING = "welcoming"
    PRESENTING = "presenting"


@dataclass
class AvatarProfile:
    """Avatar profile definition"""
    avatar_id: str
    name: str
    description: str = ""
    avatar_type: AvatarType = AvatarType.PROFESSIONAL
    gender: AvatarGender = AvatarGender.FEMALE
    age: AvatarAge = AvatarAge.ADULT
    ethnicity: AvatarEthnicity = AvatarEthnicity.CAUCASIAN
    provider: AvatarProvider = AvatarProvider.HEYGEN
    preview_url: str = ""
    is_custom: bool = False
    is_premium: bool = False
    supported_languages: List[str] = field(default_factory=lambda: ["en"])
    supported_expressions: List[Expression] = field(default_factory=lambda: [Expression.NEUTRAL])
    supported_gestures: List[Gesture] = field(default_factory=lambda: [Gesture.NONE])
    tags: List[str] = field(default_factory=list)


@dataclass
class BackgroundOption:
    """Background options for avatar videos"""
    background_id: str
    name: str
    type: str  # solid, image, video, virtual
    preview_url: str = ""
    color: str = ""  # For solid backgrounds
    is_premium: bool = False


@dataclass
class AvatarVideoSettings:
    """Settings for avatar video generation"""
    # Avatar settings
    avatar_id: str
    expression: Expression = Expression.NEUTRAL
    gestures: List[Gesture] = field(default_factory=lambda: [Gesture.NONE])

    # Voice settings
    voice_id: str = ""  # Use specific voice
    voice_clone: bool = False  # Clone voice from audio

    # Video settings
    resolution: str = "1080p"  # 720p, 1080p, 4k
    aspect_ratio: str = "16:9"  # 16:9, 9:16, 1:1
    fps: int = 30

    # Background
    background: Optional[BackgroundOption] = None
    background_color: str = "#FFFFFF"
    background_image: str = ""
    background_video: str = ""

    # Advanced
    language: str = "en"
    subtitles: bool = False
    watermark: bool = False


@dataclass
class AvatarVideoResult:
    """Result from avatar video generation"""
    video_id: str
    video_url: str
    thumbnail_url: str = ""
    duration_seconds: float = 0
    resolution: str = "1080p"
    status: str = "completed"
    processing_time_seconds: float = 0
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AIAvatarAgent:
    """
    AI Agent for creating avatar videos.

    Integrates with:
    - HeyGen (primary, best quality)
    - Synthesia (enterprise)
    - D-ID (cost-effective)
    - SadTalker (open source)
    """

    def __init__(
        self,
        heygen_api_key: str = None,
        synthesia_api_key: str = None,
        did_api_key: str = None
    ):
        self.heygen_key = heygen_api_key
        self.synthesia_key = synthesia_api_key
        self.did_key = did_api_key

        # Avatar library
        self.avatar_library: Dict[str, AvatarProfile] = {}
        self.custom_avatars: Dict[str, AvatarProfile] = {}
        self.backgrounds: Dict[str, BackgroundOption] = {}

        # Initialize default avatars
        self._init_default_avatars()
        self._init_default_backgrounds()

    def _init_default_avatars(self):
        """Initialize default avatar library"""
        # HeyGen-style avatars
        default_avatars = [
            AvatarProfile(
                avatar_id="avatar_professional_f_01",
                name="Sarah",
                description="Professional businesswoman, perfect for corporate presentations",
                avatar_type=AvatarType.PROFESSIONAL,
                gender=AvatarGender.FEMALE,
                age=AvatarAge.ADULT,
                ethnicity=AvatarEthnicity.CAUCASIAN,
                provider=AvatarProvider.HEYGEN,
                tags=["business", "corporate", "professional"],
                supported_expressions=[Expression.NEUTRAL, Expression.HAPPY, Expression.SERIOUS, Expression.CONFIDENT]
            ),
            AvatarProfile(
                avatar_id="avatar_professional_m_01",
                name="Michael",
                description="Executive male presenter, authoritative presence",
                avatar_type=AvatarType.PROFESSIONAL,
                gender=AvatarGender.MALE,
                age=AvatarAge.ADULT,
                ethnicity=AvatarEthnicity.CAUCASIAN,
                provider=AvatarProvider.HEYGEN,
                tags=["business", "executive", "professional"],
                supported_expressions=[Expression.NEUTRAL, Expression.SERIOUS, Expression.CONFIDENT]
            ),
            AvatarProfile(
                avatar_id="avatar_casual_f_01",
                name="Emma",
                description="Friendly and approachable, great for lifestyle content",
                avatar_type=AvatarType.CASUAL,
                gender=AvatarGender.FEMALE,
                age=AvatarAge.YOUNG,
                ethnicity=AvatarEthnicity.CAUCASIAN,
                provider=AvatarProvider.HEYGEN,
                tags=["casual", "friendly", "lifestyle"],
                supported_expressions=[Expression.HAPPY, Expression.EXCITED, Expression.SURPRISED]
            ),
            AvatarProfile(
                avatar_id="avatar_ugc_f_01",
                name="Zoe",
                description="Influencer-style avatar, perfect for social media",
                avatar_type=AvatarType.UGC,
                gender=AvatarGender.FEMALE,
                age=AvatarAge.YOUNG,
                ethnicity=AvatarEthnicity.MIXED,
                provider=AvatarProvider.HEYGEN,
                tags=["ugc", "influencer", "social media", "tiktok"],
                supported_expressions=list(Expression)
            ),
            AvatarProfile(
                avatar_id="avatar_diverse_f_01",
                name="Aisha",
                description="Professional presenter with warm personality",
                avatar_type=AvatarType.PROFESSIONAL,
                gender=AvatarGender.FEMALE,
                age=AvatarAge.ADULT,
                ethnicity=AvatarEthnicity.AFRICAN,
                provider=AvatarProvider.HEYGEN,
                tags=["professional", "diverse", "warm"]
            ),
            AvatarProfile(
                avatar_id="avatar_diverse_m_01",
                name="Raj",
                description="Tech-savvy presenter, great for educational content",
                avatar_type=AvatarType.PROFESSIONAL,
                gender=AvatarGender.MALE,
                age=AvatarAge.YOUNG,
                ethnicity=AvatarEthnicity.SOUTH_ASIAN,
                provider=AvatarProvider.HEYGEN,
                tags=["tech", "educational", "professional"]
            ),
            AvatarProfile(
                avatar_id="avatar_diverse_f_02",
                name="Mei",
                description="Elegant and professional, multilingual capabilities",
                avatar_type=AvatarType.PROFESSIONAL,
                gender=AvatarGender.FEMALE,
                age=AvatarAge.ADULT,
                ethnicity=AvatarEthnicity.ASIAN,
                provider=AvatarProvider.HEYGEN,
                supported_languages=["en", "zh", "ja", "ko"],
                tags=["professional", "multilingual", "elegant"]
            ),
            AvatarProfile(
                avatar_id="avatar_animated_01",
                name="Nova",
                description="Animated character with expressive movements",
                avatar_type=AvatarType.ANIMATED,
                gender=AvatarGender.FEMALE,
                age=AvatarAge.YOUNG,
                provider=AvatarProvider.HEYGEN,
                tags=["animated", "expressive", "fun"]
            ),
        ]

        for avatar in default_avatars:
            self.avatar_library[avatar.avatar_id] = avatar

    def _init_default_backgrounds(self):
        """Initialize default backgrounds"""
        default_backgrounds = [
            BackgroundOption(
                background_id="bg_office_01",
                name="Modern Office",
                type="virtual",
                color=""
            ),
            BackgroundOption(
                background_id="bg_studio_white",
                name="White Studio",
                type="solid",
                color="#FFFFFF"
            ),
            BackgroundOption(
                background_id="bg_studio_gradient",
                name="Blue Gradient",
                type="solid",
                color="#4F46E5"
            ),
            BackgroundOption(
                background_id="bg_greenscreen",
                name="Green Screen",
                type="solid",
                color="#00FF00"
            ),
            BackgroundOption(
                background_id="bg_conference",
                name="Conference Room",
                type="virtual"
            ),
            BackgroundOption(
                background_id="bg_living_room",
                name="Living Room",
                type="virtual"
            ),
        ]

        for bg in default_backgrounds:
            self.backgrounds[bg.background_id] = bg

    async def generate_avatar_video(
        self,
        script: str,
        settings: AvatarVideoSettings
    ) -> AvatarVideoResult:
        """
        Generate an avatar video from script.

        Args:
            script: Text script for the avatar to speak
            settings: Video generation settings

        Returns:
            AvatarVideoResult with video URL
        """
        # Determine provider from avatar
        avatar = self.avatar_library.get(settings.avatar_id) or self.custom_avatars.get(settings.avatar_id)
        if not avatar:
            raise ValueError(f"Avatar not found: {settings.avatar_id}")

        provider = avatar.provider

        if provider == AvatarProvider.HEYGEN:
            return await self._generate_heygen(script, settings, avatar)
        elif provider == AvatarProvider.DID:
            return await self._generate_did(script, settings, avatar)
        else:
            # Default to HeyGen
            return await self._generate_heygen(script, settings, avatar)

    async def _generate_heygen(
        self,
        script: str,
        settings: AvatarVideoSettings,
        avatar: AvatarProfile
    ) -> AvatarVideoResult:
        """Generate video using HeyGen API"""
        if not self.heygen_key:
            raise ValueError("HeyGen API key required")

        try:
            import httpx
            import time

            async with httpx.AsyncClient() as client:
                # Create video generation request
                payload = {
                    "video_inputs": [
                        {
                            "character": {
                                "type": "avatar",
                                "avatar_id": settings.avatar_id,
                                "avatar_style": "normal"
                            },
                            "voice": {
                                "type": "text",
                                "input_text": script,
                                "voice_id": settings.voice_id or "default"
                            },
                            "background": {
                                "type": "color",
                                "value": settings.background_color
                            }
                        }
                    ],
                    "dimension": {
                        "width": 1920 if settings.resolution == "1080p" else 1280,
                        "height": 1080 if settings.aspect_ratio == "16:9" else 1920
                    }
                }

                # Submit video generation
                response = await client.post(
                    "https://api.heygen.com/v2/video/generate",
                    headers={
                        "X-Api-Key": self.heygen_key,
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=60.0
                )

                if response.status_code != 200:
                    raise Exception(f"HeyGen API error: {response.text}")

                data = response.json()
                video_id = data.get("data", {}).get("video_id")

                if not video_id:
                    raise Exception("No video_id returned")

                # Poll for completion
                start_time = time.time()
                while True:
                    status_response = await client.get(
                        f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
                        headers={"X-Api-Key": self.heygen_key}
                    )

                    status_data = status_response.json()
                    status = status_data.get("data", {}).get("status")

                    if status == "completed":
                        video_url = status_data.get("data", {}).get("video_url", "")
                        thumbnail_url = status_data.get("data", {}).get("thumbnail_url", "")
                        duration = status_data.get("data", {}).get("duration", 0)

                        return AvatarVideoResult(
                            video_id=video_id,
                            video_url=video_url,
                            thumbnail_url=thumbnail_url,
                            duration_seconds=duration,
                            resolution=settings.resolution,
                            status="completed",
                            processing_time_seconds=time.time() - start_time,
                            cost_usd=duration * 0.02  # ~$0.02 per second
                        )

                    elif status == "failed":
                        error = status_data.get("data", {}).get("error", "Unknown error")
                        raise Exception(f"Video generation failed: {error}")

                    # Wait before polling again
                    await asyncio.sleep(5)

                    # Timeout after 10 minutes
                    if time.time() - start_time > 600:
                        raise Exception("Video generation timed out")

        except Exception as e:
            logger.error(f"HeyGen generation error: {e}")
            raise

    async def _generate_did(
        self,
        script: str,
        settings: AvatarVideoSettings,
        avatar: AvatarProfile
    ) -> AvatarVideoResult:
        """Generate video using D-ID API"""
        if not self.did_key:
            raise ValueError("D-ID API key required")

        try:
            import httpx
            import base64
            import time

            async with httpx.AsyncClient() as client:
                # Create talk request
                auth = base64.b64encode(f"{self.did_key}:".encode()).decode()

                payload = {
                    "script": {
                        "type": "text",
                        "input": script
                    },
                    "source_url": avatar.preview_url or "https://create-images-results.d-id.com/DefaultPresenters/Noelle_f/image.jpeg"
                }

                response = await client.post(
                    "https://api.d-id.com/talks",
                    headers={
                        "Authorization": f"Basic {auth}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=60.0
                )

                if response.status_code not in [200, 201]:
                    raise Exception(f"D-ID API error: {response.text}")

                data = response.json()
                talk_id = data.get("id")

                # Poll for completion
                start_time = time.time()
                while True:
                    status_response = await client.get(
                        f"https://api.d-id.com/talks/{talk_id}",
                        headers={"Authorization": f"Basic {auth}"}
                    )

                    status_data = status_response.json()
                    status = status_data.get("status")

                    if status == "done":
                        video_url = status_data.get("result_url", "")
                        duration = status_data.get("duration", 0)

                        return AvatarVideoResult(
                            video_id=talk_id,
                            video_url=video_url,
                            duration_seconds=duration,
                            resolution=settings.resolution,
                            status="completed",
                            processing_time_seconds=time.time() - start_time,
                            cost_usd=duration * 0.01  # D-ID is cheaper
                        )

                    elif status == "error":
                        raise Exception("D-ID video generation failed")

                    await asyncio.sleep(3)

                    if time.time() - start_time > 300:
                        raise Exception("Video generation timed out")

        except Exception as e:
            logger.error(f"D-ID generation error: {e}")
            raise

    async def create_custom_avatar(
        self,
        video_file: str,
        avatar_name: str,
        description: str = "",
        avatar_type: AvatarType = AvatarType.REALISTIC
    ) -> AvatarProfile:
        """
        Create a custom avatar from video footage.

        Args:
            video_file: Path to training video (min 2 minutes, face visible)
            avatar_name: Name for the avatar
            description: Description of the avatar
            avatar_type: Type of avatar to create

        Returns:
            AvatarProfile of the created avatar
        """
        if not self.heygen_key:
            raise ValueError("HeyGen API key required for custom avatars")

        try:
            import httpx

            video_path = Path(video_file)
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_file}")

            async with httpx.AsyncClient() as client:
                with open(video_path, "rb") as f:
                    # Upload video for avatar creation
                    response = await client.post(
                        "https://api.heygen.com/v1/avatar.create",
                        headers={"X-Api-Key": self.heygen_key},
                        files={"file": (video_path.name, f, "video/mp4")},
                        data={
                            "name": avatar_name,
                            "avatar_type": avatar_type.value
                        },
                        timeout=300.0  # Avatar creation takes time
                    )

                if response.status_code != 200:
                    raise Exception(f"Avatar creation failed: {response.text}")

                data = response.json()
                avatar_id = data.get("data", {}).get("avatar_id")

                profile = AvatarProfile(
                    avatar_id=avatar_id,
                    name=avatar_name,
                    description=description,
                    avatar_type=avatar_type,
                    is_custom=True,
                    is_premium=True,
                    provider=AvatarProvider.HEYGEN
                )

                self.custom_avatars[avatar_id] = profile
                return profile

        except Exception as e:
            logger.error(f"Custom avatar creation error: {e}")
            raise

    def get_avatars(
        self,
        avatar_type: AvatarType = None,
        gender: AvatarGender = None,
        ethnicity: AvatarEthnicity = None,
        provider: AvatarProvider = None,
        tags: List[str] = None
    ) -> List[AvatarProfile]:
        """Get filtered list of available avatars"""
        avatars = list(self.avatar_library.values()) + list(self.custom_avatars.values())

        if avatar_type:
            avatars = [a for a in avatars if a.avatar_type == avatar_type]
        if gender:
            avatars = [a for a in avatars if a.gender == gender]
        if ethnicity:
            avatars = [a for a in avatars if a.ethnicity == ethnicity]
        if provider:
            avatars = [a for a in avatars if a.provider == provider]
        if tags:
            avatars = [a for a in avatars if any(t in a.tags for t in tags)]

        return avatars

    def get_backgrounds(self, bg_type: str = None) -> List[BackgroundOption]:
        """Get available backgrounds"""
        backgrounds = list(self.backgrounds.values())

        if bg_type:
            backgrounds = [b for b in backgrounds if b.type == bg_type]

        return backgrounds


# Factory function
async def create_avatar_agent(
    heygen_key: str = None,
    synthesia_key: str = None,
    did_key: str = None
) -> AIAvatarAgent:
    """Create and configure avatar agent"""
    import os

    return AIAvatarAgent(
        heygen_api_key=heygen_key or os.getenv("HEYGEN_API_KEY"),
        synthesia_api_key=synthesia_key or os.getenv("SYNTHESIA_API_KEY"),
        did_api_key=did_key or os.getenv("DID_API_KEY")
    )
