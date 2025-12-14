# Authentication Setup Explained

## Your Current Setup ✅

### Secrets (BETTER_AUTH_SECRET & JWT_SECRET)

**What they are:**
- Random strings used to sign and verify JWT tokens
- Must be the same in both backend and frontend
- Should be 32+ characters for security

**Your current values:**
```
EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
```

✅ **This is GOOD!** It's:
- 43 characters (more than 32 minimum)
- Randomly generated
- Same in both files

**Where they're used:**

**Backend (`backend/.env`):**
```bash
JWT_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
```
- Used to **verify** JWT tokens sent from frontend
- Ensures tokens weren't tampered with

**Frontend (`frontend/.env.local`):**
```bash
BETTER_AUTH_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
JWT_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
```
- Used by Better Auth to **create** JWT tokens
- Both variables point to the same value (Better Auth uses BETTER_AUTH_SECRET)

---

## How Authentication Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                        │
│                   http://localhost:3000                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Better Auth (handles signup/login)                    │ │
│  │  Routes: /api/auth/*                                   │ │
│  │  - Creates users in database                           │ │
│  │  - Issues JWT tokens                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           │ JWT Token                        │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Client (lib/api.ts)                               │ │
│  │  - Attaches JWT to requests                            │ │
│  │  - Calls backend API                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ HTTP + JWT Token
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│                   http://localhost:8000                      │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  JWT Middleware (app/middleware/auth.py)               │ │
│  │  - Verifies JWT token                                  │ │
│  │  - Extracts user_id                                    │ │
│  │  - Validates ownership                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Task API Routes (app/routes/tasks.py)                │ │
│  │  - CRUD operations for tasks                           │ │
│  │  - User data isolation                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Neon Database  │
                  │   PostgreSQL    │
                  └─────────────────┘
```

### Step-by-Step Flow

**1. User Signs Up**
```
User → Frontend → Better Auth (/api/auth/sign-up/email)
                     ↓
                  Creates user in database
                     ↓
                  Issues JWT token
                     ↓
                  Returns token to frontend
```

**2. User Makes API Request (e.g., create task)**
```
User → Frontend → API Client (adds JWT to header)
                     ↓
                  Backend (/api/{user_id}/tasks)
                     ↓
                  JWT Middleware (verifies token)
                     ↓
                  Task Route (creates task)
                     ↓
                  Database (saves task)
```

---

## The 404 Error You Saw

### What Happened

```
INFO: 127.0.0.1:57063 - "POST /api/auth/sign-up/email HTTP/1.1" 404 Not Found
```

**Problem:** Frontend was trying to call Better Auth at the **backend URL** (`http://localhost:8000/api/auth/sign-up/email`) instead of the **frontend URL** (`http://localhost:3000/api/auth/sign-up/email`).

**Why:** The `auth-client.ts` was configured with `NEXT_PUBLIC_API_URL` (backend) instead of `BETTER_AUTH_URL` (frontend).

### The Fix

**Before (WRONG):**
```typescript
// frontend/lib/auth-client.ts
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL, // ❌ Points to backend (8000)
});
```

**After (CORRECT):**
```typescript
// frontend/lib/auth-client.ts
export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL, // ✅ Points to frontend (3000)
});
```

---

## Environment Variables Explained

### Frontend (.env.local)

```bash
# Backend API URL - for task operations
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database - Better Auth connects directly to create users
DATABASE_URL=postgresql://...neon.tech/neondb?sslmode=require

# Secrets - for JWT signing (must match backend)
BETTER_AUTH_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
JWT_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE

# Better Auth URL - where Better Auth runs (frontend)
BETTER_AUTH_URL=http://localhost:3000
```

**Usage:**
- `NEXT_PUBLIC_API_URL` → Used by `lib/api.ts` for task CRUD operations
- `DATABASE_URL` → Used by Better Auth to create/verify users
- `BETTER_AUTH_SECRET` → Used by Better Auth to sign JWT tokens
- `JWT_SECRET` → Backup/alternative name for the secret
- `BETTER_AUTH_URL` → Used by `auth-client.ts` for signup/login

### Backend (.env)

```bash
# Database - for task operations
DATABASE_URL=postgresql://...neon.tech/neondb?sslmode=require

# JWT Secret - for verifying tokens (must match frontend)
JWT_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS - allow frontend to call backend
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Usage:**
- `DATABASE_URL` → Used by SQLModel to query/update tasks
- `JWT_SECRET` → Used by middleware to verify JWT tokens
- `CORS_ORIGINS` → Allows frontend (port 3000) to call backend (port 8000)

---

## Two Separate Services

### Frontend (Port 3000)
**Handles:**
- ✅ User signup/login (Better Auth)
- ✅ UI rendering
- ✅ Calling backend API

**Routes:**
- `/` - Landing page
- `/login` - Login page
- `/signup` - Signup page
- `/tasks` - Tasks page
- `/api/auth/*` - Better Auth endpoints (signup, login, etc.)

### Backend (Port 8000)
**Handles:**
- ✅ Task CRUD operations
- ✅ JWT verification
- ✅ User data isolation

**Routes:**
- `/api/{user_id}/tasks` - List/create tasks
- `/api/{user_id}/tasks/{id}` - Get/update/delete task
- `/api/{user_id}/tasks/{id}/complete` - Toggle completion

---

## Testing Your Setup

### 1. Restart Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 2. Test Signup

1. Open http://localhost:3000
2. Click "Sign Up"
3. Enter email: `test@example.com`
4. Enter password: `password123`
5. Click "Sign Up"

**Expected behavior:**
- ✅ User created in database
- ✅ JWT token issued
- ✅ Redirected to `/tasks` page
- ✅ No 404 errors

### 3. Test Task Creation

1. On tasks page, enter task title
2. Click "Add Task"

**Expected behavior:**
- ✅ Task appears in list
- ✅ Backend logs show: `POST /api/{user_id}/tasks 201`
- ✅ No authentication errors

---

## Summary

### Your Secrets Are Fine! ✅

```
BETTER_AUTH_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
JWT_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
```

- ✅ 43 characters (secure)
- ✅ Randomly generated
- ✅ Same in both files
- ✅ No need to change them

### The Fix Applied ✅

Changed `frontend/lib/auth-client.ts` to use `BETTER_AUTH_URL` instead of `NEXT_PUBLIC_API_URL`.

### What Each Secret Does

**BETTER_AUTH_SECRET:**
- Used by Better Auth (frontend) to **create** JWT tokens
- Signs tokens when users log in

**JWT_SECRET:**
- Used by backend to **verify** JWT tokens
- Ensures tokens are valid and not tampered with
- Must match BETTER_AUTH_SECRET

### Next Steps

1. ✅ Restart both servers
2. ✅ Try signing up again
3. ✅ Should work now - no more 404 errors!

---

## Still Getting Errors?

Check:
- [ ] Both servers are running
- [ ] Frontend on port 3000
- [ ] Backend on port 8000
- [ ] No typos in environment variables
- [ ] Secrets match exactly in both files
- [ ] Database URL is correct

If you still see 404 errors, share the full error message and I'll help debug!
