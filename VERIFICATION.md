# Deployment Verification Guide

This guide helps you verify that your deployment is working correctly.

## Pre-Deployment Verification

### 1. Local Development Check

Before deploying, ensure everything works locally:

```bash
# Start all services
npm run dev

# In a new terminal, run verification tests
cd backend
pytest

# Check frontend builds successfully
cd ../frontend
npm run build
```

**Expected Results**:
- ✅ Frontend accessible at http://localhost:3000
- ✅ Backend accessible at http://localhost:8000
- ✅ All tests passing
- ✅ Frontend builds without errors

### 2. Environment Variables Check

Verify all required environment variables are set:

**Frontend** (`frontend/.env.local`):
```bash
# Check variables exist
grep -E "NEXT_PUBLIC_API_URL|BETTER_AUTH_SECRET|BETTER_AUTH_URL" frontend/.env.local
```

**Backend** (`backend/.env`):
```bash
# Check variables exist
grep -E "DATABASE_URL|JWT_SECRET|CORS_ORIGINS" backend/.env
```

**Expected Results**:
- ✅ All required variables present
- ✅ No placeholder values (like "your-secret-here")
- ✅ JWT secrets match between frontend and backend

### 3. Database Connection Check

Test database connectivity:

```bash
cd backend
python -c "
from app.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('✅ Database connection successful')
"
```

**Expected Results**:
- ✅ Database connection successful
- ✅ No connection errors

### 4. API Health Check

Test backend API:

```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "todo-api",
  "version": "2.0.0"
}
```

## Post-Deployment Verification

### 1. Frontend Deployment Check

After deploying to Vercel:

```bash
# Check frontend is accessible
curl -I https://your-frontend-url.vercel.app

# Check health
curl https://your-frontend-url.vercel.app
```

**Expected Results**:
- ✅ HTTP 200 status code
- ✅ Page loads successfully
- ✅ No console errors in browser

### 2. Backend Deployment Check

After deploying backend:

```bash
# Check backend health endpoint
curl https://your-backend-url.railway.app/health

# Check API documentation
curl https://your-backend-url.railway.app/docs
```

**Expected Results**:
```json
{
  "status": "healthy",
  "service": "todo-api",
  "version": "2.0.0"
}
```

### 3. Database Connection Check (Production)

Verify production database:

```bash
# Connect to production database
psql "your-production-database-url"

# Check tables exist
\dt

# Check users table
SELECT COUNT(*) FROM users;

# Check tasks table
SELECT COUNT(*) FROM tasks;
```

**Expected Results**:
- ✅ Connection successful
- ✅ Tables exist (users, tasks)
- ✅ No errors

### 4. CORS Check

Test CORS configuration:

```bash
# Test from frontend domain
curl -H "Origin: https://your-frontend-url.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Authorization" \
     -X OPTIONS \
     https://your-backend-url.railway.app/api/test-user-id/tasks
```

**Expected Headers in Response**:
```
Access-Control-Allow-Origin: https://your-frontend-url.vercel.app
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH
Access-Control-Allow-Headers: Authorization
```

## Functional Testing

### 1. User Signup Flow

1. Visit your frontend URL
2. Click "Sign Up"
3. Enter email and password
4. Submit form

**Expected Results**:
- ✅ Account created successfully
- ✅ Redirected to tasks page
- ✅ No error messages

### 2. User Login Flow

1. Visit your frontend URL
2. Click "Log In"
3. Enter credentials
4. Submit form

**Expected Results**:
- ✅ Login successful
- ✅ Redirected to tasks page
- ✅ JWT token stored
- ✅ No error messages

### 3. Task Creation

1. Log in to application
2. Enter task title
3. Enter task description (optional)
4. Click "Add Task"

**Expected Results**:
- ✅ Task appears in list
- ✅ Success message displayed
- ✅ Task persists after page refresh

### 4. Task Update

1. Click edit on existing task
2. Modify title or description
3. Save changes

