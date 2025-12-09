# AI Program Video and Music Overlay

**Unified AI-Powered Video Creation Platform** - Complete system for video processing, music overlay, and AI-driven video generation with 10x Specialist AI Agents.

## 🎬 Overview

This is a comprehensive video creation and processing system that combines:

1. **Video & Music Overlay Processing** - Add music to videos with advanced editing
2. **AI Video Generation** - 10x Specialist AI Agents for automated video creation
3. **Social Media Integration** - Automatic publishing to multiple platforms
4. **Workflow Engine** - Sequential, parallel, and hybrid processing modes

## 🚀 Features

### Video & Music Overlay
- **Video Processing**: Support for multiple video formats (MP4, AVI, MOV, MKV, WebM)
- **Audio Overlay**: Add music/audio tracks to videos with synchronization
- **Quality Presets**: High, medium, and low quality output options
- **Memory Management**: Efficient handling of large media files with streaming
- **Format Validation**: Automatic file format detection and validation
- **Progress Tracking**: Real-time progress indicators for long operations

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

## 📁 Project Structure

```
ai-program-video-music-overlay/
├── app/                      # FastAPI backend application
│   ├── agents/              # 10x Specialist AI Agents
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
│   ├── workflows/           # Workflow Engine
│   ├── social/              # Social Media Integrations
│   ├── database/            # Database models and connections
│   └── ui/                  # Gradio Interface
├── dashboard/               # Next.js Dashboard
│   ├── app/                 # Next.js app directory
│   ├── components/          # React components
│   └── lib/                 # Utilities and API
├── src/                     # Source code (video/music processing)
│   ├── video/               # Video processing modules
│   ├── audio/               # Audio/music processing
│   ├── overlay/             # Overlay rendering
│   ├── effects/             # Video effects
│   └── utils/               # Utilities
├── config/                  # Configuration files
├── assets/                  # Media assets (videos, music)
├── output/                  # Processed output files
├── generated/               # AI-generated content
├── tests/                   # Test suite
├── docs/                    # Documentation
├── .cursor/                 # Cursor IDE configuration
└── .vscode/                 # VS Code workspace settings
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- FFmpeg (for video/audio processing)
- Sufficient disk space for media files

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/halvo78/ai-program-video-music-overlay.git
   cd ai-program-video-music-overlay
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies** (for dashboard):
   ```bash
   cd dashboard
   npm install
   ```

4. **Install FFmpeg**:
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Usage

#### Video & Music Overlay Processing

```bash
# Process video with music overlay
python src/main.py --input video.mp4 --audio music.mp3 --output result.mp4

# With quality preset
python src/main.py --input video.mp4 --audio music.mp3 --quality medium

# Preview before processing
python src/main.py --input video.mp4 --audio music.mp3 --preview
```

#### AI Video Generation (FastAPI)

```bash
# Start FastAPI server
uvicorn app.main:app --reload --port 8000

# API docs at http://localhost:8000/docs
```

#### Dashboard (Next.js)

```bash
cd dashboard
npm run dev

# Dashboard at http://localhost:3000
```

#### Python API

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

## 🎵 Supported Formats

### Video
- MP4, AVI, MOV, MKV, WebM, FLV, WMV

### Audio
- MP3, WAV, AAC, OGG, FLAC, M4A, WMA

### Images (for overlays)
- PNG, JPG, GIF, BMP, TIFF, WebP

## ⚙️ Configuration

### Quality Presets

- **High**: 1080p, 5000k video bitrate, 192k audio bitrate
- **Medium**: 720p, 2500k video bitrate, 128k audio bitrate
- **Low**: 480p, 1000k video bitrate, 96k audio bitrate

### Environment Variables

Create a `.env` file:

```env
MEDIA_OUTPUT_DIR=./output
MEDIA_TEMP_DIR=./temp
MAX_FILE_SIZE_MB=2048
DEFAULT_VIDEO_QUALITY=high
DEFAULT_AUDIO_BITRATE=192
LOG_LEVEL=INFO
```

The app can also load credentials from `C:/dev/infra/credentials/connected/`:
- `ai-providers.env` - AI API keys (OpenAI, Anthropic, Together.ai, HuggingFace, FLUX)
- `communications.env` - Social media APIs (Twitter, YouTube, Telegram)

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Test specific format
pytest tests/test_video_formats.py
```

## 📝 Code Comment Tags

Use these tags for better code organization:

```python
# MEDIA: Code that processes video/audio files
# OVERLAY: Code related to overlay rendering
# SYNC: Code that handles audio/video synchronization
# ENCODE: Code that handles encoding/decoding
# MEMORY: Code that manages memory for large files
# QUALITY: Code that affects output quality
```

## 🏗️ Architecture

### Media Processing Pipeline

1. **Input Layer** - File loading, format detection, validation
2. **Processing Layer** - Video/audio manipulation, effects
3. **Overlay Layer** - Music synchronization, overlay rendering
4. **Output Layer** - Encoding, format conversion, file writing
5. **UI Layer** - User interface, preview, controls

### AI Agent Workflow

1. **Content Analysis** - Script generation, SEO optimization
2. **Media Generation** - Video, music, images, voice
3. **Editing & Composition** - Assembly and effects
4. **Optimization** - Platform-specific encoding
5. **Safety & Analytics** - Content moderation and performance prediction
6. **Social Publishing** - Multi-platform distribution

## 🔧 Development

### Setup Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run linter:
   ```bash
   ruff check .
   ruff format .
   ```

### Project Guidelines

- **Memory Management**: Always use streaming/chunking for large files
- **File Validation**: Validate files before processing
- **Error Handling**: Wrap operations in try/except blocks
- **Progress Feedback**: Show progress for long operations
- **Resource Cleanup**: Always close file handles and release memory

## 📚 Key Libraries

- **FFmpeg**: Video/audio processing
- **OpenCV**: Video manipulation and effects
- **Pillow**: Image processing
- **MoviePy**: Python video editing
- **librosa**: Audio analysis
- **numpy**: Numerical operations
- **FastAPI**: Backend API framework
- **Next.js**: Frontend dashboard
- **HuggingFace**: AI models
- **Together.ai**: LLM inference
- **FLUX**: Image generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🙏 Acknowledgments

- FFmpeg community for excellent video processing tools
- OpenCV contributors for computer vision capabilities
- HuggingFace for AI models and infrastructure
- Together.ai for LLM inference
- FLUX by BFL for image generation
- All contributors and users of this project

---

**QUALITY FIRST. PERFORMANCE SECOND. USER EXPERIENCE THIRD.**
