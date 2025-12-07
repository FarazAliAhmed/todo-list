# Evolution of Todo - Phase II: Full-Stack Web Application

A modern, multi-user todo application built with Next.js, FastAPI, and PostgreSQL.

## Project Structure

```
todo-app-monorepo/
├── frontend/          # Next.js 16+ web application
├── backend/           # FastAPI server
├── src/               # Phase I console application (legacy)
├── .kiro/             # Kiro specs and configuration
├── package.json       # Root package.json for monorepo
└── README.md          # This file
```

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)

## Getting Started

### Prerequisites
- Node.js 18+ and npm 9+
- Python 3.13+
- PostgreSQL database (Neon account recommended)

### Installation

1. Install all dependencies:
```bash
npm run install:all
```

Or install individually:

```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

### Configuration

1. **Frontend** - Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

2. **Backend** - Create `backend/.env`:
```env
DATABASE_URL=postgresql://user:pass@host/dbname
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

### Development

Run both frontend and backend concurrently:
```bash
npm run dev
```

Or run individually:

```bash
# Frontend only (port 3000)
npm run dev:frontend

# Backend only (port 8000)
npm run dev:backend
```

### Building for Production

```bash
npm run build
```

## Features

- ✅ User authentication (signup/login)
- ✅ Create, read, update, delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ User data isolation (private tasks)
- ✅ Persistent storage with PostgreSQL
- ✅ Responsive web design
- ✅ RESTful API with JWT authentication

## API Documentation

Once the backend is running, visit:
- API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Project Phases

- **Phase I**: Console application (completed) - See `src/` directory
- **Phase II**: Full-stack web application (current) - See `frontend/` and `backend/`
- **Phase III**: Advanced features (future)

## Development Workflow

This project follows spec-driven development using Kiro. See `.kiro/specs/phase2-fullstack-web/` for:
- `requirements.md` - Feature requirements
- `design.md` - Technical design
- `tasks.md` - Implementation tasks

## License

MIT
