"""
FLUX Image Generation Client for Taj Chat

High-quality image generation using BFL FLUX API.
"""

import asyncio
import logging
import os
import base64
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class FluxResult:
    """Result from FLUX generation."""
    image_data: Optional[bytes]
    model: str
    execution_time_ms: float
    error: Optional[str] = None


class FluxClient:
    """
    FLUX image generation client.

    Models:
    - flux-pro-1.1: Highest quality
    - flux-dev: Development/testing
    - flux-schnell: Fast generation
    - flux-realism: Photorealistic
    """

    BASE_URL = "https://api.bfl.ai"

    MODELS = {
        "pro": "flux-pro-1.1",
        "dev": "flux-dev",
        "schnell": "flux-schnell",
        "realism": "flux-realism",
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BFL_API_KEY", "")

        if not self.api_key:
            logger.warning("BFL_API_KEY not set")

    async def generate(
        self,
        prompt: str,
        model: str = "pro",
        width: int = 1024,
        height: int = 1024,
        steps: int = 28,
        guidance: float = 3.5,
    ) -> FluxResult:
        """Generate image using FLUX."""

        start_time = datetime.now()
        model_id = self.MODELS.get(model, self.MODELS["pro"])

        if not self.api_key:
            return FluxResult(
                image_data=None,
                model=model_id,
                execution_time_ms=10,
                error="API key not configured",
            )

        try:
            async with aiohttp.ClientSession() as session:
                # Submit generation request
                async with session.post(
                    f"{self.BASE_URL}/v1/{model_id}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "prompt": prompt,
                        "width": width,
                        "height": height,
                        "steps": steps,
                        "guidance": guidance,
                    },
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return FluxResult(
                            image_data=None,
                            model=model_id,
                            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                            error=f"API error: {response.status} - {error_text[:200]}",
                        )

                    data = await response.json()
                    task_id = data.get("id")

                if not task_id:
                    return FluxResult(
                        image_data=None,
                        model=model_id,
                        execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                        error="No task ID returned",
                    )

                # Poll for result
                image_data = await self._poll_result(session, task_id)

                return FluxResult(
                    image_data=image_data,
                    model=model_id,
                    execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                    error=None if image_data else "Generation failed",
                )

        except Exception as e:
            return FluxResult(
                image_data=None,
                model=model_id,
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                error=str(e),
            )

    async def _poll_result(
        self,
        session: aiohttp.ClientSession,
        task_id: str,
        max_attempts: int = 60,
        interval: float = 2.0,
    ) -> Optional[bytes]:
        """Poll for generation result."""

        for _ in range(max_attempts):
            try:
                async with session.get(
                    f"{self.BASE_URL}/v1/get_result?id={task_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        status = data.get("status")

                        if status == "Ready":
                            # Get image data
                            sample = data.get("result", {}).get("sample")
                            if sample:
                                # Download image from URL
                                async with session.get(sample) as img_response:
                                    if img_response.status == 200:
                                        return await img_response.read()
                            return None

                        elif status == "Error":
                            logger.error(f"FLUX generation error: {data}")
                            return None

            except Exception as e:
                logger.warning(f"Polling error: {e}")

            await asyncio.sleep(interval)

        logger.error("FLUX generation timed out")
        return None

    async def generate_and_save(
        self,
        prompt: str,
        output_path: Path,
        model: str = "pro",
        **kwargs,
    ) -> bool:
        """Generate image and save to file."""

        result = await self.generate(prompt, model, **kwargs)

        if result.image_data:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(result.image_data)
            logger.info(f"Image saved: {output_path}")
            return True

        if result.error:
            logger.error(f"Generation failed: {result.error}")

        return False
