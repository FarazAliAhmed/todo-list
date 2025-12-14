# How to Restart Your Servers

## Quick Commands

### Restart Frontend (After Fix)

```bash
# Stop current frontend (Ctrl+C in terminal)
# Then:
cd frontend
npm run dev
```

### Restart Backend (If Needed)

```bash
# Stop current backend (Ctrl+C in terminal)
# Then:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

## Full Restart (Both Servers)

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
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

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 16.0.7
  - Local:        http://localhost:3000

 ✓ Starting...
 ✓ Ready in 2.3s
```

## What to Look For

### ✅ Good Signs (Frontend)
```
✓ Ready in 2.3s
✓ Compiled /signup in 1.2s
```

### ❌ Bad Signs (Frontend)
```
[Error [BetterAuthError]: Failed to initialize database adapter]
Error: Cannot find module 'kysely'
```

### ✅ Good Signs (Backend)
```
INFO: Application startup complete.
INFO: 127.0.0.1:xxxxx - "GET /api/xxx/tasks HTTP/1.1" 200 OK
```

### ❌ Bad Signs (Backend)
```
sqlalchemy.exc.OperationalError: could not connect to server
Error: Port 8000 is already in use
```

## Testing After Restart

### 1. Check Frontend
```bash
# Open in browser
http://localhost:3000
```

Should see: Landing page with "Sign Up" button

### 2. Check Backend
```bash
# Open in browser or use curl
http://localhost:8000/health
```

Should see: `{"status":"healthy","service":"todo-api","version":"2.0.0"}`

### 3. Test Signup
1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter email and password
4. Click "Sign Up"
5. Should redirect to tasks page

### 4. Test Task Creation
1. On tasks page, enter task title
2. Click "Add Task"
3. Task should appear in list

## Troubleshooting

### Frontend Won't Start

**Error: Port 3000 already in use**
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

**Error: Module not found**
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend Won't Start

**Error: Port 8000 already in use**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

**Error: Database connection failed**
```bash
# Test connection
cd backend
source venv/bin/activate
python test_connection.py
```

### Both Servers Running But Not Working

**Check CORS:**
- Backend CORS_ORIGINS includes http://localhost:3000
- Restart backend after changing CORS

**Check Environment Variables:**
```bash
# Frontend
cat frontend/.env.local

# Backend
cat backend/.env
```

**Check Secrets Match:**
```bash
# Should be the same
grep JWT_SECRET backend/.env
grep JWT_SECRET frontend/.env.local
```

## Clean Restart (Nuclear Option)

If nothing works, try a complete clean restart:

```bash
# 1. Stop all servers (Ctrl+C in all terminals)

# 2. Kill any lingering processes
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# 3. Clean frontend
cd frontend
rm -rf .next node_modules
npm install

# 4. Restart backend
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload

# 5. In new terminal, restart frontend
cd frontend
npm run dev
```

## Quick Status Check

Run this to see what's running:

```bash
# Check if ports are in use
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Check if processes are running
ps aux | grep "next dev"
ps aux | grep "uvicorn"
```

## Environment Variables Quick Check

```bash
# Frontend
echo "Frontend DATABASE_URL:"
grep DATABASE_URL frontend/.env.local

echo "Frontend JWT_SECRET:"
grep JWT_SECRET frontend/.env.local

# Backend
echo "Backend DATABASE_URL:"
grep DATABASE_URL backend/.env

echo "Backend JWT_SECRET:"
grep JWT_SECRET backend/.env
```

## Success Indicators

You're ready when:
- ✅ Backend shows "Application startup complete"
- ✅ Frontend shows "Ready in X.Xs"
- ✅ http://localhost:3000 loads
- ✅ http://localhost:8000/health returns healthy
- ✅ No error messages in either terminal
- ✅ Can sign up and create tasks

---

## Current Status After Fix

**What I Fixed:**
1. ✅ Installed database adapter dependencies
2. ✅ Updated Better Auth configuration
3. ✅ Fixed auth client URL

**What You Need to Do:**
1. Restart frontend: `cd frontend && npm run dev`
2. Test signup at http://localhost:3000
3. Should work now! 🚀

**If It Still Doesn't Work:**
- Check the error message
- See BETTER_AUTH_FIX.md for detailed troubleshooting
- Share the error and I'll help debug
