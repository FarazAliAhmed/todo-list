"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from app.config import settings
from app.database import create_db_and_tables
from app.routes import tasks, chat
from app.exceptions import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="RESTful API for multi-user todo application with AI chatbot",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register global exception handlers
# Requirements: Requirement 11 (Error Handling and User Feedback)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)
app.include_router(chat.router)


@app.on_event("startup")
async def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()
    
    # Fix foreign key constraints
    import os
    from sqlalchemy import create_engine, text
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            # Drop foreign key constraints that prevent user-less operation
            conn.execute(text("ALTER TABLE IF EXISTS conversations DROP CONSTRAINT IF EXISTS conversations_user_id_fkey"))
            conn.execute(text("ALTER TABLE IF EXISTS messages DROP CONSTRAINT IF EXISTS messages_conversation_id_fkey"))
            conn.execute(text("ALTER TABLE IF EXISTS messages DROP CONSTRAINT IF EXISTS messages_user_id_fkey"))
            conn.execute(text("ALTER TABLE IF EXISTS tasks DROP CONSTRAINT IF EXISTS tasks_user_id_fkey"))
            conn.commit()
            print("✓ Foreign key constraints removed")
        engine.dispose()
    except Exception as e:
        print(f"Warning: Could not remove foreign keys: {e}")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns the status of the API.
    """
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "3.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Todo API - Phase III AI Chatbot",
        "version": "3.0.0",
        "docs": "/docs",
        "auth": "disabled",
        "features": ["tasks", "ai_chat"]
    }
