"""
Virality Prediction Agent
=========================

AI-powered viral potential scoring system inspired by Opus Clip.
Analyzes content to predict social media performance.

Features:
1. Virality Score (1-100) - Overall viral potential
2. Hook Analysis - Opening strength assessment
3. Engagement Prediction - Likes, comments, shares forecast
4. Platform-Specific Scoring - TikTok, Instagram, YouTube, Twitter
5. Content Analysis - Trend alignment, emotional impact
6. Timing Recommendations - Best posting times
7. Hashtag Suggestions - Optimized for reach
8. Thumbnail Effectiveness - Click-through prediction
9. Caption Optimization - Engagement-boosting text
10. A/B Testing Suggestions - Variations to test
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class Platform(Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    THREADS = "threads"
    TELEGRAM = "telegram"


class ContentCategory(Enum):
    MOTIVATION = "motivation"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    LIFESTYLE = "lifestyle"
    BUSINESS = "business"
    TECH = "tech"
    FITNESS = "fitness"
    FOOD = "food"
    TRAVEL = "travel"
    COMEDY = "comedy"
    NEWS = "news"
    GAMING = "gaming"
    MUSIC = "music"
    ART = "art"
    OTHER = "other"


@dataclass
class HookAnalysis:
    """Analysis of the video's opening hook"""
    hook_strength: float  # 0-100
    attention_capture_time: float  # seconds
    hook_type: str  # question, statement, visual, sound, etc.
    improvement_suggestions: List[str] = field(default_factory=list)
    example_hooks: List[str] = field(default_factory=list)


@dataclass
class EngagementPrediction:
    """Predicted engagement metrics"""
    views_estimate: Tuple[int, int]  # min, max range
    likes_rate: float  # percentage of views
    comments_rate: float
    shares_rate: float
    saves_rate: float
    watch_time_percentage: float  # avg % of video watched
    replay_rate: float  # % who watch again


@dataclass
class PlatformScore:
    """Platform-specific virality score"""
    platform: Platform
    score: float  # 0-100
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    optimizations: List[str] = field(default_factory=list)
    best_posting_times: List[str] = field(default_factory=list)
    hashtag_recommendations: List[str] = field(default_factory=list)


@dataclass
class ViralityReport:
    """Complete virality analysis report"""
    # Core Scores
    overall_score: float  # 0-100, the main virality score
    confidence: float  # 0-1, how confident the prediction is

    # Breakdown
    hook_analysis: HookAnalysis
    engagement_prediction: EngagementPrediction
    platform_scores: Dict[Platform, PlatformScore] = field(default_factory=dict)

    # Content Analysis
    category: ContentCategory = ContentCategory.OTHER
    trending_alignment: float = 0.0  # 0-100
    emotional_impact: float = 0.0  # 0-100
    originality: float = 0.0  # 0-100
    production_quality: float = 0.0  # 0-100

    # Recommendations
    title_suggestions: List[str] = field(default_factory=list)
    caption_suggestions: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    thumbnail_suggestions: List[str] = field(default_factory=list)
    music_suggestions: List[str] = field(default_factory=list)
    ab_test_ideas: List[str] = field(default_factory=list)

    # Meta
    analysis_timestamp: datetime = field(default_factory=datetime.utcnow)
    model_version: str = "1.0.0"


