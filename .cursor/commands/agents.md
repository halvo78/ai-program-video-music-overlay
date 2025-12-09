# /agents Command

Manage and monitor AI agents.

## Usage

```
/agents [action] [agent_name]
```

## Actions

| Action | Description |
|--------|-------------|
| `status` | Show status of all agents (default) |
| `start` | Start an agent |
| `stop` | Stop an agent |
| `restart` | Restart an agent |
| `logs` | Show agent logs |

## Agent Names

| Agent | Purpose |
|-------|---------|
| `video` | Video generation agent |
| `music` | Music generation agent |
| `image` | Image generation agent |
| `voice` | Voice/TTS agent |
| `content` | Content analysis agent |
| `editing` | Video editing agent |
| `optimization` | Platform optimization agent |
| `analytics` | Analytics agent |
| `safety` | Content moderation agent |
| `social` | Social media agent |
| `all` | All agents |

## Examples

```bash
# Show status of all agents
/agents

# Show status of specific agent
/agents status video

# Start video agent
/agents start video

# Stop music agent
/agents stop music

# Restart all agents
/agents restart all

# Show logs for content agent
/agents logs content
```

## Output

### Agent Status

```
╔══════════════════════════════════════════════════════════════╗
║                    AGENT STATUS                              ║
╠══════════════════════════════════════════════════════════════╣
║  Video Agent:        RUNNING                                 ║
║  Music Agent:        RUNNING                                 ║
║  Image Agent:        IDLE                                    ║
║  Voice Agent:        RUNNING                                 ║
║  Content Agent:      RUNNING                                 ║
║  Editing Agent:      IDLE                                    ║
║  Optimization Agent: RUNNING                                 ║
║  Analytics Agent:    RUNNING                                 ║
║  Safety Agent:       RUNNING                                 ║
║  Social Agent:       IDLE                                    ║
╚══════════════════════════════════════════════════════════════╝
```
