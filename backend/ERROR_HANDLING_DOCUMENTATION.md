# Error Handling and Validation Documentation

## Overview

This document describes the comprehensive error handling and validation system implemented for the Todo API, fulfilling **Requirement 11 (Error Handling and User Feedback)**.

## Features Implemented

### 1. Global Exception Handlers

Located in `app/exceptions.py`, the API includes global exception handlers for:

- **Validation Errors (400)**: Pydantic validation failures with detailed field-level error messages
- **Database Errors (500)**: SQLAlchemy exceptions with safe error messages
- **Generic Errors (500)**: Catch-all for unexpected exceptions

### 2. Consistent Error Response Format

All errors return a consistent JSON structure:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "errors": [  // Optional, for validation errors
    {
      "field": "title",
      "message": "String should have at most 200 characters",
      "type": "string_too_long"
    }
  ]
}
```

### 3. HTTP Status Codes

The API returns appropriate status codes for all scenarios:

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors, malformed requests |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | User doesn't own the resource |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected backend errors |

### 4. Input Validation

#### Title Validation
- **Minimum length**: 1 character
- **Maximum length**: 200 characters
- **Additional rules**: Cannot be empty or whitespace-only
- **Error message**: "Title cannot be empty or whitespace only"

#### Description Validation
- **Maximum length**: 1000 characters
- **Optional**: Can be null or omitted
- **Whitespace handling**: Empty strings are converted to null

### 5. Helper Functions

Located in `app/errors.py`, standardized error creation functions:

```python
unauthorized_error(detail)      # Returns 401
forbidden_error(detail)         # Returns 403
not_found_error(resource, id)   # Returns 404
bad_request_error(detail)       # Returns 400
internal_server_error(detail)   # Returns 500
```

## Examples

### Validation Error (400)

**Request:**
```bash
POST /api/{user_id}/tasks
{
  "title": "",
  "description": "Test"
}
```

**Response:**
```json
{
  "detail": "Validation error",
  "status_code": 400,
  "errors": [
    {
      "field": "title",
      "message": "Title cannot be empty or whitespace only",
      "type": "value_error"
    }
  ]
}
```

### Unauthorized Error (401)

**Request:**
```bash
GET /api/{user_id}/tasks
# No Authorization header
```

**Response:**
```json
{
  "detail": "Authentication required"
}
```

### Forbidden Error (403)

**Request:**
```bash
GET /api/other-user-id/tasks
Authorization: Bearer <valid-token-for-different-user>
```

**Response:**
```json
{
  "detail": "Access denied: You can only access your own resources"
}
```

### Not Found Error (404)

**Request:**
```bash
GET /api/{user_id}/tasks/99999
Authorization: Bearer <valid-token>
```

**Response:**
```json
{
  "detail": "Task 99999 not found"
}
```

### Title Too Long (400)

**Request:**
```bash
POST /api/{user_id}/tasks
{
  "title": "x" * 201,  // 201 characters
  "description": "Test"
}
```

**Response:**
```json
{
  "detail": "Validation error",
  "status_code": 400,
  "errors": [
    {
      "field": "title",
      "message": "String should have at most 200 characters",
      "type": "string_too_long"
    }
  ]
}
```

### Description Too Long (400)

**Request:**
```bash
POST /api/{user_id}/tasks
{
  "title": "Test",
  "description": "x" * 1001  // 1001 characters
}
```

**Response:**
```json
{
  "detail": "Validation error",
  "status_code": 400,
  "errors": [
    {
      "field": "description",
      "message": "String should have at most 1000 characters",
      "type": "string_too_long"
    }
  ]
}
```

## Implementation Details

### Schema Validation

The `TaskCreate` and `TaskUpdate` schemas in `app/schemas/task.py` include:

1. **Field constraints**: Using Pydantic's `Field` with `min_length` and `max_length`
2. **Custom validators**: Using `@field_validator` for whitespace checking
3. **Automatic trimming**: Whitespace is stripped from inputs

### Middleware Error Handling

The authentication middleware in `app/middleware/auth.py`:

1. Returns 401 for missing or invalid tokens
2. Returns 401 for malformed user IDs in tokens
3. Returns 403 for user ID mismatches
4. Returns 400 for invalid UUID formats in URLs

### Route Error Handling

All routes in `app/routes/tasks.py`:

1. Use consistent error helpers from `app/errors.py`
2. Validate user ownership before operations
3. Return 404 for non-existent resources
4. Rely on schema validation for input checking

## Testing

Comprehensive tests are available in:

- `test_error_handling.py`: Full test suite with pytest
- `test_error_simple2.py`: Simplified tests without pytest
- `test_task_endpoints.py`: Integration tests for all endpoints

Run tests:
```bash
python test_error_simple2.py
python test_task_endpoints.py
```

## Requirements Fulfilled

✅ **Requirement 11.1**: Global exception handler implemented
✅ **Requirement 11.2**: Title length validation (1-200 chars)
✅ **Requirement 11.3**: Description length validation (max 1000 chars)
✅ **Requirement 11.4**: Appropriate HTTP status codes (400, 401, 403, 404, 500)
✅ **Requirement 11.5**: Consistent error response format

## Security Considerations

1. **No sensitive data in errors**: Database errors return generic messages
2. **Detailed validation errors**: Help developers debug without exposing internals
3. **Consistent format**: Makes it easy for frontend to handle errors
4. **Proper status codes**: Enables correct client-side error handling

## Future Enhancements

Potential improvements for future iterations:

1. Rate limiting with 429 status codes
2. Request ID tracking for error correlation
3. Structured logging with error context
4. Custom error codes for specific business logic errors
5. Localization support for error messages
