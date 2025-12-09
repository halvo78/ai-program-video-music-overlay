# AI Program Video and Music Overlay

An AI-powered video and music overlay processing system for adding music to videos with advanced editing capabilities.

## 🎬 Features

- **Video Processing**: Support for multiple video formats (MP4, AVI, MOV, MKV, WebM)
- **Audio Overlay**: Add music/audio tracks to videos with synchronization
- **Quality Presets**: High, medium, and low quality output options
- **Memory Management**: Efficient handling of large media files with streaming
- **Format Validation**: Automatic file format detection and validation
- **Progress Tracking**: Real-time progress indicators for long operations

## 📁 Project Structure

```
ai-program-video-music-overlay/
├── src/                    # Source code
│   ├── video/              # Video processing modules
│   ├── audio/              # Audio/music processing
│   ├── overlay/            # Overlay rendering
│   ├── effects/            # Video effects
│   └── utils/              # Utilities
├── config/                 # Configuration files
├── assets/                 # Media assets (videos, music)
├── output/                 # Processed output files
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .cursor/                # Cursor IDE configuration
└── .vscode/                # VS Code workspace settings
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (if using Python)
- Node.js 18+ (if using Node.js)
- FFmpeg (for video/audio processing)
- Sufficient disk space for media files

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-program-video-music-overlay.git
   cd ai-program-video-music-overlay
   ```

2. **Set up Python environment** (if using Python):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies** (if using Node.js):
   ```bash
   npm install
   ```

4. **Install FFmpeg**:
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Usage

```bash
# Process video with music overlay
python src/main.py --input video.mp4 --audio music.mp3 --output result.mp4

# With quality preset
python src/main.py --input video.mp4 --audio music.mp3 --quality medium

# Preview before processing
python src/main.py --input video.mp4 --audio music.mp3 --preview
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
- All contributors and users of this project

---

**QUALITY FIRST. PERFORMANCE SECOND. USER EXPERIENCE THIRD.**
