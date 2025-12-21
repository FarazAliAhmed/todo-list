"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
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
    description="RESTful API for multi-user todo application",
    version="2.0.0",
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


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns the status of the API.
    """
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "2.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Todo API",
        "version": "2.0.1",
        "docs": "/docs",
        "auth": "disabled"
    }
