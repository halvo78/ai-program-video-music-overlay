"""
Content-to-Video System for Taj Chat

Inspired by Pictory and InVideo.
Convert blogs, URLs, scripts, and documents to videos.
"""

import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from enum import Enum
import logging
import re

logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Types of content that can be converted."""
    URL = "url"
    BLOG_POST = "blog_post"
    SCRIPT = "script"
    TRANSCRIPT = "transcript"
    ARTICLE = "article"
    SLIDES = "slides"
    DOCUMENT = "document"
    SOCIAL_POST = "social_post"
    PRODUCT_DESCRIPTION = "product_description"


class VideoFormat(Enum):
    """Output video formats."""
    SHORT_FORM = "short_form"  # 15-60 seconds (TikTok, Reels, Shorts)
    MEDIUM_FORM = "medium_form"  # 1-5 minutes
    LONG_FORM = "long_form"  # 5+ minutes
    HIGHLIGHT_REEL = "highlight_reel"  # Best moments
    SERIES = "series"  # Multiple videos


@dataclass
class ContentSource:
    """Source content for conversion."""
    content_type: ContentType
    content: str  # Text content or URL
    title: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class VideoScene:
    """Single scene in generated video."""
    scene_id: str
    text: str  # Script/narration text
    duration_seconds: float
    visual_prompt: str  # AI prompt for visuals
    b_roll_keywords: List[str] = field(default_factory=list)
    music_mood: Optional[str] = None
    transition: str = "fade"


@dataclass
class ContentToVideoRequest:
    """Request for content-to-video conversion."""
    source: ContentSource
    output_format: VideoFormat = VideoFormat.SHORT_FORM

    # Visual settings
    visual_style: str = "professional"
    aspect_ratio: str = "9:16"
    include_captions: bool = True
    caption_style: str = "modern"  # modern, classic, minimal, bold

    # Audio settings
    voice_id: Optional[str] = None
    voice_gender: str = "female"
    music_style: Optional[str] = None

    # B-roll settings
    use_stock_footage: bool = True
    use_ai_generated: bool = True

    # Branding
    brand_colors: Optional[List[str]] = None
    logo_url: Optional[str] = None
    watermark: bool = False


@dataclass
class ContentToVideoResult:
    """Result of content-to-video conversion."""
    video_id: str
    status: str

    # Output
    video_url: Optional[str] = None
    scenes: List[VideoScene] = field(default_factory=list)
    total_duration_seconds: float = 0.0

    # Additional outputs
    script_url: Optional[str] = None
    captions_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    # Processing info
    source_word_count: int = 0
    processing_time_seconds: float = 0.0
    error: Optional[str] = None


class ContentParser:
    """Parse different content types."""

    @staticmethod
    async def parse_url(url: str) -> Dict:
        """Parse content from URL."""
        # In production, would fetch and parse webpage
        return {
            "title": "Article Title",
            "text": "Article content...",
            "images": [],
            "metadata": {},
        }

    @staticmethod
    async def parse_blog(text: str) -> Dict:
        """Parse blog post content."""
        # Extract sections, headings, key points
        paragraphs = text.split("\n\n")
        return {
            "title": paragraphs[0] if paragraphs else "",
            "sections": paragraphs[1:],
            "word_count": len(text.split()),
        }

    @staticmethod
    async def parse_transcript(text: str) -> Dict:
        """Parse video/audio transcript."""
        # Extract speakers, timestamps, key moments
        lines = text.split("\n")
        return {
            "lines": lines,
            "speakers": [],
            "highlights": [],
        }


class ScriptGenerator:
    """Generate video scripts from content."""

    def __init__(self):
        self.max_words_per_scene = 30  # For short form
        self.target_wpm = 150  # Words per minute

    async def generate_script(
        self,
        content: Dict,
        target_duration: float,
    ) -> List[VideoScene]:
        """
        Generate video script from parsed content.
        Breaks content into scenes with timings.
        """
        scenes = []
        text = content.get("text", "") or " ".join(content.get("sections", []))

        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Group sentences into scenes
        current_scene_text = []
        current_words = 0

        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())

            if current_words + word_count > self.max_words_per_scene:
                # Create scene
                scene_text = " ".join(current_scene_text)
                duration = (current_words / self.target_wpm) * 60

                scenes.append(VideoScene(
                    scene_id=f"scene_{len(scenes)+1:03d}",
                    text=scene_text,
                    duration_seconds=duration,
                    visual_prompt=self._generate_visual_prompt(scene_text),
                    b_roll_keywords=self._extract_keywords(scene_text),
                ))

                current_scene_text = [sentence]
                current_words = word_count
            else:
                current_scene_text.append(sentence)
                current_words += word_count

        # Last scene
        if current_scene_text:
            scene_text = " ".join(current_scene_text)
            duration = (current_words / self.target_wpm) * 60

            scenes.append(VideoScene(
                scene_id=f"scene_{len(scenes)+1:03d}",
                text=scene_text,
                duration_seconds=duration,
                visual_prompt=self._generate_visual_prompt(scene_text),
                b_roll_keywords=self._extract_keywords(scene_text),
            ))

        return scenes

    def _generate_visual_prompt(self, text: str) -> str:
        """Generate visual prompt from scene text."""
        # Extract key concepts for visual generation
        return f"Cinematic shot representing: {text[:100]}..."

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords for b-roll search."""
        # Simple keyword extraction
        words = text.lower().split()
        # Filter common words
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "to", "for", "of", "and", "or"}
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        return keywords[:5]