**Expected Results**:
- ✅ Task updated successfully
- ✅ Changes visible immediately
- ✅ Changes persist after page refresh

### 5. Task Completion Toggle

1. Click checkbox on task
2. Verify visual change

**Expected Results**:
- ✅ Task marked as complete
- ✅ Visual indicator changes
- ✅ Status persists after page refresh

### 6. Task Deletion

1. Click delete on task
2. Confirm deletion

**Expected Results**:
- ✅ Task removed from list
- ✅ Confirmation dialog shown
- ✅ Task not visible after page refresh

### 7. User Isolation

1. Create tasks with User A
2. Log out
3. Sign up as User B
4. Check task list

**Expected Results**:
- ✅ User B sees empty task list
- ✅ User B cannot see User A's tasks
- ✅ No errors in console

### 8. JWT Expiration Handling

1. Log in to application
2. Wait for token to expire (or manually expire it)
3. Try to perform an action

**Expected Results**:
- ✅ Redirected to login page
- ✅ Error message displayed
- ✅ Can log in again successfully

## Performance Testing

### 1. Frontend Load Time

```bash
# Test with curl
time curl https://your-frontend-url.vercel.app

# Or use Lighthouse in Chrome DevTools
```

**Expected Results**:
- ✅ Page loads in < 3 seconds
- ✅ Lighthouse score > 90

### 2. API Response Time

```bash
# Test API endpoint
time curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-backend-url.railway.app/api/USER_ID/tasks
```

**Expected Results**:
- ✅ Response time < 500ms
- ✅ No timeout errors

### 3. Database Query Performance

```sql
-- Check slow queries in Neon dashboard
-- Or run EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = 'test-user-id';
```

**Expected Results**:
- ✅ Query execution time < 100ms
- ✅ Indexes being used

## Security Testing

### 1. Authentication Required

Test that endpoints require authentication:

```bash
# Try to access without token
curl https://your-backend-url.railway.app/api/test-user-id/tasks
```

**Expected Response**:
```json
{
  "detail": "Invalid or expired token"
}
```

### 2. User Isolation

Test that users can't access other users' data:

```bash
# Try to access another user's tasks
curl -H "Authorization: Bearer USER_A_TOKEN" \
     https://your-backend-url.railway.app/api/USER_B_ID/tasks
```

**Expected Response**:
```json
{
  "detail": "You don't have permission to access this resource"
}
```

### 3. HTTPS Enforcement

Verify all production URLs use HTTPS:

```bash
# Check frontend
curl -I https://your-frontend-url.vercel.app

# Check backend
curl -I https://your-backend-url.railway.app
```

**Expected Results**:
- ✅ All URLs use HTTPS
- ✅ No HTTP redirects
- ✅ Valid SSL certificates

### 4. SQL Injection Prevention

Test that SQL injection is prevented:

```bash
# Try SQL injection in task title
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "'; DROP TABLE tasks; --"}' \
     https://your-backend-url.railway.app/api/USER_ID/tasks
```

**Expected Results**:
- ✅ Request handled safely
- ✅ No database errors
- ✅ Tables still exist

## Error Handling Testing

### 1. Invalid Input

Test validation errors:

```bash
# Empty title
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": ""}' \
     https://your-backend-url.railway.app/api/USER_ID/tasks
```

**Expected Response**:
```json
{
  "detail": "Title must be between 1 and 200 characters"
}
```

### 2. Not Found

Test 404 errors:

```bash
# Non-existent task
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-backend-url.railway.app/api/USER_ID/tasks/99999
```

**Expected Response**:
```json
{
  "detail": "Task not found"
}
```

### 3. Network Errors

Test frontend handles network errors:

1. Disconnect from internet
2. Try to create a task
3. Reconnect

**Expected Results**:
- ✅ Error message displayed
- ✅ Retry option available
- ✅ Works after reconnecting

## Monitoring Setup

### 1. Vercel Analytics

