# Design Document - Phase II: Full-Stack Web Application

## Overview

This document outlines the technical design for transforming the Phase I console application into a modern, multi-user web application. The system follows a client-server architecture with a Next.js frontend, FastAPI backend, and PostgreSQL database, implementing secure authentication and RESTful API communication.

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Next.js 16+ Frontend                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │ │
│  │  │   Pages/     │  │  Components  │  │   API Client    │ │ │
│  │  │   Routes     │  │   (UI)       │  │  (with JWT)     │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │           Better Auth (Authentication)               │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTPS + JWT
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                      FastAPI Backend Server                       │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                  API Routes Layer                          │  │
│  │  /api/{user_id}/tasks (GET, POST, PUT, DELETE, PATCH)    │  │
│  └───────────────────────┬────────────────────────────────────┘  │
│                          │                                        │
│  ┌───────────────────────▼────────────────────────────────────┐  │
│  │              JWT Middleware                                │  │
│  │  (Verify token, extract user_id, validate ownership)      │  │
│  └───────────────────────┬────────────────────────────────────┘  │
│                          │                                        │
│  ┌───────────────────────▼────────────────────────────────────┐  │
│  │              Business Logic Layer                          │  │
│  │  (Task operations with user isolation)                     │  │
│  └───────────────────────┬────────────────────────────────────┘  │
│                          │                                        │
│  ┌───────────────────────▼────────────────────────────────────┐  │
│  │              SQLModel ORM Layer                            │  │
│  │  (Database models and queries)                             │  │
│  └───────────────────────┬────────────────────────────────────┘  │
└──────────────────────────┼────────────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────────────────┐
│              Neon Serverless PostgreSQL Database                  │
│  ┌──────────────┐  ┌──────────────┐                              │
│  │  users       │  │   tasks      │                              │
│  │  table       │  │   table      │                              │
│  └──────────────┘  └──────────────┘                              │
└───────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**: Frontend, backend, and database are independent layers
2. **Stateless API**: Backend doesn't maintain session state (JWT-based auth)
3. **User Isolation**: All data operations filtered by authenticated user
4. **RESTful Design**: Standard HTTP methods and status codes
5. **Security First**: Authentication required for all operations

## Components and Interfaces

### 1. Frontend (Next.js 16+)

#### Technology Stack
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT plugin
- **HTTP Client**: Fetch API / Axios

#### Directory Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── signup/
│   │       └── page.tsx
│   ├── (dashboard)/
│   │   └── tasks/
│   │       └── page.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── TaskList.tsx
│   ├── TaskItem.tsx
│   ├── TaskForm.tsx
│   ├── Header.tsx
│   └── AuthForm.tsx
├── lib/
│   ├── api.ts              # API client with JWT
│   ├── auth.ts             # Better Auth configuration
│   └── types.ts            # TypeScript interfaces
├── public/
└── package.json
```

#### Key Components

**API Client (`lib/api.ts`)**
```typescript
interface ApiClient {
  getTasks(userId: string): Promise<Task[]>
  createTask(userId: string, data: CreateTaskDto): Promise<Task>
  updateTask(userId: string, taskId: number, data: UpdateTaskDto): Promise<Task>
  deleteTask(userId: string, taskId: number): Promise<void>
  toggleComplete(userId: string, taskId: number): Promise<Task>
}
```

**Better Auth Configuration (`lib/auth.ts`)**
- JWT plugin enabled
- Email/password authentication
- Session management
- Token refresh logic

**Task Components**
- `TaskList`: Display all tasks with filtering
- `TaskItem`: Individual task with actions (edit, delete, toggle)
- `TaskForm`: Create/edit task form with validation
- `Header`: Navigation and user menu
- `AuthForm`: Login/signup forms

### 2. Backend (FastAPI)

#### Technology Stack
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: PostgreSQL (via Neon)
- **Authentication**: JWT verification
- **Validation**: Pydantic models

#### Directory Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration and environment
│   ├── database.py             # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── task.py             # Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py             # Pydantic schemas
│   │   └── user.py             # User schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py            # Task API endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py             # JWT verification middleware
│   └── services/
│       ├── __init__.py
│       └── task_service.py     # Business logic
├── requirements.txt
└── pyproject.toml
```

#### API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /api/{user_id}/tasks | List all user's tasks | Yes |
| POST | /api/{user_id}/tasks | Create new task | Yes |
| GET | /api/{user_id}/tasks/{id} | Get task details | Yes |
| PUT | /api/{user_id}/tasks/{id} | Update task | Yes |
| DELETE | /api/{user_id}/tasks/{id} | Delete task | Yes |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion | Yes |

#### Request/Response Schemas

**Create Task Request**
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

**Task Response**
```json
{
  "id": 1,
  "user_id": "user-uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-04T10:30:00Z",
  "updated_at": "2025-12-04T10:30:00Z"
}
```

**Error Response**
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### 3. Database (Neon PostgreSQL)

#### Schema Design

**users table** (managed by Better Auth)
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

