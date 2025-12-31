# Taj Chat MCP Server

Model Context Protocol (MCP) server for integrating Taj Chat video generation capabilities with AI assistants like Claude.

## Features

- **create_video** - Create AI-generated videos from text prompts
- **get_video_status** - Check video generation progress
- **list_templates** - Browse available video templates
- **get_agent_status** - View AI agent system status
- **analyze_content** - Get SEO and engagement optimization suggestions
- **generate_music** - Create AI-generated background music
- **generate_image** - Generate thumbnails and overlays
- **publish_video** - Publish to social media platforms

## Installation

```bash
cd mcp
npm install
npm run build
```

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "taj-chat": {
      "command": "node",
      "args": ["/path/to/mcp/dist/video-agent-server.js"],
      "env": {
        "TAJ_CHAT_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

## Usage with Claude Code

Add to your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "taj-chat": {
      "command": "node",
      "args": ["./mcp/dist/video-agent-server.js"],
      "env": {
        "TAJ_CHAT_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

## Development

```bash
npm run dev
```

## API Reference

### create_video

```json
{
  "prompt": "Create a motivational video about success",
  "platform": "tiktok",
  "style": "cinematic",
  "music_mood": "inspiring",
  "include_voice": true,
  "include_captions": true
}
```

### get_video_status

```json
{
  "workflow_id": "wf_12345"
}
```

### list_templates

```json
{
  "category": "business"
}
```

### analyze_content

```json
{
  "text": "Check out our new product!",
  "platforms": ["tiktok", "instagram"]
}
```

### generate_music

```json
{
  "mood": "upbeat",
  "duration_seconds": 30,
  "genre": "electronic"
}
```

### generate_image

```json
{
  "prompt": "Futuristic city skyline",
  "style": "photorealistic",
  "aspect_ratio": "16:9"
}
```

### publish_video

```json
{
  "video_path": "/output/video.mp4",
  "platforms": ["tiktok", "instagram"],
  "caption": "Check this out!",
  "hashtags": ["viral", "fyp"]
}
```

## Environment Variables

- `TAJ_CHAT_API_URL` - Backend API URL (default: http://localhost:8000)
