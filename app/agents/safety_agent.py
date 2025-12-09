"""
Safety & Compliance Agent

Content moderation and compliance:
- Content moderation
- Copyright detection
- AI labeling
- Platform compliance
"""

import logging
from typing import Any
import os

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class SafetyComplianceAgent(BaseAgent):
    """
    Safety & Compliance Agent for content moderation.

    Ensures content meets platform guidelines and legal requirements.
    """

    # Content categories to check
    SAFETY_CATEGORIES = [
        "violence",
        "hate_speech",
        "adult_content",
        "dangerous_activities",
        "misinformation",
        "copyright",
        "spam",
        "harassment",
    ]

    def __init__(self):
        super().__init__(
            agent_type=AgentType.SAFETY,
            priority=AgentPriority.CRITICAL,
            parallel_capable=False,  # Must run before export
        )

    @property
    def name(self) -> str:
        return "Safety & Compliance Agent"

    @property
    def models(self) -> list[str]:
        return ["Content Moderation API", "Copyright Detection"]

    @property
    def capabilities(self) -> list[str]:
        return [
            "content moderation",
            "copyright detection",
            "AI content labeling",
            "platform compliance check",
            "age restriction detection",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Check content for safety and compliance."""

        context = task.context
        parameters = task.parameters

        prompt = task.prompt
        platforms = context.get("platforms", ["tiktok"])
        content_analysis = context.get("content_analysis", {})

        logger.info("Running safety and compliance checks...")

        try:
            safety_report = await self._check_safety(
                prompt=prompt,
                platforms=platforms,
                content_analysis=content_analysis,
                context=context,
            )

            # Determine if content is safe to publish
            is_safe = safety_report.get("overall_safe", True)

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success" if is_safe else "warning",
                output=safety_report,
                metadata={
                    "is_safe": is_safe,
                    "flags_count": len(safety_report.get("flags", [])),
                    "platforms_checked": platforms,
                },
            )

        except Exception as e:
            logger.error(f"Safety check error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _check_safety(
        self,
        prompt: str,
        platforms: list[str],
        content_analysis: dict,
        context: dict,
    ) -> dict:
        """Perform comprehensive safety checks."""

        flags = []
        warnings = []

        # Check for problematic keywords
        problematic_keywords = {
            "violence": ["kill", "murder", "attack", "weapon", "gun", "bomb"],
            "hate_speech": ["hate", "racist", "slur"],
            "adult_content": ["nsfw", "explicit", "nude"],
            "dangerous": ["challenge", "dangerous", "don't try"],
            "misinformation": ["fake", "hoax", "conspiracy"],
        }

        text_to_check = f"{prompt} {' '.join(content_analysis.get('keywords', []))}".lower()

        for category, keywords in problematic_keywords.items():
            for keyword in keywords:
                if keyword in text_to_check:
                    flags.append({
                        "category": category,
                        "keyword": keyword,
                        "severity": "high" if category in ["violence", "hate_speech"] else "medium",
                    })

        # Platform-specific compliance checks
        platform_issues = []
        for platform in platforms:
            issues = self._check_platform_compliance(platform, content_analysis)
            platform_issues.extend(issues)

        # AI content labeling requirement
        ai_label_required = True  # Most platforms now require AI disclosure

        # Copyright check (simplified)
        music_info = context.get("music_generation", {})
        if music_info:
            # AI-generated music is typically safe
            warnings.append("Music is AI-generated - no copyright issues expected")

        # Calculate overall safety
        high_severity_flags = [f for f in flags if f.get("severity") == "high"]
        overall_safe = len(high_severity_flags) == 0

        return {
            "overall_safe": overall_safe,
            "flags": flags,
            "warnings": warnings,
            "platform_issues": platform_issues,
            "ai_label_required": ai_label_required,
            "age_restriction": "none" if overall_safe else "13+",
            "recommendations": self._get_recommendations(flags, platform_issues),
            "compliance_score": 100 - (len(flags) * 10) - (len(platform_issues) * 5),
        }

    def _check_platform_compliance(
        self,
        platform: str,
        content_analysis: dict,
    ) -> list:
        """Check platform-specific compliance."""

        issues = []

        # Platform-specific rules
        platform_rules = {
            "tiktok": {
                "max_hashtags": 30,
                "required_disclosures": ["ai_generated", "sponsored"],
            },
            "instagram_reels": {
                "max_hashtags": 30,
                "required_disclosures": ["ai_generated", "sponsored"],
            },
            "youtube_shorts": {
                "max_hashtags": 15,
                "required_disclosures": ["ai_generated"],
            },
            "twitter": {
                "max_hashtags": 10,
                "required_disclosures": ["ai_generated"],
            },
        }

        rules = platform_rules.get(platform, {})

        # Check hashtag count
        hashtags = content_analysis.get("hashtags", [])
        max_hashtags = rules.get("max_hashtags", 30)
        if len(hashtags) > max_hashtags:
            issues.append({
                "platform": platform,
                "issue": f"Too many hashtags ({len(hashtags)} > {max_hashtags})",
                "severity": "low",
            })

        return issues

    def _get_recommendations(self, flags: list, platform_issues: list) -> list:
        """Generate safety recommendations."""

        recommendations = []

        if flags:
            recommendations.append("Review flagged content before publishing")

            categories = set(f["category"] for f in flags)
            if "violence" in categories:
                recommendations.append("Remove or modify violent content")
            if "hate_speech" in categories:
                recommendations.append("Remove potentially offensive language")

        if platform_issues:
            recommendations.append("Address platform-specific compliance issues")

        # Always recommend AI disclosure
        recommendations.append("Add AI-generated content disclosure as required by platforms")

        return recommendations
