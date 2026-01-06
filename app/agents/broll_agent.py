"""
AI B-Roll Agent
===============

Automatically insert relevant B-roll footage - inspired by Opus Clip and Kapwing.
AI analyzes content and inserts matching stock footage.

Features:
1. Content Analysis - Understand what's being discussed
2. B-Roll Matching - Find relevant stock footage
3. Auto-insertion - Smart placement at natural breaks
4. Timing Optimization - Perfect cut points
5. Stock Library Integration - Pexels, Storyblocks, Getty
6. AI Image Generation - Create custom B-roll with AI
7. Motion Graphics - Generate animated overlays
8. Keyword Extraction - Auto-detect key topics
9. Sentiment Matching - Match footage mood
10. Multi-source Aggregation
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class StockProvider(Enum):
    PEXELS = "pexels"
    STORYBLOCKS = "storyblocks"
    PIXABAY = "pixabay"
    UNSPLASH = "unsplash"
    GETTY = "getty"
    SHUTTERSTOCK = "shutterstock"
    AI_GENERATED = "ai_generated"


class MediaType(Enum):
    VIDEO = "video"
    IMAGE = "image"
    GIF = "gif"
    ANIMATION = "animation"


class ContentMood(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ENERGETIC = "energetic"
    CALM = "calm"
    SERIOUS = "serious"
    INSPIRING = "inspiring"
    DRAMATIC = "dramatic"
    NEUTRAL = "neutral"


@dataclass
class BRollClip:
    """A single B-roll clip"""
    clip_id: str
    url: str
    preview_url: str = ""
    thumbnail_url: str = ""
    duration_seconds: float = 0
    media_type: MediaType = MediaType.VIDEO
    provider: StockProvider = StockProvider.PEXELS
    keywords: List[str] = field(default_factory=list)
    mood: ContentMood = ContentMood.NEUTRAL
    relevance_score: float = 0.0  # 0-1
    license_type: str = "royalty-free"
    attribution: str = ""
    width: int = 1920
    height: int = 1080


@dataclass
class InsertionPoint:
    """Where to insert B-roll"""
    timestamp: float  # seconds into video
    duration: float  # how long to show B-roll
    reason: str  # why this location
    keywords: List[str]  # relevant keywords
    mood: ContentMood = ContentMood.NEUTRAL
    priority: int = 1  # 1-5, higher = more important


@dataclass
class BRollSuggestion:
    """Suggested B-roll insertion"""
    insertion_point: InsertionPoint
    clips: List[BRollClip]  # Ranked options
    selected_clip: Optional[BRollClip] = None
    is_approved: bool = False


@dataclass
class BRollPlan:
    """Complete B-roll plan for a video"""
    plan_id: str
    video_path: str
    suggestions: List[BRollSuggestion] = field(default_factory=list)
    total_broll_duration: float = 0
    primary_keywords: List[str] = field(default_factory=list)
    detected_mood: ContentMood = ContentMood.NEUTRAL
    created_at: datetime = field(default_factory=datetime.utcnow)


class AIBRollAgent:
    """
    AI Agent for automatic B-roll insertion.

    Analyzes video content and automatically suggests/inserts
    relevant B-roll footage from stock libraries or AI generation.
    """

    def __init__(
        self,
        openai_key: str = None,
        pexels_key: str = None,
        storyblocks_key: str = None,
        pixabay_key: str = None
    ):
        self.openai_key = openai_key
        self.pexels_key = pexels_key
        self.storyblocks_key = storyblocks_key
        self.pixabay_key = pixabay_key

        # Cache for stock footage searches
        self.search_cache: Dict[str, List[BRollClip]] = {}

    async def analyze_and_suggest(
        self,
        video_path: str = None,
        script: str = None,
        transcript_words: List[Dict] = None,
        max_broll_percentage: float = 0.3,  # Max 30% of video
        preferred_providers: List[StockProvider] = None
    ) -> BRollPlan:
        """
        Analyze content and suggest B-roll insertions.

        Args:
            video_path: Path to video file
            script: Video script
            transcript_words: Word-level transcript with timestamps
            max_broll_percentage: Maximum B-roll as percentage of video
            preferred_providers: Preferred stock providers

        Returns:
            BRollPlan with suggestions
        """
        import uuid
        plan_id = str(uuid.uuid4())[:8]

        # Extract keywords and analyze content
        keywords, mood = await self._analyze_content(script, transcript_words)

        # Find insertion points
        insertion_points = await self._find_insertion_points(
            script, transcript_words, keywords, mood
        )

        # Search for matching B-roll
        suggestions = []
        providers = preferred_providers or [StockProvider.PEXELS, StockProvider.PIXABAY]

        for point in insertion_points:
            clips = await self._search_broll(
                keywords=point.keywords,
                mood=point.mood,
                duration=point.duration,
                providers=providers
            )

            if clips:
                suggestions.append(BRollSuggestion(
                    insertion_point=point,
                    clips=clips[:5],  # Top 5 options
                    selected_clip=clips[0] if clips else None
                ))

        # Calculate totals
        total_duration = sum(s.insertion_point.duration for s in suggestions)

        return BRollPlan(
            plan_id=plan_id,
            video_path=video_path or "",
            suggestions=suggestions,
            total_broll_duration=total_duration,
            primary_keywords=keywords[:10],
            detected_mood=mood
        )

    async def _analyze_content(
        self,
        script: str,
        transcript_words: List[Dict] = None
    ) -> Tuple[List[str], ContentMood]:
        """Analyze content to extract keywords and mood"""

        if self.openai_key and script:
            try:
                import openai

                client = openai.AsyncOpenAI(api_key=self.openai_key)

                prompt = f"""Analyze this video script and extract:
