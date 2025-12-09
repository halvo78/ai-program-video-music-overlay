"""
Content Analysis Agent - ENHANCED

Uses Together.ai and OpenRouter for content analysis:
- Script generation
- Key point extraction  
- SEO optimization
- Hashtag suggestions
- URL/Blog to Video conversion (NEW - like Pictory)
- Video Summarization (NEW)
- AI Storyboard generation (NEW)
"""

import asyncio
import logging
from typing import Any, Optional, List, Dict
import aiohttp
import os
import re
from urllib.parse import urlparse
import json

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class ContentAnalysisAgent(BaseAgent):
    """
    Content Analysis Agent using LLMs.

    This agent runs FIRST in workflows to inform other agents.
    Uses multi-model consensus for best results.
    
    NEW FEATURES:
    - URL to Video: Scrape any URL and generate video script (like Pictory)
    - Blog to Video: Convert blog posts to video content
    - Video Summarization: Create summaries of long content
    - AI Storyboard: Generate visual storyboard before video creation
    """

    # Together.ai models
    TOGETHER_MODELS = {
        "deepseek": "deepseek-ai/DeepSeek-R1",
        "llama": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "qwen": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "mixtral": "mistralai/Mixtral-8x22B-Instruct-v0.1",
    }

    def __init__(self):
        super().__init__(
            agent_type=AgentType.CONTENT_ANALYSIS,
            priority=AgentPriority.HIGH,
            parallel_capable=False,  # Runs first, informs others
        )

        self.together_api_key = os.getenv("TOGETHER_AI_API_KEY", "")
        self.together_base_url = "https://api.together.xyz/v1"
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")

    @property
    def name(self) -> str:
        return "Content Analysis Agent"

    @property
    def models(self) -> list[str]:
        return list(self.TOGETHER_MODELS.values())

    @property
    def capabilities(self) -> list[str]:
        return [
            "script generation",
            "key point extraction",
            "SEO optimization",
            "hashtag suggestions",
            "mood detection",
            "target audience analysis",
            "url to video conversion",
            "blog to video conversion",
            "video summarization",
            "ai storyboard generation",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Analyze content and generate script."""

        prompt = task.prompt
        parameters = task.parameters
        context = task.context

        platforms = context.get("platforms", ["tiktok"])
        content_type = parameters.get("content_type", "prompt")  # prompt, url, blog, summarize

        logger.info(f"Analyzing content ({content_type}): {prompt[:50]}...")

        try:
            # Route to appropriate handler
            if content_type == "url":
                analysis = await self._url_to_video(prompt, platforms, parameters)
            elif content_type == "blog":
                analysis = await self._blog_to_video(prompt, platforms, parameters)
            elif content_type == "summarize":
                analysis = await self._summarize_content(prompt, platforms, parameters)
            else:
                analysis = await self._analyze_content(
                    prompt=prompt,
                    platforms=platforms,
                    parameters=parameters,
                )

            # Generate storyboard if requested
            if parameters.get("generate_storyboard", False):
                storyboard = await self._generate_storyboard(analysis)
                analysis["storyboard"] = storyboard

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=analysis,
                metadata={
                    "platforms": platforms,
                    "content_type": content_type,
                    "script_length": len(analysis.get("script", "")),
                    "keywords_count": len(analysis.get("keywords", [])),
                    "has_storyboard": "storyboard" in analysis,
                },
            )

        except Exception as e:
            logger.error(f"Content analysis error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _url_to_video(
        self,
        url: str,
        platforms: list[str],
        parameters: dict,
    ) -> dict:
        """
        Convert any URL to video content (like Pictory).
        
        Scrapes the URL, extracts key content, and generates a video script.
        """
        
        logger.info(f"Converting URL to video: {url}")
        
        # Validate URL
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format")
        except Exception:
            # Treat as text content if not a valid URL
            return await self._analyze_content(url, platforms, parameters)
        
        # Scrape URL content
        content = await self._scrape_url(url)
        
        if not content:
            logger.warning(f"Could not scrape URL: {url}")
            return await self._analyze_content(f"Content from: {url}", platforms, parameters)
        
        # Generate video script from scraped content
        system_prompt = """You are an expert at converting web content into engaging short-form video scripts.
        
Given the content from a webpage, create:
1. A compelling 30-60 second video script
2. Key visual scenes to show
3. A hook for the first 3 seconds
4. Relevant hashtags

Focus on the most interesting/valuable points. Make it engaging for social media.

Format as JSON with: script, scenes, hook, hashtags, key_points, mood, duration_suggestion"""

        user_prompt = f"""Convert this webpage content into a short-form video script:

URL: {url}

Content:
{content[:4000]}

Target platforms: {', '.join(platforms)}"""

        result = await self._query_together(system_prompt, user_prompt)
        
        if result:
            analysis = self._parse_analysis(result, content)
            analysis["source_url"] = url
            analysis["content_type"] = "url_to_video"
            return analysis
        
        return self._generate_default_analysis(content[:500], platforms)

    async def _blog_to_video(
        self,
        blog_content: str,
        platforms: list[str],
        parameters: dict,
    ) -> dict:
        """
        Convert blog post content to video (like Pictory/Lumen5).
        
        Takes blog text and creates an engaging video script with scenes.
        """
        
        logger.info("Converting blog to video...")
        
        # Check if it's a URL to a blog
        if blog_content.startswith("http"):
            return await self._url_to_video(blog_content, platforms, parameters)
        
        system_prompt = """You are an expert at converting blog posts into engaging short-form video content.

Given a blog post, create:
1. A compelling video script (30-60 seconds)
2. 5-8 visual scenes with descriptions
3. Key points to highlight with text overlays
4. An attention-grabbing hook
5. Relevant hashtags
6. Suggested B-roll footage types

Make it visually engaging and optimized for social media attention spans.

Format as JSON with: script, scenes, key_points, hook, hashtags, broll_suggestions, mood, duration_suggestion, text_overlays"""

        user_prompt = f"""Convert this blog post into a short-form video:

{blog_content[:5000]}

Target platforms: {', '.join(platforms)}
Video style: {parameters.get('style', 'educational')}"""

        result = await self._query_together(system_prompt, user_prompt)
        
        if result:
            analysis = self._parse_analysis(result, blog_content)
            analysis["content_type"] = "blog_to_video"
            return analysis
        
        return self._generate_default_analysis(blog_content[:500], platforms)

    async def _summarize_content(
        self,
        content: str,
        platforms: list[str],
        parameters: dict,
    ) -> dict:
        """
        Summarize long content into short-form video script (like Pictory).
        
        Takes long-form content (transcript, article, etc.) and creates a summary video.
        """
        
        logger.info("Summarizing content for video...")
        
        target_duration = parameters.get("target_duration", 60)  # seconds
        
        system_prompt = f"""You are an expert at summarizing long content into engaging short-form videos.

Given long content, create a {target_duration}-second video summary:
1. Extract the 3-5 most important/interesting points
2. Create a compelling narrative arc
3. Write a script that hooks viewers immediately
4. Suggest visual scenes for each point
5. Add text overlays for key statistics/quotes

Format as JSON with: script, key_points, scenes, hook, text_overlays, hashtags, mood, original_length, summary_length"""

        user_prompt = f"""Summarize this content into a {target_duration}-second video:

{content[:8000]}

Target platforms: {', '.join(platforms)}
Focus on: {parameters.get('focus', 'key insights')}"""

        result = await self._query_together(system_prompt, user_prompt)
        
        if result:
            analysis = self._parse_analysis(result, content)
            analysis["content_type"] = "summarization"
            analysis["original_length"] = len(content)
            return analysis
        
        return self._generate_default_analysis(content[:500], platforms)

    async def _generate_storyboard(self, analysis: dict) -> List[Dict]:
        """
        Generate AI Storyboard (like Lumen5).
        
        Creates a visual storyboard with scene descriptions, timing, and visual suggestions.
        """
        
        logger.info("Generating AI storyboard...")
        
        scenes = analysis.get("scenes", [])
        script = analysis.get("script", "")
        duration = analysis.get("duration_suggestion", 30)
        
        # Calculate timing per scene
        num_scenes = max(len(scenes), 3)
        time_per_scene = duration / num_scenes
        
        storyboard = []
        current_time = 0
        
        for i, scene in enumerate(scenes):
            if isinstance(scene, str):
                scene_desc = scene
            else:
                scene_desc = scene.get("description", str(scene))
            
            storyboard_item = {
                "scene_number": i + 1,
                "start_time": round(current_time, 1),
                "end_time": round(current_time + time_per_scene, 1),
                "duration": round(time_per_scene, 1),
                "description": scene_desc,
                "visual_type": self._suggest_visual_type(scene_desc),
                "text_overlay": self._extract_text_overlay(scene_desc, script),
                "transition": "cut" if i == 0 else "fade",
                "camera_movement": self._suggest_camera_movement(scene_desc),
                "audio_notes": "Music continues" if i > 0 else "Hook music/sound",
            }
            
            storyboard.append(storyboard_item)
            current_time += time_per_scene
        
        return storyboard

    def _suggest_visual_type(self, scene_desc: str) -> str:
        """Suggest visual type based on scene description."""
        
        scene_lower = scene_desc.lower()
        
        if any(word in scene_lower for word in ["person", "face", "talking", "speaking"]):
            return "talking_head"
        elif any(word in scene_lower for word in ["product", "item", "object", "show"]):
            return "product_shot"
        elif any(word in scene_lower for word in ["text", "title", "quote", "stat"]):
            return "text_animation"
        elif any(word in scene_lower for word in ["action", "movement", "doing"]):
            return "b_roll_action"
        elif any(word in scene_lower for word in ["location", "place", "scene"]):
            return "establishing_shot"
        else:
            return "b_roll_general"

    def _suggest_camera_movement(self, scene_desc: str) -> str:
        """Suggest camera movement based on scene."""
        
        scene_lower = scene_desc.lower()
        
        if any(word in scene_lower for word in ["reveal", "show", "introduce"]):
            return "slow_zoom_in"
        elif any(word in scene_lower for word in ["overview", "all", "everything"]):
            return "slow_zoom_out"
        elif any(word in scene_lower for word in ["action", "movement", "follow"]):
            return "pan"
        else:
            return "static"

    def _extract_text_overlay(self, scene_desc: str, script: str) -> Optional[str]:
        """Extract potential text overlay for scene."""
        
        # Look for numbers/statistics
        numbers = re.findall(r'\d+%|\d+\+|\$\d+|\d+ million|\d+ billion', scene_desc + " " + script)
        if numbers:
            return numbers[0]
        
        # Look for quoted text
        quotes = re.findall(r'"([^"]+)"', scene_desc)
        if quotes:
            return quotes[0][:50]
        
        return None

    async def _scrape_url(self, url: str) -> Optional[str]:
        """Scrape content from URL."""
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # Basic HTML parsing - extract text content
                        # Remove script and style tags
                        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
                        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
                        
                        # Remove HTML tags
                        text = re.sub(r'<[^>]+>', ' ', html)
                        
                        # Clean up whitespace
                        text = re.sub(r'\s+', ' ', text).strip()
                        
                        # Extract title if present
                        title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
                        title = title_match.group(1) if title_match else ""
                        
                        return f"Title: {title}\n\nContent:\n{text[:5000]}"
                    
                    return None
                    
        except Exception as e:
            logger.warning(f"URL scraping failed: {e}")
            return None

    async def _analyze_content(
        self,
        prompt: str,
        platforms: list[str],
        parameters: dict = None,
    ) -> dict:
        """Generate comprehensive content analysis."""

        system_prompt = """You are an expert short-form video content creator and analyst.
Analyze the user's prompt and generate:
1. A compelling video script optimized for the target platform(s)
2. Key visual scenes to include
3. Mood/tone for music selection
4. Relevant keywords and hashtags
5. Hook for the first 3 seconds

Format your response as JSON with these fields:
- script: The narration/voiceover script
- scenes: List of visual scene descriptions
- mood: Overall mood (happy, energetic, calm, dramatic, etc.)
- keywords: List of relevant keywords
- hashtags: Platform-optimized hashtags
- hook: Attention-grabbing opening
- duration_suggestion: Recommended video length in seconds
- target_audience: Who this content is for"""

        user_prompt = f"""Create a short-form video content plan for:

"{prompt}"

Target platforms: {', '.join(platforms)}

Generate a complete content analysis."""

        # Try Together.ai first
        if self.together_api_key:
            try:
                result = await self._query_together(system_prompt, user_prompt)
                if result:
                    return self._parse_analysis(result, prompt)
            except Exception as e:
                logger.warning(f"Together.ai failed: {e}")

        # Fallback to default analysis
        return self._generate_default_analysis(prompt, platforms)

    async def _query_together(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = None,
    ) -> Optional[str]:
        """Query Together.ai API."""

        model = model or self.TOGETHER_MODELS["llama"]

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.together_api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 2048,
                "temperature": 0.7,
            }

            async with session.post(
                f"{self.together_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    logger.warning(f"Together.ai error: {response.status} - {error_text}")
                    return None

    def _parse_analysis(self, response: str, prompt: str) -> dict:
        """Parse LLM response into structured analysis."""

        # Try to parse as JSON
        try:
            # Find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # Fallback to extracting key information
        return self._generate_default_analysis(prompt, ["tiktok"])

    def _generate_default_analysis(self, prompt: str, platforms: list[str]) -> dict:
        """Generate default analysis when API is unavailable."""

        # Extract keywords from prompt
        words = prompt.lower().split()
        keywords = [w for w in words if len(w) > 4][:10]

        # Generate hashtags
        hashtags = [f"#{w}" for w in keywords[:5]]
        hashtags.extend(["#fyp", "#viral", "#trending"])

        # Determine mood from keywords
        mood_keywords = {
            "happy": ["happy", "fun", "joy", "exciting", "amazing"],
            "calm": ["peaceful", "relaxing", "calm", "serene", "quiet"],
            "energetic": ["energy", "power", "fast", "dynamic", "action"],
            "dramatic": ["epic", "intense", "dramatic", "powerful"],
        }

        mood = "neutral"
        for m, kws in mood_keywords.items():
            if any(kw in prompt.lower() for kw in kws):
                mood = m
                break

        # Platform-specific duration
        durations = {
            "tiktok": 30,
            "instagram_reels": 30,
            "youtube_shorts": 45,
            "twitter": 45,
        }
        duration = durations.get(platforms[0], 30)

        return {
            "script": prompt,
            "scenes": [
                f"Opening hook scene for: {prompt[:50]}",
                "Main content visualization",
                "Call to action / closing",
            ],
            "mood": mood,
            "keywords": keywords,
            "hashtags": hashtags,
            "hook": f"You won't believe this: {prompt[:30]}...",
            "duration_suggestion": duration,
            "target_audience": "general",
        }
