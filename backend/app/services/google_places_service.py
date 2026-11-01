"""
Google Places API service for fetching nearby hospitals
"""
import requests
import os
from typing import List, Dict, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GooglePlacesService:
    """Service for interacting with Google Places API"""
    
    BASE_URL = "https://maps.googleapis.com/maps/api/place"
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key or self.api_key == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
            logger.warning("Google Maps API key not configured")
    
    def search_nearby_hospitals(
        self,
        latitude: float,
        longitude: float,
        radius_meters: int = 50000,  # 50km default
        include_clinics: bool = True
    ) -> List[Dict]:
        """
        Search for hospitals near a location using Google Places API
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            radius_meters: Search radius in meters (max 50000)
            include_clinics: Include clinics and health facilities
            
        Returns:
            List of hospital dictionaries with standardized format
        """
        if not self.api_key or self.api_key == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
            logger.error("Google Maps API key not configured")
            return []
        
        # Limit radius to Google's maximum
        radius_meters = min(radius_meters, 50000)
        
        try:
            # Search for hospitals
            hospitals = self._search_places(
                latitude, longitude, radius_meters, "hospital"
            )
            
            # Optionally include clinics and health centers
            if include_clinics:
                clinics = self._search_places(
                    latitude, longitude, radius_meters, "doctor"
                )
                hospitals.extend(clinics)
            
            # Convert to our standard format
            standardized = []
            for place in hospitals:
                hospital_data = self._convert_to_hospital_format(
                    place, latitude, longitude
                )
                if hospital_data:
                    standardized.append(hospital_data)
            
            # Remove duplicates based on place_id
            seen_ids = set()
            unique_hospitals = []
            for hospital in standardized:
                place_id = hospital.get("place_id")
                if place_id and place_id not in seen_ids:
                    seen_ids.add(place_id)
                    unique_hospitals.append(hospital)
            
            logger.info(f"Found {len(unique_hospitals)} hospitals from Google Places API")
            return unique_hospitals
            
        except Exception as e:
            logger.error(f"Error fetching hospitals from Google Places: {str(e)}")
            return []
    
    def _search_places(
        self,
        latitude: float,
        longitude: float,
        radius: int,
        place_type: str
    ) -> List[Dict]:
        """Search Google Places API for a specific type"""
        url = f"{self.BASE_URL}/nearbysearch/json"
        
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "type": place_type,
            "key": self.api_key
        }
        
        all_results = []
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK" and data.get("status") != "ZERO_RESULTS":
                logger.error(f"Google Places API error: {data.get('status')} - {data.get('error_message', '')}")
                return []
            
            all_results.extend(data.get("results", []))
            
            # Handle pagination (up to 60 results total)
            next_page_token = data.get("next_page_token")
            attempts = 0
            while next_page_token and attempts < 2:  # Max 3 pages = 60 results
                # Need to wait a bit for next_page_token to become valid
                import time
                time.sleep(2)
                
                next_params = {
                    "pagetoken": next_page_token,
                    "key": self.api_key
                }
                
                response = requests.get(url, params=next_params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "OK":
                    all_results.extend(data.get("results", []))
                    next_page_token = data.get("next_page_token")
                else:
                    break
                
                attempts += 1
            
            return all_results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error in Google Places API: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Google Places search: {str(e)}")
            return []
    
    def _convert_to_hospital_format(
        self,
        place: Dict,
        user_lat: float,
        user_lon: float
    ) -> Optional[Dict]:
        """Convert Google Places result to our hospital format"""
        try:
            from math import radians, sin, cos, sqrt, atan2
            
            # Extract location
            location = place.get("geometry", {}).get("location", {})
            lat = location.get("lat")
            lon = location.get("lng")
            
            if not lat or not lon:
                return None
            
            # Calculate distance using Haversine formula
            R = 6371  # Earth's radius in km
            
            lat1, lon1 = radians(user_lat), radians(user_lon)
            lat2, lon2 = radians(lat), radians(lon)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance_km = R * c
            
            # Determine hospital type
            types = place.get("types", [])
            is_hospital = "hospital" in types
            hospital_type = "Government" if "hospital" in types else "Private"
            
            # Check if currently open
            opening_hours = place.get("opening_hours", {})
            is_open = opening_hours.get("open_now", False)
            
            # Build hospital object
            hospital = {
                "place_id": place.get("place_id"),
                "name": place.get("name"),
                "address": place.get("vicinity", "Address not available"),
                "location": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "phone": place.get("formatted_phone_number", "Not available"),
                "rating": place.get("rating", 0.0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "emergency_available": is_hospital,  # Hospitals likely have emergency
                "type": hospital_type,
                "services": types,
                "is_open": is_open,
                "distance_km": round(distance_km, 2),
                "source": "google_places"
            }
            
            return hospital
            
        except Exception as e:
            logger.error(f"Error converting place to hospital format: {str(e)}")
            return None


# Singleton instance
google_places_service = GooglePlacesService()