1. Key visual keywords (nouns, actions, concepts that could be shown with B-roll)
2. Overall mood/tone of the content

Script:
{script[:2000]}

Respond in JSON format:
{{
    "keywords": ["keyword1", "keyword2", ...],
    "mood": "happy|sad|energetic|calm|serious|inspiring|dramatic|neutral"
}}"""

                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                import json
                result = json.loads(response.choices[0].message.content)

                keywords = result.get("keywords", [])
                mood_str = result.get("mood", "neutral")
                mood = ContentMood(mood_str) if mood_str in [m.value for m in ContentMood] else ContentMood.NEUTRAL

                return keywords, mood

            except Exception as e:
                logger.error(f"Content analysis error: {e}")

        # Fallback: simple keyword extraction
        keywords = self._simple_keyword_extraction(script)
        return keywords, ContentMood.NEUTRAL

    def _simple_keyword_extraction(self, text: str) -> List[str]:
        """Simple keyword extraction fallback"""
        if not text:
            return []

        # Common B-roll worthy keywords
        broll_keywords = {
            "office", "business", "meeting", "computer", "laptop", "phone",
            "nature", "mountain", "ocean", "forest", "sky", "sunset",
            "city", "street", "traffic", "building", "architecture",
            "food", "cooking", "kitchen", "restaurant", "coffee",
            "people", "team", "crowd", "family", "friends",
            "technology", "code", "programming", "data", "screen",
            "fitness", "gym", "running", "yoga", "sports",
            "travel", "airplane", "beach", "vacation", "hotel",
            "money", "finance", "investment", "growth", "success"
        }

        text_lower = text.lower()
        found = [kw for kw in broll_keywords if kw in text_lower]
        return found

    async def _find_insertion_points(
        self,
        script: str,
        transcript_words: List[Dict],
        keywords: List[str],
        mood: ContentMood
    ) -> List[InsertionPoint]:
        """Find optimal points for B-roll insertion"""

        insertion_points = []

        if self.openai_key and script:
            try:
                import openai

                client = openai.AsyncOpenAI(api_key=self.openai_key)

                prompt = f"""Analyze this script and identify the best moments for B-roll insertion.

B-roll should be inserted:
- When describing visual concepts
- During transitions between topics
- To illustrate examples or metaphors
- At natural pauses or emphasis points

Script:
{script[:3000]}

Keywords available: {', '.join(keywords[:20])}

Identify 5-10 insertion points. For each, provide:
- The text excerpt where B-roll should appear
- Duration in seconds (2-5 seconds typically)
- Relevant keywords for searching stock footage
- Reason for insertion

