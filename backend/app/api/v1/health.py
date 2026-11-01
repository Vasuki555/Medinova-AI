"""
Health Check Endpoint
Provides system health status and database connectivity check
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from app.config import settings
from app.database import Database

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: datetime
    database_connected: bool


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API and database are running properly"
)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        - status: Overall system status
        - app_name: Application name
        - version: Application version
        - environment: Current environment (development/production)
        - timestamp: Current server time
        - database_connected: MongoDB connection status
    """
    
    # Check database connection
    db_connected = await Database.check_connection()
    
    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.utcnow(),
        database_connected=db_connected
    )
