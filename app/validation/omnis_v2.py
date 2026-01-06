"""
OMNIS-2: Omniscient Multi-AI Convergence, Validation & Release Authority System
================================================================================

Ultimate Multi-AI Validation Framework for Taj Chat
Version 2.0 - Enhanced with Competitor Intelligence

This system leverages ALL available AI providers to validate:
1. Code Quality & Security
2. User Experience & Design
3. Performance & Scalability
4. Content Safety & Compliance
5. Market Competitiveness
6. Production Readiness

Available AI Providers:
- OpenAI (GPT-4o, GPT-4 Turbo)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
- Google (Gemini 1.5 Pro, Gemini 2.0)
- OpenRouter (Access to all models)
- Together.ai (Open source models)
- HuggingFace Pro (Specialized models)
- Cohere (Command R+)
- DeepSeek (DeepSeek V3)

Architecture: 15 Hard Gates + Multi-AI Consensus
"""

import asyncio
import hashlib
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ============================================
# ENUMS & CONSTANTS
# ============================================

class ValidationGate(Enum):
    """15 Hard Gates for Production Release"""
    GATE_01_SYNTAX = "syntax_validation"
    GATE_02_SECURITY = "security_audit"
    GATE_03_PERFORMANCE = "performance_benchmarks"
    GATE_04_TESTING = "test_coverage"
    GATE_05_DEPENDENCIES = "dependency_check"
    GATE_06_DOCUMENTATION = "documentation_review"
    GATE_07_ACCESSIBILITY = "accessibility_audit"
    GATE_08_UX = "user_experience"
    GATE_09_CONTENT_SAFETY = "content_safety"
    GATE_10_COMPLIANCE = "compliance_check"
    GATE_11_SCALABILITY = "scalability_test"
    GATE_12_INTEGRATION = "integration_test"
    GATE_13_COMPETITIVE = "competitive_analysis"
    GATE_14_ADVERSARIAL = "adversarial_testing"
    GATE_15_CONSENSUS = "multi_ai_consensus"


class ValidationStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    BLOCKED = "blocked"


class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OPENROUTER = "openrouter"
    TOGETHER = "together"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    DEEPSEEK = "deepseek"


class ConsensusLevel(Enum):
    """Required agreement level for validation"""
    UNANIMOUS = "unanimous"      # All AIs must agree
    SUPERMAJORITY = "supermajority"  # 75%+ must agree
    MAJORITY = "majority"        # 50%+ must agree
    ANY = "any"                  # Any single AI approval


# ============================================
# DATA CLASSES
# ============================================

@dataclass
class AIValidationResult:
    """Result from a single AI provider validation"""
    provider: AIProvider
    model: str
    passed: bool
    confidence: float  # 0.0 - 1.0
    reasoning: str
    suggestions: List[str] = field(default_factory=list)
    issues_found: List[Dict[str, Any]] = field(default_factory=list)
    execution_time_ms: int = 0
    tokens_used: int = 0
    cost_usd: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class GateResult:
    """Result from a validation gate"""
    gate: ValidationGate
    status: ValidationStatus
    ai_results: List[AIValidationResult] = field(default_factory=list)
    consensus_reached: bool = False
    consensus_level: ConsensusLevel = ConsensusLevel.MAJORITY
    aggregated_score: float = 0.0
    blocking_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    execution_time_ms: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ValidationReport:
    """Complete validation report"""
    report_id: str
    project_name: str
    version: str
    gates: Dict[ValidationGate, GateResult] = field(default_factory=dict)
    overall_status: ValidationStatus = ValidationStatus.PENDING
    overall_score: float = 0.0
    total_issues: int = 0
    blocking_issues: int = 0
    warnings: int = 0
    ai_consensus_achieved: bool = False
    total_execution_time_ms: int = 0
    total_cost_usd: float = 0.0
    truth_log_hash: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    signed_by: List[str] = field(default_factory=list)


# ============================================
# AI VALIDATOR INTERFACE
# ============================================

