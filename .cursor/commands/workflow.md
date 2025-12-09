# /workflow Command

Manage video creation workflows.

## Usage

```
/workflow [action] [workflow_id]
```

## Actions

| Action | Description |
|--------|-------------|
| `create` | Create a new workflow |
| `status` | Show workflow status |
| `list` | List all workflows |
| `cancel` | Cancel a workflow |

## Workflow Modes

| Mode | Description |
|------|-------------|
| `sequential` | Best quality, step-by-step |
| `parallel` | Fastest, concurrent |
| `hybrid` | Balanced (recommended) |

## Examples

```bash
# Create a new workflow
/workflow create "Create a motivational video" --mode hybrid --platforms tiktok,instagram

# Show workflow status
/workflow status <workflow_id>

# List all workflows
/workflow list

# Cancel a workflow
/workflow cancel <workflow_id>
```

## Create Workflow Parameters

```json
{
  "prompt": "Create a motivational video about success",
  "mode": "hybrid",
  "platforms": ["tiktok", "instagram_reels"],
  "parameters": {
    "duration": 60,
    "style": "energetic"
  }
}
```
