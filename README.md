# Evolution of Todo - Phase II: Full-Stack Web Application

A modern, multi-user todo application built with Next.js, FastAPI, and PostgreSQL. This project demonstrates spec-driven development with secure authentication, RESTful API design, and user data isolation.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd todo-app-monorepo

# Install all dependencies
npm run install:all

# Set up environment variables (see Configuration section)
cp frontend/.env.local.example frontend/.env.local
cp backend/.env.example backend/.env

# Run database migrations
cd backend
python -m app.migrations.create_tables

# Start development servers
cd ..
npm run dev
```

Visit http://localhost:3000 to see the application!

## 📁 Project Structure

```
todo-app-monorepo/
├── frontend/              # Next.js 16+ web application
│   ├── app/              # App Router pages and layouts
│   ├── components/       # React components
│   ├── lib/              # Utilities, API client, auth config
│   └── .env.local        # Frontend environment variables
├── backend/              # FastAPI server
│   ├── app/              # Application code
│   │   ├── models/       # SQLModel database models
│   │   ├── routes/       # API endpoints
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── middleware/   # JWT authentication middleware
│   │   └── migrations/   # Database migration scripts
│   └── .env              # Backend environment variables
├── src/                  # Phase I console application (legacy)
├── .kiro/                # Kiro specs and configuration
│   └── specs/
│       └── phase2-fullstack-web/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── docker-compose.yml    # Docker setup for local development
├── package.json          # Root package.json for monorepo
└── README.md             # This file
```

## 🛠 Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT plugin
- **HTTP Client**: Fetch API

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (Neon Serverless)
- **Authentication**: JWT token verification
- **Validation**: Pydantic models

## 📋 Prerequisites

- **Node.js** 18+ and npm 9+
- **Python** 3.13+
- **PostgreSQL** database (Neon account recommended for serverless)
- **Git** for version control

## 🔧 Installation

### Option 1: Install All Dependencies (Recommended)

```bash
npm run install:all
```

This command installs:
- Root dependencies
- Frontend dependencies (Next.js, React, Tailwind, Better Auth)
- Backend dependencies (FastAPI, SQLModel, python-jose)

### Option 2: Install Individually

```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Configuration

### Frontend Environment Variables

Create `frontend/.env.local` with the following variables:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Optional: Database URL for Better Auth (if using database sessions)
# DATABASE_URL=postgresql://user:pass@host/dbname
```

**Environment Variable Descriptions:**

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | Yes | - |
| `BETTER_AUTH_SECRET` | Secret key for JWT signing (min 32 chars) | Yes | - |
| `BETTER_AUTH_URL` | Frontend application URL | Yes | - |

### Backend Environment Variables

Create `backend/.env` with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@host:5432/database_name

# JWT Configuration
JWT_SECRET=your-secret-key-must-match-frontend-better-auth-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Optional: Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Environment Variable Descriptions:**

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `JWT_SECRET` | Secret key for JWT verification (must match frontend) | Yes | - |
| `JWT_ALGORITHM` | JWT signing algorithm | No | HS256 |
| `JWT_EXPIRATION_DAYS` | Token expiration time in days | No | 7 |
| `CORS_ORIGINS` | Comma-separated allowed origins | Yes | - |
| `ENVIRONMENT` | Environment name (development/production) | No | development |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | No | INFO |

### Database Setup (Neon PostgreSQL)

1. **Create a Neon account**: Visit https://neon.tech and sign up
2. **Create a new project**: Click "New Project" in the dashboard
3. **Get connection string**: Copy the connection string from project settings
4. **Update backend/.env**: Paste the connection string as `DATABASE_URL`
5. **Run migrations**:
   ```bash
   cd backend
   python -m app.migrations.create_tables
   ```

### Security Notes

- **Never commit `.env` or `.env.local` files** to version control
- **Use strong secrets**: Generate secrets with `openssl rand -base64 32`
- **Match JWT secrets**: `JWT_SECRET` (backend) must equal `BETTER_AUTH_SECRET` (frontend)
- **Use HTTPS in production**: Always use secure connections for production deployments

## 🚀 Development

### Start All Services

Run both frontend and backend concurrently:

```bash
npm run dev
```

This starts:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Start Services Individually

```bash
# Frontend only (port 3000)
npm run dev:frontend

# Backend only (port 8000)
npm run dev:backend
```

### Using Docker Compose (Optional)

```bash
# Start all services with Docker
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build
```

## 🏗 Building for Production

### Frontend

```bash
cd frontend
npm run build
npm start
```

### Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Full Build

```bash
npm run build
```

## ✨ Features

- ✅ **User Authentication**: Secure signup/login with Better Auth and JWT
- ✅ **Task Management**: Create, read, update, delete tasks
- ✅ **Task Completion**: Mark tasks as complete/incomplete
- ✅ **User Data Isolation**: Private tasks per user
- ✅ **Persistent Storage**: PostgreSQL database with Neon
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **RESTful API**: JWT-authenticated API endpoints
- ✅ **Error Handling**: Comprehensive error messages and validation
- ✅ **Type Safety**: Full TypeScript support

## 📚 API Documentation

### Base URL

- **Development**: `http://localhost:8000`
- **Production**: Your deployed backend URL

### Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

The token is automatically included by the frontend API client after login.

### Endpoints

#### List Tasks

```http
GET /api/{user_id}/tasks
```

**Description**: Retrieve all tasks for the authenticated user.

**Path Parameters**:
- `user_id` (string, required): User ID from JWT token

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-13T10:30:00Z",
    "updated_at": "2025-12-13T10:30:00Z"
  }
]
```

#### Create Task

```http
POST /api/{user_id}/tasks
```

**Description**: Create a new task for the authenticated user.

**Path Parameters**:
- `user_id` (string, required): User ID from JWT token

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation Rules**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-13T10:30:00Z",
  "updated_at": "2025-12-13T10:30:00Z"
}
```

#### Get Task

```http
GET /api/{user_id}/tasks/{task_id}
```

**Description**: Retrieve a specific task by ID.

**Path Parameters**:
- `user_id` (string, required): User ID from JWT token
- `task_id` (integer, required): Task ID

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-13T10:30:00Z",
  "updated_at": "2025-12-13T10:30:00Z"
}
```

#### Update Task

```http
PUT /api/{user_id}/tasks/{task_id}
```

**Description**: Update an existing task.

**Path Parameters**:
- `user_id` (string, required): User ID from JWT token
- `task_id` (integer, required): Task ID

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": false
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "completed": false,
  "created_at": "2025-12-13T10:30:00Z",
  "updated_at": "2025-12-13T11:45:00Z"
}
```

#### Delete Task

```http
DELETE /api/{user_id}/tasks/{task_id}
```

**Description**: Delete a task permanently.

**Path Parameters**:
- `user_id` (string, required): User ID from JWT token
- `task_id` (integer, required): Task ID

**Response** (204 No Content)

#### Toggle Task Completion

```http
PATCH /api/{user_id}/tasks/{task_id}/complete
```

**Description**: Toggle the completion status of a task.

**Path Parameters**:
- `user_id` (string, required): User ID from JWT token
- `task_id` (integer, required): Task ID

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-12-13T10:30:00Z",
  "updated_at": "2025-12-13T12:00:00Z"
}
```

### Error Responses

All endpoints may return the following error responses:

#### 400 Bad Request
```json
{
  "detail": "Title must be between 1 and 200 characters"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

#### 403 Forbidden
```json
{
  "detail": "You don't have permission to access this resource"
}
```

#### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

### Interactive API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Frontend Tests

```bash
cd frontend
npm test
```

### Backend Tests

```bash
cd backend
pytest
```

### Integration Tests

```bash
cd backend
pytest test_integration.py
```

## 🐳 Docker Support

### Using Docker Compose

The project includes a `docker-compose.yml` file for easy local development:

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build
```

Services included:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **PostgreSQL**: localhost:5432 (for local development without Neon)

## 🚢 Deployment

### Frontend Deployment (Vercel)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy from frontend directory**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variables** in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your backend URL
   - `BETTER_AUTH_SECRET`: Your secret key
   - `BETTER_AUTH_URL`: Your frontend URL

4. **Deploy to production**:
   ```bash
   vercel --prod
   ```

### Backend Deployment

#### Option 1: Docker Container

```bash
cd backend
docker build -t todo-backend .
docker run -p 8000:8000 --env-file .env todo-backend
```

#### Option 2: Platform as a Service (Railway, Render, etc.)

1. Connect your Git repository
2. Set environment variables in platform dashboard
3. Deploy automatically on push

### Database (Neon)

Neon is serverless and production-ready by default:
1. Use the same connection string from development
2. Or create a separate production database in Neon dashboard
3. Update `DATABASE_URL` in production environment

### Post-Deployment Checklist

- [ ] Frontend deployed and accessible
- [ ] Backend deployed and accessible
- [ ] Database migrations run successfully
- [ ] Environment variables configured correctly
- [ ] CORS origins include production frontend URL
- [ ] JWT secrets match between frontend and backend
- [ ] HTTPS enabled for both frontend and backend
- [ ] Test user signup and login
- [ ] Test task CRUD operations
- [ ] Verify user data isolation

## 📖 Project Phases

- **Phase I**: Console application (completed) - See `src/` directory
- **Phase II**: Full-stack web application (current) - See `frontend/` and `backend/`
- **Phase III**: Advanced features (future)

## 🔄 Development Workflow

This project follows **spec-driven development** using Kiro. See `.kiro/specs/phase2-fullstack-web/` for:
- `requirements.md` - Feature requirements with acceptance criteria
- `design.md` - Technical design and architecture
- `tasks.md` - Implementation tasks and progress

## 📚 Additional Documentation

- **[API.md](API.md)** - Complete API reference with examples
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide for production
- **[ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)** - Environment variable reference
- **[VERIFICATION.md](VERIFICATION.md)** - Deployment verification checklist
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines

## 🔍 Quick Verification

Run the verification script to check your deployment:

```bash
# Local development
./verify-deployment.sh

# Production
FRONTEND_URL=https://your-frontend.vercel.app \
BACKEND_URL=https://your-backend.railway.app \
./verify-deployment.sh
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📄 License

MIT
