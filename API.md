# API Documentation - Evolution of Todo

Complete API reference for the Evolution of Todo backend service.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: Your deployed backend URL

## Authentication

All API endpoints (except `/health` and `/`) require JWT authentication.

### Authentication Header

Include the JWT token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### Getting a Token

Tokens are issued by Better Auth on the frontend after successful login/signup. The frontend automatically includes the token in all API requests.

### Token Structure

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "exp": 1734567890,
  "iat": 1734481490
}
```

- `sub`: User ID (UUID)
- `email`: User's email address
- `exp`: Expiration timestamp (Unix time)
- `iat`: Issued at timestamp (Unix time)

## Endpoints

### Health Check

Check if the API is running.

```http
GET /health
```

**Authentication**: Not required

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "todo-api",
  "version": "2.0.0"
}
```

---

### Root

Get API information.

```http
GET /
```

**Authentication**: Not required

**Response** (200 OK):
```json
{
  "message": "Todo API",
  "version": "2.0.0",
  "docs": "/docs"
}
```

---

### List Tasks

Retrieve all tasks for the authenticated user.

```http
GET /api/{user_id}/tasks
```

**Authentication**: Required

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User ID from JWT token |

**Query Parameters**: None

**Request Headers**:
```http
Authorization: Bearer <jwt-token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-13T10:30:00.000Z",
    "updated_at": "2025-12-13T10:30:00.000Z"
  },
  {
    "id": 2,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Finish project",
    "description": "Complete Phase II implementation",
    "completed": true,
    "created_at": "2025-12-12T09:00:00.000Z",
    "updated_at": "2025-12-13T14:20:00.000Z"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in URL doesn't match token
- `500 Internal Server Error`: Database or server error

**Example**:
```bash
curl -X GET "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### Create Task

Create a new task for the authenticated user.

```http
POST /api/{user_id}/tasks
```

**Authentication**: Required

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User ID from JWT token |

**Request Headers**:
```http
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Body Parameters**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 characters | Task title |
| `description` | string | No | Max 1000 characters | Task description |

**Response** (201 Created):
```json
{
  "id": 3,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-13T15:45:00.000Z",
  "updated_at": "2025-12-13T15:45:00.000Z"
}
```

**Error Responses**:
- `400 Bad Request`: Validation error (title too long, empty, etc.)
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User ID in URL doesn't match token
- `500 Internal Server Error`: Database or server error

**Validation Errors**:
```json
{
  "detail": "Title must be between 1 and 200 characters"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

---

### Get Task

Retrieve a specific task by ID.

```http
GET /api/{user_id}/tasks/{task_id}
```

**Authentication**: Required

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User ID from JWT token |
| `task_id` | integer | Yes | Task ID |

**Request Headers**:
```http
Authorization: Bearer <jwt-token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-13T10:30:00.000Z",
  "updated_at": "2025-12-13T10:30:00.000Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database or server error

**Example**:
```bash
curl -X GET "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### Update Task

Update an existing task.

```http
PUT /api/{user_id}/tasks/{task_id}
```

**Authentication**: Required

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User ID from JWT token |
| `task_id` | integer | Yes | Task ID |

**Request Headers**:
```http
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables",
  "completed": false
}
```

**Body Parameters**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 characters | Task title |
| `description` | string | No | Max 1000 characters | Task description |
| `completed` | boolean | No | true/false | Completion status |

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables",
  "completed": false,
  "created_at": "2025-12-13T10:30:00.000Z",
  "updated_at": "2025-12-13T16:15:00.000Z"
}
```

**Error Responses**:
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database or server error

**Example**:
```bash
curl -X PUT "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and cook dinner", "description": "Milk, eggs, bread, chicken", "completed": false}'
```

---

### Delete Task

Delete a task permanently.

```http
DELETE /api/{user_id}/tasks/{task_id}
```

**Authentication**: Required

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User ID from JWT token |
| `task_id` | integer | Yes | Task ID |

**Request Headers**:
```http
Authorization: Bearer <jwt-token>
```

**Response** (204 No Content):
No response body

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database or server error

**Example**:
```bash
curl -X DELETE "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### Toggle Task Completion

Toggle the completion status of a task.

```http
PATCH /api/{user_id}/tasks/{task_id}/complete
```

**Authentication**: Required

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string (UUID) | Yes | User ID from JWT token |
| `task_id` | integer | Yes | Task ID |

**Request Headers**:
```http
Authorization: Bearer <jwt-token>
```

**Request Body**: None

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-12-13T10:30:00.000Z",
  "updated_at": "2025-12-13T16:30:00.000Z"
}
```

**Behavior**:
- If task is incomplete (`completed: false`), it becomes complete (`completed: true`)
- If task is complete (`completed: true`), it becomes incomplete (`completed: false`)

**Error Responses**:
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database or server error

**Example**:
```bash
curl -X PATCH "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks/1/complete" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

Validation error or malformed request.

```json
{
  "detail": "Title must be between 1 and 200 characters"
}
```

### 401 Unauthorized

Missing or invalid JWT token.

```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden

User doesn't have permission to access the resource.

```json
{
  "detail": "You don't have permission to access this resource"
}
```

### 404 Not Found

Resource doesn't exist.

```json
{
  "detail": "Task not found"
}
```

### 500 Internal Server Error

Unexpected server error.

```json
{
  "detail": "Internal server error"
}
```

## Data Models

### Task

```typescript
interface Task {
  id: number;                    // Auto-generated task ID
  user_id: string;               // UUID of task owner
  title: string;                 // Task title (1-200 chars)
  description: string | null;    // Task description (max 1000 chars)
  completed: boolean;            // Completion status
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
}
```

### User

```typescript
interface User {
  id: string;                    // UUID
  email: string;                 // User email (unique)
  name: string | null;           // User display name
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
}
```

## Rate Limiting

Currently, there are no rate limits enforced. This may change in future versions.

## Versioning

The API is currently at version 2.0.0. Future breaking changes will be versioned appropriately.

## Interactive Documentation

For interactive API documentation with the ability to test endpoints:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Code Examples

### JavaScript/TypeScript (Frontend)

```typescript
// API client example
const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function getTasks(userId: string, token: string): Promise<Task[]> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

async function createTask(
  userId: string,
  token: string,
  data: { title: string; description?: string }
): Promise<Task> {
  const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}
```

### Python

```python
import requests

API_URL = "http://localhost:8000"
TOKEN = "your-jwt-token"

def get_tasks(user_id: str) -> list:
    response = requests.get(
        f"{API_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    response.raise_for_status()
    return response.json()

def create_task(user_id: str, title: str, description: str = None) -> dict:
    response = requests.post(
        f"{API_URL}/api/{user_id}/tasks",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        },
        json={"title": title, "description": description}
    )
    response.raise_for_status()
    return response.json()
```

### cURL

```bash
# Get all tasks
curl -X GET "http://localhost:8000/api/USER_ID/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create task
curl -X POST "http://localhost:8000/api/USER_ID/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New task", "description": "Task details"}'

# Update task
curl -X PUT "http://localhost:8000/api/USER_ID/tasks/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task", "completed": true}'

# Delete task
curl -X DELETE "http://localhost:8000/api/USER_ID/tasks/1" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Toggle completion
curl -X PATCH "http://localhost:8000/api/USER_ID/tasks/1/complete" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Support

For issues or questions about the API:
- Check the interactive documentation at `/docs`
- Review this API documentation
- Check the project README.md
- Open an issue on GitHub
