# GitHub Cloud Agents Setup Guide

## ☁️ Complete GitHub Setup for Cloud Agents

This guide will help you set up GitHub for cloud agent execution and automation.

## 📋 Prerequisites

1. GitHub repository: https://github.com/halvo78/ai-program-video-music-overlay
2. GitHub account with Actions enabled
3. AWS account (optional, for AWS agents)
4. Docker (optional, for Docker agents)

## 🔧 Setup Steps

### 1. Enable GitHub Actions

1. Go to your repository: https://github.com/halvo78/ai-program-video-music-overlay
2. Click **Settings** → **Actions** → **General**
3. Enable **Allow all actions and reusable workflows**
4. Save changes

### 2. Configure GitHub Secrets

Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

#### Required Secrets

```bash
# AWS (for AWS cloud agents)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# API Keys (for AI agents)
TOGETHER_AI_API_KEY=your_together_key
HUGGINGFACE_API_KEY=your_hf_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional
FLUX_API_KEY=your_flux_key
STRIPE_SECRET_KEY=your_stripe_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

#### Vercel (for dashboard deployment)
```bash
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
```

### 3. Configure GitHub Environments

Go to **Settings** → **Environments** → **New environment**

Create environments:
- **staging** - For staging deployments
- **production** - For production deployments

For each environment, add:
- **Deployment branches**: `main` for production, `develop` for staging
- **Required reviewers**: (optional)
- **Secrets**: Environment-specific secrets

### 4. Set Up Branch Protection

Go to **Settings** → **Branches** → **Add rule**

For `main` branch:
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Include administrators

Required status checks:
- `lint-and-test`
- `test-dashboard`
- `security-scan`

### 5. Configure Dependabot

Dependabot is already configured in `.github/dependabot.yml`. It will:
- Check Python dependencies weekly
- Check Node.js dependencies weekly
- Check GitHub Actions weekly
- Create PRs automatically

## 🚀 Using Cloud Agents

### Manual Execution

1. Go to **Actions** tab
2. Select **Cloud Agents - Distributed Processing**
3. Click **Run workflow**
4. Select:
   - **Agent type**: video, music, image, etc., or "all"
   - **Workflow mode**: sequential, parallel, or hybrid
   - **Platform**: aws, docker, github-actions, or all
5. Click **Run workflow**

### Scheduled Execution

Cloud agents run automatically:
- **Daily at 2 AM UTC**: Health check for all agents
- **On push to main**: If agent files changed

### Via API

You can trigger workflows via GitHub API:

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/halvo78/ai-program-video-music-overlay/actions/workflows/cloud-agents.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "agent_type": "video",
      "workflow_mode": "hybrid",
      "platform": "github-actions"
    }
  }'
```

## 📊 Workflow Overview

### 1. CI Workflow (`ci.yml`)
- Runs on every push/PR
- Lints and tests Python code
- Tests dashboard
- Security scanning
- **Runs on**: GitHub Actions runners

### 2. Cloud Agents Workflow (`cloud-agents.yml`)
- Manual execution or scheduled
- Runs agents on selected platform
- Orchestrates distributed processing
- Health checks
- **Runs on**: GitHub Actions, AWS, or Docker

### 3. Deploy Workflow (`deploy.yml`)
- Manual execution
- Deploys backend to AWS
- Deploys dashboard to Vercel
- **Runs on**: GitHub Actions runners

### 4. Agent Testing Workflow (`agent-testing.yml`)
- Tests individual agents
- Integration tests
- **Runs on**: GitHub Actions runners

## 🎯 Cloud Agent Platforms

### GitHub Actions (Default)
- **Cost**: Free (2000 minutes/month)
- **Max Agents**: Unlimited (within limits)
- **Setup**: Automatic
- **Best for**: Testing, CI/CD, scheduled tasks

### AWS EC2
- **Cost**: Pay per use
- **Max Agents**: 50 (configurable)
- **Setup**: Requires AWS credentials
- **Best for**: Production, high-performance tasks

### Docker
- **Cost**: Free (local) or hosting cost
- **Max Agents**: 20 (configurable)
- **Setup**: Requires Docker
- **Best for**: Local development, containerized execution

## 📈 Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. Select workflow
3. View run details, logs, and artifacts

### View Agent Logs

Agent logs are uploaded as artifacts:
- Available for 7 days
- Download from workflow run page
- Named: `agent-logs-{agent-type}`

### Health Checks

Health checks run daily and:
- Test all agents
- Create issues on failure
- Report status in workflow summary

## 🔍 Troubleshooting

### Workflow Not Running

1. Check **Actions** tab for errors
2. Verify secrets are set correctly
3. Check branch protection rules
4. Verify workflow file syntax

### Agent Execution Fails

1. Check agent logs in artifacts
2. Verify API keys in secrets
3. Check agent code for errors
4. Review workflow logs

### AWS Agents Not Working

1. Verify AWS credentials in secrets
2. Check AWS region (us-east-1)
3. Verify IAM permissions
4. Check AWS service limits

### Docker Agents Not Working

1. Verify Docker is available
2. Check Docker image exists
3. Verify Docker permissions
4. Check resource limits

## 🔐 Security Best Practices

1. **Never commit secrets**: Use GitHub Secrets
2. **Use environment-specific secrets**: Different secrets for staging/production
3. **Limit secret access**: Only grant access to needed workflows
4. **Rotate secrets regularly**: Update API keys periodically
5. **Review workflow changes**: Always review PRs that change workflows
6. **Use branch protection**: Protect main branch

## 📚 Workflow Files

All workflows are in `.github/workflows/`:

- `ci.yml` - Continuous Integration
- `cloud-agents.yml` - Cloud agent execution
- `deploy.yml` - Deployment
- `agent-testing.yml` - Agent testing
- `codespaces-setup.yml` - Codespaces setup

## 🎉 You're Ready!

Your GitHub repository is now configured for cloud agents. You can:

1. **Run agents manually**: Actions → Cloud Agents → Run workflow
2. **Monitor execution**: View workflow runs and logs
3. **Deploy automatically**: Use deploy workflow
4. **Test agents**: Use agent testing workflow

## 📞 Support

- **Workflow Issues**: Check Actions tab
- **Agent Issues**: Use agent issue template
- **Cloud Agent Requests**: Use cloud agent request template

---

**Cloud agents are ready to use on GitHub!**
