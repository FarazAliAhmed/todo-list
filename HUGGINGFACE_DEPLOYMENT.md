# Hugging Face Spaces Deployment Guide

Deploy your FastAPI backend to Hugging Face Spaces for FREE (no credit card required).

## 🆓 Why Hugging Face Spaces?

| Feature | Hugging Face | Render Free |
|---------|--------------|-------------|
| Credit Card | ❌ NOT required | ⚠️ Required |
| Sleep Time | 48 hours inactivity | 15 minutes |
| Wake Up | ~30 seconds | ~30 seconds |
| CPU | 2 vCPU | Shared |
| RAM | 16 GB | Limited |
| Cost | FREE | FREE |

## 🚀 Deployment Steps

### Step 1: Create Hugging Face Account

1. Go to https://huggingface.co
2. Click "Sign Up"
3. Create account with email or GitHub
4. Verify your email

### Step 2: Create a New Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Owner**: Your username
   - **Space name**: `todo-backend`
   - **License**: MIT
   - **SDK**: Select **Docker**
   - **Hardware**: **CPU basic (Free)**
   - **Visibility**: Public

3. Click "Create Space"

### Step 3: Clone the Space Repository

```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
cd todo-backend
```

### Step 4: Copy Backend Files

Copy these files from your project to the space:

```bash
# From your project root
cp -r backend/app ./todo-backend/
cp backend/requirements.txt ./todo-backend/
```

### Step 5: Create Dockerfile

Create a `Dockerfile` in your space (not Dockerfile.huggingface):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Step 6: Create README.md for Space

Create `README.md` with this frontmatter:

```markdown
---
title: Todo API Backend
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo API Backend

FastAPI backend for the Evolution of Todo application.

Visit `/docs` for API documentation.
```

### Step 7: Set Environment Variables (Secrets)

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/todo-backend`
2. Click "Settings" tab
3. Scroll to "Repository secrets"
4. Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DATABASE_URL` | Your Neon connection string |
| `JWT_SECRET` | Your secret key (32+ chars) |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_EXPIRATION_DAYS` | `7` |
| `CORS_ORIGINS` | `https://your-app.vercel.app` |

### Step 8: Update Backend Config to Read Secrets

The backend needs to read from environment variables. Your `backend/app/config.py` should already do this.

### Step 9: Push to Hugging Face

```bash
cd todo-backend

# Add all files
git add .
git commit -m "Deploy Todo API backend"

# Push to Hugging Face
git push
```

### Step 10: Wait for Build

1. Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/todo-backend`
2. Click "App" tab to see build logs
3. Wait 3-5 minutes for build and deployment
4. Once running, your API is at: `https://YOUR_USERNAME-todo-backend.hf.space`

### Step 11: Test Your Deployment

```bash
# Test health endpoint
curl https://YOUR_USERNAME-todo-backend.hf.space/health

# Should return:
# {"status":"healthy","service":"todo-api","version":"2.0.0"}

# Test API docs
# Visit: https://YOUR_USERNAME-todo-backend.hf.space/docs
```

## 📁 Final Space Structure

Your Hugging Face Space should look like:

```
todo-backend/
├── Dockerfile
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── database.py
    ├── exceptions.py
    ├── models/
    ├── routes/
    ├── schemas/
    ├── middleware/
    └── migrations/
```

## 🔧 Update Frontend Environment

After deployment, update your Vercel frontend:

1. Go to Vercel dashboard
2. Project Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL`:
   ```
   NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-todo-backend.hf.space
   ```
4. Redeploy frontend

## ⚠️ Important Notes

### Port 7860
Hugging Face Spaces expects apps to run on port **7860**, not 8000.

### Secrets vs Environment Variables
- Use "Repository secrets" in Settings for sensitive data
- Secrets are injected as environment variables at runtime

### Sleep Behavior
- Free spaces sleep after **48 hours** of inactivity (much better than Render's 15 min!)
- First request after sleep takes ~30 seconds

### Public Visibility
- Free tier requires public spaces
- Your code will be visible, but secrets are hidden

## 🔄 Alternative: Direct Git Push

Instead of cloning, you can push directly:

```bash
# From your project root
cd backend

# Add Hugging Face as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/todo-backend

# Create a branch with only backend files
git subtree push --prefix=backend hf main
```

## 🐛 Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Ensure all required files are present
- Check build logs in "App" tab

### App Won't Start
- Verify port is 7860
- Check environment variables/secrets
- Review runtime logs

### Database Connection Fails
- Verify DATABASE_URL secret is set correctly
- Ensure Neon allows connections from Hugging Face IPs
- Check for `?sslmode=require` in connection string

### CORS Errors
- Update CORS_ORIGINS secret with your Vercel URL
- Rebuild the space after changing secrets

## 📊 Your Deployment URLs

After deployment:

| Service | URL |
|---------|-----|
| **Backend API** | `https://YOUR_USERNAME-todo-backend.hf.space` |
| **API Docs** | `https://YOUR_USERNAME-todo-backend.hf.space/docs` |
| **Health Check** | `https://YOUR_USERNAME-todo-backend.hf.space/health` |
| **Frontend** | `https://your-app.vercel.app` |

## ✅ Deployment Checklist

- [ ] Hugging Face account created
- [ ] Space created with Docker SDK
- [ ] Files copied to space
- [ ] Dockerfile created (port 7860)
- [ ] README.md with frontmatter created
- [ ] Secrets configured (DATABASE_URL, JWT_SECRET, etc.)
- [ ] Code pushed to space
- [ ] Build completed successfully
- [ ] Health endpoint returns 200
- [ ] API docs accessible
- [ ] Frontend updated with new API URL
- [ ] End-to-end test passed

## 🎉 Done!

Your backend is now deployed on Hugging Face Spaces for FREE!

**Backend URL**: `https://YOUR_USERNAME-todo-backend.hf.space`

Use this URL in your hackathon submission along with your Vercel frontend URL.
