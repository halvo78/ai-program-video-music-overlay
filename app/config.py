"""
Taj Chat Configuration

Supports loading credentials from:
1. AWS Secrets Manager (production)
2. Environment variables
3. Local .env files (development)
"""

import os
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Try to load from AWS Secrets Manager first
def load_aws_secrets():
    """Load secrets from AWS Secrets Manager."""
    try:
        import boto3
        from botocore.exceptions import ClientError

        # Get secret names from environment or use defaults
        secret_names = os.getenv("AWS_SECRET_NAMES", "taj-chat/api-keys,taj-chat/social-keys").split(",")
        region = os.getenv("AWS_REGION", "us-east-1")

        client = boto3.client("secretsmanager", region_name=region)

        for secret_name in secret_names:
            try:
                response = client.get_secret_value(SecretId=secret_name.strip())
                secret_data = json.loads(response["SecretString"])

                # Load all keys into environment
                for key, value in secret_data.items():
                    if value:
                        os.environ[key] = str(value)

                logger.info(f"✅ Loaded secrets from AWS: {secret_name}")

            except ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    logger.warning(f"Secret not found: {secret_name}")
                else:
                    logger.error(f"AWS Secrets error: {e}")

    except ImportError:
        logger.info("boto3 not installed - skipping AWS Secrets Manager")
    except Exception as e:
        logger.warning(f"Could not load AWS secrets: {e}")


# Try AWS Secrets first
load_aws_secrets()

# Then load from local .env files as fallback
CREDENTIALS_PATH = Path(os.getenv("CREDENTIALS_PATH", "C:/dev/infra/credentials/connected"))
if CREDENTIALS_PATH.exists():
    for env_file in CREDENTIALS_PATH.glob("*.env"):
        load_dotenv(env_file)
        logger.info(f"Loaded: {env_file.name}")

# Also load from current directory .env
load_dotenv()


@dataclass
class AIProviders:
    """AI Provider API keys and configurations."""

    # OpenAI
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    # Anthropic Claude
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # Google Gemini
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = "gemini-2.0-flash-exp"

    # OpenRouter (50+ models)
    openrouter_api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # Together.ai
    together_api_key: str = field(default_factory=lambda: os.getenv("TOGETHER_AI_API_KEY", ""))
    together_base_url: str = "https://api.together.xyz"

    # HuggingFace Pro
    hf_token: str = field(default_factory=lambda: os.getenv("HF_TOKEN_PRO", ""))
    hf_token_alt: str = field(default_factory=lambda: os.getenv("HF_TOKEN_ALT", ""))
    hf_username: str = field(default_factory=lambda: os.getenv("HUGGINGFACE_USERNAME", "Halvo78"))
    hf_base_url: str = "https://api-inference.huggingface.co"

    # BFL/FLUX (Image Generation)
    flux_api_key: str = field(default_factory=lambda: os.getenv("BFL_API_KEY", ""))
    flux_base_url: str = "https://api.bfl.ai"
    flux_models: list = field(default_factory=lambda: ["flux-pro-1.1", "flux-dev", "flux-schnell"])

    # Cohere
    cohere_api_key: str = field(default_factory=lambda: os.getenv("COHERE_API_KEY", ""))

    # DeepSeek
    deepseek_api_key: str = field(default_factory=lambda: os.getenv("DEEPSEEK_API_KEY", ""))

    # ElevenLabs (Voice Cloning)
    elevenlabs_api_key: str = field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""))

    # HeyGen (AI Avatars)
    heygen_api_key: str = field(default_factory=lambda: os.getenv("HEYGEN_API_KEY", ""))

    # D-ID (AI Avatars - backup)
    did_api_key: str = field(default_factory=lambda: os.getenv("DID_API_KEY", ""))

    # Synthesia (AI Avatars - enterprise)
    synthesia_api_key: str = field(default_factory=lambda: os.getenv("SYNTHESIA_API_KEY", ""))

    # AssemblyAI (Transcription)
    assembly_ai_key: str = field(default_factory=lambda: os.getenv("ASSEMBLYAI_API_KEY", ""))

    # Deepgram (Transcription)
    deepgram_api_key: str = field(default_factory=lambda: os.getenv("DEEPGRAM_API_KEY", ""))

    # Pexels (Stock Video B-Roll)
    pexels_api_key: str = field(default_factory=lambda: os.getenv("PEXELS_API_KEY", ""))

    # Pixabay (Stock Video B-Roll)
    pixabay_api_key: str = field(default_factory=lambda: os.getenv("PIXABAY_API_KEY", ""))


