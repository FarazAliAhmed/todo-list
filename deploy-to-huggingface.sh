#!/bin/bash

# Hugging Face Deployment Script for Todo Backend
# This script deploys your FastAPI backend to Hugging Face Spaces

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤗 Hugging Face Spaces Deployment Script${NC}"
echo ""

# Configuration
HF_USERNAME="faraz7530"  # Your Hugging Face username
HF_SPACE_NAME="todo-backend"  # Your space name
HF_TOKEN="${HF_TOKEN:-}"  # Set this as environment variable
TMP_DIR="/tmp/${HF_SPACE_NAME}"
PROJECT_BACKEND_DIR="$HOME/Project/Panaversity-todo/backend"

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
  echo -e "${RED}Error: HF_TOKEN environment variable is not set${NC}"
  echo "Usage: HF_TOKEN=your_token ./deploy-to-huggingface.sh"
  exit 1
fi

echo -e "${YELLOW}Configuration:${NC}"
echo "  Username: ${HF_USERNAME}"
echo "  Space: ${HF_SPACE_NAME}"
echo "  Backend: ${PROJECT_BACKEND_DIR}"
echo ""

# Step 1: Clean up old deployment
echo -e "${YELLOW}Step 1: Cleaning up old deployment...${NC}"
rm -rf "${TMP_DIR}"
echo -e "${GREEN}✓ Cleaned up${NC}"
echo ""

# Step 2: Clone the Hugging Face Space
echo -e "${YELLOW}Step 2: Cloning Hugging Face Space...${NC}"
git clone "https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE_NAME}" "${TMP_DIR}"
echo -e "${GREEN}✓ Space cloned${NC}"
echo ""

# Step 3: Copy backend files
echo -e "${YELLOW}Step 3: Copying backend files...${NC}"
cd "${TMP_DIR}"

# Copy all backend files
cp -r "${PROJECT_BACKEND_DIR}"/* .

echo -e "${GREEN}✓ Files copied${NC}"
echo ""

# Step 4: Create Dockerfile for Hugging Face (port 7860)
echo -e "${YELLOW}Step 4: Creating Dockerfile...${NC}"
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Hugging Face Spaces uses port 7860
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
EOF
echo -e "${GREEN}✓ Dockerfile created${NC}"
echo ""

# Step 5: Create README.md with Hugging Face frontmatter
echo -e "${YELLOW}Step 5: Creating README.md...${NC}"
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

## Features

- RESTful API for task management
- JWT authentication with Better Auth
- PostgreSQL database with Neon
- User data isolation
- Comprehensive error handling

## API Endpoints

- `GET /health` - Health check
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Documentation

Visit `/docs` for interactive Swagger UI documentation.

## Environment Variables

Set these in Space Settings → Repository secrets:

- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT (must match frontend)
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `JWT_EXPIRATION_DAYS` - Token expiration (default: 7)
- `CORS_ORIGINS` - Allowed origins (your Vercel frontend URL)

## Tech Stack

- FastAPI
- SQLModel
- Neon PostgreSQL
- Python 3.11+
EOF
echo -e "${GREEN}✓ README.md created${NC}"
echo ""

# Step 6: Remove sensitive files
echo -e "${YELLOW}Step 6: Removing sensitive files...${NC}"
rm -f .env .env.local
rm -rf __pycache__ .pytest_cache venv
rm -f test_*.py
echo -e "${GREEN}✓ Sensitive files removed${NC}"
echo ""

# Step 7: Create .gitignore
echo -e "${YELLOW}Step 7: Creating .gitignore...${NC}"
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.env
.env.local
.pytest_cache/
*.log
EOF
echo -e "${GREEN}✓ .gitignore created${NC}"
echo ""

# Step 8: Git add and commit
echo -e "${YELLOW}Step 8: Committing changes...${NC}"
git add .
git commit -m "Deploy Todo API backend - Phase II complete" || echo "No changes to commit"
echo -e "${GREEN}✓ Changes committed${NC}"
echo ""

# Step 9: Push to Hugging Face
echo -e "${YELLOW}Step 9: Pushing to Hugging Face...${NC}"
git push
echo -e "${GREEN}✓ Pushed to Hugging Face${NC}"
echo ""

# Step 10: Display success message
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Your backend is deploying at:${NC}"
echo -e "  https://huggingface.co/spaces/${HF_USERNAME}/${HF_SPACE_NAME}"
echo ""
echo -e "${YELLOW}Once deployed, your API will be at:${NC}"
echo -e "  https://${HF_USERNAME}-${HF_SPACE_NAME}.hf.space"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Go to Space Settings → Repository secrets"
echo "  2. Add these secrets:"
echo "     - DATABASE_URL (your Neon connection string)"
echo "     - JWT_SECRET (must match frontend BETTER_AUTH_SECRET)"
echo "     - CORS_ORIGINS (your Vercel frontend URL)"
echo "  3. Wait 3-5 minutes for build to complete"
echo "  4. Test: curl https://${HF_USERNAME}-${HF_SPACE_NAME}.hf.space/health"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