class ViralityAgent:
    """
    AI Agent for predicting viral potential of video content.

    Uses multi-model analysis combining:
    - GPT-4 for content understanding
    - Claude for nuanced analysis
    - Custom ML models for engagement prediction
    - Historical data for trend analysis
    """

    def __init__(
        self,
        openai_client=None,
        anthropic_client=None,
        historical_data_path: str = None
    ):
        self.openai = openai_client
        self.anthropic = anthropic_client
        self.historical_data_path = historical_data_path
        self.model_version = "1.0.0"

        # Platform-specific weights for scoring
        self.platform_weights = {
            Platform.TIKTOK: {
                "hook_weight": 0.35,
                "trend_weight": 0.25,
                "music_weight": 0.20,
                "originality_weight": 0.20
            },
            Platform.INSTAGRAM: {
                "hook_weight": 0.25,
                "visual_weight": 0.30,
                "trend_weight": 0.25,
                "hashtag_weight": 0.20
            },
            Platform.YOUTUBE: {
                "thumbnail_weight": 0.30,
                "title_weight": 0.25,
                "content_depth_weight": 0.25,
                "engagement_weight": 0.20
            },
            Platform.TWITTER: {
                "hook_weight": 0.30,
                "controversy_weight": 0.20,
                "timing_weight": 0.25,
                "hashtag_weight": 0.25
            }
        }

        # Trending topics cache
        self.trending_topics: Dict[Platform, List[str]] = {}

    async def analyze(
        self,
        video_path: str = None,
        script: str = None,
        title: str = None,
        description: str = None,
        duration_seconds: int = None,
        target_platforms: List[Platform] = None,
        category: ContentCategory = None,
        music_info: Dict[str, Any] = None
    ) -> ViralityReport:
        """
        Analyze content and generate virality prediction.

        Args:
            video_path: Path to video file
            script: Video script/transcript
            title: Video title
            description: Video description
            duration_seconds: Video duration
            target_platforms: Platforms to analyze for
            category: Content category
            music_info: Music/audio information

        Returns:
            ViralityReport with complete analysis
        """
        target_platforms = target_platforms or [Platform.TIKTOK, Platform.INSTAGRAM]

        # Run all analyses in parallel
        analyses = await asyncio.gather(
            self._analyze_hook(script, video_path),
            self._analyze_content(script, title, description, category),
            self._predict_engagement(script, title, duration_seconds),
            self._analyze_trending_alignment(script, title, target_platforms),
            self._generate_recommendations(script, title, target_platforms)
        )

        hook_analysis, content_analysis, engagement, trending, recommendations = analyses

        # Calculate platform-specific scores
        platform_scores = {}
        for platform in target_platforms:
            platform_scores[platform] = await self._calculate_platform_score(
                platform=platform,
                hook_analysis=hook_analysis,
                content_analysis=content_analysis,
                engagement=engagement,
                trending=trending
            )

        # Calculate overall score (weighted average of platforms)
        overall_score = sum(ps.score for ps in platform_scores.values()) / len(platform_scores)

        # Build report
        report = ViralityReport(
            overall_score=overall_score,
            confidence=self._calculate_confidence(platform_scores),
            hook_analysis=hook_analysis,
            engagement_prediction=engagement,
            platform_scores=platform_scores,
            category=category or ContentCategory.OTHER,
            trending_alignment=trending.get("alignment_score", 0),
            emotional_impact=content_analysis.get("emotional_impact", 0),
            originality=content_analysis.get("originality", 0),
            production_quality=content_analysis.get("production_quality", 0),
            title_suggestions=recommendations.get("titles", []),
            caption_suggestions=recommendations.get("captions", []),
            hashtags=recommendations.get("hashtags", []),
            thumbnail_suggestions=recommendations.get("thumbnails", []),
            music_suggestions=recommendations.get("music", []),
            ab_test_ideas=recommendations.get("ab_tests", [])
        )

        return report

    async def _analyze_hook(
        self,
        script: str = None,
        video_path: str = None
    ) -> HookAnalysis:
        """Analyze the opening hook of the content"""

        if self.openai:
            try:
                prompt = f"""Analyze the opening hook of this video content.

Script/Transcript:
{script[:500] if script else "Not provided"}

Rate the hook on these criteria:
1. Hook Strength (0-100): How compelling is the opening?
2. Attention Capture Time: How many seconds to capture attention?
3. Hook Type: What technique is used? (question, bold statement, visual surprise, sound, emotion, curiosity gap)

Provide:
- 3 specific suggestions to improve the hook
- 3 example hooks that would work better

Respond in JSON format:
{{
    "hook_strength": 0-100,
    "attention_capture_time": seconds,
    "hook_type": "type",
    "improvement_suggestions": ["suggestion1", "suggestion2", "suggestion3"],
    "example_hooks": ["hook1", "hook2", "hook3"]
}}"""

                response = await self.openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                import json
                result = json.loads(response.choices[0].message.content)

                return HookAnalysis(
                    hook_strength=result.get("hook_strength", 50),
                    attention_capture_time=result.get("attention_capture_time", 3.0),
                    hook_type=result.get("hook_type", "unknown"),
                    improvement_suggestions=result.get("improvement_suggestions", []),
                    example_hooks=result.get("example_hooks", [])
                )
            except Exception as e:
                logger.error(f"Hook analysis error: {e}")

        # Fallback analysis
        return HookAnalysis(
            hook_strength=50.0,
            attention_capture_time=3.0,
            hook_type="unknown",
            improvement_suggestions=[
                "Start with a question to engage viewers",
                "Use a bold statement in the first 2 seconds",
                "Add a visual hook or surprising element"
            ],
            example_hooks=[
                "You won't believe what happens next...",
                "Here's what nobody tells you about...",
                "Stop scrolling if you want to learn..."
            ]
        )

    async def _analyze_content(
        self,
        script: str,
        title: str,
        description: str,
        category: ContentCategory
    ) -> Dict[str, Any]:
        """Analyze content quality and characteristics"""

        if self.anthropic:
            try:
                import anthropic

                prompt = f"""Analyze this video content:

Title: {title or "Not provided"}
Description: {description or "Not provided"}
Category: {category.value if category else "unknown"}
Script: {script[:1000] if script else "Not provided"}

Provide scores (0-100) for:
1. Emotional Impact: How emotionally engaging is this content?
2. Originality: How unique/fresh is this content?
3. Production Quality Indicators: Based on script, how polished does this seem?
4. Educational Value: How informative is this?
5. Entertainment Value: How entertaining is this?

Respond in JSON:
{{
    "emotional_impact": 0-100,
    "originality": 0-100,
    "production_quality": 0-100,
    "educational_value": 0-100,
    "entertainment_value": 0-100,
    "key_themes": ["theme1", "theme2"],
    "target_audience": "description of ideal audience"
}}"""

                response = await self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )

                import json
                import re
                content = response.content[0].text
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    return json.loads(json_match.group())

            except Exception as e:
                logger.error(f"Content analysis error: {e}")

        return {
            "emotional_impact": 50,
            "originality": 50,
            "production_quality": 50,
            "educational_value": 50,
            "entertainment_value": 50
        }

    async def _predict_engagement(
        self,
        script: str,
        title: str,
        duration_seconds: int
    ) -> EngagementPrediction:
        """Predict engagement metrics"""

        # Base engagement rates by duration (TikTok-style short form)
        if duration_seconds:
            if duration_seconds <= 15:
                base_watch_rate = 85
                base_engagement_multiplier = 1.2
            elif duration_seconds <= 30:
                base_watch_rate = 70
                base_engagement_multiplier = 1.0
            elif duration_seconds <= 60:
                base_watch_rate = 55
                base_engagement_multiplier = 0.9
            else:
                base_watch_rate = 40
                base_engagement_multiplier = 0.7
        else:
            base_watch_rate = 60
            base_engagement_multiplier = 1.0

        # Industry average rates (adjusted by multiplier)
        return EngagementPrediction(
            views_estimate=(1000, 100000),  # Very rough estimate
            likes_rate=5.0 * base_engagement_multiplier,  # ~5% of views
            comments_rate=0.5 * base_engagement_multiplier,  # ~0.5% of views
            shares_rate=1.0 * base_engagement_multiplier,  # ~1% of views
            saves_rate=2.0 * base_engagement_multiplier,  # ~2% of views
            watch_time_percentage=base_watch_rate,
            replay_rate=15.0 * base_engagement_multiplier  # ~15% replay
        )

    async def _analyze_trending_alignment(
        self,
        script: str,
        title: str,
        platforms: List[Platform]
    ) -> Dict[str, Any]:
        """Analyze alignment with current trends"""

        # In production, this would fetch real trending data
        current_trends = {
            Platform.TIKTOK: [
                "AI tools", "productivity hacks", "morning routines",
                "money tips", "relationship advice", "outfit ideas"
            ],
            Platform.INSTAGRAM: [
                "aesthetic content", "reels transitions", "travel",
                "food content", "fitness transformations", "skincare"
            ],
            Platform.YOUTUBE: [
                "tutorials", "day in my life", "reviews",
                "challenges", "reactions", "educational"
            ],
            Platform.TWITTER: [
                "hot takes", "threads", "breaking news",
                "memes", "tech updates", "politics"
            ]
        }

        # Calculate alignment score (simplified)
        content_lower = f"{title or ''} {script or ''}".lower()
        alignment_scores = []

        for platform in platforms:
            platform_trends = current_trends.get(platform, [])
            matches = sum(1 for trend in platform_trends if trend.lower() in content_lower)
            score = min(100, (matches / max(len(platform_trends), 1)) * 200)
            alignment_scores.append(score)

        return {
            "alignment_score": sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0,
            "matching_trends": [],
            "suggested_trends": current_trends.get(platforms[0], [])[:5] if platforms else []
        }

    async def _generate_recommendations(
        self,
        script: str,
        title: str,
        platforms: List[Platform]
    ) -> Dict[str, List[str]]:
        """Generate optimization recommendations"""

        if self.openai:
            try:
                prompt = f"""Generate viral content recommendations for this video:

Title: {title or "Not provided"}
Platforms: {", ".join(p.value for p in platforms)}
Script excerpt: {script[:500] if script else "Not provided"}

Provide:
1. 3 alternative title options optimized for virality
2. 3 caption/description options
3. 10 relevant hashtags
4. 3 thumbnail concepts
5. 3 music/sound suggestions
6. 3 A/B test ideas

JSON format:
{{
    "titles": ["title1", "title2", "title3"],
    "captions": ["caption1", "caption2", "caption3"],
    "hashtags": ["tag1", "tag2", ...],
    "thumbnails": ["concept1", "concept2", "concept3"],
    "music": ["suggestion1", "suggestion2", "suggestion3"],
    "ab_tests": ["test1", "test2", "test3"]
}}"""

                response = await self.openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                import json
                return json.loads(response.choices[0].message.content)

            except Exception as e:
                logger.error(f"Recommendations error: {e}")

        # Fallback recommendations
        return {
            "titles": [
                f"You Need to See This: {title or 'Amazing Video'}",
                f"The Truth About {title or 'This Topic'}",
                f"Why Nobody Talks About {title or 'This'}"
            ],
            "captions": [
                "Save this for later 📌",
                "Comment if you agree 👇",
                "Share with someone who needs this 🔄"
            ],
            "hashtags": [
                "#fyp", "#viral", "#trending", "#foryou", "#foryoupage",
                "#explore", "#reels", "#content", "#creator", "#tips"
            ],
            "thumbnails": [
                "Surprised face with bold text overlay",
                "Before/after split screen",
                "Eye-catching color contrast with emoji"
            ],
            "music": [
                "Trending viral sound",
                "Upbeat energetic track",
                "Emotional piano for storytelling"
            ],
            "ab_tests": [
                "Test different opening hooks (question vs statement)",
                "Test with/without face in thumbnail",
                "Test different posting times"
            ]
        }

    async def _calculate_platform_score(
        self,
        platform: Platform,
        hook_analysis: HookAnalysis,
        content_analysis: Dict[str, Any],
        engagement: EngagementPrediction,
        trending: Dict[str, Any]
    ) -> PlatformScore:
        """Calculate platform-specific virality score"""

        weights = self.platform_weights.get(platform, {
            "hook_weight": 0.25,
            "content_weight": 0.25,
            "engagement_weight": 0.25,
            "trend_weight": 0.25
        })

        # Calculate weighted score
        hook_score = hook_analysis.hook_strength
        content_score = (
            content_analysis.get("emotional_impact", 50) +
            content_analysis.get("originality", 50) +
            content_analysis.get("production_quality", 50)
        ) / 3
        engagement_score = (engagement.likes_rate * 10 + engagement.watch_time_percentage) / 2
        trend_score = trending.get("alignment_score", 50)

        weighted_score = (
            hook_score * weights.get("hook_weight", 0.25) +
            content_score * weights.get("content_weight", 0.25) +
            engagement_score * weights.get("engagement_weight", 0.25) +
            trend_score * weights.get("trend_weight", 0.25)
        )

        # Platform-specific optimizations
        platform_optimizations = {
            Platform.TIKTOK: {
                "strengths": ["Short-form optimized", "Hook-focused"],
                "weaknesses": ["Needs trending sound", "Quick cuts required"],
                "optimizations": [
                    "Add trending TikTok sound",
                    "Use text overlays",
                    "Keep under 30 seconds",
                    "Add captions"
                ],
                "best_times": ["9am", "12pm", "7pm", "10pm"]
            },
            Platform.INSTAGRAM: {
                "strengths": ["Visual quality", "Aesthetic appeal"],
                "weaknesses": ["Needs strong visual hook", "Cover image crucial"],
                "optimizations": [
                    "Optimize first frame as cover",
                    "Use Instagram-native features",
                    "Add location tags",
                    "Use carousel format"
                ],
                "best_times": ["11am", "1pm", "5pm", "8pm"]
            },
            Platform.YOUTUBE: {
                "strengths": ["SEO potential", "Long-form value"],
                "weaknesses": ["Thumbnail critical", "Title must be searchable"],
                "optimizations": [
                    "Create click-worthy thumbnail",
                    "Optimize title for search",
                    "Add end screens",
                    "Include cards"
                ],
                "best_times": ["2pm", "4pm", "9pm"]
            },
            Platform.TWITTER: {
                "strengths": ["Conversation starter", "Shareable"],
                "weaknesses": ["Needs hook in first 3 seconds", "Text thread potential"],
                "optimizations": [
                    "Add engaging caption",
                    "Start a conversation",
                    "Quote tweet strategy",
                    "Timing with news"
                ],
                "best_times": ["8am", "12pm", "5pm", "9pm"]
            }
        }

        platform_data = platform_optimizations.get(platform, {})

        return PlatformScore(
            platform=platform,
            score=min(100, max(0, weighted_score)),
            strengths=platform_data.get("strengths", []),
            weaknesses=platform_data.get("weaknesses", []),
            optimizations=platform_data.get("optimizations", []),
            best_posting_times=platform_data.get("best_times", []),
            hashtag_recommendations=trending.get("suggested_trends", [])[:10]
        )

    def _calculate_confidence(self, platform_scores: Dict[Platform, PlatformScore]) -> float:
        """Calculate confidence in the prediction"""
        if not platform_scores:
            return 0.0

        # Higher confidence if scores are consistent across platforms
        scores = [ps.score for ps in platform_scores.values()]
        avg_score = sum(scores) / len(scores)
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)

        # Lower variance = higher confidence
        confidence = max(0.3, min(0.95, 1 - (variance / 1000)))
        return confidence

    def format_report(self, report: ViralityReport) -> str:
        """Format report as readable markdown"""

        def score_emoji(score: float) -> str:
            if score >= 80:
                return "🔥"
            elif score >= 60:
                return "✨"
            elif score >= 40:
                return "👍"
            else:
                return "📈"

        md = f"""# Virality Analysis Report

## Overall Score: {report.overall_score:.0f}/100 {score_emoji(report.overall_score)}
**Confidence:** {report.confidence * 100:.0f}%

---

## Hook Analysis

| Metric | Score |
|--------|-------|
| Hook Strength | {report.hook_analysis.hook_strength:.0f}/100 |
| Attention Capture | {report.hook_analysis.attention_capture_time:.1f}s |
| Hook Type | {report.hook_analysis.hook_type} |

**Improvement Suggestions:**
{chr(10).join(f"- {s}" for s in report.hook_analysis.improvement_suggestions)}

**Example Hooks:**
{chr(10).join(f'- "{h}"' for h in report.hook_analysis.example_hooks)}

---

## Engagement Prediction

| Metric | Predicted |
|--------|-----------|
| Views | {report.engagement_prediction.views_estimate[0]:,} - {report.engagement_prediction.views_estimate[1]:,} |
| Like Rate | {report.engagement_prediction.likes_rate:.1f}% |
| Comment Rate | {report.engagement_prediction.comments_rate:.1f}% |
| Share Rate | {report.engagement_prediction.shares_rate:.1f}% |
| Save Rate | {report.engagement_prediction.saves_rate:.1f}% |
| Avg Watch % | {report.engagement_prediction.watch_time_percentage:.0f}% |
| Replay Rate | {report.engagement_prediction.replay_rate:.0f}% |

---

## Platform Scores

"""
        for platform, score in report.platform_scores.items():
            md += f"""### {platform.value.title()} - {score.score:.0f}/100 {score_emoji(score.score)}

**Strengths:** {", ".join(score.strengths)}
**Areas to Improve:** {", ".join(score.weaknesses)}

**Optimizations:**
{chr(10).join(f"- {o}" for o in score.optimizations)}

**Best Posting Times:** {", ".join(score.best_posting_times)}

**Recommended Hashtags:** {" ".join(f"#{h}" for h in score.hashtag_recommendations[:5])}

"""

        md += f"""---

## Content Analysis

| Factor | Score |
|--------|-------|
| Trending Alignment | {report.trending_alignment:.0f}/100 |
| Emotional Impact | {report.emotional_impact:.0f}/100 |
| Originality | {report.originality:.0f}/100 |
| Production Quality | {report.production_quality:.0f}/100 |

---

## Recommendations

### Title Options
{chr(10).join(f"- {t}" for t in report.title_suggestions)}

### Caption Options
{chr(10).join(f"- {c}" for c in report.caption_suggestions)}

### Hashtags
{" ".join(f"#{h}" for h in report.hashtags)}

### Thumbnail Concepts
{chr(10).join(f"- {t}" for t in report.thumbnail_suggestions)}

### Music Suggestions
{chr(10).join(f"- {m}" for m in report.music_suggestions)}

### A/B Test Ideas
{chr(10).join(f"- {a}" for a in report.ab_test_ideas)}

---

*Analysis by Taj Chat Virality Agent v{report.model_version}*
*Generated: {report.analysis_timestamp.isoformat()}*
"""
        return md


# Standalone usage
if __name__ == "__main__":
    async def main():
        agent = ViralityAgent()

        report = await agent.analyze(
            script="Hey! You won't believe what I discovered about productivity. Most people waste 3 hours every day on this one mistake...",
            title="The #1 Productivity Mistake Everyone Makes",
            duration_seconds=45,
            target_platforms=[Platform.TIKTOK, Platform.INSTAGRAM, Platform.YOUTUBE],
            category=ContentCategory.EDUCATION
        )

        print(agent.format_report(report))

    asyncio.run(main())