1. Go to Vercel dashboard
2. Select your project
3. Click "Analytics"
4. Verify data is being collected

### 2. Backend Logs

Check backend logs for errors:

**Railway**:
```bash
railway logs
```

**Render**:
Check dashboard → Logs tab

**Expected Results**:
- ✅ No error logs
- ✅ Request logs visible
- ✅ Performance metrics available

### 3. Database Monitoring

1. Go to Neon dashboard
2. Select your project
3. Check "Monitoring" tab

**Expected Results**:
- ✅ Connection count normal
- ✅ Query performance good
- ✅ No slow queries

## Automated Verification Script

Save this as `verify-deployment.sh`:

```bash
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

echo "🔍 Verifying deployment..."
echo ""

# Check frontend
echo "Checking frontend..."
if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -q "200"; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend is not accessible${NC}"
fi

# Check backend health
echo "Checking backend health..."
HEALTH_RESPONSE=$(curl -s "$BACKEND_URL/health")
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend is not healthy${NC}"
fi

# Check API docs
echo "Checking API documentation..."
if curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/docs" | grep -q "200"; then
    echo -e "${GREEN}✅ API docs are accessible${NC}"
else
    echo -e "${RED}❌ API docs are not accessible${NC}"
fi

echo ""
echo "✨ Verification complete!"
```

Run with:
```bash
chmod +x verify-deployment.sh
./verify-deployment.sh

# For production
FRONTEND_URL=https://your-frontend.vercel.app \
BACKEND_URL=https://your-backend.railway.app \
./verify-deployment.sh
```

## Troubleshooting Common Issues

### Issue: "Failed to fetch" errors

**Diagnosis**:
```bash
# Check CORS configuration
curl -I -H "Origin: https://your-frontend-url.vercel.app" \
     https://your-backend-url.railway.app/health
```

**Solution**:
1. Verify `CORS_ORIGINS` includes frontend URL
2. Restart backend after changes
3. Clear browser cache

### Issue: "Invalid token" errors

**Diagnosis**:
```bash
# Check JWT secrets match
echo "Frontend secret: $BETTER_AUTH_SECRET"
echo "Backend secret: $JWT_SECRET"
```

**Solution**:
1. Ensure secrets match exactly
2. Regenerate if needed
3. Redeploy both services

### Issue: Database connection errors

**Diagnosis**:
```bash
# Test database connection
psql "$DATABASE_URL"
```

**Solution**:
1. Verify connection string format
2. Check database is running
3. Ensure `sslmode=require` for production

### Issue: Slow performance

**Diagnosis**:
```bash
# Check response times
time curl https://your-backend-url.railway.app/health
```

**Solution**:
1. Check database query performance
2. Review backend logs for errors
3. Consider adding caching
4. Check network latency

## Checklist

Use this checklist for deployment verification:

### Pre-Deployment
- [ ] All tests passing locally
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Frontend builds successfully
- [ ] Backend starts without errors

### Post-Deployment
- [ ] Frontend accessible
- [ ] Backend health check passes
- [ ] API documentation accessible
- [ ] Database connection works
- [ ] CORS configured correctly

### Functional Testing
- [ ] User signup works
- [ ] User login works
- [ ] Task creation works
- [ ] Task update works
- [ ] Task deletion works
- [ ] Task completion toggle works
- [ ] User isolation verified
- [ ] JWT expiration handled

### Security Testing
- [ ] Authentication required
- [ ] User isolation enforced
- [ ] HTTPS enabled
- [ ] SQL injection prevented

### Performance Testing
- [ ] Frontend loads quickly
- [ ] API responds quickly
- [ ] Database queries optimized

### Monitoring
- [ ] Frontend analytics enabled
- [ ] Backend logs accessible
- [ ] Database monitoring enabled

## Support

If you encounter issues during verification:
1. Check the logs first
2. Review this verification guide
3. Consult the DEPLOYMENT.md guide
4. Check platform-specific documentation
