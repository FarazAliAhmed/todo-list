# Deployment Guide - Phase II Full-Stack Application

This guide covers deploying the Evolution of Todo application to production environments.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Backend Deployment](#backend-deployment)
4. [Database Setup (Neon)](#database-setup-neon)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Troubleshooting](#troubleshooting)

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Tested the application locally
- [ ] All tests passing
- [ ] Environment variables documented
- [ ] Database migrations ready
- [ ] CORS origins configured
- [ ] JWT secrets generated (minimum 32 characters)
- [ ] Git repository pushed to GitHub/GitLab

## Frontend Deployment (Vercel)

Vercel is the recommended platform for deploying Next.js applications.

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy from Frontend Directory

```bash
cd frontend
vercel
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Select your account
- **Link to existing project?** No (first time)
- **Project name?** evolution-of-todo (or your preferred name)
- **Directory?** ./ (current directory)
- **Override settings?** No

### Step 4: Configure Environment Variables

In the Vercel dashboard (https://vercel.com/dashboard):

1. Go to your project
2. Click **Settings** → **Environment Variables**
3. Add the following variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | Your backend URL (e.g., https://api.yourdomain.com) | Production |
| `BETTER_AUTH_SECRET` | Your 32+ character secret | Production |
| `BETTER_AUTH_URL` | Your frontend URL (e.g., https://yourdomain.com) | Production |

### Step 5: Deploy to Production

```bash
vercel --prod
```

Your frontend is now live! Note the deployment URL.

### Alternative: GitHub Integration

1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your repository
4. Configure environment variables
5. Deploy automatically on every push

## Backend Deployment

### Option 1: Railway

Railway provides easy deployment for Python applications.

#### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

#### Step 2: Login and Initialize

```bash
railway login
cd backend
railway init
```

#### Step 3: Add Environment Variables

```bash
railway variables set DATABASE_URL="your-neon-connection-string"
railway variables set JWT_SECRET="your-secret-key"
railway variables set JWT_ALGORITHM="HS256"
railway variables set JWT_EXPIRATION_DAYS="7"
railway variables set CORS_ORIGINS="https://your-frontend-url.vercel.app"
```

#### Step 4: Deploy

```bash
railway up
```

#### Step 5: Get Deployment URL

```bash
railway domain
```

### Option 2: Render

#### Step 1: Create New Web Service

1. Go to https://render.com/dashboard
2. Click **New** → **Web Service**
3. Connect your Git repository
4. Configure:
   - **Name**: todo-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 2: Add Environment Variables

In the Render dashboard, add:
- `DATABASE_URL`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `JWT_EXPIRATION_DAYS`
- `CORS_ORIGINS`

#### Step 3: Deploy

Render will automatically deploy your application.

### Option 3: Docker Container (Any Platform)

#### Step 1: Build Docker Image

```bash
cd backend
docker build -t todo-backend .
```

#### Step 2: Test Locally

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="your-connection-string" \
  -e JWT_SECRET="your-secret" \
  -e CORS_ORIGINS="http://localhost:3000" \
  todo-backend
```

#### Step 3: Push to Container Registry

```bash
# Tag image
docker tag todo-backend your-registry/todo-backend:latest

# Push to registry
docker push your-registry/todo-backend:latest
```

#### Step 4: Deploy to Cloud Platform

Deploy the container to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## Database Setup (Neon)

Neon is a serverless PostgreSQL database that's production-ready by default.

### Step 1: Create Production Database

1. Go to https://console.neon.tech
2. Click **New Project**
3. Configure:
   - **Name**: evolution-of-todo-prod
   - **Region**: Choose closest to your backend
   - **PostgreSQL Version**: 16 (latest)

### Step 2: Get Connection String

1. Go to project dashboard
2. Click **Connection Details**
3. Copy the connection string
4. Format: `postgresql://user:password@host/database?sslmode=require`

### Step 3: Run Migrations

```bash
# Set DATABASE_URL temporarily
export DATABASE_URL="your-production-connection-string"

# Run migrations
cd backend
python -m app.migrations.create_tables
```

### Step 4: Verify Database

```bash
# Connect with psql
psql "your-connection-string"

# Check tables
\dt

# Verify schema
\d users
\d tasks
```

## Environment Variables

### Production Environment Variables Summary

#### Frontend (Vercel)

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
BETTER_AUTH_SECRET=your-32-character-secret-key-here
BETTER_AUTH_URL=https://your-frontend-url.vercel.app
```

#### Backend (Railway/Render/Docker)

```env
DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require
JWT_SECRET=your-32-character-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://your-frontend-url.vercel.app
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Security Best Practices

1. **Generate Strong Secrets**:
   ```bash
   openssl rand -base64 32
   ```

2. **Match JWT Secrets**: Ensure `JWT_SECRET` (backend) equals `BETTER_AUTH_SECRET` (frontend)

3. **Use Environment-Specific Values**: Never use development secrets in production

4. **Enable SSL**: Always use `sslmode=require` for database connections

5. **Restrict CORS**: Only allow your frontend domain in `CORS_ORIGINS`

## Post-Deployment Verification

### Step 1: Check Backend Health

```bash
curl https://your-backend-url.railway.app/health
```

Expected response:
```json
{"status": "healthy"}
```

### Step 2: Check API Documentation

Visit: `https://your-backend-url.railway.app/docs`

You should see the Swagger UI with all endpoints.

### Step 3: Test Frontend

1. Visit your frontend URL
2. Sign up for a new account
3. Log in
4. Create a task
5. Update the task
6. Mark as complete
7. Delete the task

### Step 4: Verify User Isolation

1. Create a second user account
2. Log in as second user
3. Verify you cannot see first user's tasks

### Step 5: Check Logs

#### Vercel Logs
```bash
vercel logs
```

#### Railway Logs
```bash
railway logs
```

#### Render Logs
Check the Render dashboard → Logs tab

## Troubleshooting

### Frontend Issues

#### "Failed to fetch" errors

**Cause**: CORS not configured correctly

**Solution**:
1. Check `CORS_ORIGINS` in backend includes your frontend URL
2. Ensure no trailing slashes in URLs
3. Verify HTTPS is used in production

#### "Invalid token" errors

**Cause**: JWT secrets don't match

**Solution**:
1. Verify `JWT_SECRET` (backend) equals `BETTER_AUTH_SECRET` (frontend)
2. Regenerate secrets if needed
3. Redeploy both frontend and backend

### Backend Issues

#### Database connection errors

**Cause**: Invalid `DATABASE_URL` or network issues

**Solution**:
1. Verify connection string format
2. Check Neon database is running
3. Ensure `sslmode=require` is included
4. Test connection with `psql`

#### 500 Internal Server Error

**Cause**: Application error or missing environment variables

**Solution**:
1. Check backend logs for stack traces
2. Verify all environment variables are set
3. Ensure database migrations have run
4. Check database connectivity

### Database Issues

#### Tables not found

**Cause**: Migrations not run

**Solution**:
```bash
export DATABASE_URL="your-production-url"
cd backend
python -m app.migrations.create_tables
```

#### Connection timeout

**Cause**: Network or firewall issues

**Solution**:
1. Check Neon database status
2. Verify IP allowlist (if configured)
3. Test connection from deployment platform

## Monitoring and Maintenance

### Set Up Monitoring

1. **Vercel Analytics**: Enable in project settings
2. **Backend Monitoring**: Use platform-specific tools (Railway metrics, Render monitoring)
3. **Database Monitoring**: Check Neon dashboard for query performance

### Regular Maintenance

- [ ] Monitor error logs weekly
- [ ] Review database performance monthly
- [ ] Update dependencies quarterly
- [ ] Backup database regularly (Neon has automatic backups)
- [ ] Review and rotate secrets annually

## Rollback Procedure

### Frontend Rollback (Vercel)

```bash
# List deployments
vercel ls

# Rollback to previous deployment
vercel rollback [deployment-url]
```

### Backend Rollback

#### Railway
```bash
railway rollback
```

#### Render
Use the Render dashboard to redeploy a previous version.

#### Docker
```bash
# Deploy previous image version
docker pull your-registry/todo-backend:previous-tag
# Redeploy container
```

## Support

For issues or questions:
- Check application logs first
- Review this deployment guide
- Consult platform-specific documentation
- Check GitHub issues

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Neon Documentation](https://neon.tech/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
