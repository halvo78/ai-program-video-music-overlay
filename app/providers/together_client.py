"""
Together.ai Client for Taj Chat

Adapted from UTS app/verification/together_client.py
Multi-model consensus for content analysis.
"""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class ModelResponse:
    """Response from a single model."""
    model: str
    response: str
    confidence: float
    execution_time_ms: float
    tokens_used: int
    error: Optional[str] = None


@dataclass
class ConsensusResult:
    """Result of multi-model consensus."""
    query: str
    consensus_answer: str
    confidence: float
    agreement_rate: float
    model_responses: list[ModelResponse] = field(default_factory=list)
    timestamp: str = ""


class TogetherClient:
    """
    Together.ai client for multi-model AI operations.

    Models available:
    - DeepSeek R1: Deep reasoning
    - Llama 3.3 70B: General analysis
    - Qwen 2.5 Coder: Code-specific
    - Mixtral 8x22B: Diverse perspectives
    """

    MODELS = {
        "deepseek": "deepseek-ai/DeepSeek-R1",
        "llama": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "qwen": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "mixtral": "mistralai/Mixtral-8x22B-Instruct-v0.1",
    }

    BASE_URL = "https://api.together.xyz/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TOGETHER_AI_API_KEY", "")
        self.timeout = 60

        if not self.api_key:
            logger.warning("TOGETHER_AI_API_KEY not set")

    async def query(
        self,
        prompt: str,
        model: str = "llama",
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> ModelResponse:
        """Query a single model."""

        start_time = datetime.now()
        model_id = self.MODELS.get(model, self.MODELS["llama"])

        if not self.api_key:
            return ModelResponse(
                model=model_id,
                response=f"[MOCK] Response for: {prompt[:50]}...",
                confidence=0.85,
                execution_time_ms=100,
                tokens_used=50,
            )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model_id,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                    },
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        tokens = data.get("usage", {}).get("total_tokens", 0)

                        return ModelResponse(
                            model=model_id,
                            response=content,
                            confidence=0.9,
                            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                            tokens_used=tokens,
                        )
                    else:
                        error_text = await response.text()
                        return ModelResponse(
                            model=model_id,
                            response="",
                            confidence=0,
                            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                            tokens_used=0,
                            error=f"API error: {response.status} - {error_text[:200]}",
                        )

        except Exception as e:
            return ModelResponse(
                model=model_id,
                response="",
                confidence=0,
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                tokens_used=0,
                error=str(e),
            )

    async def multi_query(
        self,
        prompt: str,
        models: Optional[list[str]] = None,
        system_prompt: Optional[str] = None,
    ) -> list[ModelResponse]:
        """Query multiple models in parallel."""

        models = models or list(self.MODELS.keys())

        tasks = [
            self.query(prompt, model, system_prompt)
            for model in models
        ]

        return await asyncio.gather(*tasks)

    async def get_consensus(
        self,
        query: str,
        context: Optional[str] = None,
    ) -> ConsensusResult:
        """Get multi-model consensus on a query."""

        system_prompt = """Analyze the query and provide a clear answer.
Format: ANSWER: [your answer] | CONFIDENCE: [0-100]%"""

        full_prompt = f"Context: {context}\n\nQuery: {query}" if context else query

        responses = await self.multi_query(full_prompt, system_prompt=system_prompt)

        valid_responses = [r for r in responses if not r.error]

        if not valid_responses:
            return ConsensusResult(
                query=query,
                consensus_answer="ERROR",
                confidence=0,
                agreement_rate=0,
                timestamp=datetime.utcnow().isoformat(),
            )

        # Simple consensus: use response from highest confidence model
        best_response = max(valid_responses, key=lambda r: r.confidence)

        return ConsensusResult(
            query=query,
            consensus_answer=best_response.response,
            confidence=best_response.confidence,
            agreement_rate=len(valid_responses) / len(responses),
            model_responses=responses,
            timestamp=datetime.utcnow().isoformat(),
        )