@dataclass
class SocialMedia:
    """Social media API credentials."""

    # Twitter/X - Full API v2
    twitter_api_key: str = field(default_factory=lambda: os.getenv("TWITTER_API_KEY", ""))
    twitter_api_secret: str = field(default_factory=lambda: os.getenv("TWITTER_API_SECRET", ""))
    twitter_access_token: str = field(default_factory=lambda: os.getenv("TWITTER_ACCESS_TOKEN", ""))
    twitter_access_secret: str = field(default_factory=lambda: os.getenv("TWITTER_ACCESS_SECRET", ""))
    twitter_bearer_token: str = field(default_factory=lambda: os.getenv("TWITTER_BEARER_TOKEN", ""))
    twitter_client_id: str = field(default_factory=lambda: os.getenv("TWITTER_CLIENT_ID", ""))
    twitter_client_secret: str = field(default_factory=lambda: os.getenv("TWITTER_CLIENT_SECRET", ""))

    # YouTube - Full Data API v3 + Analytics + Live
    youtube_api_key: str = field(default_factory=lambda: os.getenv("YOUTUBE_API_KEY", ""))
    youtube_client_id: str = field(default_factory=lambda: os.getenv("YOUTUBE_CLIENT_ID", ""))
    youtube_client_secret: str = field(default_factory=lambda: os.getenv("YOUTUBE_CLIENT_SECRET", ""))
    youtube_refresh_token: str = field(default_factory=lambda: os.getenv("YOUTUBE_REFRESH_TOKEN", ""))
    youtube_access_token: str = field(default_factory=lambda: os.getenv("YOUTUBE_ACCESS_TOKEN", ""))
    youtube_channel_id: str = field(default_factory=lambda: os.getenv("YOUTUBE_CHANNEL_ID", ""))

    # Meta (Facebook + Instagram + Threads)
    meta_app_id: str = field(default_factory=lambda: os.getenv("META_APP_ID", ""))
    meta_app_secret: str = field(default_factory=lambda: os.getenv("META_APP_SECRET", ""))
    meta_access_token: str = field(default_factory=lambda: os.getenv("META_ACCESS_TOKEN", ""))
    facebook_page_id: str = field(default_factory=lambda: os.getenv("FACEBOOK_PAGE_ID", ""))
    facebook_client_token: str = field(default_factory=lambda: os.getenv("FACEBOOK_CLIENT_TOKEN", ""))
    facebook_page_access_token: str = field(default_factory=lambda: os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", ""))
    instagram_account_id: str = field(default_factory=lambda: os.getenv("INSTAGRAM_ACCOUNT_ID", ""))
    instagram_access_token: str = field(default_factory=lambda: os.getenv("INSTAGRAM_ACCESS_TOKEN", ""))

    # Threads
    threads_app_id: str = field(default_factory=lambda: os.getenv("THREADS_APP_ID", ""))
    threads_app_secret: str = field(default_factory=lambda: os.getenv("THREADS_APP_SECRET", ""))
    threads_app_token: str = field(default_factory=lambda: os.getenv("THREADS_APP_TOKEN", ""))
    threads_access_token: str = field(default_factory=lambda: os.getenv("THREADS_ACCESS_TOKEN", ""))
    threads_user_id: str = field(default_factory=lambda: os.getenv("THREADS_USER_ID", ""))

    # TikTok - Content Posting API + Login Kit
    tiktok_org_id: str = field(default_factory=lambda: os.getenv("TIKTOK_ORG_ID", ""))
    tiktok_client_key: str = field(default_factory=lambda: os.getenv("TIKTOK_CLIENT_KEY", ""))
    tiktok_client_secret: str = field(default_factory=lambda: os.getenv("TIKTOK_CLIENT_SECRET", ""))
    tiktok_access_token: str = field(default_factory=lambda: os.getenv("TIKTOK_ACCESS_TOKEN", ""))
    tiktok_refresh_token: str = field(default_factory=lambda: os.getenv("TIKTOK_REFRESH_TOKEN", ""))
    tiktok_open_id: str = field(default_factory=lambda: os.getenv("TIKTOK_OPEN_ID", ""))

    # Telegram
    telegram_bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))