class BRollEngine:
    """
    Smart B-Roll selection and generation.
    Like Kapwing's Smart B-Roll feature.
    """

    def __init__(self):
        self.stock_libraries = ["pexels", "unsplash", "pixabay"]

    async def find_stock_footage(
        self,
        keywords: List[str],
        duration_needed: float,
    ) -> List[Dict]:
        """Search stock libraries for matching footage."""
        # In production, would search actual stock APIs
        return [
            {
                "source": "pexels",
                "url": f"https://videos.pexels.com/{keywords[0]}.mp4",
                "duration": 10.0,
                "relevance_score": 0.95,
            }
            for keyword in keywords
        ]

    async def generate_ai_footage(
        self,
        prompt: str,
        duration_seconds: float,
    ) -> Dict:
        """Generate AI footage for scene."""
        import uuid

        return {
            "type": "ai_generated",
            "url": f"/generated/broll/{uuid.uuid4().hex[:8]}.mp4",
            "duration": duration_seconds,
            "prompt": prompt,
        }

    async def select_best_footage(
        self,
        scene: VideoScene,
        use_stock: bool = True,
        use_ai: bool = True,
    ) -> List[Dict]:
        """Select best footage for a scene."""
        options = []

        if use_stock:
            stock = await self.find_stock_footage(
                scene.b_roll_keywords,
                scene.duration_seconds,
            )
            options.extend(stock)

        if use_ai:
            ai_footage = await self.generate_ai_footage(
                scene.visual_prompt,
                scene.duration_seconds,
            )
            options.append(ai_footage)

        # Sort by relevance
        options.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return options


class HighlightExtractor:
    """
    Extract highlights from long videos.
    Like Pictory's Video Highlights feature.
    """

    async def extract_highlights(
        self,
        video_url: str,
        max_duration_seconds: float = 60.0,
        num_highlights: int = 5,
    ) -> List[Dict]:
        """Extract key moments from video."""
        # In production, would analyze video content
        return [
            {
                "start": i * 60,
                "end": i * 60 + 10,
                "score": 0.9 - (i * 0.1),
                "description": f"Highlight {i+1}",
            }
            for i in range(num_highlights)
        ]

    async def create_highlight_reel(
        self,
        video_url: str,
        target_duration: float = 60.0,
    ) -> ContentToVideoResult:
        """Create highlight reel from long video."""
        import uuid

        highlights = await self.extract_highlights(
            video_url,
            max_duration_seconds=target_duration,
        )

        video_id = f"highlights_{uuid.uuid4().hex[:8]}"

        return ContentToVideoResult(
            video_id=video_id,
            status="completed",
            video_url=f"/generated/highlights/{video_id}.mp4",
            total_duration_seconds=target_duration,
        )


