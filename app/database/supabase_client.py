"""
Taj Chat Supabase Client

Handles all database operations for the AI Video Creation Platform.
Uses Supabase for storage, auth, and real-time features.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from dotenv import load_dotenv
from supabase import create_client, Client

# Load credentials
CREDENTIALS_PATH = Path("C:/dev/infra/credentials/connected")
for env_file in CREDENTIALS_PATH.glob("*.env"):
    load_dotenv(env_file)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://cmwelibfxzplxjzspryh.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

# Global client
_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get or create the Supabase client."""
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not configured")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ============================================
# VIDEO OPERATIONS
# ============================================

async def create_video(user_id: str, title: str, prompt: str = None, **kwargs) -> Dict:
    """Create a new video."""
    client = get_supabase()
    data = {
        "user_id": user_id,
        "title": title,
        "prompt": prompt,
        "status": "draft",
        **kwargs
    }
    result = client.table("videos").insert(data).execute()
    return result.data[0] if result.data else None


async def get_video(video_id: str) -> Optional[Dict]:
    """Get a video by ID."""
    client = get_supabase()
    result = client.table("videos").select("*").eq("id", video_id).single().execute()
    return result.data


async def get_user_videos(user_id: str, status: str = None, limit: int = 50) -> List[Dict]:
    """Get all videos for a user."""
    client = get_supabase()
    query = client.table("videos").select("*").eq("user_id", user_id)
    if status:
        query = query.eq("status", status)
    result = query.order("created_at", desc=True).limit(limit).execute()
    return result.data or []


async def update_video(video_id: str, **updates) -> Dict:
    """Update a video."""
    client = get_supabase()
    result = client.table("videos").update(updates).eq("id", video_id).execute()
    return result.data[0] if result.data else None


async def delete_video(video_id: str) -> bool:
    """Delete a video."""
    client = get_supabase()
    result = client.table("videos").delete().eq("id", video_id).execute()
    return len(result.data) > 0


# ============================================
# AI AGENT OPERATIONS
# ============================================

async def get_agents() -> List[Dict]:
    """Get all AI agents."""
    client = get_supabase()
    result = client.table("ai_agents").select("*").order("name").execute()
    return result.data or []


async def get_agent(agent_type: str) -> Optional[Dict]:
    """Get an agent by type."""
    client = get_supabase()
    result = client.table("ai_agents").select("*").eq("agent_type", agent_type).single().execute()
    return result.data


async def update_agent_status(agent_id: str, status: str, current_task: str = None) -> Dict:
    """Update agent status."""
    client = get_supabase()
    updates = {"status": status, "current_task": current_task}
    result = client.table("ai_agents").update(updates).eq("id", agent_id).execute()
    return result.data[0] if result.data else None


# ============================================
# GENERATION JOB OPERATIONS
# ============================================

async def create_generation_job(video_id: str, job_type: str, **kwargs) -> Dict:
    """Create a new generation job."""
    client = get_supabase()
    data = {
        "video_id": video_id,
        "job_type": job_type,
        "status": "pending",
        **kwargs
    }
    result = client.table("generation_jobs").insert(data).execute()
    return result.data[0] if result.data else None


async def update_job_status(job_id: str, status: str, **updates) -> Dict:
    """Update job status."""
    client = get_supabase()
    data = {"status": status, **updates}
    if status == "running":
        data["started_at"] = datetime.utcnow().isoformat()
    elif status in ["completed", "failed"]:
        data["completed_at"] = datetime.utcnow().isoformat()
    result = client.table("generation_jobs").update(data).eq("id", job_id).execute()
    return result.data[0] if result.data else None


# ============================================
# SOCIAL ACCOUNT OPERATIONS
# ============================================

async def get_social_accounts(user_id: str) -> List[Dict]:
    """Get all social accounts for a user."""
    client = get_supabase()
    result = client.table("social_accounts").select("*").eq("user_id", user_id).execute()
    return result.data or []


async def connect_social_account(user_id: str, platform: str, **account_data) -> Dict:
    """Connect a social media account."""
    client = get_supabase()
    data = {
        "user_id": user_id,
        "platform": platform,
        "is_connected": True,
        **account_data
    }
    result = client.table("social_accounts").upsert(data).execute()
    return result.data[0] if result.data else None


# ============================================
# TEMPLATE OPERATIONS
# ============================================

async def get_templates(category: str = None, featured_only: bool = False, limit: int = 50) -> List[Dict]:
    """Get templates."""
    client = get_supabase()
    query = client.table("templates").select("*")
    if category:
        query = query.eq("category", category)
    if featured_only:
        query = query.eq("is_featured", True)
    result = query.order("uses_count", desc=True).limit(limit).execute()
    return result.data or []


async def use_template(template_id: str) -> Dict:
    """Increment template usage count."""
    client = get_supabase()
    # Get current count
    template = client.table("templates").select("uses_count").eq("id", template_id).single().execute()
    if template.data:
        new_count = (template.data.get("uses_count") or 0) + 1
        result = client.table("templates").update({"uses_count": new_count}).eq("id", template_id).execute()
        return result.data[0] if result.data else None
    return None


# ============================================
# MUSIC OPERATIONS
# ============================================

async def get_music_tracks(mood: str = None, genre: str = None, limit: int = 50) -> List[Dict]:
    """Get music tracks."""
    client = get_supabase()
    query = client.table("music_tracks").select("*")
    if mood:
        query = query.eq("mood", mood)
    if genre:
        query = query.eq("genre", genre)
    result = query.order("uses_count", desc=True).limit(limit).execute()
    return result.data or []


# ============================================
-- ANALYTICS OPERATIONS
# ============================================

async def record_video_analytics(video_id: str, platform: str, **metrics) -> Dict:
    """Record video analytics."""
    client = get_supabase()
    data = {
        "video_id": video_id,
        "platform": platform,
        **metrics
    }
    result = client.table("video_analytics").insert(data).execute()
    return result.data[0] if result.data else None


async def get_video_analytics(video_id: str) -> List[Dict]:
    """Get analytics for a video."""
    client = get_supabase()
    result = client.table("video_analytics").select("*").eq("video_id", video_id).order("recorded_at", desc=True).execute()
    return result.data or []


# ============================================
# HEALTH CHECK
# ============================================

async def check_connection() -> Dict[str, Any]:
    """Check Supabase connection and get stats."""
    try:
        client = get_supabase()

        # Get counts
        agents = client.table("ai_agents").select("id", count="exact").execute()
        templates = client.table("templates").select("id", count="exact").execute()

        return {
            "connected": True,
            "url": SUPABASE_URL,
            "agents_count": agents.count or 0,
            "templates_count": templates.count or 0,
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }
