"""
Taj Chat Database Migration Script

Run this script to create all necessary tables for the AI Video Creation Platform.

Usage:
    python -m app.database.migrate
"""

import asyncio
import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

# Load credentials
CREDENTIALS_PATH = Path("C:/dev/infra/credentials/connected")
for env_file in CREDENTIALS_PATH.glob("*.env"):
    load_dotenv(env_file)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_CNBSu9nakz7G@ep-restless-paper-ahj5dyl5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
)


async def run_migration():
    """Run the database migration."""
    print("🚀 Starting Taj Chat database migration...")

    # Read schema
    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        print(f"❌ Schema file not found: {schema_path}")
        return False

    schema_sql = schema_path.read_text()

    try:
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to database")

        # Run schema
        await conn.execute(schema_sql)
        print("✅ Schema executed successfully")

        # Verify tables
        tables = await conn.fetch("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        taj_tables = [t['table_name'] for t in tables if t['table_name'].startswith('taj_') or t['table_name'] in [
            'users', 'user_settings', 'videos', 'video_assets', 'video_tracks',
            'video_clips', 'generation_jobs', 'ai_agents', 'social_accounts',
            'scheduled_posts', 'published_posts', 'video_analytics',
            'platform_analytics', 'templates', 'music_tracks'
        ]]

        print(f"\n📊 Taj Chat Tables Created: {len(taj_tables)}")
        for table in taj_tables:
            print(f"   ✅ {table}")

        # Check AI agents
        agents = await conn.fetch("SELECT name, status FROM ai_agents ORDER BY name")
        print(f"\n🤖 AI Agents: {len(agents)}")
        for agent in agents:
            print(f"   ✅ {agent['name']} ({agent['status']})")

        await conn.close()
        print("\n✅ Migration completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(run_migration())
