"""
Hospital Service
Business logic for government hospital finder using Geospatial indexes
"""

import math
from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from app.services.google_places_service import google_places_service

class HospitalService:
    """Service for searching hospitals and clinics"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.hospitals_collection = db.hospitals

    def _haversine_distance(self, lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """Calculate the great circle distance between two points on the earth in km"""
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return round(c * r, 2)

    async def get_nearby_hospitals(self, latitude: float, longitude: float, radius_km: float = 10.0, use_google_places: bool = True) -> List[Dict[str, Any]]:
        """
        Locate nearby hospitals (government and private).
        Combines MongoDB database hospitals with Google Places API results.
        """
        nearby_hospitals = []
        
        # 1. Get hospitals from our database
        try:
            # Try MongoDB geospatial query - updated to match our schema
            # Our schema has "location.coordinates" not "address.location.coordinates"
            cursor = self.hospitals_collection.find({
                "location": {
                    "$nearSphere": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [longitude, latitude]
                        },
                        "$maxDistance": radius_km * 1000  # meters
                    }
                }
            })
            
            results = await cursor.to_list(200)
            for doc in results:
                doc["id"] = str(doc["_id"])
                doc.pop("_id", None)
                if doc.get("location", {}).get("coordinates"):
                    doc_lon, doc_lat = doc["location"]["coordinates"]
                    doc["distance_km"] = self._haversine_distance(longitude, latitude, doc_lon, doc_lat)
                doc["source"] = "database"
                nearby_hospitals.append(doc)
                
        except Exception as e:
            logging.error(f"Geospatial query failed: {e}, falling back to manual distance calc")
            # Fallback: retrieve all hospitals and calculate distances manually
            hospitals = await self.hospitals_collection.find({}).to_list(500)
            
            for doc in hospitals:
                doc["id"] = str(doc["_id"])
                doc.pop("_id", None)
                
                if doc.get("location", {}).get("coordinates"):
                    coordinates = doc["location"]["coordinates"]
                    doc_lon, doc_lat = coordinates[0], coordinates[1]
                    distance = self._haversine_distance(longitude, latitude, doc_lon, doc_lat)
                    
                    if distance <= radius_km:
                        doc["distance_km"] = distance
                        doc["source"] = "database"
                        nearby_hospitals.append(doc)
        
        # 2. Get hospitals from Google Places API
        if use_google_places:
            try:
                google_hospitals = google_places_service.search_nearby_hospitals(
                    latitude=latitude,
                    longitude=longitude,
                    radius_meters=int(radius_km * 1000),
                    include_clinics=True
                )
                
                # Filter by radius and add to results
                for hospital in google_hospitals:
                    if hospital.get("distance_km", 999) <= radius_km:
                        # Add unique ID for Google Places hospitals
                        hospital["id"] = hospital.get("place_id", f"google_{len(nearby_hospitals)}")
                        nearby_hospitals.append(hospital)
                
                logging.info(f"Added {len(google_hospitals)} hospitals from Google Places API")
                
            except Exception as e:
                logging.error(f"Error fetching Google Places hospitals: {e}")
        
        # Sort all hospitals by distance
        nearby_hospitals.sort(key=lambda x: x.get("distance_km", 999))
        
        logging.info(f"Total hospitals found: {len(nearby_hospitals)} (DB + Google Places)")
        return nearby_hospitals

    async def create_hospital(self, hospital_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a government hospital record into the DB"""
        hospital_data["created_at"] = datetime.utcnow()
        hospital_data["updated_at"] = datetime.utcnow()
        
        result = await self.hospitals_collection.insert_one(hospital_data)
        created = await self.hospitals_collection.find_one({"_id": result.inserted_id})
        created["id"] = str(created["_id"])
        return created
