"""
Hospitals Router
FastAPI endpoints for nearby government hospital locators
"""

import logging
from typing import List
from fastapi import APIRouter, Depends, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.core.dependencies import get_current_user, require_admin
from app.schemas.hospital import HospitalCreate, HospitalResponse
from app.services.hospital_service import HospitalService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

@router.get("/nearby", response_model=List[HospitalResponse])
async def get_nearby_govt_hospitals(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Latitude of user current location"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Longitude of user current location"),
    radius_km: float = Query(10.0, ge=0.1, le=100.0, description="Radius range in kilometers"),
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Find nearby government hospitals based on location coordinates"""
    logger.info(f"🏥 Hospitals API called - Location: ({latitude}, {longitude}), Radius: {radius_km}km")
    try:
        service = HospitalService(db)
        hospitals = await service.get_nearby_hospitals(latitude, longitude, radius_km)
        logger.info(f"✅ Found {len(hospitals)} hospitals")
        return hospitals
    except Exception as e:
        logger.error(f"❌ Error fetching hospitals: {e}", exc_info=True)
        raise

@router.post("", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
async def add_hospital(
    data: HospitalCreate,
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Add a new government hospital profile (admins only)"""
    service = HospitalService(db)
    hospital = await service.create_hospital(data.dict())
    return hospital
