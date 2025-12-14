# Deployment Checklist

Use this checklist to ensure a smooth deployment of the Evolution of Todo application.

## 📋 Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing locally
- [ ] No console errors in browser
- [ ] No linting errors
- [ ] Code reviewed and approved
- [ ] Git repository up to date

### Documentation
- [ ] README.md updated with setup instructions
- [ ] API.md documents all endpoints
- [ ] ENVIRONMENT_VARIABLES.md lists all required variables
- [ ] DEPLOYMENT.md provides deployment guide
- [ ] VERIFICATION.md includes verification steps

### Environment Configuration
- [ ] Frontend `.env.local.example` exists
- [ ] Backend `.env.example` exists
- [ ] All required environment variables documented
- [ ] Secrets generated (minimum 32 characters)
- [ ] JWT secrets match between frontend and backend

### Database
- [ ] Neon PostgreSQL account created
- [ ] Database instance created
- [ ] Connection string obtained
- [ ] Migrations tested locally
- [ ] Database schema verified

### Docker (Optional)
- [ ] `docker-compose.yml` created
- [ ] Frontend `Dockerfile` created
- [ ] Backend `Dockerfile` created
- [ ] `.dockerignore` files created
- [ ] Docker setup tested locally

## 🚀 Deployment Steps

### 1. Database Setup

- [ ] Create production database in Neon
- [ ] Copy production connection string
- [ ] Run migrations on production database:
  ```bash
  export DATABASE_URL="production-connection-string"
  cd backend
  python -m app.migrations.create_tables
  ```
- [ ] Verify tables created successfully

### 2. Backend Deployment

#### Option A: Railway
- [ ] Install Railway CLI: `npm install -g @railway/cli`
- [ ] Login: `railway login`
- [ ] Initialize: `cd backend && railway init`
- [ ] Set environment variables:
  ```bash
  railway variables set DATABASE_URL="..."
  railway variables set JWT_SECRET="..."
  railway variables set CORS_ORIGINS="..."
  ```
- [ ] Deploy: `railway up`
- [ ] Get URL: `railway domain`
- [ ] Test health endpoint: `curl https://your-url.railway.app/health`

#### Option B: Render
- [ ] Create account at render.com
- [ ] Create new Web Service
- [ ] Connect Git repository
- [ ] Configure build/start commands
- [ ] Set environment variables in dashboard
- [ ] Deploy and verify

#### Option C: Docker
- [ ] Build image: `docker build -t todo-backend backend/`
- [ ] Test locally: `docker run -p 8000:8000 --env-file backend/.env todo-backend`
- [ ] Push to registry
- [ ] Deploy to cloud platform

### 3. Frontend Deployment

#### Vercel (Recommended)
- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Login: `vercel login`
- [ ] Deploy: `cd frontend && vercel`
- [ ] Set environment variables in Vercel dashboard:
  - `NEXT_PUBLIC_API_URL`: Backend URL
  - `BETTER_AUTH_SECRET`: Same as backend JWT_SECRET
  - `BETTER_AUTH_URL`: Frontend URL
- [ ] Deploy to production: `vercel --prod`
- [ ] Verify deployment

### 4. Environment Variables Configuration

#### Frontend (Vercel)
- [ ] `NEXT_PUBLIC_API_URL` set to backend URL
- [ ] `BETTER_AUTH_SECRET` set (matches backend)
- [ ] `BETTER_AUTH_URL` set to frontend URL
- [ ] All variables saved
- [ ] Deployment triggered

#### Backend (Railway/Render)
- [ ] `DATABASE_URL` set to production database
- [ ] `JWT_SECRET` set (matches frontend)
- [ ] `JWT_ALGORITHM` set to HS256
- [ ] `JWT_EXPIRATION_DAYS` set to 7
- [ ] `CORS_ORIGINS` includes frontend URL
- [ ] All variables saved
- [ ] Service restarted

## ✅ Post-Deployment Verification

### Automated Verification
- [ ] Run verification script:
  ```bash
  FRONTEND_URL=https://your-frontend.vercel.app \
  BACKEND_URL=https://your-backend.railway.app \
  ./verify-deployment.sh
  ```
- [ ] All checks passing

### Manual Verification

#### Frontend
- [ ] Frontend URL accessible
- [ ] No console errors
- [ ] Page loads quickly (< 3 seconds)
- [ ] Responsive on mobile
- [ ] All assets loading

