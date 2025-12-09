-- ============================================
-- TAJ CHAT - AI VIDEO CREATION PLATFORM
-- Database Schema
-- ============================================
-- Created: 2025-12-08
-- Database: PostgreSQL (Neon)
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS & AUTHENTICATION
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    bio TEXT,
    plan VARCHAR(20) DEFAULT 'free', -- free, pro, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(20) DEFAULT 'dark',
    notifications_enabled BOOLEAN DEFAULT true,
    auto_publish BOOLEAN DEFAULT false,
    default_platform VARCHAR(50) DEFAULT 'tiktok',
    default_aspect_ratio VARCHAR(10) DEFAULT '9:16',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- VIDEOS & CONTENT
-- ============================================

CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    prompt TEXT, -- Original user prompt
    script TEXT, -- AI-generated script

    -- Video specs
    duration_seconds INTEGER,
    width INTEGER DEFAULT 1080,
    height INTEGER DEFAULT 1920,
    fps INTEGER DEFAULT 30,
    aspect_ratio VARCHAR(10) DEFAULT '9:16',

    -- File paths
    video_url TEXT,
    thumbnail_url TEXT,
    preview_url TEXT,

    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, processing, completed, failed, published
    processing_progress INTEGER DEFAULT 0, -- 0-100
    error_message TEXT,

    -- Metadata
    tags TEXT[], -- Array of tags
    category VARCHAR(50),

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    asset_type VARCHAR(50) NOT NULL, -- music, image, overlay, voiceover, b-roll
    name VARCHAR(255),
    file_url TEXT NOT NULL,
    duration_seconds FLOAT,
    start_time FLOAT DEFAULT 0, -- Position in timeline
    end_time FLOAT,

    -- Asset-specific metadata
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video_tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    track_type VARCHAR(50) NOT NULL, -- video, audio, overlay, text
    track_index INTEGER DEFAULT 0,
    name VARCHAR(100),
    is_muted BOOLEAN DEFAULT false,
    is_locked BOOLEAN DEFAULT false,
    volume FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video_clips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    track_id UUID REFERENCES video_tracks(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES video_assets(id) ON DELETE SET NULL,

    -- Timeline position
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,

    -- Transformations
    position_x FLOAT DEFAULT 0,
    position_y FLOAT DEFAULT 0,
    scale FLOAT DEFAULT 1.0,
    rotation FLOAT DEFAULT 0,
    opacity FLOAT DEFAULT 1.0,

    -- Effects
    effects JSONB DEFAULT '[]',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- AI GENERATION
-- ============================================

CREATE TABLE IF NOT EXISTS generation_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL, -- script, music, image, voice, video, optimize

    -- AI Provider info
    provider VARCHAR(50), -- openai, anthropic, together, flux, etc.
    model VARCHAR(100),

    -- Input/Output
    input_prompt TEXT,
    input_params JSONB DEFAULT '{}',
    output_url TEXT,
    output_data JSONB DEFAULT '{}',

    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed
    progress INTEGER DEFAULT 0,
    error_message TEXT,

    -- Timing
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,

    -- Cost tracking
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 6),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    agent_type VARCHAR(50) NOT NULL, -- content, video, music, image, voice, editing, optimization, analytics, safety, social
    description TEXT,

    -- Status
    status VARCHAR(20) DEFAULT 'ready', -- ready, running, completed, error
    current_task TEXT,

    -- Stats
    tasks_completed INTEGER DEFAULT 0,
    avg_duration_ms INTEGER,
    success_rate FLOAT DEFAULT 1.0,

    -- Config
    config JSONB DEFAULT '{}',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- SOCIAL MEDIA PUBLISHING
-- ============================================

CREATE TABLE IF NOT EXISTS social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- tiktok, instagram, youtube, twitter, facebook, threads

    -- Account info
    platform_user_id VARCHAR(255),
    username VARCHAR(100),
    display_name VARCHAR(255),
    avatar_url TEXT,
    followers_count INTEGER,

    -- Auth tokens (encrypted in production)
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,

    -- Status
    is_connected BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, platform)
);

CREATE TABLE IF NOT EXISTS scheduled_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,

    -- Scheduling
    scheduled_at TIMESTAMP NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',

    -- Target platforms
    platforms TEXT[] NOT NULL, -- Array of platform names

    -- Post content
    caption TEXT,
    hashtags TEXT[],

    -- Status
    status VARCHAR(20) DEFAULT 'scheduled', -- scheduled, publishing, published, failed, cancelled

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS published_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scheduled_post_id UUID REFERENCES scheduled_posts(id) ON DELETE SET NULL,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    social_account_id UUID REFERENCES social_accounts(id) ON DELETE CASCADE,

    -- Platform info
    platform VARCHAR(50) NOT NULL,
    platform_post_id VARCHAR(255), -- ID on the platform
    post_url TEXT,

    -- Status
    status VARCHAR(20) DEFAULT 'published', -- published, deleted, flagged

    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ANALYTICS
