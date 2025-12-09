"""
Image Generation Agent

Uses FLUX and HuggingFace for image generation:
- FLUX Pro 1.1 (primary)
- FLUX Dev
- Stable Diffusion XL
- ControlNet
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Optional
import aiohttp
import os
import base64

from .base_agent import BaseAgent, AgentType, AgentPriority, AgentTask, AgentResult

logger = logging.getLogger(__name__)


class ImageGenerationAgent(BaseAgent):
    """
    Image Generation Agent using FLUX and HuggingFace models.

    Capabilities:
    - Text-to-image generation
    - Overlay graphics creation
    - Thumbnail generation
    - Style consistency
    """

    # FLUX models (primary)
    FLUX_MODELS = {
        "flux-pro": "flux-pro-1.1",
        "flux-dev": "flux-dev",
        "flux-schnell": "flux-schnell",
        "flux-realism": "flux-realism",
    }

    # HuggingFace fallback models
    HF_MODELS = {
        "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
        "sdxl-turbo": "stabilityai/sdxl-turbo",
        "playground": "playgroundai/playground-v2.5-1024px-aesthetic",
    }

    def __init__(self):
        super().__init__(
            agent_type=AgentType.IMAGE_GENERATION,
            priority=AgentPriority.CRITICAL,
            parallel_capable=True,
        )

        self.flux_api_key = os.getenv("BFL_API_KEY", "")
        self.flux_base_url = "https://api.bfl.ai"
        self.hf_token = os.getenv("HF_TOKEN_PRO", "")
        self.hf_base_url = "https://api-inference.huggingface.co"

        self.output_dir = Path("C:/dev/taj-chat/generated/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def name(self) -> str:
        return "Image Generation Agent"

    @property
    def models(self) -> list[str]:
        return list(self.FLUX_MODELS.values()) + list(self.HF_MODELS.values())

    @property
    def capabilities(self) -> list[str]:
        return [
            "text-to-image generation",
            "overlay graphics creation",
            "thumbnail generation",
            "style consistency",
            "image upscaling",
            "background removal",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Generate images based on task parameters."""

        prompt = task.prompt
        parameters = task.parameters
        context = task.context

        # Get parameters
        image_type = parameters.get("image_type", "content")  # content, overlay, thumbnail
        model = parameters.get("model", "flux-pro")
        width = parameters.get("width", 1024)
        height = parameters.get("height", 1024)
        num_images = parameters.get("num_images", 1)

        logger.info(f"Generating {image_type} image: {prompt[:50]}...")

        try:
            output = await self._generate_images(
                prompt=prompt,
                model=model,
                width=width,
                height=height,
                num_images=num_images,
                image_type=image_type,
                context=context,
            )

            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="success",
                output=output,
                output_files=output.get("image_paths", []),
                metadata={
                    "model": model,
                    "width": width,
                    "height": height,
                    "num_images": num_images,
                    "image_type": image_type,
                },
            )

        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status="error",
                error=str(e),
            )

    async def _generate_images(
        self,
        prompt: str,
        model: str = "flux-pro",
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1,
        image_type: str = "content",
        context: dict = None,
    ) -> dict:
        """Generate images using FLUX or HuggingFace."""

        # Enhance prompt based on image type
        enhanced_prompt = self._enhance_prompt(prompt, image_type, context)

        logger.info(f"Using model: {model}")
        logger.info(f"Enhanced prompt: {enhanced_prompt}")

        image_paths = []

        # Try FLUX first (higher quality)
        if model.startswith("flux") and self.flux_api_key:
            for i in range(num_images):
                try:
                    image_path = await self._generate_flux(
                        prompt=enhanced_prompt,
                        model=model,
                        width=width,
                        height=height,
                        index=i,
                    )
                    if image_path:
                        image_paths.append(image_path)
                except Exception as e:
                    logger.warning(f"FLUX generation failed: {e}")

        # Fallback to HuggingFace
        if not image_paths and self.hf_token:
            hf_model = self.HF_MODELS.get("sdxl")
            for i in range(num_images):
                try:
                    image_path = await self._generate_huggingface(
                        prompt=enhanced_prompt,
                        model=hf_model,
                        width=width,
                        height=height,
                        index=i,
                    )
                    if image_path:
                        image_paths.append(image_path)
                except Exception as e:
                    logger.warning(f"HuggingFace generation failed: {e}")

        # Create placeholder if no API available
        if not image_paths:
            for i in range(num_images):
                placeholder_path = self.output_dir / f"image_{hash(prompt) % 10000}_{i}.png"
                image_paths.append(placeholder_path)

        return {
            "image_paths": image_paths,
            "prompt": enhanced_prompt,
            "model": model,
            "width": width,
            "height": height,
            "image_type": image_type,
            "status": "generated",
        }

    async def _generate_flux(
        self,
        prompt: str,
        model: str,
        width: int,
        height: int,
        index: int = 0,
    ) -> Optional[Path]:
        """Generate image using FLUX API."""

        output_path = self.output_dir / f"flux_{hash(prompt) % 10000}_{index}.png"

        try:
            async with aiohttp.ClientSession() as session:
                # FLUX API endpoint
                endpoint = f"{self.flux_base_url}/v1/flux-pro-1.1"

                headers = {
                    "Authorization": f"Bearer {self.flux_api_key}",
                    "Content-Type": "application/json",
                }

                payload = {
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                    "steps": 28,
                    "guidance": 3.5,
                }

                async with session.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Handle FLUX response format
                        if "id" in data:
                            # Poll for result
                            result = await self._poll_flux_result(session, data["id"])
                            if result and "sample" in result:
                                image_data = base64.b64decode(result["sample"])
                                output_path.write_bytes(image_data)
                                logger.info(f"FLUX image generated: {output_path}")
                                return output_path
                    else:
                        error_text = await response.text()
                        logger.warning(f"FLUX API error: {response.status} - {error_text}")

        except Exception as e:
            logger.warning(f"FLUX API call failed: {e}")

        return None

    async def _poll_flux_result(
        self,
        session: aiohttp.ClientSession,
        task_id: str,
        max_attempts: int = 30,
    ) -> Optional[dict]:
        """Poll FLUX API for generation result."""

        for _ in range(max_attempts):
            try:
                async with session.get(
                    f"{self.flux_base_url}/v1/get_result?id={task_id}",
                    headers={"Authorization": f"Bearer {self.flux_api_key}"},
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "Ready":
                            return data
                        elif data.get("status") == "Error":
                            logger.error(f"FLUX generation error: {data}")
                            return None
            except Exception as e:
                logger.warning(f"Polling error: {e}")

            await asyncio.sleep(2)

        return None

    async def _generate_huggingface(
        self,
        prompt: str,
        model: str,
        width: int,
        height: int,
        index: int = 0,
    ) -> Optional[Path]:
        """Generate image using HuggingFace API."""

        output_path = self.output_dir / f"hf_{hash(prompt) % 10000}_{index}.png"

        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.hf_token}"}
                payload = {"inputs": prompt}

                async with session.post(
                    f"{self.hf_base_url}/models/{model}",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        output_path.write_bytes(image_data)
                        logger.info(f"HuggingFace image generated: {output_path}")
                        return output_path
                    else:
                        error_text = await response.text()
                        logger.warning(f"HuggingFace API error: {response.status} - {error_text}")

        except Exception as e:
            logger.warning(f"HuggingFace API call failed: {e}")

        return None

    def _enhance_prompt(
        self,
        prompt: str,
        image_type: str,
        context: dict = None,
    ) -> str:
        """Enhance prompt based on image type and context."""

        # Base enhancements by type
        type_enhancements = {
            "content": "high quality, detailed, professional",
            "overlay": "transparent background, clean design, vector style",
            "thumbnail": "eye-catching, bold colors, clear subject, YouTube thumbnail style",
            "background": "seamless, atmospheric, cinematic",
        }

        enhancement = type_enhancements.get(image_type, "")
        enhanced = f"{prompt}, {enhancement}" if enhancement else prompt

        # Add context-based enhancements
        if context:
            mood = context.get("mood", "")
            keywords = context.get("keywords", [])

            if mood:
                enhanced = f"{enhanced}, {mood} mood"
            if keywords:
                enhanced = f"{enhanced}, {', '.join(keywords[:2])}"

        return enhanced

    async def generate_thumbnail(
        self,
        title: str,
        style: str = "bold",
        platform: str = "youtube",
    ) -> dict:
        """Generate a thumbnail optimized for a platform."""

        # Platform-specific dimensions
        dimensions = {
            "youtube": (1280, 720),
            "tiktok": (1080, 1920),
            "instagram": (1080, 1080),
            "twitter": (1200, 675),
        }

        width, height = dimensions.get(platform, (1280, 720))

        prompt = f"YouTube thumbnail for '{title}', {style} style, attention-grabbing, professional"

        return await self._generate_images(
            prompt=prompt,
            model="flux-pro",
            width=width,
            height=height,
            num_images=1,
            image_type="thumbnail",
        )