class AIValidator(ABC):
    """Abstract base class for AI validators"""

    def __init__(self, provider: AIProvider, api_key: str = None):
        self.provider = provider
        self.api_key = api_key
        self.models: List[str] = []

    @abstractmethod
    async def validate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any],
        model: str = None
    ) -> AIValidationResult:
        """Run validation for a specific gate"""
        pass

    @abstractmethod
    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code for issues"""
        pass

    @abstractmethod
    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        """Security vulnerability scan"""
        pass

    @abstractmethod
    async def evaluate_ux(self, ui_description: str) -> Dict[str, Any]:
        """UX evaluation"""
        pass


# ============================================
# AI PROVIDER IMPLEMENTATIONS
# ============================================

class OpenAIValidator(AIValidator):
    """OpenAI GPT-4 Validator"""

    def __init__(self, api_key: str = None):
        super().__init__(AIProvider.OPENAI, api_key)
        self.models = ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]

    async def validate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any],
        model: str = None
    ) -> AIValidationResult:
        """OpenAI validation implementation"""
        model = model or self.models[0]
        start_time = datetime.utcnow()

        try:
            # Import only when needed
            import openai

            client = openai.AsyncOpenAI(api_key=self.api_key)

            prompt = self._build_validation_prompt(gate, context)

            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(gate)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=result.get("passed", False),
                confidence=result.get("confidence", 0.0),
                reasoning=result.get("reasoning", ""),
                suggestions=result.get("suggestions", []),
                issues_found=result.get("issues", []),
                execution_time_ms=execution_time,
                tokens_used=response.usage.total_tokens,
                cost_usd=self._calculate_cost(response.usage, model)
            )
        except Exception as e:
            logger.error(f"OpenAI validation error: {e}")
            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=False,
                confidence=0.0,
                reasoning=f"Validation error: {str(e)}",
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )

    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code using GPT-4"""
        # Implementation details
        pass

    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        """Security scan using GPT-4"""
        # Implementation details
        pass

    async def evaluate_ux(self, ui_description: str) -> Dict[str, Any]:
        """UX evaluation using GPT-4"""
        # Implementation details
        pass

    def _get_system_prompt(self, gate: ValidationGate) -> str:
        """Get system prompt based on gate"""
        prompts = {
            ValidationGate.GATE_01_SYNTAX: """You are an expert code syntax validator.
            Analyze code for syntax errors, type issues, and structural problems.
            Return JSON with: passed (bool), confidence (0-1), reasoning, suggestions, issues[]""",

            ValidationGate.GATE_02_SECURITY: """You are a senior security auditor.
            Analyze code for OWASP Top 10, injection vulnerabilities, XSS, CSRF,
            authentication issues, data exposure, and other security risks.
            Return JSON with: passed (bool), confidence (0-1), reasoning, suggestions, issues[]""",

            ValidationGate.GATE_03_PERFORMANCE: """You are a performance optimization expert.
            Analyze for bottlenecks, memory leaks, inefficient algorithms, N+1 queries,
            and scalability issues.
            Return JSON with: passed (bool), confidence (0-1), reasoning, suggestions, issues[]""",

            ValidationGate.GATE_08_UX: """You are a UX expert analyzing user interfaces.
            Evaluate usability, accessibility, visual hierarchy, interaction patterns,
            and overall user experience.
            Return JSON with: passed (bool), confidence (0-1), reasoning, suggestions, issues[]""",

            ValidationGate.GATE_09_CONTENT_SAFETY: """You are a content safety specialist.
            Check for inappropriate content, bias, harmful outputs, misinformation risks,
            and content policy violations.
            Return JSON with: passed (bool), confidence (0-1), reasoning, suggestions, issues[]""",

            ValidationGate.GATE_13_COMPETITIVE: """You are a market analyst comparing features.
            Evaluate against competitors: Opus Clip, Pictory, Synthesia, InVideo,
            Lumen5, Descript, Kapwing, HeyGen, Runway, Pika.
            Return JSON with: passed (bool), confidence (0-1), reasoning, suggestions, issues[]"""
        }
        return prompts.get(gate, "You are an expert validator. Return JSON with: passed, confidence, reasoning, suggestions, issues[]")

    def _build_validation_prompt(self, gate: ValidationGate, context: Dict[str, Any]) -> str:
        """Build validation prompt from context"""
        return f"""
        Validate the following for {gate.value}:

        Context:
        {json.dumps(context, indent=2, default=str)}

        Provide a detailed analysis with:
        1. Whether it passes validation (passed: true/false)
        2. Your confidence level (0.0 to 1.0)
        3. Detailed reasoning
        4. Specific suggestions for improvement
        5. List of issues found with severity
        """

    def _calculate_cost(self, usage, model: str) -> float:
        """Calculate API cost"""
        costs = {
            "gpt-4o": (0.005, 0.015),      # input, output per 1K tokens
            "gpt-4-turbo": (0.01, 0.03),
            "gpt-4o-mini": (0.00015, 0.0006)
        }
        input_cost, output_cost = costs.get(model, (0.01, 0.03))
        return (usage.prompt_tokens * input_cost + usage.completion_tokens * output_cost) / 1000


