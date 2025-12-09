-- ============================================
-- TAJ CHAT - AI VIDEO CREATION PLATFORM
-- Supabase Database Schema
-- ============================================
-- Database: Supabase (cmwelibfxzplxjzspryh)
-- Created: 2025-12-08
-- ============================================

-- Enable UUID extension (usually already enabled in Supabase)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS (extends Supabase auth.users)
-- ============================================

CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255),
    username VARCHAR(50) UNIQUE,
    display_name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,
    plan VARCHAR(20) DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'enterprise')),

    -- Settings
    theme VARCHAR(20) DEFAULT 'dark',
    notifications_enabled BOOLEAN DEFAULT true,
    auto_publish BOOLEAN DEFAULT false,
    default_platform VARCHAR(50) DEFAULT 'tiktok',
    default_aspect_ratio VARCHAR(10) DEFAULT '9:16',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- ============================================
-- VIDEOS
-- ============================================

CREATE TABLE IF NOT EXISTS public.videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    prompt TEXT,
    script TEXT,

    -- Video specs
    duration_seconds INTEGER,
    width INTEGER DEFAULT 1080,
    height INTEGER DEFAULT 1920,
    fps INTEGER DEFAULT 30,
    aspect_ratio VARCHAR(10) DEFAULT '9:16',

    -- File paths (Supabase Storage)
    video_url TEXT,
    thumbnail_url TEXT,
    preview_url TEXT,

    -- Status
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'processing', 'completed', 'failed', 'published')),
    processing_progress INTEGER DEFAULT 0 CHECK (processing_progress >= 0 AND processing_progress <= 100),
    error_message TEXT,

    -- Metadata
    tags TEXT[],
    category VARCHAR(50),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ
);

-- Enable RLS
ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;

-- Videos policies
CREATE POLICY "Users can view own videos" ON public.videos
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own videos" ON public.videos
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own videos" ON public.videos
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own videos" ON public.videos
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- VIDEO ASSETS
-- ============================================

CREATE TABLE IF NOT EXISTS public.video_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    asset_type VARCHAR(50) NOT NULL CHECK (asset_type IN ('music', 'image', 'overlay', 'voiceover', 'b-roll')),
    name VARCHAR(255),
    file_url TEXT NOT NULL,
    duration_seconds FLOAT,
    start_time FLOAT DEFAULT 0,
    end_time FLOAT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.video_assets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own video assets" ON public.video_assets
    FOR ALL USING (
        EXISTS (SELECT 1 FROM public.videos WHERE videos.id = video_assets.video_id AND videos.user_id = auth.uid())
    );

-- ============================================
-- VIDEO TRACKS & CLIPS
-- ============================================

CREATE TABLE IF NOT EXISTS public.video_tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    track_type VARCHAR(50) NOT NULL CHECK (track_type IN ('video', 'audio', 'overlay', 'text')),
    track_index INTEGER DEFAULT 0,
    name VARCHAR(100),
    is_muted BOOLEAN DEFAULT false,
    is_locked BOOLEAN DEFAULT false,
    volume FLOAT DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.video_clips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    track_id UUID REFERENCES public.video_tracks(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES public.video_assets(id) ON DELETE SET NULL,
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,
    position_x FLOAT DEFAULT 0,
    position_y FLOAT DEFAULT 0,
    scale FLOAT DEFAULT 1.0,
    rotation FLOAT DEFAULT 0,
    opacity FLOAT DEFAULT 1.0,
    effects JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.video_tracks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.video_clips ENABLE ROW LEVEL SECURITY;

-- ============================================
-- AI GENERATION JOBS
-- ============================================

CREATE TABLE IF NOT EXISTS public.generation_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL CHECK (job_type IN ('script', 'music', 'image', 'voice', 'video', 'optimize')),
    provider VARCHAR(50),
    model VARCHAR(100),
    input_prompt TEXT,
    input_params JSONB DEFAULT '{}',
    output_url TEXT,
    output_data JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER,
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 6),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.generation_jobs ENABLE ROW LEVEL SECURITY;

-- ============================================
-- AI AGENTS (System table - no RLS needed)
-- ============================================

CREATE TABLE IF NOT EXISTS public.ai_agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    agent_type VARCHAR(50) NOT NULL CHECK (agent_type IN ('content', 'video', 'music', 'image', 'voice', 'editing', 'optimization', 'analytics', 'safety', 'social')),
    description TEXT,
    status VARCHAR(20) DEFAULT 'ready' CHECK (status IN ('ready', 'running', 'completed', 'error')),
    current_task TEXT,
    tasks_completed INTEGER DEFAULT 0,
    avg_duration_ms INTEGER,
    success_rate FLOAT DEFAULT 1.0,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- SOCIAL ACCOUNTS
-- ============================================

CREATE TABLE IF NOT EXISTS public.social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL CHECK (platform IN ('tiktok', 'instagram', 'youtube', 'twitter', 'facebook', 'threads')),
    platform_user_id VARCHAR(255),
    username VARCHAR(100),
    display_name VARCHAR(255),
    avatar_url TEXT,
    followers_count INTEGER,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMPTZ,
    is_connected BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, platform)
);

ALTER TABLE public.social_accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own social accounts" ON public.social_accounts
    FOR ALL USING (auth.uid() = user_id);

-- ============================================
-- SCHEDULED & PUBLISHED POSTS
-- ============================================

