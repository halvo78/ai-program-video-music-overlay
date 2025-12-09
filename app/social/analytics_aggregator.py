"""
Social Media Analytics Aggregator
=================================

Unified analytics across all platforms:
- Cross-platform metrics
- Performance comparison
- Trend analysis
- Audience insights
- Content recommendations
"""

import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

from .meta_client import MetaClient
from .twitter_client import TwitterClient
from .tiktok_client import TikTokClient
from .youtube_client import YouTubeClient
from .instagram_client import InstagramClient

logger = logging.getLogger(__name__)


@dataclass
class PlatformMetrics:
    """Metrics for a single platform"""
    platform: str
    followers: int = 0
    following: int = 0
    total_posts: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    engagement_rate: float = 0.0
    avg_views_per_post: float = 0.0
    growth_rate: float = 0.0
    top_posts: List[Dict] = field(default_factory=list)
    demographics: Dict = field(default_factory=dict)
    best_posting_times: List[str] = field(default_factory=list)


@dataclass
class ContentPerformance:
    """Performance metrics for a piece of content"""
    content_id: str
    platform: str
    title: str
    published_at: datetime
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    engagement_rate: float = 0.0
    watch_time: float = 0.0  # seconds
    completion_rate: float = 0.0


@dataclass
class AggregatedMetrics:
    """Aggregated metrics across all platforms"""
    total_followers: int = 0
    total_views: int = 0
    total_engagement: int = 0
    overall_engagement_rate: float = 0.0
    platform_breakdown: Dict[str, PlatformMetrics] = field(default_factory=dict)
    top_performing_content: List[ContentPerformance] = field(default_factory=list)
    growth_trend: List[Dict] = field(default_factory=list)
    audience_overlap: Dict = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class AnalyticsAggregator:
    """
    Unified analytics aggregator for all social media platforms

    Features:
    1. Cross-platform metrics aggregation
    2. Performance comparison
    3. Trend analysis
    4. Audience demographics
    5. Content performance ranking
    6. Best posting time analysis
    7. Growth tracking
    8. Engagement analysis
    9. Content recommendations
    10. Export and reporting
    """

    def __init__(
        self,
        meta_client: MetaClient = None,
        twitter_client: TwitterClient = None,
        tiktok_client: TikTokClient = None,
        youtube_client: YouTubeClient = None,
        instagram_client: InstagramClient = None,
    ):
        self.meta = meta_client
        self.twitter = twitter_client
        self.tiktok = tiktok_client
        self.youtube = youtube_client
        self.instagram = instagram_client

        self._cache: Dict[str, Any] = {}
        self._cache_ttl = 300  # 5 minutes

    async def get_aggregated_metrics(
        self,
        days: int = 30,
    ) -> AggregatedMetrics:
        """
        Get aggregated metrics across all platforms

        Args:
            days: Number of days to analyze

        Returns:
            AggregatedMetrics with cross-platform data
        """
        # Fetch metrics from all platforms in parallel
        tasks = []

        if self.instagram:
            tasks.append(("instagram", self._get_instagram_metrics(days)))
        if self.twitter:
            tasks.append(("twitter", self._get_twitter_metrics(days)))
        if self.tiktok:
            tasks.append(("tiktok", self._get_tiktok_metrics(days)))
        if self.youtube:
            tasks.append(("youtube", self._get_youtube_metrics(days)))
        if self.meta:
            tasks.append(("facebook", self._get_facebook_metrics(days)))

        # Execute all fetches in parallel
        results = await asyncio.gather(
            *[task[1] for task in tasks],
            return_exceptions=True
        )

        # Process results
        platform_metrics = {}
        for i, (platform_name, _) in enumerate(tasks):
            if isinstance(results[i], Exception):
                logger.error(f"Failed to fetch {platform_name} metrics: {results[i]}")
            else:
                platform_metrics[platform_name] = results[i]

        # Aggregate metrics
        aggregated = AggregatedMetrics()
        aggregated.platform_breakdown = platform_metrics

        # Calculate totals
        for metrics in platform_metrics.values():
            aggregated.total_followers += metrics.followers
            aggregated.total_views += metrics.total_views
            aggregated.total_engagement += (
                metrics.total_likes +
                metrics.total_comments +
                metrics.total_shares
            )

        # Calculate overall engagement rate
        if aggregated.total_views > 0:
            aggregated.overall_engagement_rate = (
                aggregated.total_engagement / aggregated.total_views
            ) * 100

        # Collect top performing content
        all_content = []
        for metrics in platform_metrics.values():
            all_content.extend(metrics.top_posts)

        # Sort by engagement
        aggregated.top_performing_content = sorted(
            all_content,
            key=lambda x: x.get("engagement", 0),
            reverse=True
        )[:10]

        # Generate recommendations
        aggregated.recommendations = self._generate_recommendations(aggregated)

        return aggregated

    async def _get_instagram_metrics(self, days: int) -> PlatformMetrics:
        """Fetch Instagram metrics"""
        metrics = PlatformMetrics(platform="instagram")

        async with self.instagram:
            # Get account info
            account = await self.instagram.get_account_info()
            metrics.followers = account.get("followers_count", 0)
            metrics.following = account.get("follows_count", 0)
            metrics.total_posts = account.get("media_count", 0)

            # Get insights
            try:
                insights = await self.instagram.get_account_insights(
                    metrics="impressions,reach,profile_views",
                    period="day",
                )

                for metric in insights.get("data", []):
                    if metric["name"] == "impressions":
                        metrics.total_views = sum(v["value"] for v in metric.get("values", []))

            except Exception as e:
                logger.warning(f"Could not fetch Instagram insights: {e}")

            # Get recent media performance
            media = await self.instagram.get_media(limit=25)

            for item in media.get("data", []):
                metrics.total_likes += item.get("like_count", 0)
                metrics.total_comments += item.get("comments_count", 0)

                metrics.top_posts.append({
                    "id": item.get("id"),
                    "type": item.get("media_type"),
                    "likes": item.get("like_count", 0),
                    "comments": item.get("comments_count", 0),
                    "engagement": item.get("like_count", 0) + item.get("comments_count", 0),
                    "timestamp": item.get("timestamp"),
                })

            # Calculate engagement rate
            if metrics.followers > 0 and metrics.total_posts > 0:
                avg_engagement = (metrics.total_likes + metrics.total_comments) / min(metrics.total_posts, 25)
                metrics.engagement_rate = (avg_engagement / metrics.followers) * 100

        return metrics

    async def _get_twitter_metrics(self, days: int) -> PlatformMetrics:
        """Fetch Twitter metrics"""
        metrics = PlatformMetrics(platform="twitter")

        async with self.twitter:
            # Get user info
            user = await self.twitter.verify_credentials()
            user_data = user.get("data", {})
            public_metrics = user_data.get("public_metrics", {})

            metrics.followers = public_metrics.get("followers_count", 0)
            metrics.following = public_metrics.get("following_count", 0)
            metrics.total_posts = public_metrics.get("tweet_count", 0)

            # Get recent tweets
            user_id = user_data.get("id")
            if user_id:
                tweets = await self.twitter.get_user_tweets(user_id, max_results=25)

                for tweet in tweets.get("data", []):
                    tweet_metrics = tweet.get("public_metrics", {})
                    metrics.total_likes += tweet_metrics.get("like_count", 0)
                    metrics.total_comments += tweet_metrics.get("reply_count", 0)
                    metrics.total_shares += tweet_metrics.get("retweet_count", 0)
                    metrics.total_views += tweet_metrics.get("impression_count", 0)

                    metrics.top_posts.append({
                        "id": tweet.get("id"),
                        "text": tweet.get("text", "")[:100],
                        "likes": tweet_metrics.get("like_count", 0),
                        "comments": tweet_metrics.get("reply_count", 0),
                        "retweets": tweet_metrics.get("retweet_count", 0),
                        "views": tweet_metrics.get("impression_count", 0),
                        "engagement": (
                            tweet_metrics.get("like_count", 0) +
                            tweet_metrics.get("reply_count", 0) +
                            tweet_metrics.get("retweet_count", 0)
                        ),
                    })

            # Calculate engagement rate
            if metrics.total_views > 0:
                total_engagement = metrics.total_likes + metrics.total_comments + metrics.total_shares
                metrics.engagement_rate = (total_engagement / metrics.total_views) * 100

        return metrics

    async def _get_tiktok_metrics(self, days: int) -> PlatformMetrics:
        """Fetch TikTok metrics"""
        metrics = PlatformMetrics(platform="tiktok")

        async with self.tiktok:
            # Get user info
            user = await self.tiktok.get_user_info()
            user_data = user.get("data", {}).get("user", {})

            metrics.followers = user_data.get("follower_count", 0)
            metrics.following = user_data.get("following_count", 0)
            metrics.total_likes = user_data.get("likes_count", 0)
            metrics.total_posts = user_data.get("video_count", 0)

            # Get videos
            videos = await self.tiktok.get_user_videos(max_count=20)

            for video in videos.get("data", {}).get("videos", []):
                metrics.total_views += video.get("view_count", 0)
                metrics.total_comments += video.get("comment_count", 0)
                metrics.total_shares += video.get("share_count", 0)

                metrics.top_posts.append({
                    "id": video.get("id"),
                    "title": video.get("title", "")[:100],
                    "views": video.get("view_count", 0),
                    "likes": video.get("like_count", 0),
                    "comments": video.get("comment_count", 0),
                    "shares": video.get("share_count", 0),
                    "engagement": (
                        video.get("like_count", 0) +
                        video.get("comment_count", 0) +
                        video.get("share_count", 0)
                    ),
                })

            # Calculate engagement rate
            if metrics.total_views > 0:
                total_engagement = metrics.total_likes + metrics.total_comments + metrics.total_shares
                metrics.engagement_rate = (total_engagement / metrics.total_views) * 100

        return metrics

    async def _get_youtube_metrics(self, days: int) -> PlatformMetrics:
        """Fetch YouTube metrics"""
        metrics = PlatformMetrics(platform="youtube")

        async with self.youtube:
            # Get channel info
            channel = await self.youtube.get_my_channel()
            channel_data = channel.get("items", [{}])[0]
            statistics = channel_data.get("statistics", {})

            metrics.followers = int(statistics.get("subscriberCount", 0))
            metrics.total_posts = int(statistics.get("videoCount", 0))
            metrics.total_views = int(statistics.get("viewCount", 0))

            # Get recent videos
            videos = await self.youtube.get_channel_videos(max_results=25)

            for item in videos.get("items", []):
                video_id = item.get("id", {}).get("videoId")
                if video_id:
                    video_details = await self.youtube.get_video(video_id)
                    video_stats = video_details.get("items", [{}])[0].get("statistics", {})

                    likes = int(video_stats.get("likeCount", 0))
                    comments = int(video_stats.get("commentCount", 0))
                    views = int(video_stats.get("viewCount", 0))

                    metrics.total_likes += likes
                    metrics.total_comments += comments

                    metrics.top_posts.append({
                        "id": video_id,
                        "title": item.get("snippet", {}).get("title", "")[:100],
                        "views": views,
                        "likes": likes,
                        "comments": comments,
                        "engagement": likes + comments,
                    })

            # Calculate engagement rate
            if metrics.total_views > 0:
                total_engagement = metrics.total_likes + metrics.total_comments
                metrics.engagement_rate = (total_engagement / metrics.total_views) * 100

        return metrics

    async def _get_facebook_metrics(self, days: int) -> PlatformMetrics:
        """Fetch Facebook metrics"""
        metrics = PlatformMetrics(platform="facebook")

        async with self.meta:
            # Get page info
            page = await self.meta.get_page_info()

            metrics.followers = page.get("followers_count", 0)
            metrics.total_likes = page.get("fan_count", 0)

            # Get page posts
            posts = await self.meta.get_page_posts(limit=25)

            for post in posts.get("data", []):
                reactions = post.get("reactions", {}).get("summary", {}).get("total_count", 0)
                comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)
                shares = post.get("shares", {}).get("count", 0) if post.get("shares") else 0

                metrics.total_comments += comments
                metrics.total_shares += shares

                metrics.top_posts.append({
                    "id": post.get("id"),
                    "message": post.get("message", "")[:100],
                    "reactions": reactions,
                    "comments": comments,
                    "shares": shares,
                    "engagement": reactions + comments + shares,
                })

            # Calculate engagement rate
            if metrics.followers > 0:
                avg_engagement = sum(p["engagement"] for p in metrics.top_posts) / max(len(metrics.top_posts), 1)
                metrics.engagement_rate = (avg_engagement / metrics.followers) * 100

        return metrics

    def _generate_recommendations(
        self,
        metrics: AggregatedMetrics,
    ) -> List[str]:
        """Generate content recommendations based on metrics"""
        recommendations = []

        # Find best performing platform
        best_platform = None
        best_engagement = 0

        for platform, data in metrics.platform_breakdown.items():
            if data.engagement_rate > best_engagement:
                best_engagement = data.engagement_rate
                best_platform = platform

        if best_platform:
            recommendations.append(
                f"Focus more content on {best_platform.title()} - "
                f"it has your highest engagement rate ({best_engagement:.2f}%)"
            )

        # Analyze posting frequency
        for platform, data in metrics.platform_breakdown.items():
            if data.total_posts < 10:
                recommendations.append(
                    f"Increase posting frequency on {platform.title()} - "
                    f"only {data.total_posts} posts in the analysis period"
                )

        # Engagement recommendations
        if metrics.overall_engagement_rate < 1:
            recommendations.append(
                "Consider using more engaging content formats like "
                "polls, questions, and call-to-actions"
            )

        # Growth recommendations
        if metrics.total_followers < 1000:
            recommendations.append(
                "Focus on growing your audience through collaborations, "
                "hashtag strategy, and consistent posting"
            )

        # Content type recommendations based on top performing
        if metrics.top_performing_content:
            video_count = sum(1 for c in metrics.top_performing_content if "video" in str(c.get("type", "")).lower())
            if video_count > len(metrics.top_performing_content) / 2:
                recommendations.append(
                    "Video content is performing well - "
                    "consider creating more Reels, Shorts, and TikToks"
                )

        return recommendations

    async def get_content_performance(
        self,
        content_id: str,
        platform: str,
    ) -> ContentPerformance:
        """Get detailed performance for a specific piece of content"""
        performance = ContentPerformance(
            content_id=content_id,
            platform=platform,
            title="",
            published_at=datetime.now(),
        )

        if platform == "instagram" and self.instagram:
            async with self.instagram:
                insights = await self.instagram.get_media_insights(content_id)
                # Parse insights...

        elif platform == "twitter" and self.twitter:
            async with self.twitter:
                tweet = await self.twitter.get_tweet(content_id)
                metrics = tweet.get("data", {}).get("public_metrics", {})
                performance.views = metrics.get("impression_count", 0)
                performance.likes = metrics.get("like_count", 0)
                performance.comments = metrics.get("reply_count", 0)
                performance.shares = metrics.get("retweet_count", 0)

        elif platform == "tiktok" and self.tiktok:
            async with self.tiktok:
                videos = await self.tiktok.query_videos([content_id])
                video = videos.get("data", {}).get("videos", [{}])[0]
                performance.views = video.get("view_count", 0)
                performance.likes = video.get("like_count", 0)
                performance.comments = video.get("comment_count", 0)
                performance.shares = video.get("share_count", 0)

        elif platform == "youtube" and self.youtube:
            async with self.youtube:
                video = await self.youtube.get_video(content_id)
                stats = video.get("items", [{}])[0].get("statistics", {})
                performance.views = int(stats.get("viewCount", 0))
                performance.likes = int(stats.get("likeCount", 0))
                performance.comments = int(stats.get("commentCount", 0))

        # Calculate engagement rate
        if performance.views > 0:
            total_engagement = performance.likes + performance.comments + performance.shares
            performance.engagement_rate = (total_engagement / performance.views) * 100

        return performance

    async def compare_platforms(self) -> Dict[str, Any]:
        """Compare performance across all platforms"""
        metrics = await self.get_aggregated_metrics()

        comparison = {
            "platforms": {},
            "rankings": {
                "by_followers": [],
                "by_engagement": [],
                "by_growth": [],
            },
            "summary": "",
        }

        # Build platform comparison
        for platform, data in metrics.platform_breakdown.items():
            comparison["platforms"][platform] = {
                "followers": data.followers,
                "engagement_rate": data.engagement_rate,
                "total_views": data.total_views,
                "avg_views_per_post": data.avg_views_per_post,
            }

        # Create rankings
        platforms = list(metrics.platform_breakdown.items())

        comparison["rankings"]["by_followers"] = sorted(
            [(p, d.followers) for p, d in platforms],
            key=lambda x: x[1],
            reverse=True
        )

        comparison["rankings"]["by_engagement"] = sorted(
            [(p, d.engagement_rate) for p, d in platforms],
            key=lambda x: x[1],
            reverse=True
        )

        # Generate summary
        if comparison["rankings"]["by_followers"]:
            top_platform = comparison["rankings"]["by_followers"][0][0]
            comparison["summary"] = (
                f"Your strongest platform is {top_platform.title()} with "
                f"{comparison['rankings']['by_followers'][0][1]:,} followers. "
            )

        if comparison["rankings"]["by_engagement"]:
            top_engagement = comparison["rankings"]["by_engagement"][0]
            comparison["summary"] += (
                f"Best engagement is on {top_engagement[0].title()} "
                f"at {top_engagement[1]:.2f}%."
            )

        return comparison

    def export_report(
        self,
        metrics: AggregatedMetrics,
        format: str = "json",
    ) -> str:
        """Export analytics report"""
        import json

        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_followers": metrics.total_followers,
                "total_views": metrics.total_views,
                "total_engagement": metrics.total_engagement,
                "overall_engagement_rate": metrics.overall_engagement_rate,
            },
            "platforms": {},
            "top_content": [],
            "recommendations": metrics.recommendations,
        }

        for platform, data in metrics.platform_breakdown.items():
            report["platforms"][platform] = {
                "followers": data.followers,
                "engagement_rate": data.engagement_rate,
                "total_views": data.total_views,
                "total_likes": data.total_likes,
                "total_comments": data.total_comments,
            }

        for content in metrics.top_performing_content[:5]:
            report["top_content"].append(content)

        if format == "json":
            return json.dumps(report, indent=2, default=str)
        else:
            # Could add CSV, PDF, etc.
            return json.dumps(report, indent=2, default=str)
