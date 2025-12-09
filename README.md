# Taj Chat - Ultimate AI Video Creation Platform

🎬 **10x Specialist AI Agents** working in **Sequential & Parallel Workflows** to create the best possible short-form videos with automatic music, overlays, and social media delivery.

## Features

### 10x Specialist AI Agents

| Agent | Purpose | Models |
|-------|---------|--------|
| 1. Video Generation | Text-to-video, image animation | HuggingFace (SVD, AnimateDiff, CogVideo) |
| 2. Music Generation | AI soundtrack creation | HuggingFace (MusicGen, Riffusion) |
| 3. Image Generation | Overlays, thumbnails | FLUX Pro, SDXL |
| 4. Voice & Speech | TTS, transcription, captions | Whisper, Bark |
| 5. Content Analysis | Script, SEO, hashtags | Together.ai (Llama, DeepSeek) |
| 6. Editing | Composition, effects | FFmpeg, MoviePy |
| 7. Optimization | Platform encoding | FFmpeg |
| 8. Analytics | Performance prediction | Claude, GPT-4o |
| 9. Safety | Content moderation | Content filters |
| 10. Social Media | Upload, scheduling | Twitter, YouTube, Telegram APIs |

### Workflow Modes

- **Sequential**: Best quality, step-by-step processing
- **Parallel**: Fastest, concurrent generation
- **Hybrid**: Balanced approach (recommended)

### Supported Platforms

- TikTok (9:16, 1080x1920)
- Instagram Reels (9:16, 1080x1920)
- YouTube Shorts (9:16, up to 4K)
- Twitter/X (16:9, 1280x720)

## Installation

```bash
# Clone or navigate to the project
cd C:/dev/taj-chat

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
# Link to existing credentials or create .env
```

## Configuration

The app loads credentials from `C:/dev/infra/credentials/connected/`:

- `ai-providers.env` - AI API keys (OpenAI, Anthropic, Together.ai, HuggingFace, FLUX)
- `communications.env` - Social media APIs (Twitter, YouTube, Telegram)

## Usage

### API Server

```bash
# Start FastAPI server
uvicorn app.main:app --reload --port 8000

# API docs at http://localhost:8000/docs
```

### Gradio UI

```bash
# Launch Gradio interface
python -c "from app.ui import launch_ui; launch_ui()"

# UI at http://localhost:7860
```

### Python API

```python
import asyncio
from app.workflows.engine import WorkflowEngine, WorkflowMode

async def main():
    engine = WorkflowEngine()

    result = await engine.create_video(
        prompt="Create an energetic video about morning exercise",
        mode=WorkflowMode.HYBRID,
        platforms=["tiktok", "instagram_reels"],
    )

    print(f"Status: {result.status}")
    print(f"Output files: {result.output_files}")

asyncio.run(main())
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root info |
| `/status` | GET | System status |
| `/create` | POST | Create video |
| `/workflow/{id}` | GET | Get workflow status |
| `/agents` | GET | Get agent status |
| `/health` | GET | Health check |

### Create Video Request

```json
POST /create
{
  "prompt": "Create a motivational video about success",
  "mode": "hybrid",
  "platforms": ["tiktok", "instagram_reels"],
  "parameters": {}
}
```

## Project Structure

```
taj-chat/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration loader
│   ├── agents/              # 10x Specialist Agents
│   │   ├── base_agent.py
│   │   ├── orchestrator.py
│   │   ├── video_agent.py
│   │   ├── music_agent.py
│   │   ├── image_agent.py
│   │   ├── voice_agent.py
│   │   ├── content_agent.py
│   │   ├── editing_agent.py
│   │   ├── optimization_agent.py
│   │   ├── analytics_agent.py
│   │   ├── safety_agent.py
│   │   └── social_agent.py
│   ├── providers/           # AI Provider Clients
│   │   ├── together_client.py
│   │   ├── huggingface_client.py
│   │   └── flux_client.py
│   ├── workflows/           # Workflow Engine
│   │   └── engine.py
│   └── ui/                  # Gradio Interface
│       └── gradio_interface.py
├── generated/               # Output files
├── tests/
├── requirements.txt
├── mcp.json                 # MCP server config
└── README.md
```

## AI Providers Used

| Provider | Models | Purpose |
|----------|--------|---------|
| Together.ai | DeepSeek R1, Llama 3.3, Qwen, Mixtral | Content analysis |
| HuggingFace Pro | SVD, MusicGen, SDXL, Whisper, Bark | Generation |
| FLUX (BFL) | flux-pro-1.1, flux-dev | High-quality images |
| OpenAI | GPT-4o | Multi-model consensus |
| Anthropic | Claude-3.5-Sonnet | Complex reasoning |

## Social Media Integration

| Platform | API | Status |
|----------|-----|--------|
| Twitter/X | Full API (OAuth) | ✅ Ready |
| YouTube | Data API v3 | ✅ Ready |
| Telegram | Bot API | ✅ Ready |
| TikTok | Manual upload | 📁 Files ready |
| Instagram | Manual upload | 📁 Files ready |

## License

MIT License

## Credits

Built with:
- FastAPI
- Gradio
- FFmpeg
- MoviePy
- HuggingFace Transformers
- Together.ai
- FLUX by BFL
