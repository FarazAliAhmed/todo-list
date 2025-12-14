# Vercel Deployment - Complete Step-by-Step Guide

Follow these steps exactly to deploy your frontend to Vercel.

## ✅ Step 1: Push Code to GitHub

### Fix GitHub Authentication

You're getting a 403 error. Here's how to fix it:

**Option A: Use GitHub CLI (Recommended)**

```bash
# Install GitHub CLI if not installed
brew install gh

# Login to GitHub
gh auth login

# Follow prompts:
# - What account? GitHub.com
# - Protocol? HTTPS
# - Authenticate? Yes (opens browser)

# After login, push again
git push origin main
```

**Option B: Use Personal Access Token**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Vercel Deployment"
4. Select scopes: `repo` (all)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

Then push with token:
```bash
# Use token as password
git push https://YOUR_USERNAME:YOUR_TOKEN@github.com/FarazAliAhmed/todo-list.git main
```

**Option C: Use SSH**

```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# 1. Go to https://github.com/settings/keys
# 2. Click "New SSH key"
# 3. Paste your public key
# 4. Click "Add SSH key"

# Change remote to SSH
git remote set-url origin git@github.com:FarazAliAhmed/todo-list.git

# Push
git push origin main
```

---

## ✅ Step 2: Sign Up for Vercel

1. **Go to**: https://vercel.com
2. **Click**: "Sign Up"
3. **Choose**: "Continue with GitHub"
4. **Authorize**: Vercel to access your GitHub account
5. **Done**: You're now logged into Vercel!

---

## ✅ Step 3: Import Your Project

### 3.1 Start Import

1. In Vercel dashboard, click **"Add New..."** button (top right)
2. Select **"Project"**
3. You'll see "Import Git Repository"

### 3.2 Connect Repository

1. Find your repository: `FarazAliAhmed/todo-list`
2. Click **"Import"** next to it

If you don't see it:
- Click "Adjust GitHub App Permissions"
- Select your repository
- Click "Install"

### 3.3 Configure Project

Vercel will detect Next.js automatically. Configure:

```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build (auto-detected)
Output Directory: .next (auto-detected)
Install Command: npm install (auto-detected)
```

**Important**: Set **Root Directory** to `frontend`!

### 3.4 Add Environment Variables

Click **"Environment Variables"** and add these:

| Name | Value | Notes |
|------|-------|-------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | We'll update this after backend deployment |
| `BETTER_AUTH_SECRET` | Generate with: `openssl rand -base64 32` | Must be 32+ characters |
| `BETTER_AUTH_URL` | Leave empty for now | We'll add this after getting Vercel URL |

**To generate secret:**
```bash
openssl rand -base64 32
```

Copy the output and paste as `BETTER_AUTH_SECRET`.

### 3.5 Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. You'll see "Congratulations!" when done
4. Copy your URL: `https://your-project-name.vercel.app`

---

## ✅ Step 4: Update Environment Variables

Now that you have your Vercel URL, update the environment variable:

1. Go to your project in Vercel dashboard
2. Click **"Settings"** tab
3. Click **"Environment Variables"** in sidebar
4. Find `BETTER_AUTH_URL`
5. Click **"Edit"**
6. Set value to: `https://your-project-name.vercel.app`
7. Click **"Save"**

---

## ✅ Step 5: Redeploy

After updating environment variables:

1. Go to **"Deployments"** tab
2. Find the latest deployment
3. Click the **"..."** menu (three dots)
4. Click **"Redeploy"**
5. Confirm by clicking **"Redeploy"**
6. Wait 1-2 minutes

---

## ✅ Step 6: Test Your Frontend

### 6.1 Visit Your Site

Open: `https://your-project-name.vercel.app`

You should see the Todo app homepage!

### 6.2 Test Navigation

- Click "Sign Up" - should show signup form
- Click "Log In" - should show login form

⚠️ **Note**: Authentication won't work yet because backend isn't deployed. That's normal!

---

## 📝 Save Your URLs

Write these down for later:

```
Frontend URL: https://your-project-name.vercel.app
Backend URL: (will get after Hugging Face deployment)
```

---

## 🎉 Vercel Deployment Complete!

Your frontend is now live on Vercel!

**Next Steps:**
1. Deploy backend to Hugging Face Spaces
2. Update `NEXT_PUBLIC_API_URL` in Vercel with backend URL
3. Update `CORS_ORIGINS` in backend with frontend URL
4. Test end-to-end

---

## 🐛 Troubleshooting

### Build Fails

**Error**: "Cannot find module 'next'"
- **Fix**: Make sure Root Directory is set to `frontend`

**Error**: "Environment variable not found"
- **Fix**: Add all required environment variables in Settings

### Site Loads But Shows Errors

**Error**: "Failed to fetch"
- **Fix**: Backend not deployed yet (normal at this stage)

**Error**: "Invalid token"
- **Fix**: `BETTER_AUTH_SECRET` not set or too short

### Can't See Repository

- **Fix**: Go to https://github.com/apps/vercel
- Click "Configure"
- Select your repository
- Click "Save"

---

## 📊 Vercel Dashboard Overview

After deployment, you can:

- **Deployments**: See all deployments and their status
- **Analytics**: View page views and performance (free tier)
- **Logs**: Check function logs for errors
- **Settings**: Update environment variables, domains, etc.

---

## 🔄 Automatic Deployments

Vercel automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel automatically deploys!
```

You'll get:
- Preview URL for each commit
- Production URL for main branch
- Email notifications

---

## ✅ Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Project imported from GitHub
- [ ] Root directory set to `frontend`
- [ ] Environment variables added
- [ ] First deployment successful
- [ ] `BETTER_AUTH_URL` updated with Vercel URL
- [ ] Redeployed after updating env vars
- [ ] Site accessible at Vercel URL
- [ ] URLs saved for hackathon submission

---

## 📝 For Hackathon Submission

You'll need:

1. ✅ **Frontend URL**: `https://your-project-name.vercel.app`
2. ⏳ **Backend URL**: (after Hugging Face deployment)
3. ⏳ **Demo Video**: (record after both are deployed)

---

**Next**: Deploy backend to Hugging Face Spaces!

See: [HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md)
