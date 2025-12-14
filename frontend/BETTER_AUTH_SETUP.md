# Better Auth Configuration Guide

This document explains the Better Auth setup for the Todo App frontend.

## Overview

Better Auth is configured with:
- ✅ JWT plugin enabled
- ✅ Email/password authentication
- ✅ Shared secret with backend (HS256 algorithm)
- ✅ 7-day token expiration (matching backend)
- ✅ PostgreSQL database integration (Neon)

## Files Created

1. **`lib/auth.ts`** - Server-side Better Auth configuration
2. **`lib/auth-client.ts`** - Client-side React hooks and utilities
3. **`app/api/auth/[...all]/route.ts`** - Next.js API route handler

## Environment Variables

Copy `.env.local.example` to `.env.local` and configure:

```bash
# Database (same as backend)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Auth Secret (MUST match backend JWT_SECRET)
BETTER_AUTH_SECRET=your-secret-key-change-in-production
JWT_SECRET=your-secret-key-change-in-production

# Base URL
BETTER_AUTH_URL=http://localhost:3000

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage in Components

### Sign Up
```typescript
import { signUp } from "@/lib/auth-client";

const handleSignUp = async (email: string, password: string, name: string) => {
  const { data, error } = await signUp.email({
    email,
    password,
    name,
  });

  if (error) {
    console.error("Sign up failed:", error);
    return;
  }

  console.log("User created:", data);
};
```

### Sign In
```typescript
import { signIn } from "@/lib/auth-client";

const handleSignIn = async (email: string, password: string) => {
  const { data, error } = await signIn.email({
    email,
    password,
  });

  if (error) {
    console.error("Sign in failed:", error);
    return;
  }

  console.log("Signed in:", data);
};
```

### Get Current Session
```typescript
import { useSession } from "@/lib/auth-client";

function MyComponent() {
  const { data: session, isPending } = useSession();

  if (isPending) return <div>Loading...</div>;
  if (!session) return <div>Not authenticated</div>;

  return <div>Welcome, {session.user.email}!</div>;
}
```

### Sign Out
```typescript
import { signOut } from "@/lib/auth-client";

const handleSignOut = async () => {
  await signOut();
  // Redirect to login page
};
```

## API Endpoints

Better Auth automatically creates these endpoints:

- `POST /api/auth/sign-up/email` - Create new user
- `POST /api/auth/sign-in/email` - Sign in user
- `POST /api/auth/sign-out` - Sign out user
- `GET /api/auth/session` - Get current session
- `POST /api/auth/refresh` - Refresh JWT token

## JWT Token Structure

The JWT token contains:
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

## Security Notes

1. **Shared Secret**: The `BETTER_AUTH_SECRET` MUST match the backend's `JWT_SECRET`
2. **Algorithm**: Both frontend and backend use HS256
3. **Expiration**: Tokens expire after 7 days
4. **HTTPS**: Use HTTPS in production
5. **Secret Strength**: Use a strong, random secret (minimum 32 characters)

## Database Schema

Better Auth will create a `users` table in your Neon database:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing the Setup

1. Start the development server:
   ```bash
   npm run dev
   ```

2. The Better Auth API should be available at:
   - http://localhost:3000/api/auth/*

3. Test with curl:
   ```bash
   # Sign up
   curl -X POST http://localhost:3000/api/auth/sign-up/email \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

   # Sign in
   curl -X POST http://localhost:3000/api/auth/sign-in/email \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
   ```

## Next Steps

- Task 9: Create authentication pages (login/signup)
- Task 10: Implement API client with JWT token attachment
- Task 11: Build task management components

## Troubleshooting

### "Database connection failed"
- Verify `DATABASE_URL` is correct
- Ensure Neon database is accessible
- Check database credentials

### "JWT verification failed"
- Ensure `BETTER_AUTH_SECRET` matches backend `JWT_SECRET`
- Verify algorithm is HS256 on both sides
- Check token hasn't expired

### "Module not found: better-auth"
- Run `npm install` to ensure dependencies are installed
- Check `package.json` includes `better-auth@^1.4.5`