class AnthropicValidator(AIValidator):
    """Anthropic Claude Validator"""

    def __init__(self, api_key: str = None):
        super().__init__(AIProvider.ANTHROPIC, api_key)
        self.models = ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-5-haiku-20241022"]

    async def validate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any],
        model: str = None
    ) -> AIValidationResult:
        """Anthropic validation implementation"""
        model = model or self.models[0]
        start_time = datetime.utcnow()

        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=self.api_key)

            prompt = self._build_validation_prompt(gate, context)

            response = await client.messages.create(
                model=model,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system=self._get_system_prompt(gate)
            )

            # Parse JSON from response
            content = response.content[0].text
            # Extract JSON from response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {"passed": False, "confidence": 0.0, "reasoning": content}

            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=result.get("passed", False),
                confidence=result.get("confidence", 0.0),
                reasoning=result.get("reasoning", ""),
                suggestions=result.get("suggestions", []),
                issues_found=result.get("issues", []),
                execution_time_ms=execution_time,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                cost_usd=self._calculate_cost(response.usage, model)
            )
        except Exception as e:
            logger.error(f"Anthropic validation error: {e}")
            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=False,
                confidence=0.0,
                reasoning=f"Validation error: {str(e)}",
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )

    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        pass

    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        pass

    async def evaluate_ux(self, ui_description: str) -> Dict[str, Any]:
        pass

    def _get_system_prompt(self, gate: ValidationGate) -> str:
        """Get specialized system prompt for Claude"""
        base = """You are Claude, an expert AI validator. Your role is to provide thorough,
        honest, and accurate validation. Always respond with valid JSON containing:
        - passed: boolean
        - confidence: float 0-1
        - reasoning: detailed explanation
        - suggestions: array of improvement suggestions
        - issues: array of {severity, description, location}"""

        gate_specific = {
            ValidationGate.GATE_02_SECURITY: """
            Focus on security analysis:
            - OWASP Top 10 vulnerabilities
            - Injection attacks (SQL, XSS, Command)
            - Authentication/Authorization flaws
            - Sensitive data exposure
            - Security misconfigurations
            - Cryptographic failures
            """,
            ValidationGate.GATE_14_ADVERSARIAL: """
            Perform adversarial testing:
            - Try to break the system
            - Find edge cases
            - Test for robustness
            - Identify failure modes
            - Check error handling
            """
        }
        return base + gate_specific.get(gate, "")

    def _build_validation_prompt(self, gate: ValidationGate, context: Dict[str, Any]) -> str:
        return f"""
        Please validate the following for {gate.value}:

        Context:
        ```json
        {json.dumps(context, indent=2, default=str)}
        ```

        Respond with a JSON object containing your validation results.
        """

    def _calculate_cost(self, usage, model: str) -> float:
        costs = {
            "claude-3-5-sonnet-20241022": (0.003, 0.015),
            "claude-3-opus-20240229": (0.015, 0.075),
            "claude-3-5-haiku-20241022": (0.001, 0.005)
        }
        input_cost, output_cost = costs.get(model, (0.003, 0.015))
        return (usage.input_tokens * input_cost + usage.output_tokens * output_cost) / 1000


class GoogleValidator(AIValidator):
    """Google Gemini Validator"""

    def __init__(self, api_key: str = None):
        super().__init__(AIProvider.GOOGLE, api_key)
        self.models = ["gemini-1.5-pro", "gemini-2.0-flash-exp", "gemini-1.5-flash"]

    async def validate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any],
        model: str = None
    ) -> AIValidationResult:
        """Google Gemini validation implementation"""
        model = model or self.models[0]
        start_time = datetime.utcnow()

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)

            model_instance = genai.GenerativeModel(model)

            prompt = self._build_validation_prompt(gate, context)

            response = await model_instance.generate_content_async(prompt)

            # Parse JSON from response
            content = response.text
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {"passed": False, "confidence": 0.0, "reasoning": content}

            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=result.get("passed", False),
                confidence=result.get("confidence", 0.0),
                reasoning=result.get("reasoning", ""),
                suggestions=result.get("suggestions", []),
                issues_found=result.get("issues", []),
                execution_time_ms=execution_time,
                tokens_used=0,  # Gemini doesn't return token count in same way
                cost_usd=0.0
            )
        except Exception as e:
            logger.error(f"Google validation error: {e}")
            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=False,
                confidence=0.0,
                reasoning=f"Validation error: {str(e)}",
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )

    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        pass

    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        pass

    async def evaluate_ux(self, ui_description: str) -> Dict[str, Any]:
        pass

    def _build_validation_prompt(self, gate: ValidationGate, context: Dict[str, Any]) -> str:
        return f"""
        You are an expert validator. Analyze the following for {gate.value}.

        Context:
        {json.dumps(context, indent=2, default=str)}

        Respond with ONLY valid JSON:
        {{
            "passed": true/false,
            "confidence": 0.0-1.0,
            "reasoning": "detailed explanation",
            "suggestions": ["suggestion1", "suggestion2"],
            "issues": [{{"severity": "high/medium/low", "description": "...", "location": "..."}}]
        }}
        """


