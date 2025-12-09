"""
Analytics Agent - ENHANCED

Content performance analysis with VIRALITY SCORING:
- Virality Score prediction (0-100)
- Performance prediction
- A/B testing suggestions
- Engagement analysis
- Trend detection
- Optimal posting times
- Competitor benchmarking
"""

import logging
from typing import Any, Dict, List
import os
import re
from datetime import datetime, timedelta

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class AnalyticsAgent(BaseAgent):
    """
    Analytics Agent for content performance analysis.
    
    UNIQUE FEATURE: Virality Score - AI prediction of video viral potential
    Similar to Opus Clip's virality prediction but more comprehensive.
    """

    # Trending topics database (would be updated from API in production)
    TRENDING_TOPICS = {
        "tiktok": ["asmr", "storytime", "grwm", "ootd", "haul", "challenge", "duet", "pov", "transition"],
        "instagram": ["reels", "aesthetic", "lifestyle", "travel", "food", "fashion", "fitness"],
        "youtube": ["shorts", "tutorial", "review", "vlog", "gaming", "reaction", "explained"],
        "twitter": ["thread", "breaking", "news", "meme", "viral", "trending"],
    }

    # Viral trigger words that boost engagement
    VIRAL_TRIGGERS = [
        "secret", "hack", "never", "always", "shocking", "unbelievable", 
        "you won't believe", "nobody talks about", "stop scrolling",
        "wait for it", "game changer", "life hack", "must watch",
        "don't miss", "breaking", "exclusive", "revealed", "exposed",
        "finally", "truth about", "why nobody", "how i", "mistake",
    ]

    # Hook patterns that perform well
    HOOK_PATTERNS = [
        r"^(did you know|have you ever|what if|imagine|picture this)",
        r"^(stop|wait|hold on|listen|attention)",
        r"^(the secret|the truth|the reason|the problem)",
        r"^(i can't believe|i never thought|i was today years old)",
        r"^(here's (why|how|what)|this is (why|how|what))",
    ]

    def __init__(self):
        super().__init__(
            agent_type=AgentType.ANALYTICS,
            priority=AgentPriority.MEDIUM,
            parallel_capable=True,
        )

    @property
    def name(self) -> str:
        return "Analytics Agent"

    @property
    def models(self) -> list[str]:
        return ["Claude-3.5-Sonnet", "GPT-4o", "Virality-ML-v1"]

    @property
    def capabilities(self) -> list[str]:
        return [
            "virality score prediction",
            "performance prediction",
            "A/B testing suggestions",
            "engagement analysis",
            "trend detection",
            "optimal posting time",
            "competitor benchmarking",
            "hashtag optimization",
            "hook strength analysis",
            "retention prediction",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Analyze content for performance prediction."""

        context = task.context
        parameters = task.parameters

        prompt = task.prompt
        platforms = context.get("platforms", ["tiktok"])
        content_analysis = context.get("content_analysis", {})

        logger.info("Analyzing content performance potential...")

        try:
            # Generate comprehensive virality analysis
            virality_analysis = await self._calculate_virality_score(
                prompt=prompt,
                platforms=platforms,
                content_analysis=content_analysis,
            )

            # Generate performance prediction
            performance = await self._analyze_performance(
                prompt=prompt,
                platforms=platforms,
                content_analysis=content_analysis,
                virality_score=virality_analysis["virality_score"],
            )

            # Combine results
            analysis = {
                **virality_analysis,
                **performance,
            }

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=analysis,
                metadata={
                    "platforms": platforms,
                    "virality_score": analysis["virality_score"],
                    "predicted_performance": analysis["predicted_performance"],
                },
            )

        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _calculate_virality_score(
        self,
        prompt: str,
        platforms: list[str],
        content_analysis: dict,
    ) -> dict:
        """
        Calculate Virality Score (0-100) based on multiple factors.
        
        This is our UNIQUE feature that competitors like Opus Clip have.
        """

        scores = {
            "hook_strength": 0,
            "trend_alignment": 0,
            "emotional_triggers": 0,
            "format_optimization": 0,
            "hashtag_strategy": 0,
            "timing_potential": 0,
            "engagement_hooks": 0,
            "shareability": 0,
        }

        prompt_lower = prompt.lower()
        hook = content_analysis.get("hook", prompt[:100])
        keywords = content_analysis.get("keywords", [])
        hashtags = content_analysis.get("hashtags", [])
        mood = content_analysis.get("mood", "neutral")
        duration = content_analysis.get("duration_suggestion", 30)

        # 1. Hook Strength Analysis (0-15)
        hook_score = 0
        hook_lower = hook.lower()
        
        # Check for viral trigger words
        for trigger in self.VIRAL_TRIGGERS:
            if trigger in hook_lower:
                hook_score += 3
        
        # Check for hook patterns
        for pattern in self.HOOK_PATTERNS:
            if re.match(pattern, hook_lower):
                hook_score += 5
                break
        
        # Question hooks perform well
        if "?" in hook[:50]:
            hook_score += 3
        
        # Direct address ("you") increases engagement
        if "you" in hook_lower[:30]:
            hook_score += 2
        
        scores["hook_strength"] = min(hook_score, 15)

        # 2. Trend Alignment (0-15)
        trend_score = 0
        for platform in platforms:
            trending = self.TRENDING_TOPICS.get(platform, [])
            for topic in trending:
                if topic in prompt_lower:
                    trend_score += 3
        scores["trend_alignment"] = min(trend_score, 15)

        # 3. Emotional Triggers (0-15)
        emotional_words = {
            "positive": ["amazing", "incredible", "love", "best", "perfect", "beautiful", "awesome"],
            "curiosity": ["secret", "hidden", "unknown", "mystery", "revealed", "discover"],
            "urgency": ["now", "today", "immediately", "hurry", "limited", "last chance"],
            "fear": ["warning", "danger", "mistake", "avoid", "never", "wrong"],
        }
        
        emotion_score = 0
        for category, words in emotional_words.items():
            for word in words:
                if word in prompt_lower:
                    emotion_score += 2
        scores["emotional_triggers"] = min(emotion_score, 15)

        # 4. Format Optimization (0-10)
        format_score = 5  # Base score
        
        # Optimal duration for short-form
        if 15 <= duration <= 60:
            format_score += 3
        elif duration < 15:
            format_score += 1
        
        # Vertical format assumption for short-form
        format_score += 2
        
        scores["format_optimization"] = min(format_score, 10)

        # 5. Hashtag Strategy (0-10)
        hashtag_score = 0
        if hashtags:
            # Mix of popular and niche hashtags
            if 5 <= len(hashtags) <= 10:
                hashtag_score += 5
            elif len(hashtags) > 0:
                hashtag_score += 2
            
            # Check for platform-specific hashtags
            platform_tags = ["fyp", "foryou", "viral", "trending", "reels", "shorts"]
            if any(tag.lower().replace("#", "") in platform_tags for tag in hashtags):
                hashtag_score += 3
        
        scores["hashtag_strategy"] = min(hashtag_score, 10)

        # 6. Timing Potential (0-10)
        # Based on content type and current trends
        timing_score = 5  # Base - would use real-time data in production
        
        # Evergreen content scores higher
        evergreen_topics = ["how to", "tutorial", "tips", "guide", "learn"]
        if any(topic in prompt_lower for topic in evergreen_topics):
            timing_score += 3
        
        scores["timing_potential"] = min(timing_score, 10)

        # 7. Engagement Hooks (0-15)
        engagement_score = 0
        
        # Call to action presence
        cta_phrases = ["comment", "share", "follow", "like", "subscribe", "save", "try this"]
        for cta in cta_phrases:
            if cta in prompt_lower:
                engagement_score += 2
        
        # Question prompts engagement
        if "?" in prompt:
            engagement_score += 3
        
        # Controversial or debate-worthy content
        debate_words = ["unpopular opinion", "hot take", "controversial", "debate"]
        if any(word in prompt_lower for word in debate_words):
            engagement_score += 4
        
        scores["engagement_hooks"] = min(engagement_score, 15)

        # 8. Shareability (0-10)
        share_score = 0
        
        # Relatable content
        relatable_phrases = ["when you", "that moment", "pov:", "me when", "everyone"]
        for phrase in relatable_phrases:
            if phrase in prompt_lower:
                share_score += 3
        
        # Educational/valuable content
        value_words = ["learn", "teach", "tip", "hack", "secret", "how to"]
        if any(word in prompt_lower for word in value_words):
            share_score += 3
        
        # Entertaining content
        entertainment_words = ["funny", "hilarious", "comedy", "joke", "prank"]
        if any(word in prompt_lower for word in entertainment_words):
            share_score += 2
        
        scores["shareability"] = min(share_score, 10)

        # Calculate total virality score
        total_score = sum(scores.values())
        max_possible = 100
        virality_score = min(total_score, max_possible)

        # Determine virality tier
        if virality_score >= 80:
            virality_tier = "VIRAL POTENTIAL 🔥"
            virality_emoji = "🔥"
        elif virality_score >= 60:
            virality_tier = "HIGH POTENTIAL ⚡"
            virality_emoji = "⚡"
        elif virality_score >= 40:
            virality_tier = "GOOD POTENTIAL 👍"
            virality_emoji = "👍"
        elif virality_score >= 20:
            virality_tier = "MODERATE 📊"
            virality_emoji = "📊"
        else:
            virality_tier = "NEEDS IMPROVEMENT 🔧"
            virality_emoji = "🔧"

        # Generate improvement suggestions
        improvements = []
        if scores["hook_strength"] < 10:
            improvements.append("Strengthen your hook with a viral trigger word or pattern")
        if scores["trend_alignment"] < 8:
            improvements.append("Align content with current trending topics")
        if scores["emotional_triggers"] < 8:
            improvements.append("Add emotional triggers to increase engagement")
        if scores["hashtag_strategy"] < 6:
            improvements.append("Optimize hashtag strategy (5-10 mixed hashtags)")
        if scores["engagement_hooks"] < 8:
            improvements.append("Add a clear call-to-action")
        if scores["shareability"] < 6:
            improvements.append("Make content more relatable or valuable to increase shares")

        return {
            "virality_score": virality_score,
            "virality_tier": virality_tier,
            "virality_emoji": virality_emoji,
            "score_breakdown": scores,
            "max_score": max_possible,
            "improvement_suggestions": improvements,
            "viral_potential_percentage": f"{virality_score}%",
        }

    async def _analyze_performance(
        self,
        prompt: str,
        platforms: list[str],
        content_analysis: dict,
        virality_score: int,
    ) -> dict:
        """Analyze and predict content performance."""

        keywords = content_analysis.get("keywords", [])
        mood = content_analysis.get("mood", "neutral")
        hashtags = content_analysis.get("hashtags", [])
        hook = content_analysis.get("hook", "")

        # Generate recommendations based on virality score
        recommendations = []
        
        if virality_score < 40:
            recommendations.extend([
                "Consider a more attention-grabbing hook",
                "Add trending sounds or music",
                "Include a surprise element or twist",
            ])
        elif virality_score < 70:
            recommendations.extend([
                "Optimize posting time for your audience",
                "Test different thumbnail styles",
                "Add text overlays for silent viewing",
            ])
        else:
            recommendations.extend([
                "Great content! Consider cross-posting to multiple platforms",
                "Prepare follow-up content to capitalize on potential virality",
                "Engage with early comments to boost algorithm",
            ])

        # Best posting times by platform
        best_times = {
            "tiktok": {
                "best": ["7 PM - 9 PM", "12 PM - 1 PM"],
                "good": ["9 AM - 11 AM", "3 PM - 5 PM"],
                "timezone": "Local time",
            },
            "instagram": {
                "best": ["11 AM - 1 PM", "7 PM - 9 PM"],
                "good": ["9 AM - 10 AM", "2 PM - 3 PM"],
                "timezone": "Local time",
            },
            "youtube_shorts": {
                "best": ["2 PM - 4 PM", "8 PM - 10 PM"],
                "good": ["12 PM - 2 PM", "6 PM - 8 PM"],
                "timezone": "Local time",
            },
            "twitter": {
                "best": ["9 AM - 11 AM", "1 PM - 3 PM"],
                "good": ["8 AM - 9 AM", "5 PM - 6 PM"],
                "timezone": "Local time",
            },
        }

        # Predicted metrics based on virality score
        base_views = 1000
        multiplier = virality_score / 20  # 0-5x multiplier
        
        predicted_metrics = {
            "estimated_views": int(base_views * multiplier * (1 + len(platforms) * 0.5)),
            "estimated_likes": int(base_views * multiplier * 0.08),
            "estimated_comments": int(base_views * multiplier * 0.02),
            "estimated_shares": int(base_views * multiplier * 0.01),
            "estimated_saves": int(base_views * multiplier * 0.03),
        }

        # A/B test suggestions
        ab_suggestions = [
            {
                "element": "Hook",
                "variant_a": hook[:50] if hook else "Current hook",
                "variant_b": f"POV: {prompt[:30]}..." if "pov" not in prompt.lower() else f"Wait for it: {prompt[:30]}...",
                "hypothesis": "Testing attention-grabbing hook styles",
            },
            {
                "element": "Music",
                "variant_a": f"{mood} mood music",
                "variant_b": "Trending sound",
                "hypothesis": "Testing original vs trending audio impact",
            },
            {
                "element": "Duration",
                "variant_a": "15-30 seconds",
                "variant_b": "45-60 seconds",
                "hypothesis": "Testing optimal video length",
            },
        ]

        # Performance prediction
        if virality_score >= 70:
            predicted_performance = "HIGH"
            confidence = "85%"
        elif virality_score >= 50:
            predicted_performance = "MEDIUM-HIGH"
            confidence = "70%"
        elif virality_score >= 30:
            predicted_performance = "MEDIUM"
            confidence = "60%"
        else:
            predicted_performance = "LOW-MEDIUM"
            confidence = "50%"

        return {
            "predicted_performance": predicted_performance,
            "confidence": confidence,
            "recommendations": recommendations,
            "best_posting_times": {p: best_times.get(p, best_times["tiktok"]) for p in platforms},
            "predicted_metrics": predicted_metrics,
            "ab_test_suggestions": ab_suggestions,
            "retention_prediction": {
                "hook_retention": f"{min(95, 50 + virality_score * 0.5):.0f}%",
                "mid_video_retention": f"{min(80, 40 + virality_score * 0.4):.0f}%",
                "completion_rate": f"{min(70, 30 + virality_score * 0.4):.0f}%",
            },
        }

    async def benchmark_against_competitors(
        self,
        content_metrics: dict,
        niche: str,
    ) -> dict:
        """Benchmark content against competitor averages in the niche."""
        
        # Industry benchmarks (would be from real data in production)
        benchmarks = {
            "general": {"avg_views": 5000, "avg_engagement": 5.0},
            "education": {"avg_views": 8000, "avg_engagement": 6.5},
            "entertainment": {"avg_views": 15000, "avg_engagement": 7.0},
            "business": {"avg_views": 3000, "avg_engagement": 4.5},
            "lifestyle": {"avg_views": 10000, "avg_engagement": 6.0},
        }
        
        niche_benchmark = benchmarks.get(niche, benchmarks["general"])
        
        return {
            "niche": niche,
            "your_metrics": content_metrics,
            "niche_average": niche_benchmark,
            "performance_vs_average": {
                "views": f"{(content_metrics.get('views', 0) / niche_benchmark['avg_views'] * 100):.0f}%",
                "engagement": f"{(content_metrics.get('engagement', 0) / niche_benchmark['avg_engagement'] * 100):.0f}%",
            },
        }
