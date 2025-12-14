# Todo App Frontend - Phase II

This is the frontend for the Phase II Full-Stack Web Application, built with Next.js 16+ and TypeScript.

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Authentication**: Better Auth (to be configured in Task 8)
- **State Management**: React hooks

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Authentication routes
│   │   ├── login/         # Login page
│   │   └── signup/        # Signup page
│   ├── (dashboard)/       # Protected dashboard routes
│   │   └── tasks/         # Tasks management page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── AuthForm.tsx       # Authentication form
│   ├── Header.tsx         # Navigation header
│   ├── TaskForm.tsx       # Task creation/edit form
│   ├── TaskItem.tsx       # Individual task component
│   └── TaskList.tsx       # Task list component
├── lib/                   # Utilities and configurations
│   ├── api.ts            # API client (to be implemented)
│   ├── auth.ts           # Better Auth config (to be implemented)
│   └── types.ts          # TypeScript interfaces
└── public/               # Static assets
```

## Getting Started

### Prerequisites

- Node.js 20+ (specified in `.nvmrc`)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your configuration:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Build

Create a production build:

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

## Implementation Status

- [x] Task 7: Next.js Project Setup
  - [x] Initialize Next.js 16+ with App Router
  - [x] Install TypeScript and Tailwind CSS
  - [x] Install Better Auth
  - [x] Set up project structure (app, components, lib)
  - [x] Create basic routing and layout

- [ ] Task 8: Better Auth Configuration
- [ ] Task 9: Authentication Pages
- [ ] Task 10: API Client
- [ ] Task 11: Task Components
- [ ] Task 12: Task Management Page
- [ ] Task 13: Navigation and Layout
- [ ] Task 14: Error Handling and Feedback

## Routes

- `/` - Home page with navigation
- `/login` - User login (to be implemented)
- `/signup` - User registration (to be implemented)
- `/tasks` - Task management dashboard (to be implemented)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |
| `BETTER_AUTH_SECRET` | Secret key for Better Auth | Yes |
| `BETTER_AUTH_URL` | Frontend URL for Better Auth | Yes |

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://www.better-auth.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