class ContentToVideoEngine:
    """
    Main Content-to-Video Engine.

    Features inspired by:
    - Pictory: Blog-to-Video, URL-to-Video, Highlights
    - InVideo: Prompt to full video
    - Kapwing: Smart B-Roll, AI editing
    """

    def __init__(self):
        self.parser = ContentParser()
        self.script_generator = ScriptGenerator()
        self.broll_engine = BRollEngine()
        self.highlight_extractor = HighlightExtractor()

    async def convert(
        self,
        request: ContentToVideoRequest,
    ) -> ContentToVideoResult:
        """
        Convert content to video.
        Main entry point for content-to-video conversion.
        """
        import uuid
        import time

        video_id = f"content_video_{uuid.uuid4().hex[:8]}"
        start_time = time.time()

        logger.info(f"Converting content to video: {video_id}")
        logger.info(f"Content type: {request.source.content_type.value}")
        logger.info(f"Output format: {request.output_format.value}")

        # Parse content
        if request.source.content_type == ContentType.URL:
            parsed = await self.parser.parse_url(request.source.content)
        elif request.source.content_type == ContentType.TRANSCRIPT:
            parsed = await self.parser.parse_transcript(request.source.content)
        else:
            parsed = await self.parser.parse_blog(request.source.content)

        # Calculate target duration based on format
        target_duration = {
            VideoFormat.SHORT_FORM: 45.0,
            VideoFormat.MEDIUM_FORM: 180.0,
            VideoFormat.LONG_FORM: 600.0,
            VideoFormat.HIGHLIGHT_REEL: 60.0,
        }.get(request.output_format, 60.0)

        # Generate script
        scenes = await self.script_generator.generate_script(
            parsed,
            target_duration,
        )

        # Get b-roll for each scene
        for scene in scenes:
            await self.broll_engine.select_best_footage(
                scene,
                use_stock=request.use_stock_footage,
                use_ai=request.use_ai_generated,
            )

        total_duration = sum(s.duration_seconds for s in scenes)

        return ContentToVideoResult(
            video_id=video_id,
            status="completed",
            video_url=f"/generated/content/{video_id}.mp4",
            scenes=scenes,
            total_duration_seconds=total_duration,
            script_url=f"/generated/content/{video_id}_script.txt",
            captions_url=f"/generated/content/{video_id}.srt",
            thumbnail_url=f"/generated/content/{video_id}_thumb.jpg",
            source_word_count=parsed.get("word_count", 0),
            processing_time_seconds=time.time() - start_time,
        )

    async def url_to_video(
        self,
        url: str,
        output_format: VideoFormat = VideoFormat.SHORT_FORM,
    ) -> ContentToVideoResult:
        """Convert URL content to video."""
        return await self.convert(ContentToVideoRequest(
            source=ContentSource(
                content_type=ContentType.URL,
                content=url,
            ),
            output_format=output_format,
        ))

    async def blog_to_video(
        self,
        blog_text: str,
        output_format: VideoFormat = VideoFormat.SHORT_FORM,
    ) -> ContentToVideoResult:
        """Convert blog post to video."""
        return await self.convert(ContentToVideoRequest(
            source=ContentSource(
                content_type=ContentType.BLOG_POST,
                content=blog_text,
            ),
            output_format=output_format,
        ))

    async def script_to_video(
        self,
        script: str,
        voice_id: Optional[str] = None,
    ) -> ContentToVideoResult:
        """Convert script to video."""
        return await self.convert(ContentToVideoRequest(
            source=ContentSource(
                content_type=ContentType.SCRIPT,
                content=script,
            ),
            voice_id=voice_id,
        ))


# Global instance
content_to_video = ContentToVideoEngine()
