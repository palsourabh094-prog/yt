# Deployment Guide

This guide covers deploying the YouTube Transcript API to various hosting platforms.

## Table of Contents
1. [Vercel (Free Tier)](#vercel) ⭐ Recommended
2. [Heroku](#heroku)
3. [Railway](#railway)
4. [Render](#render)
5. [Docker-Based Platforms](#docker-based)

---

## Vercel

**Recommended for free hosting** - 0 setup cost, scales automatically, no credit card required for free tier.

### Prerequisites
- GitHub account with this repository pushed
- Vercel account (free)

### Step 1: Prepare Your Repository
```bash
# Ensure these files exist in root:
# - api/index.py (serverless handler)
# - vercel.json (configuration)
# - requirements.txt (dependencies)
# - run.sh (optional, for local testing)
```

### Step 2: Deploy to Vercel
```bash
# Option A: Via GitHub (Recommended)
# 1. Push your repo to GitHub
# 2. Go to https://vercel.com/new
# 3. Select "Import Git Repository"
# 4. Select your repository
# 5. Click "Deploy" (Vercel auto-detects Python project)

# Option B: Via Vercel CLI
npm install -g vercel
vercel
# Follow interactive prompts
```

### Step 3: Verify Deployment
```bash
# Get your deployment URL from Vercel dashboard
curl https://your-vercel-url.vercel.app/health
# Expected: {"status": "healthy"}

curl -X POST https://yt-phi-nine.vercel.app/transcript \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/O-1wyUQX4yc"}'
```

### Vercel Environment Variables
If you add environment variables later:
1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Add your variables
3. Redeploy

### Limits (Free Tier)
- Maximum function duration: 60 seconds
- Memory: 1024 MB
- Concurrent requests: Sufficient for moderate use
- Perfect for personal/hobby projects

### Production URL
Your API will be available at: `https://your-project-name.vercel.app`

---

## Heroku

**Good alternative** - Requires credit card, but offers free tier credits. Easier setup than Railway/Render.

### Prerequisites
- Heroku account (requires credit card)
- Heroku CLI installed

### Step 1: Create Heroku App
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Check app created
heroku apps
```

### Step 2: Deploy
```bash
# Push code to Heroku
git push heroku main  # or master depending on your branch

# View logs
heroku logs --tail
```

### Step 3: Verify
```bash
curl https://your-app-name.herokuapp.com/health
```

### Configuration
- `Procfile` already configured: `web: gunicorn app:app`
- `runtime.txt` specifies Python version
- Dependencies from `requirements.txt` auto-installed

---

## Railway

**Good option** - $5/month credit, pay-as-you-go after that.

### Prerequisites
- Railway account
- GitHub connected to Railway

### Step 1: Deploy
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select this repository
4. Railway auto-detects Python project
5. Click "Deploy"

### Step 2: Configure
- Environment variables in Railway dashboard if needed
- Check build logs in dashboard

### Step 3: Access
Railway assigns a public URL automatically

---

## Render

**Good option** - Free tier with limitations, paid plans available.

### Prerequisites
- Render account
- GitHub connected to Render

### Step 1: Deploy
1. Go to https://render.com
2. Click "New+" → "Web Service"
3. Select "Deploy an existing repository"
4. Choose this repository
5. Set Runtime: Python 3.11
6. Build Command: `pip install -r requirements.txt`
7. Start Command: `gunicorn app:app`
8. Click "Create Web Service"

### Step 2: Verify
Render provides a public URL when deployment completes

---

## Docker-Based Platforms

For platforms that require Docker (AWS, Google Cloud, Azure, DigitalOcean):

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### Create .dockerignore
```
.venv
*.pyc
__pycache__
.git
.gitignore
*.md
tests/
.env
```

### Build & Run Locally
```bash
docker build -t yt-transcript-api .
docker run -p 5000:5000 yt-transcript-api
```

### Deploy to AWS (ECS/Fargate)
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag yt-transcript-api:latest <account>.dkr.ecr.<region>.amazonaws.com/yt-transcript-api:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/yt-transcript-api:latest

# Create ECS task definition and service
# (AWS Console or CloudFormation template)
```

### Deploy to Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/yt-transcript-api
gcloud run deploy yt-transcript-api --image gcr.io/PROJECT-ID/yt-transcript-api
```

### Deploy to Azure Container Instances
```bash
az acr build --registry <registry-name> --image yt-transcript-api:latest .
az container create --resource-group <group> --name yt-transcript-api --image <registry>.azurecr.io/yt-transcript-api:latest
```

---

## Local Development

### Running Locally
```bash
# Activate virtual environment
source run.sh  # or .venv/bin/activate on Linux

# Run Flask app
python app.py

# Test endpoint
curl http://localhost:5000/health
```

### Running with Gunicorn (Production-like)
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

---

## Testing Your Deployment

### Basic Health Check
```bash
curl https://your-url/health
# Should return: {"status": "healthy"}
```

### Get Transcript
```bash
curl -X POST https://your-url/transcript \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtu.be/O-1wyUQX4yc",
    "language": "en"
  }'
```

### Get Transcript as Text
```bash
curl -X POST https://your-url/transcript/text \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/O-1wyUQX4yc"}'
```

### List Available Transcripts
```bash
curl -X POST https://your-url/list-transcripts \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/O-1wyUQX4yc"}'
```

---

## Troubleshooting

### "Module not found" errors
- Ensure `requirements.txt` has all dependencies
- Rebuild/redeploy after updating requirements
- Check `pip freeze` output locally

### Timeout errors on Vercel
- Vercel free tier has 60-second limit
- Large transcripts might timeout
- Consider chunking requests or upgrading plan

### YouTube blocks requests
- Some YouTube videos have disabled transcripts
- Some videos only have auto-generated transcripts
- Try different video URLs to test

### 404 errors
- Ensure routing is correct in `vercel.json` or Procfile
- Check that endpoints match your requests

---

## Comparison Table

| Platform | Free Tier | Setup | Scaling | Best For |
|----------|-----------|-------|---------|----------|
| **Vercel** | ✅ Yes | 2 min | Auto | Personal projects, best free option |
| **Heroku** | ⚠️ Limited | 5 min | Manual | Hobby projects with credit |
| **Railway** | ✅ $5 credit | 5 min | Auto | Small to medium projects |
| **Render** | ⚠️ Spinning down | 5 min | Auto | Sleep after inactivity |
| **AWS/GCP** | ❌ Paid | 15 min | Auto | Production, heavy use |

---

## Summary

- **Start here:** Deploy to Vercel (free, automatic, no credit card)
- **Need more power:** Railway or Render
- **Production use:** Docker-based platforms (AWS, GCP, Azure)
- **Legacy support:** Heroku (requires credit card)

Choose Vercel for the easiest setup with the YouTube Transcript API!