-- ============================================

CREATE TABLE IF NOT EXISTS video_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    platform VARCHAR(50),

    -- Metrics
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,

    -- Engagement
    watch_time_seconds INTEGER DEFAULT 0,
    avg_watch_percentage FLOAT,
    engagement_rate FLOAT,

    -- Demographics (JSONB for flexibility)
    demographics JSONB DEFAULT '{}',

    -- Timestamp
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(video_id, platform, recorded_at)
);

CREATE TABLE IF NOT EXISTS platform_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,

    -- Follower metrics
    followers_count INTEGER DEFAULT 0,
    followers_gained INTEGER DEFAULT 0,
    followers_lost INTEGER DEFAULT 0,

    -- Content metrics
    total_views INTEGER DEFAULT 0,
    total_likes INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    total_shares INTEGER DEFAULT 0,

    -- Period
    period_start TIMESTAMP,
    period_end TIMESTAMP,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TEMPLATES
-- ============================================

CREATE TABLE IF NOT EXISTS templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- motivation, education, lifestyle, business, entertainment

    -- Template content
    thumbnail_url TEXT,
    preview_url TEXT,
    template_data JSONB NOT NULL, -- Full template configuration

    -- Stats
    uses_count INTEGER DEFAULT 0,
    rating FLOAT DEFAULT 0,

    -- Metadata
    tags TEXT[],
    is_featured BOOLEAN DEFAULT false,
    is_trending BOOLEAN DEFAULT false,
    is_new BOOLEAN DEFAULT true,

    -- Author
    author_name VARCHAR(100),
    author_id UUID REFERENCES users(id) ON DELETE SET NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- MUSIC LIBRARY
-- ============================================

CREATE TABLE IF NOT EXISTS music_tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255),
    genre VARCHAR(50),
    mood VARCHAR(50), -- energetic, calm, happy, sad, dramatic, etc.

    -- Audio info
    file_url TEXT NOT NULL,
    duration_seconds INTEGER,
    bpm INTEGER,
    key VARCHAR(10),

    -- Licensing
    license_type VARCHAR(50), -- royalty-free, ai-generated, licensed
    attribution_required BOOLEAN DEFAULT false,

    -- Stats
    uses_count INTEGER DEFAULT 0,

    -- AI generation info
    is_ai_generated BOOLEAN DEFAULT false,
    generation_prompt TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_videos_user_id ON videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_video_assets_video_id ON video_assets(video_id);
CREATE INDEX IF NOT EXISTS idx_video_clips_track_id ON video_clips(track_id);

CREATE INDEX IF NOT EXISTS idx_generation_jobs_video_id ON generation_jobs(video_id);
CREATE INDEX IF NOT EXISTS idx_generation_jobs_status ON generation_jobs(status);

CREATE INDEX IF NOT EXISTS idx_social_accounts_user_id ON social_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_social_accounts_platform ON social_accounts(platform);

CREATE INDEX IF NOT EXISTS idx_scheduled_posts_scheduled_at ON scheduled_posts(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_scheduled_posts_status ON scheduled_posts(status);

CREATE INDEX IF NOT EXISTS idx_video_analytics_video_id ON video_analytics(video_id);
CREATE INDEX IF NOT EXISTS idx_video_analytics_platform ON video_analytics(platform);

CREATE INDEX IF NOT EXISTS idx_templates_category ON templates(category);
CREATE INDEX IF NOT EXISTS idx_templates_is_featured ON templates(is_featured);

CREATE INDEX IF NOT EXISTS idx_music_tracks_genre ON music_tracks(genre);
CREATE INDEX IF NOT EXISTS idx_music_tracks_mood ON music_tracks(mood);

-- ============================================
-- INITIAL DATA
-- ============================================

-- Insert default AI agents
INSERT INTO ai_agents (name, agent_type, description, status) VALUES
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
ON CONFLICT DO NOTHING;

-- ============================================
-- COMMENTS
-- ============================================
COMMENT ON TABLE videos IS 'Main table for user-created videos';
COMMENT ON TABLE video_assets IS 'Media assets (music, images, overlays) used in videos';
COMMENT ON TABLE video_tracks IS 'Timeline tracks for video editing';
COMMENT ON TABLE video_clips IS 'Individual clips placed on tracks';
COMMENT ON TABLE generation_jobs IS 'AI generation job tracking';
COMMENT ON TABLE ai_agents IS 'AI agent status and configuration';
COMMENT ON TABLE social_accounts IS 'Connected social media accounts';
COMMENT ON TABLE scheduled_posts IS 'Scheduled video publications';
COMMENT ON TABLE published_posts IS 'Published post records';
COMMENT ON TABLE video_analytics IS 'Per-video performance metrics';
COMMENT ON TABLE platform_analytics IS 'Per-platform aggregate metrics';
COMMENT ON TABLE templates IS 'Video templates library';
COMMENT ON TABLE music_tracks IS 'Music library for videos';
