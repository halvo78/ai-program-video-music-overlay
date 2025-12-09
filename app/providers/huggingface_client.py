"""
HuggingFace Pro Client for Taj Chat

Adapted from UTS app/verification/hf_client.py
Uses HuggingFace MCP server for model access.
"""

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class InferenceResult:
    """Result from HuggingFace inference."""
    model: str
    output: Any
    execution_time_ms: float
    error: Optional[str] = None


class HuggingFaceClient:
    """
    HuggingFace Pro client for AI generation.

    Models available via HF MCP:
    - Video: Stable Video Diffusion, AnimateDiff, CogVideo
    - Music: MusicGen, Riffusion, AudioCraft
    - Image: SDXL, Stable Diffusion 3
    - Voice: Whisper, Bark, Coqui TTS
    """

    BASE_URL = "https://api-inference.huggingface.co"

    # Model registry
    MODELS = {
        # Video
        "svd": "stabilityai/stable-video-diffusion-img2vid-xt",
        "animatediff": "guoyww/animatediff-motion-adapter-v1-5-2",

        # Music
        "musicgen": "facebook/musicgen-large",
        "musicgen_melody": "facebook/musicgen-melody",
        "riffusion": "riffusion/riffusion-model-v1",

        # Image
        "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
        "sdxl_turbo": "stabilityai/sdxl-turbo",

        # Voice
        "whisper": "openai/whisper-large-v3",
        "bark": "suno/bark",
        "speecht5": "microsoft/speecht5_tts",

        # Text
        "embedding": "sentence-transformers/all-MiniLM-L6-v2",
        "classification": "facebook/bart-large-mnli",
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("HF_TOKEN_PRO", "")
        self.username = username or os.getenv("HUGGINGFACE_USERNAME", "Halvo78")

        if not self.api_key:
            logger.warning("HF_TOKEN_PRO not set")

    async def inference(
        self,
        model: str,
        inputs: Any,
        parameters: Optional[dict] = None,
    ) -> InferenceResult:
        """Run inference on a HuggingFace model."""

        start_time = datetime.now()
        model_id = self.MODELS.get(model, model)

        if not self.api_key:
            return InferenceResult(
                model=model_id,
                output={"mock": True},
                execution_time_ms=10,
            )

        payload = {"inputs": inputs}
        if parameters:
            payload["parameters"] = parameters

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.BASE_URL}/models/{model_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120),
                ) as response:
                    exec_time = (datetime.now() - start_time).total_seconds() * 1000

                    if response.status == 200:
                        # Check content type
                        content_type = response.headers.get("Content-Type", "")

                        if "application/json" in content_type:
                            data = await response.json()
                        else:
                            # Binary data (audio, image)
                            data = await response.read()

                        return InferenceResult(
                            model=model_id,
                            output=data,
                            execution_time_ms=exec_time,
                        )
                    else:
                        error_text = await response.text()
                        return InferenceResult(
                            model=model_id,
                            output=None,
                            execution_time_ms=exec_time,
                            error=f"API error: {response.status} - {error_text[:200]}",
                        )

        except Exception as e:
            return InferenceResult(
                model=model_id,
                output=None,
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                error=str(e),
            )

    async def generate_music(
        self,
        prompt: str,
        duration: int = 30,
    ) -> InferenceResult:
        """Generate music using MusicGen."""
        return await self.inference("musicgen", prompt)

    async def generate_image(
        self,
        prompt: str,
    ) -> InferenceResult:
        """Generate image using SDXL."""
        return await self.inference("sdxl", prompt)

    async def transcribe(
        self,
        audio_data: bytes,
    ) -> InferenceResult:
        """Transcribe audio using Whisper."""
        return await self.inference("whisper", audio_data)

    async def text_to_speech(
        self,
        text: str,
    ) -> InferenceResult:
        """Convert text to speech using Bark."""
        return await self.inference("bark", text)

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """Generate text embeddings."""
        result = await self.inference("embedding", text)
        if result.error:
            return []
        return result.output if isinstance(result.output, list) else []
