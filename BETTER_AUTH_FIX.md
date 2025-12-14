# Better Auth Database Connection Fix

## The Problem

Error: `Failed to initialize database adapter`

This happened because Better Auth couldn't connect to the PostgreSQL database.

## The Solution

### What I Fixed

1. **Installed Required Dependencies**
   ```bash
   npm install kysely kysely-postgres-js postgres pg @types/pg
   ```

2. **Updated `frontend/lib/auth.ts`**
   - Changed from simple connection string to Kysely + postgres.js
   - Added proper SSL configuration for Neon
   - Configured connection pooling

### Why This Works

Better Auth needs a database adapter to:
- Create user tables
- Store user credentials
- Manage sessions
- Handle authentication

The new configuration uses:
- **postgres.js** - Modern PostgreSQL client
- **Kysely** - Type-safe SQL query builder
- **Proper SSL** - Required for Neon connections

## How to Test

### Step 1: Restart Frontend

```bash
# Stop the frontend (Ctrl+C)
cd frontend
npm run dev
```

### Step 2: Check for Errors

Look for these in the terminal:
- ✅ No "Failed to initialize database adapter" errors
- ✅ Server starts successfully
- ✅ "Ready" message appears

### Step 3: Test Signup

1. Open http://localhost:3000
2. Click "Sign Up"
3. Enter email: `test@example.com`
4. Enter password: `password123`
5. Click "Sign Up"

**Expected Result:**
- ✅ User created successfully
- ✅ Redirected to tasks page
- ✅ No errors in console

### Step 4: Check Database

Better Auth will automatically create these tables:
- `user` - Stores user accounts
- `session` - Stores active sessions
- `account` - Stores OAuth accounts (if used)
- `verification` - Stores email verification tokens

You can verify in your Neon dashboard:
1. Go to https://console.neon.tech
2. Select your project
3. Go to "Tables"
4. You should see the Better Auth tables

## Troubleshooting

### Error: "Connection refused"

**Check:**
- [ ] DATABASE_URL is correct in `frontend/.env.local`
- [ ] Neon database is not paused
- [ ] Internet connection is working

**Fix:**
```bash
# Test connection
cd backend
source venv/bin/activate
python test_connection.py
```

### Error: "SSL required"

**Check:**
- [ ] DATABASE_URL includes `?sslmode=require`
- [ ] Connection string is complete

**Fix:**
Your connection string should look like:
```
postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### Error: "Module not found"

**Check:**
- [ ] All dependencies installed

**Fix:**
```bash
cd frontend
npm install kysely kysely-postgres-js postgres pg @types/pg
```

### Error: "Invalid secret"

**Check:**
- [ ] BETTER_AUTH_SECRET is set in `frontend/.env.local`
- [ ] Secret is at least 32 characters

**Fix:**
```bash
# Generate new secret
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Update frontend/.env.local
BETTER_AUTH_SECRET=<your-new-secret>
JWT_SECRET=<same-secret>
```

## Configuration Files

### frontend/.env.local (Should Have)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database Configuration (for Better Auth)
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Better Auth Configuration
BETTER_AUTH_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE
JWT_SECRET=EHMQOd61AxDipZU8rqb-fn6pVXV5JjUKw2yxmyNEWGE

# Better Auth Base URL
BETTER_AUTH_URL=http://localhost:3000
```

### frontend/lib/auth.ts (Updated)

Now uses:
- ✅ Kysely for database queries
- ✅ postgres.js for connection
- ✅ Proper SSL configuration
- ✅ Connection pooling

## What Happens on First Signup

1. **User submits signup form**
   - Frontend sends request to `/api/auth/sign-up/email`

2. **Better Auth processes request**
   - Checks if tables exist (creates them if not)
   - Hashes password
   - Creates user record
   - Creates session
   - Issues JWT token

3. **User is authenticated**
   - JWT token stored in browser
   - User redirected to tasks page
   - Can now make authenticated API calls

## Database Tables Created

Better Auth will create these tables automatically:

### `user` table
```sql
CREATE TABLE user (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  emailVerified BOOLEAN DEFAULT FALSE,
  name TEXT,
  image TEXT,
  createdAt TIMESTAMP DEFAULT NOW(),
  updatedAt TIMESTAMP DEFAULT NOW()
);
```

### `session` table
```sql
CREATE TABLE session (
  id TEXT PRIMARY KEY,
  userId TEXT NOT NULL,
  expiresAt TIMESTAMP NOT NULL,
  token TEXT UNIQUE NOT NULL,
  ipAddress TEXT,
  userAgent TEXT,
  FOREIGN KEY (userId) REFERENCES user(id)
);
```

### `account` table
```sql
CREATE TABLE account (
  id TEXT PRIMARY KEY,
  userId TEXT NOT NULL,
  accountId TEXT NOT NULL,
  providerId TEXT NOT NULL,
  accessToken TEXT,
  refreshToken TEXT,
  expiresAt TIMESTAMP,
  FOREIGN KEY (userId) REFERENCES user(id)
);
```

## Verification Checklist

After applying the fix:

- [ ] Frontend starts without errors
- [ ] No "Failed to initialize database adapter" error
- [ ] Can access http://localhost:3000
- [ ] Signup page loads
- [ ] Can create a new account
- [ ] Redirected to tasks page after signup
- [ ] Can create tasks
- [ ] Can log out and log back in

## Next Steps

Once signup works:

1. ✅ Test login with existing account
2. ✅ Test creating tasks
3. ✅ Test task CRUD operations
4. ✅ Verify data persists after logout/login
5. ✅ Ready for Task 16!

## Still Having Issues?

If you still see errors:

1. **Share the exact error message**
2. **Check both terminal outputs** (frontend and backend)
3. **Verify environment variables** are set correctly
4. **Test database connection** from backend

Common issues:
- Database URL typo
- Missing environment variables
- Neon database paused (free tier auto-pauses)
- Port conflicts (3000 or 8000 already in use)

---

## Summary

**What was wrong:**
- Better Auth couldn't connect to PostgreSQL database
- Missing database adapter dependencies

**What I fixed:**
- Installed Kysely and postgres.js
- Updated auth configuration
- Added proper SSL settings

**What to do now:**
- Restart frontend
- Try signing up again
- Should work! ✅
