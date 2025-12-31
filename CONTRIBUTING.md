# Contributing to Taj Chat

Thank you for your interest in contributing to Taj Chat! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- FFmpeg
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-program-video-music-overlay.git
   cd ai-program-video-music-overlay
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Install dashboard dependencies**
   ```bash
   cd dashboard
   npm install
   cd ..
   ```

4. **Run validation**
   ```bash
   python cli/validate.py
   ```

5. **Start development servers**
   ```bash
   # Terminal 1: Backend
   uvicorn app.main:app --reload --port 8000

   # Terminal 2: Frontend
   cd dashboard && npm run dev
   ```

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python/Node versions)
   - Screenshots or logs if applicable

### Suggesting Features

1. Check existing issues and discussions
2. Create a feature request with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach
   - Any relevant examples or references

### Pull Requests

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**
   - Follow the coding style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Backend tests
   pytest tests/ -v

   # Frontend tests
   cd dashboard && npm test

   # Validation
   python cli/validate.py --full
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `style:` Formatting, no code change
   - `refactor:` Code restructuring
   - `test:` Adding tests
   - `chore:` Maintenance

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub.

## Coding Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for public functions/classes

```python
def create_video(
    prompt: str,
    platform: str = "tiktok",
    style: str = "cinematic",
) -> VideoResult:
    """
    Create a video from a text prompt.

    Args:
        prompt: Description of the video to create
        platform: Target platform (tiktok, instagram_reels, etc.)
        style: Visual style of the video

    Returns:
        VideoResult object with workflow details
    """
    pass
```

### TypeScript/React Style

- Use TypeScript for all new code
- Prefer functional components with hooks
- Use named exports
- Maximum line length: 100 characters

```typescript
interface VideoCardProps {
  title: string;
  thumbnail: string;
  onClick: () => void;
}

export function VideoCard({ title, thumbnail, onClick }: VideoCardProps) {
  return (
    <div className="video-card" onClick={onClick}>
      <img src={thumbnail} alt={title} />
      <h3>{title}</h3>
    </div>
  );
}
```

### CSS/Tailwind

- Use Tailwind CSS classes
- For custom styles, use CSS modules or globals.css
- Follow mobile-first responsive design
- Use CSS variables for theming

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use meaningful test names

```python
def test_video_agent_creates_valid_output():
    """Test that video agent produces valid video file."""
    agent = VideoGenerationAgent()
    result = agent.generate(prompt="Test video")
    assert result.status == "success"
    assert result.output_path.exists()
```

## Project Structure

```
ai-program-video-music-overlay/
├── app/                  # FastAPI backend
│   ├── agents/          # AI agents
│   ├── providers/       # AI provider clients
│   ├── workflows/       # Workflow engine
│   ├── social/          # Social media integrations
│   └── database/        # Database models
├── dashboard/           # Next.js frontend
│   ├── app/            # Pages and routes
│   ├── components/     # React components
│   └── lib/            # Utilities
├── cli/                # CLI tools
├── mcp/                # MCP servers
├── tests/              # Python tests
└── docs/               # Documentation
```

## Agent Development

When adding or modifying AI agents:

1. Extend `BaseAgent` class
2. Implement required methods: `process()`, `validate()`
3. Add to orchestrator registration
4. Write comprehensive tests
5. Update documentation

```python
from app.agents.base_agent import BaseAgent, AgentType

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_type=AgentType.CUSTOM,
            name="My New Agent",
            description="Does something amazing",
        )

    async def process(self, task: AgentTask) -> AgentResult:
        # Implementation
        pass
```

## Documentation

- Update README.md for major features
- Add docstrings to all public APIs
- Create examples in docs/ for complex features
- Keep CHANGELOG.md updated

## Review Process

1. All PRs require at least one review
2. CI checks must pass
3. Code coverage should not decrease
4. Documentation must be updated

## Getting Help

- Open a Discussion for questions
- Join our community channels
- Check existing issues and PRs

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Taj Chat!
