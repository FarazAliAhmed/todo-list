# Quick Hugging Face Deployment (Using Your Method)

This guide uses the same method you used for your previous project.

## 🚀 Quick Steps

### Step 1: Create Hugging Face Space (One-Time Setup)

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Owner**: `faraz7530` (your username)
   - **Space name**: `todo-backend`
   - **License**: MIT
   - **SDK**: **Docker**
   - **Hardware**: **CPU basic (Free)**
   - **Visibility**: Public
3. Click **"Create Space"**

### Step 2: Run Deployment Script

```bash
# Make sure you're in the project root
cd ~/Project/Panaversity-todo

# Run the deployment script
./deploy-to-huggingface.sh
```

The script will:
- ✅ Clean up old deployment
- ✅ Clone your Hugging Face Space
- ✅ Copy backend files
- ✅ Create Dockerfile (port 7860)
- ✅ Create README.md with frontmatter
- ✅ Remove sensitive files (.env)
- ✅ Commit and push to Hugging Face

### Step 3: Add Secrets in Hugging Face

1. Go to: https://huggingface.co/spaces/faraz7530/todo-backend
2. Click **"Settings"** tab
3. Scroll to **"Repository secrets"**
4. Add these secrets:

| Secret Name | Value | Where to Get |
|-------------|-------|--------------|
| `DATABASE_URL` | Your Neon connection string | From `backend/.env` |
| `JWT_SECRET` | Your secret key (32+ chars) | Same as Vercel `BETTER_AUTH_SECRET` |
| `JWT_ALGORITHM` | `HS256` | Fixed value |
| `JWT_EXPIRATION_DAYS` | `7` | Fixed value |
| `CORS_ORIGINS` | Your Vercel URL | From Vercel deployment |

**Example values:**
```
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=<same as your Vercel BETTER_AUTH_SECRET>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://your-app.vercel.app
```

### Step 4: Wait for Build

1. Go to **"App"** tab in your Space
2. Watch the build logs
3. Wait 3-5 minutes for build to complete
4. Once you see "Running", your API is live!

### Step 5: Test Your Backend

```bash
# Test health endpoint
curl https://faraz7530-todo-backend.hf.space/health

# Should return:
# {"status":"healthy","service":"todo-api","version":"2.0.0"}
```

Or visit in browser:
- **API**: https://faraz7530-todo-backend.hf.space
- **Docs**: https://faraz7530-todo-backend.hf.space/docs

### Step 6: Update Vercel Frontend

Now update your frontend to use the new backend:

1. Go to Vercel dashboard
2. Your project → **Settings** → **Environment Variables**
3. Edit `NEXT_PUBLIC_API_URL`
4. Change to: `https://faraz7530-todo-backend.hf.space`
5. Go to **Deployments** → Click **"..."** → **"Redeploy"**

## ✅ Done!

Your full stack is now deployed:

| Service | URL |
|---------|-----|
| **Frontend** | https://your-app.vercel.app |
| **Backend** | https://faraz7530-todo-backend.hf.space |
| **API Docs** | https://faraz7530-todo-backend.hf.space/docs |

## 🧪 Test End-to-End

1. Visit your Vercel frontend
2. Sign up for a new account
3. Log in
4. Create a task
5. Update the task
6. Mark as complete
7. Delete the task

Everything should work! 🎉

## 🐛 Troubleshooting

### Script fails with "Space not found"
- Make sure you created the Space first (Step 1)
- Check the space name is exactly `todo-backend`

### Build fails on Hugging Face
- Check build logs in "App" tab
- Verify Dockerfile syntax
- Ensure all files copied correctly

### "Connection refused" errors
- Wait for build to complete (3-5 minutes)
- Check Space is "Running" not "Building"

### CORS errors in frontend
- Verify `CORS_ORIGINS` secret includes your Vercel URL
- Rebuild the Space after adding secrets

### "Invalid token" errors
- Ensure `JWT_SECRET` matches Vercel `BETTER_AUTH_SECRET` exactly
- Both must be the same value

## 📝 For Hackathon Submission

You now have:

1. ✅ **GitHub Repo**: https://github.com/FarazAliAhmed/todo-list
2. ✅ **Frontend URL**: https://your-app.vercel.app
3. ✅ **Backend URL**: https://faraz7530-todo-backend.hf.space
4. ⏳ **Demo Video**: Record now (max 90 seconds)

Submit at: https://forms.gle/CQsSEGM3GeCrL43c8

## 🔄 Redeployment

To redeploy after making changes:

```bash
# Make changes to your backend
cd ~/Project/Panaversity-todo/backend

# Run deployment script again
cd ..
./deploy-to-huggingface.sh
```

The script handles everything automatically!
