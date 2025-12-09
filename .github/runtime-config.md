# GitHub Runtime Configuration Guide

## 🔐 Authentication Setup

### 1. Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name: `Cursor Cloud Agents`
4. Expiration: Set appropriate expiration (90 days recommended)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `actions:read` (Read GitHub Actions)
   - ✅ `actions:write` (Write GitHub Actions)
6. Click **Generate token**
7. **Copy the token immediately** (you won't see it again)

### 2. Set Environment Variable

#### Windows (PowerShell)
```powershell
# Set for current session
$env:GITHUB_TOKEN = "your_token_here"

# Set permanently (User)
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token_here", "User")
```

#### Windows (Command Prompt)
```cmd
setx GITHUB_TOKEN "your_token_here"
```

#### Linux/Mac
```bash
export GITHUB_TOKEN="your_token_here"
echo 'export GITHUB_TOKEN="your_token_here"' >> ~/.bashrc
```

### 3. Add to GitHub Secrets (for Actions)

1. Go to: https://github.com/halvo78/ai-program-video-music-overlay/settings/secrets/actions
2. Click **New repository secret**
3. Name: `GITHUB_TOKEN`
4. Value: Your personal access token
5. Click **Add secret**

## ⚙️ Runtime Configuration

### Environment Variables

Create a `.env` file in the workspace root:

```env
# GitHub
GITHUB_TOKEN=your_personal_access_token
GITHUB_REPOSITORY=halvo78/ai-program-video-music-overlay
GITHUB_OWNER=halvo78

# AI Providers
TOGETHER_AI_API_KEY=your_key
HUGGINGFACE_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Optional
FLUX_API_KEY=your_key
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_key
```

### Verify Configuration

```bash
# Check GitHub token
echo $env:GITHUB_TOKEN  # Windows PowerShell
echo $GITHUB_TOKEN      # Linux/Mac

# Test GitHub API access
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

## 🚀 Using GitHub Runtime

### Trigger Workflows via API

```python
import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "halvo78/ai-program-video-music-overlay"

def trigger_cloud_agent(agent_type="video", mode="hybrid"):
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/cloud-agents.yml/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main",
        "inputs": {
            "agent_type": agent_type,
            "workflow_mode": mode,
            "platform": "github-actions"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

### Check Workflow Status

```python
def get_workflow_runs():
    url = f"https://api.github.com/repos/{REPO}/actions/runs"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    return response.json()
```

## 📋 Configuration Files

- `.cursor/github-runtime-config.json` - Runtime configuration
- `.cursor/git-config.json` - Git configuration
- `.cursor/environment.json` - Environment settings
- `.env` - Environment variables (create this)

## ✅ Verification Checklist

- [ ] GitHub token created with correct scopes
- [ ] GITHUB_TOKEN environment variable set
- [ ] Token added to GitHub Secrets
- [ ] .env file created (optional)
- [ ] GitHub API access tested
- [ ] Workflow can be triggered manually
- [ ] Cloud agents workflow runs successfully

## 🔒 Security Notes

1. **Never commit tokens** to repository
2. **Use environment variables** for local development
3. **Use GitHub Secrets** for Actions
4. **Rotate tokens** regularly
5. **Use minimal scopes** required

## 🆘 Troubleshooting

### Token Not Working
- Verify token has correct scopes
- Check token hasn't expired
- Verify environment variable is set
- Test with curl/API directly

### Workflow Not Triggering
- Check GitHub Actions is enabled
- Verify workflow file syntax
- Check branch protection rules
- Review workflow logs

### API Rate Limits
- GitHub API: 5000 requests/hour (authenticated)
- Use token to increase limits
- Implement retry logic
- Cache responses when possible

---

**Runtime configuration is ready! Set GITHUB_TOKEN and you're good to go.**
