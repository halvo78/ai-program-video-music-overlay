"""
Taj Chat Configuration

Loads credentials from C:/dev/infra/credentials/connected/
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

# Load credentials from dev infrastructure
CREDENTIALS_PATH = Path("C:/dev/infra/credentials/connected")

# Load all env files
for env_file in CREDENTIALS_PATH.glob("*.env"):
    load_dotenv(env_file)


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

    # Storage paths
    storage_path: Path = field(default_factory=lambda: Path("C:/dev/taj-chat/generated"))
    temp_path: Path = field(default_factory=lambda: Path("C:/dev/taj-chat/temp"))

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