CREATE TABLE IF NOT EXISTS public.scheduled_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    scheduled_at TIMESTAMPTZ NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    platforms TEXT[] NOT NULL,
    caption TEXT,
    hashtags TEXT[],
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'publishing', 'published', 'failed', 'cancelled')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.published_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scheduled_post_id UUID REFERENCES public.scheduled_posts(id) ON DELETE SET NULL,
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    social_account_id UUID REFERENCES public.social_accounts(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    platform_post_id VARCHAR(255),
    post_url TEXT,
    status VARCHAR(20) DEFAULT 'published',
    published_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.scheduled_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.published_posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own scheduled posts" ON public.scheduled_posts
    FOR ALL USING (auth.uid() = user_id);

-- ============================================
-- ANALYTICS
-- ============================================

CREATE TABLE IF NOT EXISTS public.video_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    platform VARCHAR(50),
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    watch_time_seconds INTEGER DEFAULT 0,
    avg_watch_percentage FLOAT,
    engagement_rate FLOAT,
    demographics JSONB DEFAULT '{}',
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.platform_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    followers_count INTEGER DEFAULT 0,
    followers_gained INTEGER DEFAULT 0,
    followers_lost INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    total_likes INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    total_shares INTEGER DEFAULT 0,
    period_start TIMESTAMPTZ,
    period_end TIMESTAMPTZ,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.video_analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.platform_analytics ENABLE ROW LEVEL SECURITY;

-- ============================================
-- TEMPLATES
-- ============================================

CREATE TABLE IF NOT EXISTS public.templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) CHECK (category IN ('motivation', 'education', 'lifestyle', 'business', 'entertainment', 'other')),
    thumbnail_url TEXT,
    preview_url TEXT,
    template_data JSONB NOT NULL DEFAULT '{}',
    uses_count INTEGER DEFAULT 0,
    rating FLOAT DEFAULT 0,
    tags TEXT[],
    is_featured BOOLEAN DEFAULT false,
    is_trending BOOLEAN DEFAULT false,
    is_new BOOLEAN DEFAULT true,
    author_name VARCHAR(100),
    author_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Templates are public readable
CREATE POLICY "Anyone can view templates" ON public.templates
    FOR SELECT USING (true);

-- ============================================
-- MUSIC LIBRARY
-- ============================================

CREATE TABLE IF NOT EXISTS public.music_tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255),
    genre VARCHAR(50),
    mood VARCHAR(50),
    file_url TEXT NOT NULL,
    duration_seconds INTEGER,
    bpm INTEGER,
    key VARCHAR(10),
    license_type VARCHAR(50) DEFAULT 'royalty-free',
    attribution_required BOOLEAN DEFAULT false,
    uses_count INTEGER DEFAULT 0,
    is_ai_generated BOOLEAN DEFAULT false,
    generation_prompt TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Music is public readable
CREATE POLICY "Anyone can view music tracks" ON public.music_tracks
    FOR SELECT USING (true);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_videos_user_id ON public.videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON public.videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON public.videos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_video_assets_video_id ON public.video_assets(video_id);
CREATE INDEX IF NOT EXISTS idx_generation_jobs_video_id ON public.generation_jobs(video_id);
CREATE INDEX IF NOT EXISTS idx_generation_jobs_status ON public.generation_jobs(status);
CREATE INDEX IF NOT EXISTS idx_social_accounts_user_id ON public.social_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_scheduled_at ON public.scheduled_posts(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_templates_category ON public.templates(category);
CREATE INDEX IF NOT EXISTS idx_templates_is_featured ON public.templates(is_featured);
CREATE INDEX IF NOT EXISTS idx_music_tracks_mood ON public.music_tracks(mood);

-- ============================================
-- SEED DATA: AI AGENTS
-- ============================================

INSERT INTO public.ai_agents (name, agent_type, description, status) VALUES
    ('Content Agent', 'content', 'Script generation, SEO optimization, hashtag suggestions', 'ready'),
    ('Video Agent', 'video', 'Video composition and rendering', 'ready'),
    ('Music Agent', 'music', 'AI music generation and selection', 'ready'),
    ('Image Agent', 'image', 'Thumbnail generation, overlays, backgrounds', 'ready'),
    ('Voice Agent', 'voice', 'Text-to-speech, voice cloning', 'ready'),
    ('Editing Agent', 'editing', 'Transitions, effects, color grading', 'ready'),
    ('Optimization Agent', 'optimization', 'Platform-specific optimization', 'ready'),
    ('Analytics Agent', 'analytics', 'Performance tracking and insights', 'ready'),
    ('Safety Agent', 'safety', 'Content moderation, copyright check', 'ready'),
    ('Social Agent', 'social', 'Cross-platform publishing, scheduling', 'ready')
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- SEED DATA: SAMPLE TEMPLATES
-- ============================================

INSERT INTO public.templates (name, description, category, is_featured, is_new, template_data) VALUES
    ('Motivational Quote', 'Inspiring quotes with dynamic text animations', 'motivation', true, true, '{"duration": 15, "style": "minimal", "text_position": "center"}'),
    ('Product Showcase', 'Professional product presentation template', 'business', true, false, '{"duration": 30, "style": "modern", "transitions": "smooth"}'),
    ('Tutorial Intro', 'Educational content opener', 'education', false, true, '{"duration": 10, "style": "clean", "has_voiceover": true}'),
    ('Day in My Life', 'Lifestyle vlog template', 'lifestyle', false, true, '{"duration": 60, "style": "casual", "music_mood": "upbeat"}'),
    ('Breaking News', 'News-style announcement template', 'entertainment', false, false, '{"duration": 20, "style": "bold", "text_animation": "typewriter"}')
ON CONFLICT DO NOTHING;

-- ============================================
-- FUNCTIONS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to tables with updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_videos_updated_at BEFORE UPDATE ON public.videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_agents_updated_at BEFORE UPDATE ON public.ai_agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_social_accounts_updated_at BEFORE UPDATE ON public.social_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scheduled_posts_updated_at BEFORE UPDATE ON public.scheduled_posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_templates_updated_at BEFORE UPDATE ON public.templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
