"""
Database Connection for Taj Chat

Handles PostgreSQL connection using asyncpg for async operations.
"""

import os
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator

import asyncpg
from dotenv import load_dotenv

# Load credentials
CREDENTIALS_PATH = Path("C:/dev/infra/credentials/connected")
for env_file in CREDENTIALS_PATH.glob("*.env"):
    load_dotenv(env_file)

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_CNBSu9nakz7G@ep-restless-paper-ahj5dyl5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

# Connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """Get or create the connection pool."""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=2,
            max_size=10,
            command_timeout=60,
        )
    return _pool


async def close_pool():
    """Close the connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


@asynccontextmanager
async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get a database connection from the pool."""
    pool = await get_pool()
    async with pool.acquire() as connection:
        yield connection


async def init_db():
    """Initialize the database with schema."""
    schema_path = Path(__file__).parent / "schema.sql"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    schema_sql = schema_path.read_text()

    async with get_db() as conn:
        await conn.execute(schema_sql)
        print("✅ Database schema initialized successfully")


async def check_connection() -> bool:
    """Check if database connection is working."""
    try:
        async with get_db() as conn:
            result = await conn.fetchval("SELECT 1")
            return result == 1
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def get_table_count() -> int:
    """Get count of Taj Chat tables."""
    async with get_db() as conn:
        result = await conn.fetchval("""
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN (
                'users', 'user_settings', 'videos', 'video_assets',
                'video_tracks', 'video_clips', 'generation_jobs',
                'ai_agents', 'social_accounts', 'scheduled_posts',
                'published_posts', 'video_analytics', 'platform_analytics',
                'templates', 'music_tracks'
            )
        """)
        return result or 0