**tasks table**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

#### SQLModel Models

**User Model**
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")
```

**Task Model**
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

## Authentication Flow

### JWT Token Structure

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Authentication Sequence

```
1. User Login
   ├─> Frontend: User enters email/password
   ├─> Better Auth: Validates credentials
   ├─> Better Auth: Issues JWT token
   └─> Frontend: Stores token in secure storage

2. API Request
   ├─> Frontend: Adds "Authorization: Bearer <token>" header
   ├─> Backend: JWT Middleware extracts token
   ├─> Backend: Verifies token signature
   ├─> Backend: Extracts user_id from token
   ├─> Backend: Validates user_id matches URL parameter
   └─> Backend: Processes request with user context

3. User Logout
   ├─> Frontend: Clears stored token
   └─> Frontend: Redirects to login page
```

### Security Measures

1. **JWT Verification**: Backend verifies token signature using shared secret
2. **User ID Validation**: URL user_id must match token user_id
3. **Token Expiry**: Tokens expire after 7 days
4. **HTTPS Only**: All communication over HTTPS in production
5. **Password Hashing**: Passwords hashed with bcrypt
6. **SQL Injection Prevention**: SQLModel parameterized queries

## Data Flow

### Create Task Flow

```
1. User fills form in Frontend
2. Frontend validates input (client-side)
3. Frontend sends POST /api/{user_id}/tasks with JWT
4. Backend JWT middleware verifies token
5. Backend validates user_id matches token
6. Backend validates task data (title length, etc.)
7. Backend creates task in database with user_id
8. Backend returns created task
9. Frontend updates UI with new task
```

### List Tasks Flow

```
1. User navigates to tasks page
2. Frontend sends GET /api/{user_id}/tasks with JWT
3. Backend JWT middleware verifies token
4. Backend validates user_id matches token
5. Backend queries: SELECT * FROM tasks WHERE user_id = ?
6. Backend returns filtered task list
7. Frontend renders tasks
```

### Update Task Flow

```
1. User edits task in Frontend
2. Frontend sends PUT /api/{user_id}/tasks/{id} with JWT
3. Backend JWT middleware verifies token
4. Backend validates user_id matches token
5. Backend queries task: SELECT * FROM tasks WHERE id = ? AND user_id = ?
6. If task not found or wrong user: return 403 Forbidden
7. Backend updates task in database
8. Backend returns updated task
9. Frontend updates UI
```

## Error Handling

### HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing or invalid JWT |
| 403 | Forbidden | User doesn't own resource |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected backend error |

### Frontend Error Handling

```typescript
try {
  const task = await api.createTask(userId, taskData);
  showSuccess("Task created successfully!");
} catch (error) {
  if (error.status === 401) {
    // Redirect to login
    router.push('/login');
  } else if (error.status === 400) {
    // Show validation errors
    showError(error.detail);
  } else {
    // Generic error
    showError("Something went wrong. Please try again.");
  }
}
```

### Backend Error Handling

```python
@router.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    # Validate user owns this endpoint
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Validate task data
    if not task_data.title or len(task_data.title) > 200:
        raise HTTPException(
            status_code=400,
            detail="Title must be 1-200 characters"
        )

    try:
        task = await task_service.create_task(user_id, task_data)
        return task
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Environment Configuration

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host/dbname
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

## Deployment Considerations

### Development
- Frontend: `npm run dev` (port 3000)
- Backend: `uvicorn app.main:app --reload` (port 8000)
- Database: Neon serverless (cloud-hosted)

### Production (Future)
- Frontend: Vercel deployment
- Backend: Docker container on cloud platform
- Database: Neon production instance
- HTTPS: Automatic via Vercel/cloud platform

## Testing Strategy

### Frontend Testing
- Component tests with React Testing Library
- Integration tests for user flows
- E2E tests with Playwright (optional)

### Backend Testing
- Unit tests for business logic
- Integration tests for API endpoints
- Database tests with test database

### Manual Testing Checklist
- [ ] User signup and login
- [ ] Create task (with/without description)
- [ ] View tasks (empty and populated)
- [ ] Update task
- [ ] Delete task
- [ ] Toggle completion
- [ ] User isolation (can't see other users' tasks)
- [ ] JWT expiration handling
- [ ] Error messages display correctly
- [ ] Responsive design on mobile

## Migration from Phase I

### Code Reuse
- Phase I business logic can be adapted for backend
- Validation rules remain the same
- Data models similar (add user_id field)

### New Components
- Frontend: Entirely new (Next.js)
- Authentication: New (Better Auth + JWT)
- Database: New (PostgreSQL instead of in-memory)
- API Layer: New (FastAPI routes)

## Summary

This design provides:
- ✅ Secure multi-user authentication
- ✅ RESTful API with JWT protection
- ✅ User data isolation
- ✅ Persistent storage with PostgreSQL
- ✅ Responsive web interface
- ✅ Clear separation of concerns
- ✅ Scalable architecture
- ✅ Ready for Phase III evolution