class TogetherValidator(AIValidator):
    """Together.ai Validator (Open Source Models)"""

    def __init__(self, api_key: str = None):
        super().__init__(AIProvider.TOGETHER, api_key)
        self.models = [
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "mistralai/Mixtral-8x22B-Instruct-v0.1",
            "Qwen/Qwen2-72B-Instruct"
        ]

    async def validate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any],
        model: str = None
    ) -> AIValidationResult:
        """Together.ai validation implementation"""
        model = model or self.models[0]
        start_time = datetime.utcnow()

        try:
            from together import AsyncTogether

            client = AsyncTogether(api_key=self.api_key)

            prompt = self._build_validation_prompt(gate, context)

            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert validator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=4096
            )

            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {"passed": False, "confidence": 0.0, "reasoning": content}

            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=result.get("passed", False),
                confidence=result.get("confidence", 0.0),
                reasoning=result.get("reasoning", ""),
                suggestions=result.get("suggestions", []),
                issues_found=result.get("issues", []),
                execution_time_ms=execution_time,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                cost_usd=self._calculate_cost(response.usage, model) if response.usage else 0.0
            )
        except Exception as e:
            logger.error(f"Together validation error: {e}")
            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=False,
                confidence=0.0,
                reasoning=f"Validation error: {str(e)}",
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )

    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        pass

    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        pass

    async def evaluate_ux(self, ui_description: str) -> Dict[str, Any]:
        pass

    def _build_validation_prompt(self, gate: ValidationGate, context: Dict[str, Any]) -> str:
        return f"""
        Validate for {gate.value}:

        {json.dumps(context, indent=2, default=str)}

        Respond with JSON: {{"passed": bool, "confidence": 0-1, "reasoning": str, "suggestions": [], "issues": []}}
        """

    def _calculate_cost(self, usage, model: str) -> float:
        # Together.ai has very low costs
        return (usage.total_tokens * 0.0001) / 1000 if usage else 0.0


class OpenRouterValidator(AIValidator):
    """OpenRouter Validator (Access to all models)"""

    def __init__(self, api_key: str = None):
        super().__init__(AIProvider.OPENROUTER, api_key)
        self.models = [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o",
            "google/gemini-pro-1.5",
            "meta-llama/llama-3.1-405b-instruct"
        ]

    async def validate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any],
        model: str = None
    ) -> AIValidationResult:
        """OpenRouter validation implementation"""
        model = model or self.models[0]
        start_time = datetime.utcnow()

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are an expert validator. Respond with valid JSON."},
                            {"role": "user", "content": self._build_validation_prompt(gate, context)}
                        ],
                        "temperature": 0.1
                    },
                    timeout=60.0
                )

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                import re
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = {"passed": False, "confidence": 0.0, "reasoning": content}

                execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

                return AIValidationResult(
                    provider=self.provider,
                    model=model,
                    passed=result.get("passed", False),
                    confidence=result.get("confidence", 0.0),
                    reasoning=result.get("reasoning", ""),
                    suggestions=result.get("suggestions", []),
                    issues_found=result.get("issues", []),
                    execution_time_ms=execution_time,
                    tokens_used=data.get("usage", {}).get("total_tokens", 0),
                    cost_usd=0.0  # OpenRouter handles billing separately
                )
        except Exception as e:
            logger.error(f"OpenRouter validation error: {e}")
            return AIValidationResult(
                provider=self.provider,
                model=model,
                passed=False,
                confidence=0.0,
                reasoning=f"Validation error: {str(e)}",
                execution_time_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000)
            )

    async def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        pass

    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        pass

    async def evaluate_ux(self, ui_description: str) -> Dict[str, Any]:
        pass

    def _build_validation_prompt(self, gate: ValidationGate, context: Dict[str, Any]) -> str:
        return f"""
        Validate for {gate.value}:

        {json.dumps(context, indent=2, default=str)}

        Respond with JSON: {{"passed": bool, "confidence": 0-1, "reasoning": str, "suggestions": [], "issues": []}}
        """


# ============================================
# CONSENSUS ENGINE
# ============================================

