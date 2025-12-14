#!/bin/bash

# Complete Deployment Script
# This script pushes to GitHub and deploys to Hugging Face

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Todo App - Complete Deployment Script               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
GITHUB_USERNAME="FarazAliAhmed"
GITHUB_REPO="todo-list"
GITHUB_TOKEN=""  # Will prompt for this

HF_USERNAME="faraz7530"
HF_SPACE_NAME="todo-backend"
HF_TOKEN="YOUR_HF_TOKEN_HERE"  # Replace with your HF token

# Prompt for GitHub token if not set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}Enter your GitHub Personal Access Token:${NC}"
    echo -e "${YELLOW}(Get it from: https://github.com/settings/tokens)${NC}"
    read -s GITHUB_TOKEN
    echo ""
fi

# ============================================
# PART 1: Push to GitHub
# ============================================

echo -e "${GREEN}━━━ Part 1: Pushing to GitHub ━━━${NC}"
echo ""

echo -e "${YELLOW}Checking git status...${NC}"
git status --short

echo ""
echo -e "${YELLOW}Adding all files...${NC}"
git add .

echo ""
echo -e "${YELLOW}Committing changes...${NC}"
git commit -m "Phase II complete - ready for deployment" || echo "No changes to commit"

echo ""
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push "https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git" main

echo -e "${GREEN}✓ Pushed to GitHub${NC}"
echo ""

# ============================================
# PART 2: Deploy to Hugging Face
# ============================================

echo -e "${GREEN}━━━ Part 2: Deploying to Hugging Face ━━━${NC}"
echo ""

TMP_DIR="/tmp/${HF_SPACE_NAME}"
PROJECT_BACKEND_DIR="$(pwd)/backend"

# Clean up
echo -e "${YELLOW}Cleaning up old deployment...${NC}"
rm -rf "${TMP_DIR}"
echo -e "${GREEN}✓ Cleaned up${NC}"
echo ""

# Clone HF Space
echo -e "${YELLOW}Cloning Hugging Face Space...${NC}"
git clone "https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE_NAME}" "${TMP_DIR}"
echo -e "${GREEN}✓ Space cloned${NC}"
echo ""

# Copy files
echo -e "${YELLOW}Copying backend files...${NC}"
cd "${TMP_DIR}"
cp -r "${PROJECT_BACKEND_DIR}"/* .
echo -e "${GREEN}✓ Files copied${NC}"
echo ""

# Create Dockerfile
echo -e "${YELLOW}Creating Dockerfile...${NC}"
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
EOF
echo -e "${GREEN}✓ Dockerfile created${NC}"
echo ""

# Create README
echo -e "${YELLOW}Creating README.md...${NC}"
cat > README.md << 'EOF'
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

FastAPI backend for the Evolution of Todo application (Phase II).

## API Endpoints

- `GET /health` - Health check
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Documentation

Visit `/docs` for interactive API documentation.

## Environment Variables

Set these in Space Settings → Repository secrets:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT (must match frontend)
- `CORS_ORIGINS` - Allowed origins (your Vercel frontend URL)
EOF
echo -e "${GREEN}✓ README.md created${NC}"
echo ""

# Clean up sensitive files
echo -e "${YELLOW}Removing sensitive files...${NC}"
rm -f .env .env.local
rm -rf __pycache__ .pytest_cache venv
rm -f test_*.py
echo -e "${GREEN}✓ Sensitive files removed${NC}"
echo ""

# Commit and push
echo -e "${YELLOW}Committing and pushing to Hugging Face...${NC}"
git add .
git commit -m "Deploy Todo API backend - Phase II complete" || echo "No changes to commit"
git push
echo -e "${GREEN}✓ Pushed to Hugging Face${NC}"
echo ""

# ============================================
# DEPLOYMENT COMPLETE
# ============================================

echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   🎉 Deployment Complete!                              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}📦 GitHub Repository:${NC}"
echo "  https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}"
echo ""

echo -e "${BLUE}🤗 Hugging Face Space:${NC}"
echo "  https://huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE_NAME}"
echo ""

echo -e "${BLUE}🚀 Your Backend API (once built):${NC}"
echo "  https://${HF_USERNAME}-${HF_SPACE_NAME}.hf.space"
echo ""

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Add secrets to Hugging Face Space:"
echo "   → Go to: https://huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE_NAME}/settings"
echo "   → Click 'Repository secrets'"
echo "   → Add:"
echo "      • DATABASE_URL (from backend/.env)"
echo "      • JWT_SECRET (same as Vercel BETTER_AUTH_SECRET)"
echo "      • CORS_ORIGINS (your Vercel URL)"
echo ""
echo "2. Wait 3-5 minutes for Hugging Face build"
echo ""
echo "3. Test backend:"
echo "   curl https://${HF_USERNAME}-${HF_SPACE_NAME}.hf.space/health"
echo ""
echo "4. Deploy frontend to Vercel:"
echo "   → Go to: https://vercel.com"
echo "   → Import GitHub repo"
echo "   → Set root directory to 'frontend'"
echo "   → Add environment variables"
echo ""
echo "5. Update Vercel with backend URL:"
echo "   NEXT_PUBLIC_API_URL=https://${HF_USERNAME}-${HF_SPACE_NAME}.hf.space"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