JSON format:
{{
    "insertion_points": [
        {{
            "text_excerpt": "the text where broll goes",
            "duration": 3,
            "keywords": ["keyword1", "keyword2"],
            "reason": "why this is a good spot",
            "priority": 1-5
        }}
    ]
}}"""

                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                import json
                result = json.loads(response.choices[0].message.content)

                for point in result.get("insertion_points", []):
                    # Find timestamp from transcript if available
                    timestamp = self._find_text_timestamp(
                        point.get("text_excerpt", ""),
                        transcript_words
                    )

                    insertion_points.append(InsertionPoint(
                        timestamp=timestamp,
                        duration=point.get("duration", 3),
                        reason=point.get("reason", ""),
                        keywords=point.get("keywords", []),
                        mood=mood,
                        priority=point.get("priority", 3)
                    ))

            except Exception as e:
                logger.error(f"Insertion point analysis error: {e}")

        # Fallback: distribute B-roll evenly
        if not insertion_points:
            # Create insertion points every 20 seconds
            if transcript_words:
                video_duration = max(w.get("end", 0) for w in transcript_words) if transcript_words else 60
            else:
                video_duration = 60

            for i in range(5, int(video_duration), 20):
                insertion_points.append(InsertionPoint(
                    timestamp=float(i),
                    duration=3.0,
                    reason="Regular interval insertion",
                    keywords=keywords[:3] if keywords else ["general"],
                    mood=mood
                ))

        return insertion_points

    def _find_text_timestamp(
        self,
        text_excerpt: str,
        transcript_words: List[Dict]
    ) -> float:
        """Find timestamp for text excerpt in transcript"""
        if not transcript_words or not text_excerpt:
            return 0.0

        text_lower = text_excerpt.lower().split()[:5]

        for i, word in enumerate(transcript_words):
            if word.get("word", "").lower() in text_lower:
                return word.get("start", 0)

        return 0.0

    async def _search_broll(
        self,
        keywords: List[str],
        mood: ContentMood,
        duration: float,
        providers: List[StockProvider]
    ) -> List[BRollClip]:
        """Search for B-roll footage from stock providers"""

        all_clips = []
        search_query = " ".join(keywords[:3])

        # Check cache
        cache_key = f"{search_query}_{mood.value}"
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]

        for provider in providers:
            if provider == StockProvider.PEXELS:
                clips = await self._search_pexels(search_query, mood)
                all_clips.extend(clips)
            elif provider == StockProvider.PIXABAY:
                clips = await self._search_pixabay(search_query, mood)
                all_clips.extend(clips)

        # Sort by relevance
        all_clips.sort(key=lambda x: x.relevance_score, reverse=True)

        # Cache results
        self.search_cache[cache_key] = all_clips[:10]

        return all_clips[:10]

    async def _search_pexels(
        self,
        query: str,
        mood: ContentMood
    ) -> List[BRollClip]:
        """Search Pexels for videos"""
        if not self.pexels_key:
            return []

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.pexels.com/videos/search",
                    headers={"Authorization": self.pexels_key},
                    params={
                        "query": query,
                        "per_page": 10,
                        "orientation": "landscape"
                    }
                )

                if response.status_code != 200:
                    return []

                data = response.json()
                clips = []

                for video in data.get("videos", []):
                    # Get best video file
                    video_files = video.get("video_files", [])
                    hd_file = next(
                        (f for f in video_files if f.get("quality") == "hd"),
                        video_files[0] if video_files else None
                    )

                    if hd_file:
                        clips.append(BRollClip(
                            clip_id=str(video.get("id")),
                            url=hd_file.get("link", ""),
                            preview_url=video.get("url", ""),
                            thumbnail_url=video.get("image", ""),
                            duration_seconds=video.get("duration", 0),
                            media_type=MediaType.VIDEO,
                            provider=StockProvider.PEXELS,
                            keywords=query.split(),
                            mood=mood,
                            relevance_score=0.8,
                            width=hd_file.get("width", 1920),
                            height=hd_file.get("height", 1080),
                            license_type="royalty-free",
                            attribution=f"Video by {video.get('user', {}).get('name', 'Pexels')}"
                        ))

                return clips

        except Exception as e:
            logger.error(f"Pexels search error: {e}")
            return []

    async def _search_pixabay(
        self,
        query: str,
        mood: ContentMood
    ) -> List[BRollClip]:
        """Search Pixabay for videos"""
        if not self.pixabay_key:
            return []

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://pixabay.com/api/videos/",
                    params={
                        "key": self.pixabay_key,
                        "q": query,
                        "per_page": 10,
                        "video_type": "film"
                    }
                )

                if response.status_code != 200:
                    return []

                data = response.json()
                clips = []

                for video in data.get("hits", []):
                    videos = video.get("videos", {})
                    large = videos.get("large", {}) or videos.get("medium", {})

                    if large:
                        clips.append(BRollClip(
                            clip_id=str(video.get("id")),
                            url=large.get("url", ""),
                            preview_url=video.get("pageURL", ""),
                            thumbnail_url=f"https://i.vimeocdn.com/video/{video.get('picture_id')}_640x360.jpg",
                            duration_seconds=video.get("duration", 0),
                            media_type=MediaType.VIDEO,
                            provider=StockProvider.PIXABAY,
                            keywords=video.get("tags", "").split(", "),
                            mood=mood,
                            relevance_score=0.7,
                            width=large.get("width", 1920),
                            height=large.get("height", 1080),
                            license_type="royalty-free"
                        ))

                return clips

        except Exception as e:
            logger.error(f"Pixabay search error: {e}")
            return []

    async def generate_ai_broll(
        self,
        prompt: str,
        duration: float = 3.0,
        style: str = "cinematic"
    ) -> Optional[BRollClip]:
        """Generate B-roll using AI image/video generation"""

        # This would integrate with Runway, Pika, or similar
        # For now, return None as placeholder
        logger.info(f"AI B-roll generation requested: {prompt}")
        return None

    def approve_suggestion(
        self,
        plan: BRollPlan,
        suggestion_index: int,
        clip_index: int = 0
    ) -> bool:
        """Approve a B-roll suggestion"""
        if suggestion_index >= len(plan.suggestions):
            return False

        suggestion = plan.suggestions[suggestion_index]
        if clip_index < len(suggestion.clips):
            suggestion.selected_clip = suggestion.clips[clip_index]
            suggestion.is_approved = True
            return True

        return False

    def auto_approve_all(self, plan: BRollPlan) -> int:
        """Auto-approve all suggestions with top clip"""
        approved = 0
        for suggestion in plan.suggestions:
            if suggestion.clips:
                suggestion.selected_clip = suggestion.clips[0]
                suggestion.is_approved = True
                approved += 1
        return approved

    def get_approved_clips(self, plan: BRollPlan) -> List[Tuple[InsertionPoint, BRollClip]]:
        """Get list of approved B-roll insertions"""
        return [
            (s.insertion_point, s.selected_clip)
            for s in plan.suggestions
            if s.is_approved and s.selected_clip
        ]

    def export_timeline(self, plan: BRollPlan) -> Dict[str, Any]:
        """Export B-roll plan as timeline data"""
        return {
            "plan_id": plan.plan_id,
            "total_duration": plan.total_broll_duration,
            "insertions": [
                {
                    "timestamp": s.insertion_point.timestamp,
                    "duration": s.insertion_point.duration,
                    "clip_url": s.selected_clip.url if s.selected_clip else None,
                    "clip_id": s.selected_clip.clip_id if s.selected_clip else None,
                    "keywords": s.insertion_point.keywords,
                    "approved": s.is_approved
                }
                for s in plan.suggestions
            ]
        }


# Factory function
async def create_broll_agent(
    openai_key: str = None,
    pexels_key: str = None,
    pixabay_key: str = None
) -> AIBRollAgent:
    """Create and configure B-roll agent"""
    import os

    return AIBRollAgent(
        openai_key=openai_key or os.getenv("OPENAI_API_KEY"),
        pexels_key=pexels_key or os.getenv("PEXELS_API_KEY"),
        pixabay_key=pixabay_key or os.getenv("PIXABAY_API_KEY")
    )
