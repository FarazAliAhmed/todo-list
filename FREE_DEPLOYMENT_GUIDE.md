# Free Deployment Guide (No Credit Card Required)

This guide shows you how to deploy the Todo app completely FREE without any credit card.

## 🆓 Free Services (NO Credit Card)

| Service | Purpose | Free Tier | Credit Card? |
|---------|---------|-----------|--------------|
| **Neon** | PostgreSQL Database | 0.5 GB storage | ❌ NO |
| **Hugging Face** | Backend (FastAPI) | 2 vCPU, 16GB RAM | ❌ NO |
| **Vercel** | Frontend (Next.js) | Unlimited projects | ❌ NO |

### ⚠️ Note on Render
Render now requires a credit card for new accounts. Use **Hugging Face Spaces** instead!

## 🚀 Quick Deployment Steps

### 1. Database (Neon) - Already Set Up ✅

You already have Neon configured. Just verify:

```bash
cat backend/.env | grep DATABASE_URL
```

### 2. Deploy Backend to Hugging Face Spaces (Recommended - No Credit Card!)

#### Sign Up
1. Go to https://huggingface.co
2. Sign up with email or GitHub (NO credit card required!)
3. Verify your email

#### Create Space
1. Go to https://huggingface.co/new-space
2. Configure:
   - **Owner**: Your username
   - **Space name**: `todo-backend`
   - **License**: MIT
   - **SDK**: **Docker**
   - **Hardware**: **CPU basic (Free)**
   - **Visibility**: Public
3. Click "Create Space"

#### Clone and Setup
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
cd todo-backend

# Copy backend files from your project
cp -r /path/to/your/project/backend/app ./
cp /path/to/your/project/backend/requirements.txt ./
```

#### Create Dockerfile
Create `Dockerfile` in the space:
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

#### Create README.md
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
```

#### Add Secrets
1. Go to Space Settings → Repository secrets
2. Add:
   - `DATABASE_URL`: Your Neon connection string
   - `JWT_SECRET`: Your secret key (32+ chars)
   - `JWT_ALGORITHM`: `HS256`
   - `JWT_EXPIRATION_DAYS`: `7`
   - `CORS_ORIGINS`: `https://your-app.vercel.app`

#### Deploy
```bash
git add .
git commit -m "Deploy Todo API"
git push
```

Wait 3-5 minutes. Your backend URL: `https://YOUR_USERNAME-todo-backend.hf.space`

✅ **Advantage**: Sleeps after 48 hours (not 15 min like Render!)

### 3. Deploy Frontend to Vercel

#### Sign Up
1. Go to https://vercel.com
2. Sign up with GitHub (no credit card)

#### Deploy
1. Click "Add New..." → "Project"
2. Import your GitHub repository
3. Configure:
   - **Framework**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`

4. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://todo-backend-xxxx.onrender.com
   BETTER_AUTH_SECRET=your-secret-key-must-match-backend
   BETTER_AUTH_URL=https://your-app.vercel.app
   ```

5. Click "Deploy"
6. Wait 2-3 minutes
7. Copy your frontend URL: `https://your-app.vercel.app`

#### Update Environment Variable
1. Go to Project Settings → Environment Variables
2. Update `BETTER_AUTH_URL` with your actual Vercel URL
3. Go to Deployments → Click "..." → "Redeploy"

### 4. Update Backend CORS

1. In Render dashboard, go to your backend service
2. Click "Environment"
3. Update `CORS_ORIGINS` with your Vercel URL
4. Service will auto-redeploy

### 5. Verify Deployment

```bash
# Test backend
curl https://todo-backend-xxxx.onrender.com/health

# Test frontend
curl -I https://your-app.vercel.app

# Or use the verification script
FRONTEND_URL=https://your-app.vercel.app \
BACKEND_URL=https://todo-backend-xxxx.onrender.com \
./verify-deployment.sh
```

## 🎯 Testing Your Deployment

1. Visit your Vercel URL
2. Sign up for a new account
3. Log in
4. Create a task
5. Update the task
6. Mark as complete
7. Delete the task

## ⚠️ Free Tier Limitations

### Render Free Tier
- **Spin down**: Services sleep after 15 minutes of inactivity
- **Wake up time**: ~30 seconds for first request after sleep
- **Hours**: 750 hours/month (enough for 24/7 if only one service)
- **Performance**: Slower than paid tiers

### Vercel Free Tier
- **Bandwidth**: 100 GB/month
- **Builds**: 6,000 minutes/month
- **Serverless executions**: 100 GB-hours
- **No custom domains** on free tier (use .vercel.app subdomain)

### Neon Free Tier
- **Storage**: 0.5 GB
- **Compute**: Shared
- **Branches**: 1 branch
- **History**: 7 days

## 🔧 Troubleshooting

### Backend takes 30 seconds to respond
- **Cause**: Render free tier spins down after inactivity
- **Solution**: This is normal. Wait for wake up. Consider keeping it alive with a cron job (see below)

### CORS errors
- **Cause**: `CORS_ORIGINS` doesn't match frontend URL
- **Solution**: Update `CORS_ORIGINS` in Render environment variables

### "Invalid token" errors
- **Cause**: JWT secrets don't match
- **Solution**: Ensure `JWT_SECRET` (backend) equals `BETTER_AUTH_SECRET` (frontend)

### Database connection errors
- **Cause**: Invalid `DATABASE_URL`
- **Solution**: Copy connection string from Neon dashboard, ensure `?sslmode=require` is included

## 💡 Keep Render Service Awake (Optional)

Free Render services sleep after 15 minutes. To keep it awake:

### Option 1: Use Cron-Job.org (Free)

1. Sign up at https://cron-job.org (free, no credit card)
2. Create a new cron job:
   - **URL**: `https://todo-backend-xxxx.onrender.com/health`
   - **Schedule**: Every 10 minutes
   - **Method**: GET

### Option 2: Use UptimeRobot (Free)

1. Sign up at https://uptimerobot.com (free, no credit card)
2. Add new monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://todo-backend-xxxx.onrender.com/health`
   - **Monitoring Interval**: 5 minutes

⚠️ **Note**: This uses more of your 750 free hours but keeps the service responsive.

## 📊 Monitoring Your Free Services

### Render
- Dashboard shows: Deployments, Logs, Metrics
- Check logs for errors: Service → Logs tab

### Vercel
- Dashboard shows: Deployments, Analytics, Logs
- Check function logs: Project → Logs

### Neon
- Dashboard shows: Storage usage, Queries, Connections
- Monitor database health: Project → Monitoring

## 🎓 Summary

You now have a fully deployed application with:
- ✅ Frontend on Vercel (free forever)
- ✅ Backend on Render (750 hours/month free)
- ✅ Database on Neon (0.5 GB free)
- ✅ No credit card required
- ✅ Production-ready URLs for hackathon submission

## 📝 Submission Checklist

For the hackathon form, you need:

- [ ] GitHub repository URL (public)
- [ ] Vercel frontend URL: `https://your-app.vercel.app`
- [ ] Render backend URL: `https://todo-backend-xxxx.onrender.com`
- [ ] Demo video (under 90 seconds)
- [ ] WhatsApp number

## 🚀 Next Steps

After deployment:
1. Test all features thoroughly
2. Record your demo video (max 90 seconds)
3. Submit via the hackathon form
4. Start working on Phase III (AI Chatbot)

---

**Need Help?**
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guide
- Check [VERIFICATION.md](VERIFICATION.md) for testing procedures
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

**Good luck with your submission! 🎉**