class ConsensusEngine:
    """Multi-AI Consensus Engine for validation agreement"""

    def __init__(self, required_level: ConsensusLevel = ConsensusLevel.SUPERMAJORITY):
        self.required_level = required_level
        self.weights = {
            AIProvider.ANTHROPIC: 1.2,   # Highest weight for Claude (known for accuracy)
            AIProvider.OPENAI: 1.1,       # High weight for GPT-4
            AIProvider.GOOGLE: 1.0,       # Standard weight
            AIProvider.OPENROUTER: 0.9,   # Aggregator, slightly lower
            AIProvider.TOGETHER: 0.8,     # Open source
            AIProvider.HUGGINGFACE: 0.8,
            AIProvider.COHERE: 0.9,
            AIProvider.DEEPSEEK: 0.9
        }

    def calculate_consensus(self, results: List[AIValidationResult]) -> Tuple[bool, float, str]:
        """
        Calculate consensus from multiple AI results.
        Returns: (consensus_reached, confidence_score, reasoning)
        """
        if not results:
            return False, 0.0, "No results to evaluate"

        total_weight = 0.0
        weighted_pass_score = 0.0
        weighted_confidence = 0.0

        for result in results:
            weight = self.weights.get(result.provider, 1.0)
            total_weight += weight

            if result.passed:
                weighted_pass_score += weight * result.confidence
            weighted_confidence += weight * result.confidence

        # Calculate weighted average
        if total_weight > 0:
            pass_ratio = weighted_pass_score / total_weight
            avg_confidence = weighted_confidence / total_weight
        else:
            pass_ratio = 0.0
            avg_confidence = 0.0

        # Determine if consensus is reached
        thresholds = {
            ConsensusLevel.UNANIMOUS: 1.0,
            ConsensusLevel.SUPERMAJORITY: 0.75,
            ConsensusLevel.MAJORITY: 0.5,
            ConsensusLevel.ANY: 0.0
        }

        threshold = thresholds[self.required_level]
        passed_count = sum(1 for r in results if r.passed)
        total_count = len(results)

        consensus_reached = (passed_count / total_count) >= threshold

        reasoning = f"Consensus: {passed_count}/{total_count} AIs passed ({passed_count/total_count*100:.1f}%). "
        reasoning += f"Required: {threshold*100:.0f}% for {self.required_level.value}. "
        reasoning += f"Weighted confidence: {avg_confidence:.2f}"

        return consensus_reached, avg_confidence, reasoning

    def generate_aggregated_report(self, results: List[AIValidationResult]) -> Dict[str, Any]:
        """Generate aggregated report from all AI validations"""
        consensus, confidence, reasoning = self.calculate_consensus(results)

        # Collect all unique issues
        all_issues = []
        issue_counts = {}
        for result in results:
            for issue in result.issues_found:
                issue_key = issue.get("description", str(issue))
                if issue_key not in issue_counts:
                    issue_counts[issue_key] = 0
                    all_issues.append(issue)
                issue_counts[issue_key] += 1

        # Sort by frequency
        all_issues.sort(key=lambda x: issue_counts.get(x.get("description", ""), 0), reverse=True)

        # Collect all unique suggestions
        all_suggestions = []
        seen_suggestions = set()
        for result in results:
            for suggestion in result.suggestions:
                if suggestion not in seen_suggestions:
                    seen_suggestions.add(suggestion)
                    all_suggestions.append(suggestion)

        return {
            "consensus_reached": consensus,
            "confidence": confidence,
            "reasoning": reasoning,
            "issues": all_issues[:10],  # Top 10 issues
            "suggestions": all_suggestions[:10],  # Top 10 suggestions
            "ai_breakdown": [
                {
                    "provider": r.provider.value,
                    "model": r.model,
                    "passed": r.passed,
                    "confidence": r.confidence
                }
                for r in results
            ]
        }


# ============================================
# TRUTH LOG
# ============================================

class ImmutableTruthLog:
    """Immutable truth log with cryptographic verification"""

    def __init__(self, log_path: Path = None):
        self.log_path = log_path or Path("truth_log.json")
        self.entries: List[Dict[str, Any]] = []
        self.chain_hash = ""

    def add_entry(self, entry: Dict[str, Any]) -> str:
        """Add entry to truth log and return hash"""
        timestamp = datetime.utcnow().isoformat()

        log_entry = {
            "timestamp": timestamp,
            "previous_hash": self.chain_hash,
            "data": entry
        }

        # Calculate hash
        entry_string = json.dumps(log_entry, sort_keys=True, default=str)
        entry_hash = hashlib.sha256(entry_string.encode()).hexdigest()

        log_entry["hash"] = entry_hash
        self.entries.append(log_entry)
        self.chain_hash = entry_hash

        # Persist to file
        self._save()

        return entry_hash

    def verify_chain(self) -> bool:
        """Verify the integrity of the truth log chain"""
        previous_hash = ""

        for entry in self.entries:
            # Verify previous hash
            if entry["previous_hash"] != previous_hash:
                return False

            # Verify entry hash
            entry_data = {
                "timestamp": entry["timestamp"],
                "previous_hash": entry["previous_hash"],
                "data": entry["data"]
            }
            entry_string = json.dumps(entry_data, sort_keys=True, default=str)
            calculated_hash = hashlib.sha256(entry_string.encode()).hexdigest()

            if entry["hash"] != calculated_hash:
                return False

            previous_hash = entry["hash"]

        return True

    def _save(self):
        """Save log to file"""
        with open(self.log_path, 'w') as f:
            json.dump({
                "chain_hash": self.chain_hash,
                "entries": self.entries
            }, f, indent=2, default=str)

    def load(self):
        """Load log from file"""
        if self.log_path.exists():
            with open(self.log_path, 'r') as f:
                data = json.load(f)
                self.chain_hash = data.get("chain_hash", "")
                self.entries = data.get("entries", [])


