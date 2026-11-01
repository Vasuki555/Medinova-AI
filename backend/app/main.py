"""
MediNova AI - FastAPI Main Application
Entry point for the FastAPI backend server
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import Database
from app.core.logging import setup_logging
from app.api.v1 import api_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Create uploads directory
    upload_path = settings.upload_dir_path
    os.makedirs(upload_path, exist_ok=True)
    logger.info(f"Upload directory ready: {upload_path}")
    
    # Connect to MongoDB
    await Database.connect_to_database()
    
    # Create database indexes
    from app.core.indexes import create_indexes
    await create_indexes(Database.get_database())
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await Database.close_database_connection()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
logger.info(f"Configuring CORS with origins: {settings.cors_origins_list}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"] if settings.CORS_ALLOW_METHODS == "*" else settings.CORS_ALLOW_METHODS.split(","),
    allow_headers=["*"] if settings.CORS_ALLOW_HEADERS == "*" else settings.CORS_ALLOW_HEADERS.split(","),
)

# Setup rate limiting
if settings.RATE_LIMIT_ENABLED:
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from app.core.rate_limit import limiter, rate_limit_exceeded_handler
    
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    logger.info("Rate limiting middleware enabled")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve uploaded files as static assets
# Ensure directory exists before mounting (for cases where main runs before lifespan)
_upload_path = settings.upload_dir_path
os.makedirs(_upload_path, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=_upload_path), name="uploads")


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    Returns basic API information
    """
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

