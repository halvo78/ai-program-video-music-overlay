# /api Command

Manage FastAPI backend server.

## Usage

```
/api [action]
```

## Actions

| Action | Description |
|--------|-------------|
| `start` | Start FastAPI server |
| `stop` | Stop FastAPI server |
| `restart` | Restart FastAPI server |
| `status` | Show server status |
| `docs` | Open API documentation |

## Examples

```bash
# Start API server
/api start

# Stop API server
/api stop

# Restart API server
/api restart

# Check server status
/api status

# Open API docs
/api docs
```

## Server Information

- **Port**: 8000 (default)
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Status**: http://localhost:8000/status
