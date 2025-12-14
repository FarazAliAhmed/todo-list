# Setup Checklist ✓

Use this checklist to track your setup progress.

## Prerequisites
- [ ] Python 3.13+ installed
- [ ] Node.js and npm installed
- [ ] Git installed
- [ ] Code editor (VS Code, etc.)

## Step 1: Neon Database Setup
- [ ] Created Neon account at https://neon.tech
- [ ] Created a new project
- [ ] Copied the database connection string
- [ ] Saved connection string somewhere safe

**Your connection string should look like:**
```
postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

## Step 2: Generate JWT Secret
- [ ] Generated JWT secret using one of these methods:
  - [ ] Python: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
  - [ ] OpenSSL: `openssl rand -base64 32`
  - [ ] Node: `node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"`
- [ ] Saved the generated secret

**Your secret should be 32+ characters long**

## Step 3: Backend Configuration
- [ ] Navigated to `backend` directory
- [ ] Created `.env` file (either manually or using script)
- [ ] Added `DATABASE_URL` with your Neon connection string
- [ ] Added `JWT_SECRET` with your generated secret
- [ ] Added `JWT_ALGORITHM=HS256`
- [ ] Added `JWT_EXPIRATION_DAYS=7`
- [ ] Added `CORS_ORIGINS=http://localhost:3000,http://localhost:3001`
- [ ] Saved the file

**Verify backend/.env exists and has all variables**

## Step 4: Frontend Configuration
- [ ] Navigated to `frontend` directory
- [ ] Opened `.env.local` file (already exists)
- [ ] Updated `DATABASE_URL` with SAME Neon connection string
- [ ] Updated `BETTER_AUTH_SECRET` with SAME JWT secret
- [ ] Updated `JWT_SECRET` with SAME JWT secret
- [ ] Verified `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [ ] Verified `BETTER_AUTH_URL=http://localhost:3000`
- [ ] Saved the file

**CRITICAL: JWT secrets must match in both files!**

## Step 5: Backend Setup
- [ ] Opened terminal in `backend` directory
- [ ] Activated virtual environment: `source venv/bin/activate`
- [ ] Installed dependencies (should already be done)
- [ ] Tested database connection: `python test_connection.py`
- [ ] Saw success message: "✓ Database connection successful!"

## Step 6: Frontend Setup
- [ ] Opened terminal in `frontend` directory
- [ ] Installed dependencies: `npm install` (if not done)
- [ ] No errors during installation

## Step 7: Start Backend
- [ ] Opened terminal in `backend` directory
- [ ] Activated virtual environment: `source venv/bin/activate`
- [ ] Started server: `uvicorn app.main:app --reload`
- [ ] Saw "Application startup complete" message
- [ ] Backend running on http://localhost:8000
- [ ] Saw SQL CREATE TABLE statements in logs
- [ ] No error messages

## Step 8: Start Frontend
- [ ] Opened NEW terminal in `frontend` directory
- [ ] Started dev server: `npm run dev`
- [ ] Saw "Ready" message
- [ ] Frontend running on http://localhost:3000
- [ ] No error messages

## Step 9: Test the Application
- [ ] Opened browser to http://localhost:3000
- [ ] Saw the landing page
- [ ] Clicked "Sign Up" or "Get Started"
- [ ] Filled in email and password
- [ ] Successfully created account
- [ ] Redirected to tasks page
- [ ] Created a new task
- [ ] Task appeared in the list
- [ ] Marked task as complete
- [ ] Deleted a task
- [ ] Logged out
- [ ] Logged back in
- [ ] Saw same tasks (data persisted)

## Step 10: Run Integration Tests (Optional)
- [ ] Opened terminal in `backend` directory
- [ ] Activated virtual environment
- [ ] Ran tests: `python -m pytest test_integration.py -v`
- [ ] All 22 tests passed
- [ ] No failures

## Troubleshooting Checklist

If something doesn't work, check:

### Backend Issues
- [ ] `DATABASE_URL` is correct and complete
- [ ] Neon database is accessible (not paused)
- [ ] Virtual environment is activated
- [ ] Port 8000 is not in use by another app
- [ ] No firewall blocking the connection

### Frontend Issues
- [ ] Backend is running on port 8000
- [ ] `NEXT_PUBLIC_API_URL` points to http://localhost:8000
- [ ] Port 3000 is not in use by another app
- [ ] Node modules are installed

### Authentication Issues
- [ ] `JWT_SECRET` is EXACTLY the same in both files
- [ ] No extra spaces or line breaks in secrets
- [ ] `BETTER_AUTH_SECRET` and `JWT_SECRET` match in frontend
- [ ] Secrets are at least 32 characters long

### CORS Issues
- [ ] `CORS_ORIGINS` includes http://localhost:3000
- [ ] No typos in the URL
- [ ] Backend was restarted after changing CORS settings

## Quick Commands Reference

### Backend
```bash
# Navigate and activate
cd backend
source venv/bin/activate

# Test connection
python test_connection.py

# Start server
uvicorn app.main:app --reload

# Run tests
python -m pytest test_integration.py -v
```

### Frontend
```bash
# Navigate
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## Success Criteria

You're ready to move to Task 16 when:
- ✅ Backend starts without errors
- ✅ Frontend starts without errors
- ✅ Can sign up a new user
- ✅ Can log in
- ✅ Can create, view, update, and delete tasks
- ✅ Tasks persist after logout/login
- ✅ Integration tests pass (optional but recommended)

## Files to Check

Make sure these files exist and are configured:
- [ ] `backend/.env` (created by you, not in Git)
- [ ] `frontend/.env.local` (updated by you, not in Git)
- [ ] `backend/.env.example` (template, in Git)
- [ ] `frontend/.env.local.example` (template, in Git)

## Security Reminders

- [ ] Never commit `.env` files to Git
- [ ] `.env` files are in `.gitignore`
- [ ] Using strong secrets (32+ characters)
- [ ] Different secrets for production
- [ ] Secrets stored securely

---

## Status

**Current Status**: [ ] Not Started / [ ] In Progress / [ ] Complete

**Date Completed**: _______________

**Notes**:
_______________________________________________________
_______________________________________________________
_______________________________________________________

---

## Ready for Task 16?

Once all items above are checked, you're ready to proceed to:
**Task 16: Documentation and Deployment Preparation**

Good luck! 🚀
