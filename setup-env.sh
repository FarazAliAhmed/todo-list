#!/bin/bash

# Environment Setup Script for Phase II Full-Stack Web Application
# This script helps you set up your environment variables

set -e

echo "================================================"
echo "Phase II Todo App - Environment Setup"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to generate a secure random secret
generate_secret() {
    python3 -c "import secrets; print(secrets.token_urlsafe(32))"
}

echo "This script will help you set up your environment variables."
echo ""

# Check if backend/.env already exists
if [ -f "backend/.env" ]; then
    echo -e "${YELLOW}Warning: backend/.env already exists!${NC}"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping backend/.env creation"
        SKIP_BACKEND=true
    fi
fi

# Check if frontend/.env.local needs updating
if [ -f "frontend/.env.local" ]; then
    echo -e "${YELLOW}Note: frontend/.env.local already exists${NC}"
    echo "We'll update it with your new values"
fi

echo ""
echo "================================================"
echo "Step 1: Database Configuration"
echo "================================================"
echo ""
echo "You need a Neon PostgreSQL database connection string."
echo "If you don't have one yet:"
echo "  1. Go to https://neon.tech"
echo "  2. Sign up (free tier available)"
echo "  3. Create a new project"
echo "  4. Copy the connection string"
echo ""
echo "Example: postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"
echo ""

read -p "Enter your Neon DATABASE_URL: " DATABASE_URL

if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}Error: DATABASE_URL cannot be empty${NC}"
    exit 1
fi

echo ""
echo "================================================"
echo "Step 2: JWT Secret Key"
echo "================================================"
echo ""
echo "Generating a secure JWT secret key..."
JWT_SECRET=$(generate_secret)
echo -e "${GREEN}Generated JWT Secret: $JWT_SECRET${NC}"
echo ""
echo "This secret will be used for both backend and frontend."
echo ""

# Create backend/.env
if [ "$SKIP_BACKEND" != true ]; then
    echo "Creating backend/.env..."
    cat > backend/.env << EOF
# Database Configuration
DATABASE_URL=$DATABASE_URL

# JWT Configuration
JWT_SECRET=$JWT_SECRET
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
EOF
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${YELLOW}Skipped backend/.env creation${NC}"
fi

# Update frontend/.env.local
echo "Updating frontend/.env.local..."
cat > frontend/.env.local << EOF
# Frontend Environment Variables

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database Configuration (for Better Auth)
DATABASE_URL=$DATABASE_URL

# Better Auth Configuration
# IMPORTANT: This secret MUST match JWT_SECRET in backend/.env
BETTER_AUTH_SECRET=$JWT_SECRET
JWT_SECRET=$JWT_SECRET

# Better Auth Base URL
BETTER_AUTH_URL=http://localhost:3000
EOF
echo -e "${GREEN}✓ Updated frontend/.env.local${NC}"

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo -e "${GREEN}✓ Environment variables configured${NC}"
echo ""
echo "Your configuration:"
echo "  - Database: Neon PostgreSQL"
echo "  - JWT Secret: $JWT_SECRET"
echo "  - Backend URL: http://localhost:8000"
echo "  - Frontend URL: http://localhost:3000"
echo ""
echo "Next steps:"
echo ""
echo "1. Test backend database connection:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python test_connection.py"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser to http://localhost:3000"
echo ""
echo -e "${YELLOW}IMPORTANT SECURITY NOTES:${NC}"
echo "  - Never commit .env files to Git"
echo "  - Use different secrets for production"
echo "  - Keep your secrets secure"
echo ""
echo "For detailed setup instructions, see: ENVIRONMENT_SETUP_GUIDE.md"
echo ""
