# Environment Setup Guide - Phase II Full-Stack Web Application

This guide will walk you through setting up all required API keys and environment variables for the Phase II application.

## Prerequisites

Before starting, you'll need:
1. A Neon PostgreSQL database account (free tier available)
2. Node.js and npm installed
3. Python 3.13+ installed

---

## Step 1: Create Neon PostgreSQL Database

### 1.1 Sign Up for Neon
1. Go to https://neon.tech
2. Click "Sign Up" (free tier available)
3. Sign up with GitHub, Google, or email

### 1.2 Create a New Project
1. After logging in, click "Create Project"
2. Choose a project name (e.g., "todo-app")
3. Select a region closest to you
4. Click "Create Project"

### 1.3 Get Your Database Connection String
1. After project creation, you'll see the connection details
2. Copy the **Connection String** - it looks like:
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```
3. **IMPORTANT**: Save this connection string - you'll need it for both backend and frontend

**Example Connection String:**
```
postgresql://myuser:AbCdEf123456@ep-cool-morning-12345.us-east-2.aws.neon.tech/neondb?sslmode=require
```

---

## Step 2: Generate JWT Secret Key

You need a strong, random secret key for JWT token signing. This MUST be the same in both backend and frontend.

### Option 1: Using Python (Recommended)
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Option 2: Using OpenSSL
```bash
openssl rand -base64 32
```

### Option 3: Using Node.js
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**Example Output:**
```
xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
```

**IMPORTANT**:
- Save this secret key
- Use the SAME secret in both backend and frontend
- Never commit this to Git
- Use a different secret for production

---

## Step 3: Configure Backend Environment

### 3.1 Create Backend .env File
```bash
cd backend
cp .env.example .env
```

### 3.2 Edit backend/.env
Open `backend/.env` and update with your values:

```bash
# Database Configuration
# Replace with YOUR Neon PostgreSQL connection string from Step 1.3
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require

# JWT Configuration
# Replace with YOUR generated secret from Step 2
JWT_SECRET=xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS Configuration
# Comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 3.3 Verify Backend Configuration
```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Test database connection
python test_connection.py
```

**Expected Output:**
```
✓ Database connection successful!
✓ Can create tables
✓ Can insert data
✓ Can query data
```

---

## Step 4: Configure Frontend Environment

### 4.1 Update frontend/.env.local
The file already exists, so just edit it:

```bash
cd ../frontend
# Open .env.local in your editor
```

### 4.2 Edit frontend/.env.local
Update with your values:

```bash
# Backend API URL (keep as is for local development)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database Configuration (for Better Auth)
# Use the SAME Neon connection string from Step 1.3
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require

# Better Auth Configuration
# IMPORTANT: Use the SAME JWT secret from Step 2
BETTER_AUTH_SECRET=xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
JWT_SECRET=xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV

# Better Auth Base URL (keep as is for local development)
BETTER_AUTH_URL=http://localhost:3000
```

---

## Step 5: Initialize Database Tables

### 5.1 Run Backend to Create Tables
```bash
# Make sure you're in the backend directory
cd backend
source venv/bin/activate

# Start the backend server (this will create tables automatically)
uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You should see SQL CREATE TABLE statements in the logs.

### 5.2 Verify Tables Were Created
Open a new terminal and check:

```bash
cd backend
source venv/bin/activate
python -c "
from app.database import engine
from sqlmodel import text

with engine.connect() as conn:
    result = conn.execute(text(\"SELECT tablename FROM pg_tables WHERE schemaname='public'\"))
    tables = [row[0] for row in result]
    print('Tables created:', tables)
"
```

**Expected Output:**
```
Tables created: ['users', 'tasks']
```

---

## Step 6: Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## Step 7: Verify Complete Setup

### 7.1 Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Backend should be running on: http://localhost:8000

### 7.2 Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

Frontend should be running on: http://localhost:3000

### 7.3 Test the Application
1. Open browser to http://localhost:3000
2. Click "Sign Up" to create an account
3. Fill in email and password
4. After signup, you should be redirected to the tasks page
5. Try creating a task

---

## Configuration Checklist

Use this checklist to ensure everything is configured:

### Backend Configuration
- [ ] `backend/.env` file created
- [ ] `DATABASE_URL` set to your Neon connection string
- [ ] `JWT_SECRET` set to a strong random key (32+ characters)
- [ ] `JWT_ALGORITHM` set to `HS256`
- [ ] `JWT_EXPIRATION_DAYS` set to `7`
- [ ] `CORS_ORIGINS` includes `http://localhost:3000`
- [ ] Backend starts without errors
- [ ] Database tables created (users, tasks)

### Frontend Configuration
- [ ] `frontend/.env.local` file exists
- [ ] `NEXT_PUBLIC_API_URL` set to `http://localhost:8000`
- [ ] `DATABASE_URL` set to SAME Neon connection string as backend
- [ ] `BETTER_AUTH_SECRET` set to SAME secret as backend `JWT_SECRET`
- [ ] `JWT_SECRET` set to SAME secret as backend `JWT_SECRET`
- [ ] `BETTER_AUTH_URL` set to `http://localhost:3000`
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:3000

### Integration Test
- [ ] Can sign up a new user
- [ ] Can log in with created user
- [ ] Can create a task
- [ ] Can view tasks
- [ ] Can update a task
- [ ] Can delete a task
- [ ] Can toggle task completion

---

## Common Issues and Solutions

### Issue 1: "Connection refused" when starting backend
**Solution**: Make sure your Neon database connection string is correct and your IP is allowed in Neon's settings.

### Issue 2: "Invalid or expired token" errors
**Solution**: Make sure `JWT_SECRET` is EXACTLY the same in both `backend/.env` and `frontend/.env.local`.

### Issue 3: "CORS error" in browser console
**Solution**: Make sure `CORS_ORIGINS` in `backend/.env` includes `http://localhost:3000`.

### Issue 4: Frontend can't connect to backend
**Solution**:
1. Make sure backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local` is `http://localhost:8000`

### Issue 5: Database tables not created
**Solution**:
1. Check your `DATABASE_URL` is correct
2. Restart the backend server
3. Check backend logs for SQL errors

---

## Security Notes

### For Development
- The example secrets provided are for development only
- It's okay to use simple secrets locally

### For Production
- **NEVER** commit `.env` files to Git
- Use strong, random secrets (32+ characters)
- Use different secrets for each environment
- Store secrets in environment variables or secret management service
- Enable SSL/TLS for database connections
- Use HTTPS for all API communication

---

## Quick Reference

### Backend Commands
```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Run tests
cd backend && source venv/bin/activate && python -m pytest test_integration.py -v

# Test database connection
cd backend && source venv/bin/activate && python test_connection.py
```

### Frontend Commands
```bash
# Start frontend
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Start production server
cd frontend && npm start
```

---

## Next Steps

Once everything is configured and working:
1. ✅ All environment variables are set
2. ✅ Backend is running on http://localhost:8000
3. ✅ Frontend is running on http://localhost:3000
4. ✅ You can sign up and create tasks

You're ready to move on to **Task 16: Documentation and Deployment Preparation**!

---

## Need Help?

If you encounter issues:
1. Check the logs in both backend and frontend terminals
2. Verify all environment variables are set correctly
3. Make sure both servers are running
4. Check the Common Issues section above
5. Review the integration test report: `backend/INTEGRATION_TEST_REPORT.md`
