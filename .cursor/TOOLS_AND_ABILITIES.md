# Cursor Tools and Abilities

## 🛠️ Complete Tool Configuration

Your workspace has access to all configured tools and abilities.

## 📋 Available Tools

### 1. MCP Servers

#### Required Servers
- **filesystem**: File system operations
- **github**: GitHub integration

#### Optional Servers
- **memory**: Knowledge graph and memory
- **sequential-thinking**: Advanced problem solving
- **postgres**: Database operations
- **redis**: Caching and queues
- **aws**: AWS cloud operations
- **telegram**: Telegram bot integration
- **notion**: Notion integration
- **sentry**: Error tracking

### 2. Code Generation

#### AI Models
- **Primary**: Claude Sonnet 4 (2025-05-14)
- **Fallback**: Claude Opus 3
- **Code**: Claude Sonnet 4
- **Chat**: Claude Sonnet 4

#### Capabilities
- **Context Window**: 200,000 tokens
- **Smart Context**: Enabled
- **Import Analysis**: Enabled
- **Reference Tracking**: Enabled
- **Documentation**: Included
- **Test Files**: Included

### 3. Code Quality Tools

#### Python
- **Ruff**: Linting and formatting
- **mypy**: Type checking
- **pytest**: Testing
- **coverage**: Code coverage

#### TypeScript/JavaScript
- **ESLint**: Linting
- **Prettier**: Formatting
- **Jest**: Testing
- **TypeScript**: Type checking

### 4. Development Tools

#### Git Integration
- **GitLens**: Advanced Git features
- **Auto-fetch**: Enabled
- **Smart commit**: Enabled
- **Branch protection**: Configured

#### Debugging
- **Python Debugger**: FastAPI, Pytest, Current File
- **Node.js Debugger**: Next.js development and production
- **Compound Debugging**: Full stack debugging

#### Testing
- **Unit Tests**: Python (pytest), TypeScript (Jest)
- **E2E Tests**: Playwright
- **Coverage**: HTML, text, LCOV reports
- **Parallel Execution**: 4 workers

### 5. Media Processing Tools

#### Video/Audio
- **FFmpeg**: Video/audio processing
- **OpenCV**: Video manipulation
- **MoviePy**: Python video editing
- **librosa**: Audio analysis

#### Image
- **Pillow**: Image processing
- **FLUX**: AI image generation
- **SDXL**: Image generation

### 6. AI Provider Tools

#### LLM Providers
- **Together.ai**: DeepSeek, Llama, Qwen, Mixtral
- **OpenAI**: GPT-4o
- **Anthropic**: Claude

#### AI Models
- **HuggingFace**: SVD, MusicGen, Whisper, Bark, SDXL
- **FLUX**: Image generation

### 7. Social Media Tools

#### APIs
- **Twitter/X**: Full API (OAuth)
- **YouTube**: Data API v3
- **Telegram**: Bot API
- **TikTok**: Manual upload
- **Instagram**: Manual upload

### 8. Database Tools

#### Databases
- **Supabase**: PostgreSQL
- **SQLAlchemy**: ORM
- **Migrations**: Alembic

### 9. Payment Tools

#### Payment Processing
- **Stripe**: Payment integration

## 🎯 Custom Commands

All commands are available via `/` prefix:

- `/status` - System status
- `/process` - Process video
- `/preview` - Preview media
- `/cleanup` - Clean temp files
- `/agents` - Manage AI agents
- `/workflow` - Manage workflows
- `/api` - FastAPI server
- `/dashboard` - Next.js dashboard
- `/test` - Run tests
- `/deploy` - Deploy application
- `/monitor` - Monitor system

## 🔧 Task Automation

### Available Tasks (Ctrl+Shift+P → Tasks: Run Task)

1. **🚀 Start FastAPI Server**
2. **🎨 Start Next.js Dashboard**
3. **🧪 Run Python Tests**
4. **🔍 Lint Python (Ruff)**
5. **✨ Format Python (Ruff)**
6. **🔍 Type Check Python (mypy)**
7. **🧪 Run Dashboard Tests**
8. **🏗️ Build Dashboard**
9. **📦 Install Dependencies**
10. **🔄 Full Stack (API + Dashboard)**
11. **🧹 Clean Python Cache**
12. **📊 Generate Coverage Report**

## 🐛 Debugging Configurations

### Available Debug Configurations

1. **Python: FastAPI** - Debug FastAPI server
2. **Python: Current File** - Debug current Python file
3. **Python: Pytest** - Debug tests
4. **Next.js: Debug** - Debug Next.js dev server
5. **Next.js: Debug (Production)** - Debug production build
6. **Python: Agent Test** - Debug agent execution
7. **Full Stack Debug** - Debug both API and Dashboard

## ☁️ Cloud Capabilities

### Cloud Sync
- **Workspace**: Synced
- **Settings**: Synced
- **Keybindings**: Synced
- **Snippets**: Synced
- **Tasks**: Synced
- **Launch**: Synced

### Cloud Agents
- **Distributed Agents**: Enabled
- **Auto-scaling**: Enabled
- **Load Balancing**: Enabled
- **Health Checks**: Enabled

### Cloud Storage
- **Provider**: S3
- **Encryption**: Enabled
- **Backup**: Automatic

## 📊 Monitoring Tools

### Performance
- **Metrics**: Enabled
- **Profiling**: Enabled
- **Slow Query Detection**: 1000ms threshold

### Logging
- **RPC Tracing**: Enabled
- **Log Retention**: 7 days
- **Max Log Size**: 50MB
- **Max Log Files**: 20

## 🔐 Security Tools

### Code Security
- **Secret Scanning**: Enabled
- **Dependency Scanning**: Enabled
- **Vulnerability Detection**: Enabled

### Access Control
- **File Deletion Approval**: Required
- **Git Push Approval**: Optional
- **Dangerous Operations**: Blocked

## 📚 Documentation Tools

### Documentation Generation
- **Docstrings**: Auto-generated
- **Type Hints**: Required
- **API Docs**: FastAPI auto-generated
- **README**: Maintained

## 🚀 Performance Optimization

### Code Optimization
- **Lazy Loading**: Enabled
- **Code Splitting**: Enabled
- **Caching**: Enabled

### Indexing Optimization
- **Smart Indexing**: Enabled
- **Priority Files**: Configured
- **Exclusions**: Optimized

## 💡 Tips

### Using Tools Efficiently

1. **Use Tasks**: Automate common workflows
2. **Use Debug Configurations**: Debug efficiently
3. **Use Custom Commands**: Quick access to features
4. **Use Cloud Agents**: Scale processing
5. **Use MCP Servers**: Extend capabilities

### Best Practices

1. **Format on Save**: Keep code clean
2. **Lint Before Commit**: Catch issues early
3. **Run Tests**: Ensure quality
4. **Monitor Performance**: Optimize bottlenecks
5. **Use Type Hints**: Improve code quality

---

**All tools are configured and ready to use!**