@dataclass
class Database:
    """Database configurations."""

    # PostgreSQL (Neon)
    postgres_url: str = field(default_factory=lambda: os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_CNBSu9nakz7G@ep-restless-paper-ahj5dyl5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
    ))

    # Redis (for message bus)
    redis_url: str = field(default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379"))


@dataclass
class AppSettings:
    """Application settings."""

    app_name: str = "Taj Chat"
    version: str = "1.0.0"
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Storage paths (use environment variables for cloud deployment)
    storage_path: Path = field(default_factory=lambda: Path(os.getenv("STORAGE_PATH", "/tmp/taj-chat/generated")))
    temp_path: Path = field(default_factory=lambda: Path(os.getenv("TEMP_PATH", "/tmp/taj-chat/temp")))

    # S3/Cloud Storage (production)
    s3_bucket: str = field(default_factory=lambda: os.getenv("S3_BUCKET", ""))
    s3_region: str = field(default_factory=lambda: os.getenv("AWS_REGION", "us-east-1"))
    cloudfront_domain: str = field(default_factory=lambda: os.getenv("CLOUDFRONT_DOMAIN", ""))

    # Video settings
    default_video_format: str = "mp4"
    default_video_codec: str = "h264"
    default_audio_codec: str = "aac"

    # Platform specs
    platform_specs: dict = field(default_factory=lambda: {
        "tiktok": {"width": 1080, "height": 1920, "fps": 30, "max_duration": 180},
        "instagram_reels": {"width": 1080, "height": 1920, "fps": 30, "max_duration": 90},
        "youtube_shorts": {"width": 1080, "height": 1920, "fps": 60, "max_duration": 60},
        "twitter": {"width": 1280, "height": 720, "fps": 30, "max_duration": 140},
    })


@dataclass
class Config:
    """Main configuration class."""

    ai: AIProviders = field(default_factory=AIProviders)
    social: SocialMedia = field(default_factory=SocialMedia)
    database: Database = field(default_factory=Database)
    app: AppSettings = field(default_factory=AppSettings)

    def validate(self) -> dict:
        """Validate configuration and return status."""
        status = {
            "ai_providers": {
                "openai": bool(self.ai.openai_api_key),
                "anthropic": bool(self.ai.anthropic_api_key),
                "gemini": bool(self.ai.gemini_api_key),
                "openrouter": bool(self.ai.openrouter_api_key),
                "together": bool(self.ai.together_api_key),
                "huggingface": bool(self.ai.hf_token),
                "flux": bool(self.ai.flux_api_key),
                "cohere": bool(self.ai.cohere_api_key),
                "deepseek": bool(self.ai.deepseek_api_key),
            },
            "competitor_features": {
                "elevenlabs": bool(self.ai.elevenlabs_api_key),  # Voice Cloning
                "heygen": bool(self.ai.heygen_api_key),          # AI Avatars
                "did": bool(self.ai.did_api_key),                # AI Avatars (backup)
                "synthesia": bool(self.ai.synthesia_api_key),    # AI Avatars (enterprise)
                "assemblyai": bool(self.ai.assembly_ai_key),     # Transcription
                "deepgram": bool(self.ai.deepgram_api_key),      # Transcription
                "pexels": bool(self.ai.pexels_api_key),          # Stock B-Roll
                "pixabay": bool(self.ai.pixabay_api_key),        # Stock B-Roll
            },
            "social_media": {
                "twitter": bool(self.social.twitter_bearer_token),
                "youtube": bool(self.social.youtube_api_key),
                "telegram": bool(self.social.telegram_bot_token),
                "meta": bool(self.social.meta_access_token),
                "facebook": bool(self.social.facebook_page_id),
                "instagram": bool(self.social.instagram_account_id),
                "tiktok": bool(self.social.tiktok_client_key),
            },
            "database": {
                "postgres": bool(self.database.postgres_url),
                "redis": bool(self.database.redis_url),
            }
        }
        return status


# Global config instance
config = Config()


def get_config() -> Config:
    """Get the global configuration."""
    return config
