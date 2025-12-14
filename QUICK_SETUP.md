# Quick Setup Guide - Get Started in 5 Minutes

## Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
./setup-env.sh
```

The script will:
1. Ask for your Neon database connection string
2. Generate a secure JWT secret
3. Create/update both `.env` files automatically

## Option 2: Manual Setup

### Step 1: Get Neon Database URL
1. Go to https://neon.tech and sign up (free)
2. Create a new project
3. Copy the connection string (looks like):
   ```
   postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

### Step 2: Generate JWT Secret
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Create Backend .env
```bash
cd backend
cp .env.example .env
# Edit .env and add your DATABASE_URL and JWT_SECRET
```

### Step 4: Update Frontend .env.local
```bash
cd frontend
# Edit .env.local and add:
# - Same DATABASE_URL
# - Same JWT_SECRET (in both BETTER_AUTH_SECRET and JWT_SECRET)
```

## What You Need

### 1. Neon Database Connection String
```
postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```
**Where to get it**: https://neon.tech (free tier available)

### 2. JWT Secret Key (32+ characters)
```
xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
```
**How to generate**: Run `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

**IMPORTANT**: Use the SAME secret in both backend and frontend!

## Configuration Files

### backend/.env
```bash
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
JWT_SECRET=xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### frontend/.env.local
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
JWT_SECRET=xK9mP2vN8qR5tY7wZ3aB6cD1eF4gH0jL9mN2pQ5sT8uV
BETTER_AUTH_URL=http://localhost:3000
```

## Start the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```
Backend runs on: http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:3000

## Verify Setup

1. Open http://localhost:3000
2. Click "Sign Up"
3. Create an account
4. Create a task
5. ✅ If this works, you're all set!

## Troubleshooting

### Backend won't start
- Check `DATABASE_URL` is correct
- Verify Neon database is accessible
- Run `python test_connection.py` in backend directory

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL=http://localhost:8000` in frontend/.env.local

### "Invalid token" errors
- Make sure `JWT_SECRET` is EXACTLY the same in both files
- No extra spaces or line breaks

### CORS errors
- Check `CORS_ORIGINS` includes `http://localhost:3000`

## Need More Help?

See the detailed guide: `ENVIRONMENT_SETUP_GUIDE.md`