# ============================================
# OMNIS-2 VALIDATION SYSTEM
# ============================================

class OMNIS2ValidationSystem:
    """
    OMNIS-2: Omniscient Multi-AI Convergence, Validation & Release Authority System

    The ultimate validation system for production-grade AI applications.
    """

    def __init__(
        self,
        project_name: str = "Taj Chat",
        version: str = "1.0.0",
        consensus_level: ConsensusLevel = ConsensusLevel.SUPERMAJORITY
    ):
        self.project_name = project_name
        self.version = version
        self.validators: Dict[AIProvider, AIValidator] = {}
        self.consensus_engine = ConsensusEngine(consensus_level)
        self.truth_log = ImmutableTruthLog(Path("omnis_truth_log.json"))

        # Gate configurations
        self.gate_configs: Dict[ValidationGate, Dict[str, Any]] = {
            ValidationGate.GATE_01_SYNTAX: {
                "required_providers": [AIProvider.OPENAI, AIProvider.ANTHROPIC],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": True
            },
            ValidationGate.GATE_02_SECURITY: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI, AIProvider.GOOGLE],
                "consensus_level": ConsensusLevel.SUPERMAJORITY,
                "blocking": True
            },
            ValidationGate.GATE_03_PERFORMANCE: {
                "required_providers": [AIProvider.OPENAI, AIProvider.TOGETHER],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": False
            },
            ValidationGate.GATE_04_TESTING: {
                "required_providers": [AIProvider.ANTHROPIC],
                "consensus_level": ConsensusLevel.ANY,
                "blocking": True
            },
            ValidationGate.GATE_05_DEPENDENCIES: {
                "required_providers": [AIProvider.OPENAI],
                "consensus_level": ConsensusLevel.ANY,
                "blocking": True
            },
            ValidationGate.GATE_06_DOCUMENTATION: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.GOOGLE],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": False
            },
            ValidationGate.GATE_07_ACCESSIBILITY: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": False
            },
            ValidationGate.GATE_08_UX: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI, AIProvider.GOOGLE],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": False
            },
            ValidationGate.GATE_09_CONTENT_SAFETY: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI, AIProvider.GOOGLE],
                "consensus_level": ConsensusLevel.SUPERMAJORITY,
                "blocking": True
            },
            ValidationGate.GATE_10_COMPLIANCE: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI],
                "consensus_level": ConsensusLevel.SUPERMAJORITY,
                "blocking": True
            },
            ValidationGate.GATE_11_SCALABILITY: {
                "required_providers": [AIProvider.OPENAI, AIProvider.TOGETHER],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": False
            },
            ValidationGate.GATE_12_INTEGRATION: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": True
            },
            ValidationGate.GATE_13_COMPETITIVE: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI, AIProvider.GOOGLE],
                "consensus_level": ConsensusLevel.MAJORITY,
                "blocking": False
            },
            ValidationGate.GATE_14_ADVERSARIAL: {
                "required_providers": [AIProvider.ANTHROPIC, AIProvider.OPENAI],
                "consensus_level": ConsensusLevel.UNANIMOUS,
                "blocking": True
            },
            ValidationGate.GATE_15_CONSENSUS: {
                "required_providers": list(AIProvider),  # All providers
                "consensus_level": ConsensusLevel.SUPERMAJORITY,
                "blocking": True
            }
        }

    def register_validator(self, validator: AIValidator):
        """Register an AI validator"""
        self.validators[validator.provider] = validator
        logger.info(f"Registered validator: {validator.provider.value}")

    async def validate_gate(
        self,
        gate: ValidationGate,
        context: Dict[str, Any]
    ) -> GateResult:
        """Validate a single gate using multiple AI providers"""
        start_time = datetime.utcnow()
        config = self.gate_configs.get(gate, {})
        required_providers = config.get("required_providers", [AIProvider.OPENAI])
        gate_consensus_level = config.get("consensus_level", ConsensusLevel.MAJORITY)

        # Run validations in parallel
        tasks = []
        for provider in required_providers:
            if provider in self.validators:
                tasks.append(self.validators[provider].validate(gate, context))

        if not tasks:
            return GateResult(
                gate=gate,
                status=ValidationStatus.BLOCKED,
                blocking_issues=["No validators available for this gate"]
            )

        ai_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [
            r for r in ai_results
            if isinstance(r, AIValidationResult)
        ]

        # Calculate consensus
        consensus_engine = ConsensusEngine(gate_consensus_level)
        consensus_reached, confidence, reasoning = consensus_engine.calculate_consensus(valid_results)

        # Aggregate issues and suggestions
        all_issues = []
        all_warnings = []
        all_suggestions = []

        for result in valid_results:
            for issue in result.issues_found:
                severity = issue.get("severity", "medium")
                if severity == "high":
                    all_issues.append(f"[{result.provider.value}] {issue.get('description', str(issue))}")
                else:
                    all_warnings.append(f"[{result.provider.value}] {issue.get('description', str(issue))}")
            all_suggestions.extend(result.suggestions)

        # Determine status
        if consensus_reached and all(r.passed for r in valid_results):
            status = ValidationStatus.PASSED
        elif consensus_reached:
            status = ValidationStatus.WARNING
        else:
            status = ValidationStatus.FAILED

        execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        # Log to truth log
        self.truth_log.add_entry({
            "gate": gate.value,
            "status": status.value,
            "consensus": consensus_reached,
            "confidence": confidence,
            "ai_count": len(valid_results)
        })

        return GateResult(
            gate=gate,
            status=status,
            ai_results=valid_results,
            consensus_reached=consensus_reached,
            consensus_level=gate_consensus_level,
            aggregated_score=confidence,
            blocking_issues=all_issues,
            warnings=all_warnings,
            recommendations=list(set(all_suggestions))[:10],
            execution_time_ms=execution_time
        )

    async def run_full_validation(
        self,
        context: Dict[str, Any],
        gates: List[ValidationGate] = None
    ) -> ValidationReport:
        """Run full validation across all gates"""
        start_time = datetime.utcnow()

        gates = gates or list(ValidationGate)
        report_id = hashlib.sha256(
            f"{self.project_name}-{self.version}-{start_time.isoformat()}".encode()
        ).hexdigest()[:16]

        report = ValidationReport(
            report_id=report_id,
            project_name=self.project_name,
            version=self.version
        )

        # Run gates sequentially (blocking gates stop the process)
        for gate in gates:
            logger.info(f"Running gate: {gate.value}")

            gate_result = await self.validate_gate(gate, context)
            report.gates[gate] = gate_result

            # Check if this is a blocking gate that failed
            config = self.gate_configs.get(gate, {})
            if config.get("blocking", False) and gate_result.status == ValidationStatus.FAILED:
                report.overall_status = ValidationStatus.BLOCKED
                report.blocking_issues += 1
                logger.warning(f"Blocking gate failed: {gate.value}")
                break

            if gate_result.status == ValidationStatus.FAILED:
                report.total_issues += len(gate_result.blocking_issues)
            if gate_result.status == ValidationStatus.WARNING:
                report.warnings += len(gate_result.warnings)

        # Calculate overall status
        if report.overall_status != ValidationStatus.BLOCKED:
            passed_gates = sum(1 for g in report.gates.values() if g.status == ValidationStatus.PASSED)
            total_gates = len(report.gates)

            if passed_gates == total_gates:
                report.overall_status = ValidationStatus.PASSED
            elif passed_gates >= total_gates * 0.75:
                report.overall_status = ValidationStatus.WARNING
            else:
                report.overall_status = ValidationStatus.FAILED

            report.overall_score = passed_gates / total_gates if total_gates > 0 else 0.0

        # Calculate totals
        report.total_execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        report.total_cost_usd = sum(
            sum(r.cost_usd for r in g.ai_results)
            for g in report.gates.values()
        )

        # Sign the report
        report.truth_log_hash = self.truth_log.chain_hash
        report.signed_by = [v.provider.value for v in self.validators.values()]

        # Final truth log entry
        self.truth_log.add_entry({
            "event": "validation_complete",
            "report_id": report_id,
            "status": report.overall_status.value,
            "score": report.overall_score,
            "signed_by": report.signed_by
        })

        return report

    def generate_markdown_report(self, report: ValidationReport) -> str:
        """Generate a markdown report from validation results"""
        status_emoji = {
            ValidationStatus.PASSED: "✅",
            ValidationStatus.FAILED: "❌",
            ValidationStatus.WARNING: "⚠️",
            ValidationStatus.BLOCKED: "🚫",
            ValidationStatus.PENDING: "⏳",
            ValidationStatus.RUNNING: "🔄"
        }

        md = f"""# OMNIS-2 Validation Report
## {self.project_name} v{self.version}

**Report ID:** `{report.report_id}`
**Status:** {status_emoji[report.overall_status]} {report.overall_status.value.upper()}
**Score:** {report.overall_score * 100:.1f}%
**Generated:** {report.created_at.isoformat()}
**Truth Log Hash:** `{report.truth_log_hash[:16]}...`

---

## Summary

| Metric | Value |
|--------|-------|
| Total Gates | {len(report.gates)} |
| Passed | {sum(1 for g in report.gates.values() if g.status == ValidationStatus.PASSED)} |
| Warnings | {report.warnings} |
| Blocking Issues | {report.blocking_issues} |
| Execution Time | {report.total_execution_time_ms}ms |
| Total Cost | ${report.total_cost_usd:.4f} |

---

## Gate Results

"""

        for gate, result in report.gates.items():
            md += f"""### {status_emoji[result.status]} Gate: {gate.value.replace('_', ' ').title()}

**Status:** {result.status.value} | **Consensus:** {"✅" if result.consensus_reached else "❌"} | **Confidence:** {result.aggregated_score:.2f}

"""

            if result.ai_results:
                md += "| AI Provider | Model | Passed | Confidence |\n"
                md += "|------------|-------|--------|------------|\n"
                for ai in result.ai_results:
                    md += f"| {ai.provider.value} | {ai.model} | {'✅' if ai.passed else '❌'} | {ai.confidence:.2f} |\n"
                md += "\n"

            if result.blocking_issues:
                md += "**Blocking Issues:**\n"
                for issue in result.blocking_issues:
                    md += f"- 🚫 {issue}\n"
                md += "\n"

            if result.warnings:
                md += "**Warnings:**\n"
                for warning in result.warnings[:5]:
                    md += f"- ⚠️ {warning}\n"
                md += "\n"

            if result.recommendations:
                md += "**Recommendations:**\n"
                for rec in result.recommendations[:5]:
                    md += f"- 💡 {rec}\n"
                md += "\n"

            md += "---\n\n"

        md += f"""
## Signed By

{', '.join(f'**{s.upper()}**' for s in report.signed_by)}

---

*OMNIS-2: Omniscient Multi-AI Convergence, Validation & Release Authority System*
*Truth log chain verified: {self.truth_log.verify_chain()}*
"""

        return md


