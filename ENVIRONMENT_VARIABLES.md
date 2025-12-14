# Environment Variables Reference

Complete reference for all environment variables used in the Evolution of Todo application.

## Table of Contents

1. [Frontend Environment Variables](#frontend-environment-variables)
2. [Backend Environment Variables](#backend-environment-variables)
3. [Security Best Practices](#security-best-practices)
4. [Environment-Specific Configurations](#environment-specific-configurations)
5. [Troubleshooting](#troubleshooting)

## Frontend Environment Variables

Frontend environment variables are stored in `frontend/.env.local` for local development and configured in your deployment platform (e.g., Vercel) for production.

### Required Variables

#### `NEXT_PUBLIC_API_URL`

- **Description**: Base URL of the backend API
- **Type**: String (URL)
- **Required**: Yes
- **Example (Development)**: `http://localhost:8000`
- **Example (Production)**: `https://api.yourdomain.com`
- **Notes**: 
  - Must include protocol (`http://` or `https://`)
  - No trailing slash
  - Accessible from browser (prefixed with `NEXT_PUBLIC_`)

#### `BETTER_AUTH_SECRET`

- **Description**: Secret key for JWT token signing and verification
- **Type**: String (minimum 32 characters)
- **Required**: Yes
- **Example**: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`
- **Generation**: `openssl rand -base64 32`
- **Notes**:
  - Must be at least 32 characters long
  - Must match `JWT_SECRET` in backend
  - Keep secret and never commit to version control
  - Use different secrets for development and production

#### `BETTER_AUTH_URL`

- **Description**: Base URL of the frontend application
- **Type**: String (URL)
- **Required**: Yes
- **Example (Development)**: `http://localhost:3000`
- **Example (Production)**: `https://yourdomain.com`
- **Notes**:
  - Must include protocol (`http://` or `https://`)
  - No trailing slash
  - Used for authentication callbacks

### Optional Variables

#### `DATABASE_URL`

- **Description**: PostgreSQL connection string for Better Auth (if using database sessions)
- **Type**: String (PostgreSQL connection URL)
- **Required**: No (only if using database sessions)
- **Example**: `postgresql://user:pass@host:5432/dbname`
- **Notes**: Only needed if Better Auth is configured to use database sessions

### Example `.env.local` File

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long-here
BETTER_AUTH_URL=http://localhost:3000
```

---

## Backend Environment Variables

Backend environment variables are stored in `backend/.env` for local development and configured in your deployment platform for production.

### Required Variables

#### `DATABASE_URL`

- **Description**: PostgreSQL database connection string
- **Type**: String (PostgreSQL connection URL)
- **Required**: Yes
- **Format**: `postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require`
- **Example (Neon)**: `postgresql://user:pass@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require`
- **Example (Local)**: `postgresql://todouser:todopass@localhost:5432/tododb`
- **Notes**:
  - Include `?sslmode=require` for production databases
  - Keep credentials secure
  - Use environment-specific databases

#### `JWT_SECRET`

- **Description**: Secret key for JWT token verification
- **Type**: String (minimum 32 characters)
- **Required**: Yes
- **Example**: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`
- **Generation**: `openssl rand -base64 32`
- **Notes**:
  - Must be at least 32 characters long
  - Must match `BETTER_AUTH_SECRET` in frontend
  - Keep secret and never commit to version control
  - Use different secrets for development and production

#### `CORS_ORIGINS`

- **Description**: Comma-separated list of allowed origins for CORS
- **Type**: String (comma-separated URLs)
- **Required**: Yes
- **Example (Development)**: `http://localhost:3000`
- **Example (Production)**: `https://yourdomain.com,https://www.yourdomain.com`
- **Notes**:
  - Include all frontend URLs that will access the API
  - No trailing slashes
  - Separate multiple origins with commas (no spaces)

### Optional Variables

#### `JWT_ALGORITHM`

- **Description**: Algorithm used for JWT signing
- **Type**: String
- **Required**: No
- **Default**: `HS256`
- **Allowed Values**: `HS256`, `HS384`, `HS512`
- **Notes**: Only change if you have specific security requirements

#### `JWT_EXPIRATION_DAYS`

- **Description**: Number of days until JWT tokens expire
- **Type**: Integer
- **Required**: No
- **Default**: `7`
- **Example**: `7` (one week), `30` (one month)
- **Notes**: Balance security (shorter) vs. user convenience (longer)

#### `ENVIRONMENT`

- **Description**: Environment name for logging and debugging
- **Type**: String
- **Required**: No
- **Default**: `development`
- **Allowed Values**: `development`, `staging`, `production`
- **Notes**: Used for conditional behavior and logging

#### `LOG_LEVEL`

- **Description**: Logging verbosity level
- **Type**: String
- **Required**: No
- **Default**: `INFO`
- **Allowed Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Notes**: Use `DEBUG` for development, `INFO` or `WARNING` for production

### Example `.env` File

```env
# Database Configuration
DATABASE_URL=postgresql://todouser:todopass@localhost:5432/tododb

# JWT Configuration
JWT_SECRET=your-secret-key-must-match-frontend-better-auth-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Optional Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## Security Best Practices

### 1. Generate Strong Secrets

Use cryptographically secure random strings for all secrets:

```bash
# Generate a 32-character base64 secret
openssl rand -base64 32

# Generate a 64-character hex secret
openssl rand -hex 32
```

### 2. Never Commit Secrets

- Add `.env` and `.env.local` to `.gitignore`
- Use `.env.example` files with placeholder values
- Store production secrets in deployment platform

### 3. Match JWT Secrets

The `JWT_SECRET` (backend) must exactly match `BETTER_AUTH_SECRET` (frontend):

```bash
# Generate once and use in both places
SECRET=$(openssl rand -base64 32)
echo "Frontend: BETTER_AUTH_SECRET=$SECRET"
echo "Backend: JWT_SECRET=$SECRET"
```

### 4. Use Environment-Specific Values

| Environment | Secret Strength | Database | CORS |
|-------------|----------------|----------|------|
| Development | Medium (for convenience) | Local or dev instance | `localhost:3000` |
| Staging | Strong | Staging instance | Staging URL |
| Production | Very Strong | Production instance | Production URL(s) only |

### 5. Rotate Secrets Regularly

- Rotate secrets at least annually
- Rotate immediately if compromised
- Update both frontend and backend simultaneously

### 6. Use HTTPS in Production

- Always use `https://` URLs in production
- Enable `sslmode=require` for database connections
- Configure SSL/TLS certificates properly

---

## Environment-Specific Configurations

### Development

```env
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=dev-secret-key-minimum-32-characters
BETTER_AUTH_URL=http://localhost:3000

# Backend (.env)
DATABASE_URL=postgresql://todouser:todopass@localhost:5432/tododb
JWT_SECRET=dev-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Staging

```env
# Frontend (Vercel/Platform)
NEXT_PUBLIC_API_URL=https://api-staging.yourdomain.com
BETTER_AUTH_SECRET=staging-secret-key-very-strong-32-plus-chars
BETTER_AUTH_URL=https://staging.yourdomain.com

# Backend (Railway/Platform)
DATABASE_URL=postgresql://user:pass@staging-host.neon.tech/stagingdb?sslmode=require
JWT_SECRET=staging-secret-key-very-strong-32-plus-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://staging.yourdomain.com
ENVIRONMENT=staging
LOG_LEVEL=INFO
```

### Production

```env
# Frontend (Vercel/Platform)
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
BETTER_AUTH_SECRET=production-secret-key-extremely-strong-32-plus-chars
BETTER_AUTH_URL=https://yourdomain.com

# Backend (Railway/Platform)
DATABASE_URL=postgresql://user:pass@prod-host.neon.tech/proddb?sslmode=require
JWT_SECRET=production-secret-key-extremely-strong-32-plus-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
LOG_LEVEL=WARNING
```

---

## Troubleshooting

### "Invalid or expired token" errors

**Cause**: JWT secrets don't match between frontend and backend

**Solution**:
1. Verify `BETTER_AUTH_SECRET` (frontend) equals `JWT_SECRET` (backend)
2. Check for extra spaces or newlines in secret values
3. Regenerate secrets if needed and update both services

### "CORS policy" errors

**Cause**: Frontend URL not in `CORS_ORIGINS`

**Solution**:
1. Add frontend URL to `CORS_ORIGINS` in backend
2. Ensure no trailing slashes
3. Include protocol (`http://` or `https://`)
4. Restart backend after changes

### Database connection errors

**Cause**: Invalid `DATABASE_URL` or network issues

**Solution**:
1. Verify connection string format
2. Check database is running and accessible
3. Ensure `sslmode=require` for production databases
4. Test connection with `psql`:
   ```bash
   psql "your-database-url"
   ```

### "Failed to fetch" errors

**Cause**: Incorrect `NEXT_PUBLIC_API_URL`

**Solution**:
1. Verify backend URL is correct and accessible
2. Check backend is running
3. Ensure protocol matches (`http://` vs `https://`)
4. Test backend health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

### Environment variables not loading

**Cause**: File not in correct location or not named correctly

**Solution**:
1. Frontend: Ensure file is named `.env.local` in `frontend/` directory
2. Backend: Ensure file is named `.env` in `backend/` directory
3. Restart development servers after changes
4. Check file is not in `.gitignore` accidentally

### Production deployment issues

**Cause**: Environment variables not set in deployment platform

**Solution**:
1. Verify all required variables are set in platform dashboard
2. Check for typos in variable names
3. Ensure secrets match between frontend and backend
4. Redeploy after setting variables

---

## Validation Checklist

Use this checklist to verify your environment configuration:

### Frontend
- [ ] `NEXT_PUBLIC_API_URL` is set and correct
- [ ] `BETTER_AUTH_SECRET` is at least 32 characters
- [ ] `BETTER_AUTH_URL` matches your frontend URL
- [ ] All URLs include protocol (`http://` or `https://`)
- [ ] No trailing slashes in URLs

### Backend
- [ ] `DATABASE_URL` is set and valid
- [ ] `JWT_SECRET` matches `BETTER_AUTH_SECRET` from frontend
- [ ] `JWT_SECRET` is at least 32 characters
- [ ] `CORS_ORIGINS` includes frontend URL
- [ ] Database connection works (test with `psql`)

### Security
- [ ] Different secrets for development and production
- [ ] Secrets are not committed to version control
- [ ] HTTPS used in production
- [ ] `sslmode=require` in production database URL
- [ ] CORS restricted to known origins only

### Deployment
- [ ] All variables set in deployment platform
- [ ] Secrets match between frontend and backend
- [ ] Environment-specific values used
- [ ] Services can communicate with each other

---

## Quick Reference

### Generate Secret
```bash
openssl rand -base64 32
```

### Test Backend Connection
```bash
curl http://localhost:8000/health
```

### Test Database Connection
```bash
psql "your-database-url"
```

### View Environment Variables (Development)
```bash
# Frontend
cat frontend/.env.local

# Backend
cat backend/.env
```

### Set Environment Variables (Production)

**Vercel (Frontend)**:
```bash
vercel env add NEXT_PUBLIC_API_URL
vercel env add BETTER_AUTH_SECRET
vercel env add BETTER_AUTH_URL
```

**Railway (Backend)**:
```bash
railway variables set DATABASE_URL="your-url"
railway variables set JWT_SECRET="your-secret"
railway variables set CORS_ORIGINS="your-frontend-url"
```

---

## Additional Resources

- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [FastAPI Settings Management](https://fastapi.tiangolo.com/advanced/settings/)
- [Better Auth Configuration](https://www.better-auth.com/docs/configuration)
- [Neon Database Connection](https://neon.tech/docs/connect/connect-from-any-app)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
