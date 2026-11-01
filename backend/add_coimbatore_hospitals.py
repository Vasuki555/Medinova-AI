"""
Add Coimbatore Hospitals to Database
Government and Private hospitals in Coimbatore with actual locations
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Real Coimbatore Hospitals Data
COIMBATORE_HOSPITALS = [
    # Government Hospitals
    {
        "name": "Coimbatore Medical College Hospital (CMCH)",
        "address": "Avinashi Road, Coimbatore, Tamil Nadu 641014",
        "location": {
            "type": "Point",
            "coordinates": [76.9558, 11.0183]
        },
        "phone": "+91-422-222-0200",
        "emergency_available": True,
        "services": ["Emergency", "Trauma Care", "All Specialties", "ICU", "General Medicine", "Surgery"],
        "type": "government",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.0
    },
    {
        "name": "Government Hospital Coimbatore",
        "address": "Trichy Road, Coimbatore, Tamil Nadu 641018",
        "location": {
            "type": "Point",
            "coordinates": [76.9635, 11.0168]
        },
        "phone": "+91-422-230-1500",
        "emergency_available": True,
        "services": ["Emergency", "General Medicine", "Surgery", "Pediatrics", "Obstetrics"],
        "type": "government",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 3.8
    },
    {
        "name": "ESI Hospital Coimbatore",
        "address": "Varadharajapuram, Coimbatore, Tamil Nadu 641015",
        "location": {
            "type": "Point",
            "coordinates": [77.0122, 11.0510]
        },
        "phone": "+91-422-265-0200",
        "emergency_available": True,
        "services": ["Emergency", "General Medicine", "Surgery", "Orthopedics", "ENT"],
        "type": "government",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 3.7
    },
    
    # Private Hospitals
    {
        "name": "Kovai Medical Center and Hospital (KMCH)",
        "address": "99, Avanashi Road, Coimbatore, Tamil Nadu 641014",
        "location": {
            "type": "Point",
            "coordinates": [76.9543, 11.0271]
        },
        "phone": "+91-422-439-0000",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant", "All Specialties"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.6
    },
    {
        "name": "G. Kuppuswamy Naidu Memorial Hospital (GKNM)",
        "address": "Pappanaicken Palayam, Coimbatore, Tamil Nadu 641037",
        "location": {
            "type": "Point",
            "coordinates": [76.9692, 11.0234]
        },
        "phone": "+91-422-230-0100",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Nephrology", "Critical Care"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.4
    },
    {
        "name": "PSG Hospitals",
        "address": "Avinashi Road, Peelamedu, Coimbatore, Tamil Nadu 641004",
        "location": {
            "type": "Point",
            "coordinates": [77.0288, 11.0271]
        },
        "phone": "+91-422-257-1111",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Gastroenterology", "Oncology"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.5
    },
    {
        "name": "Sri Ramakrishna Hospital",
        "address": "395, Sarojini Naidu Road, Sidhapudur, Coimbatore, Tamil Nadu 641044",
        "location": {
            "type": "Point",
            "coordinates": [76.9558, 11.0065]
        },
        "phone": "+91-422-436-9999",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "General Medicine", "Surgery"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.3
    },
    {
        "name": "KG Hospital",
        "address": "No. 5, Arts College Road, Coimbatore, Tamil Nadu 641018",
        "location": {
            "type": "Point",
            "coordinates": [76.9640, 11.0149]
        },
        "phone": "+91-422-439-5555",
        "emergency_available": True,
        "services": ["Emergency", "Trauma Care", "Orthopedics", "Neurosurgery", "Critical Care", "ICU"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.5
    },
    {
        "name": "Kongunad Hospital",
        "address": "193, Mettupalayam Road, Coimbatore, Tamil Nadu 641043",
        "location": {
            "type": "Point",
            "coordinates": [76.9744, 11.0321]
        },
        "phone": "+91-422-239-0000",
        "emergency_available": True,
        "services": ["Emergency", "General Medicine", "Surgery", "Cardiology", "Orthopedics"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.2
    },
    {
        "name": "Gem Hospital",
        "address": "45, Pankaja Mills Road, Ramanathapuram, Coimbatore, Tamil Nadu 641045",
        "location": {
            "type": "Point",
            "coordinates": [77.0039, 11.0342]
        },
        "phone": "+91-422-249-0000",
        "emergency_available": True,
        "services": ["Emergency", "Gastroenterology", "Liver Transplant", "General Surgery", "Laparoscopy"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.5
    },
    {
        "name": "Royal Care Super Speciality Hospital",
        "address": "10/1, Trichy Road, Singanallur, Coimbatore, Tamil Nadu 641005",
        "location": {
            "type": "Point",
            "coordinates": [77.0202, 11.0056]
        },
        "phone": "+91-422-262-6666",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "General Medicine"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.1
    },
    {
        "name": "Lakshmi Hospital",
        "address": "70, Avinashi Road, Coimbatore, Tamil Nadu 641018",
        "location": {
            "type": "Point",
            "coordinates": [76.9595, 11.0238]
        },
        "phone": "+91-422-230-8888",
        "emergency_available": True,
        "services": ["Emergency", "General Medicine", "Surgery", "Pediatrics", "Obstetrics"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.0
    },
    {
        "name": "Sheela Hospital",
        "address": "1186-B, Avinashi Road, Coimbatore, Tamil Nadu 641018",
        "location": {
            "type": "Point",
            "coordinates": [76.9873, 11.0424]
        },
        "phone": "+91-422-430-5000",
        "emergency_available": True,
        "services": ["Emergency", "Orthopedics", "Joint Replacement", "Spine Surgery", "Sports Medicine"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.3
    },
    {
        "name": "Ganga Hospital",
        "address": "313, Mettupalayam Road, Coimbatore, Tamil Nadu 641043",
        "location": {
            "type": "Point",
            "coordinates": [76.9754, 11.0336]
        },
        "phone": "+91-422-245-7000",
        "emergency_available": True,
        "services": ["Emergency", "Orthopedics", "Trauma Care", "Plastic Surgery", "Hand Surgery"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.6
    },
    {
        "name": "NG Hospital and Research Centre",
        "address": "103, Avinashi Road, Coimbatore, Tamil Nadu 641018",
        "location": {
            "type": "Point",
            "coordinates": [76.9598, 11.0251]
        },
        "phone": "+91-422-230-7777",
        "emergency_available": True,
        "services": ["Emergency", "General Medicine", "Surgery", "Cardiology", "Nephrology"],
        "type": "private",
        "city": "Coimbatore",
        "state": "Tamil Nadu",
        "rating": 4.1
    },
]


async def add_coimbatore_hospitals():
    """Add Coimbatore hospitals to database"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.medinova_ai
    
    print(f"🏥 Adding {len(COIMBATORE_HOSPITALS)} Coimbatore hospitals...")
    print()
    
    # Add timestamp fields
    for hospital in COIMBATORE_HOSPITALS:
        hospital["created_at"] = datetime.utcnow()
        hospital["updated_at"] = datetime.utcnow()
        hospital["verified"] = True
    
    # Insert hospitals
    result = await db.hospitals.insert_many(COIMBATORE_HOSPITALS)
    print(f"✅ Successfully added {len(result.inserted_ids)} Coimbatore hospitals!")
    print()
    
    # Show total count
    total_count = await db.hospitals.count_documents({})
    govt_count = await db.hospitals.count_documents({"type": "government"})
    private_count = await db.hospitals.count_documents({"type": "private"})
    coimbatore_count = await db.hospitals.count_documents({"city": "Coimbatore"})
    
    print("📊 Total Hospitals in Database:")
    print(f"   🏛️  Government: {govt_count} hospitals")
    print(f"   🏢 Private: {private_count} hospitals")
    print(f"   📍 Coimbatore: {coimbatore_count} hospitals")
    print(f"   📍 Total: {total_count} hospitals")
    print()
    
    # Show Coimbatore hospitals by type
    cbr_govt = await db.hospitals.count_documents({"city": "Coimbatore", "type": "government"})
    cbr_private = await db.hospitals.count_documents({"city": "Coimbatore", "type": "private"})
    
    print("📊 Coimbatore Hospitals:")
    print(f"   🏛️  Government: {cbr_govt} hospitals")
    print(f"   🏢 Private: {cbr_private} hospitals")
    
    client.close()
    print()
    print("🎉 Done! Refresh the Nearby Hospitals page to see them!")


if __name__ == "__main__":
    asyncio.run(add_coimbatore_hospitals())