# ============================================
# FACTORY FUNCTION
# ============================================

async def create_omnis_validator(
    openai_key: str = None,
    anthropic_key: str = None,
    google_key: str = None,
    together_key: str = None,
    openrouter_key: str = None,
    project_name: str = "Taj Chat",
    version: str = "1.0.0"
) -> OMNIS2ValidationSystem:
    """Factory function to create and configure OMNIS-2 validator"""

    import os

    system = OMNIS2ValidationSystem(
        project_name=project_name,
        version=version,
        consensus_level=ConsensusLevel.SUPERMAJORITY
    )

    # Register available validators
    if openai_key or os.getenv("OPENAI_API_KEY"):
        system.register_validator(
            OpenAIValidator(openai_key or os.getenv("OPENAI_API_KEY"))
        )

    if anthropic_key or os.getenv("ANTHROPIC_API_KEY"):
        system.register_validator(
            AnthropicValidator(anthropic_key or os.getenv("ANTHROPIC_API_KEY"))
        )

    if google_key or os.getenv("GOOGLE_API_KEY"):
        system.register_validator(
            GoogleValidator(google_key or os.getenv("GOOGLE_API_KEY"))
        )

    if together_key or os.getenv("TOGETHER_API_KEY"):
        system.register_validator(
            TogetherValidator(together_key or os.getenv("TOGETHER_API_KEY"))
        )

    if openrouter_key or os.getenv("OPENROUTER_API_KEY"):
        system.register_validator(
            OpenRouterValidator(openrouter_key or os.getenv("OPENROUTER_API_KEY"))
        )

    return system


# ============================================
# CLI ENTRY POINT
# ============================================

if __name__ == "__main__":
    async def main():
        # Create validator
        validator = await create_omnis_validator(
            project_name="Taj Chat",
            version="2.0.0"
        )

        # Sample context for validation
        context = {
            "project": "Taj Chat",
            "description": "AI-powered video creation platform",
            "features": [
                "10 AI agents",
                "7 social platforms",
                "9 AI providers",
                "Sequential/parallel workflows"
            ],
            "competitors": [
                "Opus Clip", "Pictory", "Synthesia",
                "InVideo", "Lumen5", "Descript",
                "Kapwing", "HeyGen", "Runway", "Pika"
            ]
        }

        # Run validation
        report = await validator.run_full_validation(context)

        # Generate markdown report
        md_report = validator.generate_markdown_report(report)
        print(md_report)

        # Save report
        with open("OMNIS2_VALIDATION_REPORT.md", "w") as f:
            f.write(md_report)

    asyncio.run(main())
