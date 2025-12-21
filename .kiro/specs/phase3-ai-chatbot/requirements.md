# Phase III: AI-Powered Todo Chatbot

## Overview
Transform the Todo app into an AI-powered chatbot that manages tasks through natural language using MCP (Model Context Protocol) server architecture.

## Due Date
December 21, 2025 (TODAY)

## Technology Stack
| Component | Technology |
|-----------|------------|
| Frontend | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth |

## Requirements

### 1. Conversational Interface
- Natural language task management
- Chat UI using OpenAI ChatKit
- Conversation history persistence

### 2. MCP Server Tools
The MCP server must expose these tools:

| Tool | Purpose | Parameters |
|------|---------|------------|
| add_task | Create a new task | user_id, title, description (optional) |
| list_tasks | Get all tasks | user_id, status (all/pending/completed) |
| complete_task | Mark task complete | user_id, task_id |
| delete_task | Remove a task | user_id, task_id |
| update_task | Modify task | user_id, task_id, title, description |

### 3. Database Models
- Task (existing from Phase II)
- Conversation (new): user_id, id, created_at, updated_at
- Message (new): user_id, id, conversation_id, role, content, created_at

### 4. API Endpoint
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/{user_id}/chat | Send message & get AI response |

### 5. Natural Language Commands
| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | add_task |
| "Show me all my tasks" | list_tasks (status: all) |
| "What's pending?" | list_tasks (status: pending) |
| "Mark task 3 as complete" | complete_task |
| "Delete the meeting task" | delete_task |
| "Change task 1 to 'Call mom'" | update_task |

## Architecture
```
┌─────────────┐     ┌──────────────────────────────────┐     ┌─────────────┐
│  ChatKit UI │────▶│  FastAPI Server                  │     │   Neon DB   │
│  (Frontend) │     │  ├── Chat Endpoint               │     │             │
│             │◀────│  ├── OpenAI Agents SDK           │────▶│  - tasks    │
│             │     │  └── MCP Server (Tools)          │◀────│  - convos   │
└─────────────┘     └──────────────────────────────────┘     │  - messages │
                                                             └─────────────┘
```

## Deliverables
1. ChatKit-based chat UI in frontend
2. MCP server with task management tools
3. OpenAI Agents SDK integration
4. Conversation persistence
5. Working natural language task management