#### Backend
- [ ] Health endpoint returns 200: `curl https://backend-url/health`
- [ ] API docs accessible: `https://backend-url/docs`
- [ ] CORS headers present
- [ ] Response times acceptable (< 500ms)

#### Database
- [ ] Connection successful
- [ ] Tables exist (users, tasks)
- [ ] Indexes created
- [ ] No connection errors

### Functional Testing

#### Authentication
- [ ] User signup works
- [ ] User login works
- [ ] JWT token issued
- [ ] Token stored securely
- [ ] Logout works

#### Task Management
- [ ] Create task works
- [ ] View tasks works
- [ ] Update task works
- [ ] Delete task works
- [ ] Toggle completion works
- [ ] Tasks persist after refresh

#### Security
- [ ] User isolation verified (users can't see each other's tasks)
- [ ] Authentication required for all endpoints
- [ ] Invalid tokens rejected
- [ ] HTTPS enforced in production
- [ ] SQL injection prevented

#### Error Handling
- [ ] Validation errors displayed
- [ ] Network errors handled
- [ ] 404 errors handled
- [ ] 500 errors handled
- [ ] User-friendly error messages

## 📊 Monitoring Setup

### Frontend (Vercel)
- [ ] Vercel Analytics enabled
- [ ] Error tracking configured
- [ ] Performance monitoring active

### Backend
- [ ] Logging configured
- [ ] Error tracking enabled
- [ ] Performance monitoring active
- [ ] Alerts configured

### Database (Neon)
- [ ] Monitoring dashboard reviewed
- [ ] Query performance checked
- [ ] Connection pool configured
- [ ] Backup schedule verified

## 🔒 Security Checklist

- [ ] All secrets are strong (32+ characters)
- [ ] Secrets not committed to Git
- [ ] Different secrets for dev/prod
- [ ] HTTPS enabled everywhere
- [ ] CORS restricted to known origins
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection enabled
- [ ] Rate limiting considered
- [ ] Security headers configured

## 📝 Documentation Checklist

- [ ] README.md updated
- [ ] API.md complete
- [ ] DEPLOYMENT.md accurate
- [ ] ENVIRONMENT_VARIABLES.md comprehensive
- [ ] VERIFICATION.md detailed
- [ ] All example files updated
- [ ] Deployment URLs documented
- [ ] Known issues documented

## 🎯 Performance Checklist

- [ ] Frontend Lighthouse score > 90
- [ ] API response time < 500ms
- [ ] Database queries optimized
- [ ] Images optimized
- [ ] Code splitting enabled
- [ ] Caching configured
- [ ] CDN configured (if applicable)

## 🔄 Rollback Plan

- [ ] Previous deployment URLs saved
- [ ] Rollback procedure documented
- [ ] Database backup created
- [ ] Rollback tested in staging

### Rollback Commands

**Vercel**:
```bash
vercel ls
vercel rollback [deployment-url]
```

**Railway**:
```bash
railway rollback
```

**Database**:
```bash
# Restore from Neon backup in dashboard
```

## 📞 Support Contacts

- [ ] Team contacts documented
- [ ] On-call schedule defined
- [ ] Escalation path defined
- [ ] Support channels configured

## 🎉 Launch Checklist

### Final Checks
- [ ] All deployment steps completed
- [ ] All verification tests passing
- [ ] Monitoring active
- [ ] Team notified
- [ ] Documentation shared
- [ ] Rollback plan ready

### Communication
- [ ] Stakeholders notified
- [ ] Users informed (if applicable)
- [ ] Social media updated (if applicable)
- [ ] Blog post published (if applicable)

### Post-Launch
- [ ] Monitor for 24 hours
- [ ] Review error logs
- [ ] Check performance metrics
- [ ] Gather user feedback
- [ ] Document lessons learned

## 📈 Success Metrics

Track these metrics after deployment:

- [ ] Uptime > 99.9%
- [ ] Response time < 500ms
- [ ] Error rate < 1%
- [ ] User satisfaction > 90%
- [ ] Zero security incidents

## 🔧 Maintenance Schedule

- [ ] Daily: Check error logs
- [ ] Weekly: Review performance metrics
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Security audit
- [ ] Annually: Rotate secrets

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Neon Documentation](https://neon.tech/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

**Note**: This checklist should be reviewed and updated regularly to reflect changes in the deployment process.

**Last Updated**: December 13, 2025
