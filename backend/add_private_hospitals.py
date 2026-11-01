"""
Add Real Private Hospitals to Database
Major private hospitals in Indian cities with actual locations
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Real Private Hospitals Data with actual locations
PRIVATE_HOSPITALS_DATA = [
    # Chennai Private Hospitals
    {
        "name": "Apollo Hospitals Greams Road",
        "address": "21, Greams Lane, Off Greams Road, Chennai, Tamil Nadu 600006",
        "location": {
            "type": "Point",
            "coordinates": [80.2503, 13.0569]
        },
        "phone": "+91-44-2829-3333",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "rating": 4.5
    },
    {
        "name": "Fortis Malar Hospital",
        "address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai, Tamil Nadu 600020",
        "location": {
            "type": "Point",
            "coordinates": [80.2571, 13.0067]
        },
        "phone": "+91-44-4289-2222",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Cardiac Surgery", "Neurology", "Orthopedics", "ICU"],
        "type": "private",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "rating": 4.3
    },
    {
        "name": "MIOT International Hospital",
        "address": "4/112, Mount Poonamallee Road, Manapakkam, Chennai, Tamil Nadu 600089",
        "location": {
            "type": "Point",
            "coordinates": [80.1614, 13.0297]
        },
        "phone": "+91-44-2249-2288",
        "emergency_available": True,
        "services": ["Emergency", "Orthopedics", "Joint Replacement", "Spine Surgery", "Cardiology"],
        "type": "private",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "rating": 4.4
    },
    {
        "name": "Kauvery Hospital Chennai",
        "address": "81, TTK Road, Alwarpet, Chennai, Tamil Nadu 600018",
        "location": {
            "type": "Point",
            "coordinates": [80.2533, 13.0338]
        },
        "phone": "+91-44-4000-6000",
        "emergency_available": True,
        "services": ["Emergency", "Critical Care", "Cardiology", "Neurology", "Gastroenterology"],
        "type": "private",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "rating": 4.2
    },
    {
        "name": "Gleneagles Global Health City",
        "address": "439, Cheran Nagar, Perumbakkam, Chennai, Tamil Nadu 600100",
        "location": {
            "type": "Point",
            "coordinates": [80.2249, 12.9099]
        },
        "phone": "+91-44-4400-2500",
        "emergency_available": True,
        "services": ["Emergency", "Transplant", "Oncology", "Cardiology", "Neurology", "Orthopedics"],
        "type": "private",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "rating": 4.6
    },
    
    # Bangalore Private Hospitals
    {
        "name": "Manipal Hospital Bangalore",
        "address": "98, HAL Airport Road, Bangalore, Karnataka 560017",
        "location": {
            "type": "Point",
            "coordinates": [77.6408, 12.9570]
        },
        "phone": "+91-80-2502-4444",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology", "Transplant"],
        "type": "private",
        "city": "Bangalore",
        "state": "Karnataka",
        "rating": 4.5
    },
    {
        "name": "Fortis Hospital Bangalore",
        "address": "154/9, Bannerghatta Road, Bangalore, Karnataka 560076",
        "location": {
            "type": "Point",
            "coordinates": [77.6050, 12.8996]
        },
        "phone": "+91-80-6621-4444",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Orthopedics", "Neurology", "Oncology"],
        "type": "private",
        "city": "Bangalore",
        "state": "Karnataka",
        "rating": 4.3
    },
    {
        "name": "Apollo Hospitals Bangalore",
        "address": "154/11, Bannerghatta Road, Bangalore, Karnataka 560076",
        "location": {
            "type": "Point",
            "coordinates": [77.6061, 12.9012]
        },
        "phone": "+91-80-2630-2630",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "Bangalore",
        "state": "Karnataka",
        "rating": 4.6
    },
    {
        "name": "Narayana Health City",
        "address": "258/A, Bommasandra Industrial Area, Bangalore, Karnataka 560099",
        "location": {
            "type": "Point",
            "coordinates": [77.7389, 12.8628]
        },
        "phone": "+91-80-7122-2222",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Cardiac Surgery", "Neurology", "Orthopedics", "Pediatrics"],
        "type": "private",
        "city": "Bangalore",
        "state": "Karnataka",
        "rating": 4.4
    },
    {
        "name": "Columbia Asia Hospital Whitefield",
        "address": "Survey No. 10P & 12P, Ramagondanahalli, Whitefield, Bangalore, Karnataka 560066",
        "location": {
            "type": "Point",
            "coordinates": [77.7499, 12.9899]
        },
        "phone": "+91-80-6797-6797",
        "emergency_available": True,
        "services": ["Emergency", "General Medicine", "Surgery", "Orthopedics", "Pediatrics"],
        "type": "private",
        "city": "Bangalore",
        "state": "Karnataka",
        "rating": 4.2
    },
    
    # Delhi/NCR Private Hospitals
    {
        "name": "Apollo Hospitals New Delhi",
        "address": "Sarita Vihar, New Delhi 110076",
        "location": {
            "type": "Point",
            "coordinates": [77.2892, 28.5355]
        },
        "phone": "+91-11-2692-5858",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "New Delhi",
        "state": "Delhi",
        "rating": 4.5
    },
    {
        "name": "Max Super Speciality Hospital Saket",
        "address": "1, Press Enclave Road, Saket, New Delhi 110017",
        "location": {
            "type": "Point",
            "coordinates": [77.2167, 28.5244]
        },
        "phone": "+91-11-2651-5050",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Critical Care"],
        "type": "private",
        "city": "New Delhi",
        "state": "Delhi",
        "rating": 4.6
    },
    {
        "name": "Fortis Escorts Heart Institute",
        "address": "Okhla Road, New Delhi 110025",
        "location": {
            "type": "Point",
            "coordinates": [77.2707, 28.5707]
        },
        "phone": "+91-11-4713-5000",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Cardiac Surgery", "Interventional Cardiology", "ICU"],
        "type": "private",
        "city": "New Delhi",
        "state": "Delhi",
        "rating": 4.4
    },
    {
        "name": "Medanta - The Medicity",
        "address": "Sector 38, Gurgaon, Haryana 122001",
        "location": {
            "type": "Point",
            "coordinates": [77.0638, 28.4353]
        },
        "phone": "+91-124-414-1414",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Transplant", "All Specialties"],
        "type": "private",
        "city": "Gurgaon",
        "state": "Haryana",
        "rating": 4.7
    },
    
    # Mumbai Private Hospitals
    {
        "name": "Lilavati Hospital and Research Centre",
        "address": "A-791, Bandra Reclamation, Bandra West, Mumbai, Maharashtra 400050",
        "location": {
            "type": "Point",
            "coordinates": [72.8199, 19.0521]
        },
        "phone": "+91-22-2640-0000",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology", "Critical Care"],
        "type": "private",
        "city": "Mumbai",
        "state": "Maharashtra",
        "rating": 4.5
    },
    {
        "name": "Breach Candy Hospital",
        "address": "60-A, Bhulabhai Desai Road, Mumbai, Maharashtra 400026",
        "location": {
            "type": "Point",
            "coordinates": [72.8049, 18.9645]
        },
        "phone": "+91-22-2367-7888",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "General Medicine"],
        "type": "private",
        "city": "Mumbai",
        "state": "Maharashtra",
        "rating": 4.4
    },
    {
        "name": "Kokilaben Dhirubhai Ambani Hospital",
        "address": "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows, Andheri West, Mumbai, Maharashtra 400053",
        "location": {
            "type": "Point",
            "coordinates": [72.8263, 19.1334]
        },
        "phone": "+91-22-3063-8888",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "Mumbai",
        "state": "Maharashtra",
        "rating": 4.7
    },
    {
        "name": "Nanavati Super Speciality Hospital",
        "address": "S.V. Road, Vile Parle West, Mumbai, Maharashtra 400056",
        "location": {
            "type": "Point",
            "coordinates": [72.8421, 19.1026]
        },
        "phone": "+91-22-2626-7500",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology", "Critical Care"],
        "type": "private",
        "city": "Mumbai",
        "state": "Maharashtra",
        "rating": 4.5
    },
    
    # Hyderabad Private Hospitals
    {
        "name": "Apollo Hospitals Jubilee Hills",
        "address": "Road No. 72, Film Nagar, Jubilee Hills, Hyderabad, Telangana 500096",
        "location": {
            "type": "Point",
            "coordinates": [78.4183, 17.4239]
        },
        "phone": "+91-40-2360-7777",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "Hyderabad",
        "state": "Telangana",
        "rating": 4.6
    },
    {
        "name": "KIMS Hospital Secunderabad",
        "address": "1-8-31/1, Minister Road, Secunderabad, Telangana 500003",
        "location": {
            "type": "Point",
            "coordinates": [78.5018, 17.4399]
        },
        "phone": "+91-40-4455-5000",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology", "Critical Care"],
        "type": "private",
        "city": "Hyderabad",
        "state": "Telangana",
        "rating": 4.4
    },
    {
        "name": "Yashoda Hospitals Somajiguda",
        "address": "Raj Bhavan Road, Somajiguda, Hyderabad, Telangana 500082",
        "location": {
            "type": "Point",
            "coordinates": [78.4583, 17.4239]
        },
        "phone": "+91-40-2337-7777",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Gastroenterology"],
        "type": "private",
        "city": "Hyderabad",
        "state": "Telangana",
        "rating": 4.3
    },
    
    # Kolkata Private Hospitals
    {
        "name": "Apollo Gleneagles Hospitals Kolkata",
        "address": "58, Canal Circular Road, Kolkata, West Bengal 700054",
        "location": {
            "type": "Point",
            "coordinates": [88.3839, 22.5244]
        },
        "phone": "+91-33-2320-2122",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "Kolkata",
        "state": "West Bengal",
        "rating": 4.5
    },
    {
        "name": "Fortis Hospital Kolkata",
        "address": "730, Anandapur, EM Bypass Road, Kolkata, West Bengal 700107",
        "location": {
            "type": "Point",
            "coordinates": [88.4045, 22.5058]
        },
        "phone": "+91-33-6628-4444",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology", "Critical Care"],
        "type": "private",
        "city": "Kolkata",
        "state": "West Bengal",
        "rating": 4.4
    },
    
    # Pune Private Hospitals
    {
        "name": "Ruby Hall Clinic Pune",
        "address": "40, Sassoon Road, Pune, Maharashtra 411001",
        "location": {
            "type": "Point",
            "coordinates": [73.8567, 18.5314]
        },
        "phone": "+91-20-6645-8888",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Oncology", "Critical Care"],
        "type": "private",
        "city": "Pune",
        "state": "Maharashtra",
        "rating": 4.5
    },
    {
        "name": "Sahyadri Super Speciality Hospital",
        "address": "30-C, Erandawane, Karve Road, Pune, Maharashtra 411004",
        "location": {
            "type": "Point",
            "coordinates": [73.8286, 18.5089]
        },
        "phone": "+91-20-6745-4545",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "General Medicine"],
        "type": "private",
        "city": "Pune",
        "state": "Maharashtra",
        "rating": 4.3
    },
    
    # Ahmedabad Private Hospitals
    {
        "name": "Apollo Hospitals Ahmedabad",
        "address": "Plot No. 1A, GIDC Estate, Bhat, Gandhinagar, Gujarat 382428",
        "location": {
            "type": "Point",
            "coordinates": [72.6369, 23.1248]
        },
        "phone": "+91-79-3051-0000",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Oncology", "Orthopedics", "Transplant"],
        "type": "private",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "rating": 4.5
    },
    {
        "name": "Sterling Hospital Ahmedabad",
        "address": "Gurukul Road, Memnagar, Ahmedabad, Gujarat 380052",
        "location": {
            "type": "Point",
            "coordinates": [72.5214, 23.0393]
        },
        "phone": "+91-79-6677-0000",
        "emergency_available": True,
        "services": ["Emergency", "Cardiology", "Neurology", "Orthopedics", "Critical Care"],
        "type": "private",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "rating": 4.4
    },
]


async def add_private_hospitals():
    """Add private hospitals to database"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.medinova_ai
    
    print(f"🏥 Adding {len(PRIVATE_HOSPITALS_DATA)} real private hospitals...")
    print()
    
    # Add timestamp fields
    for hospital in PRIVATE_HOSPITALS_DATA:
        hospital["created_at"] = datetime.utcnow()
        hospital["updated_at"] = datetime.utcnow()
        hospital["verified"] = True
    
    # Insert hospitals
    result = await db.hospitals.insert_many(PRIVATE_HOSPITALS_DATA)
    print(f"✅ Successfully added {len(result.inserted_ids)} private hospitals!")
    print()
    
    # Show total count
    total_count = await db.hospitals.count_documents({})
    govt_count = await db.hospitals.count_documents({"type": "government"})
    private_count = await db.hospitals.count_documents({"type": "private"})
    
    print("📊 Total Hospitals in Database:")
    print(f"   🏛️  Government: {govt_count} hospitals")
    print(f"   🏢 Private: {private_count} hospitals")
    print(f"   📍 Total: {total_count} hospitals")
    print()
    
    # Show summary by city
    cities = {}
    for h in PRIVATE_HOSPITALS_DATA:
        city = h["city"]
        cities[city] = cities.get(city, 0) + 1
    
    print("📊 Private Hospitals by City:")
    for city, count in sorted(cities.items()):
        print(f"   {city}: {count} hospitals")
    
    client.close()
    print()
    print("🎉 Done! Now you have both government and private hospitals!")


if __name__ == "__main__":
    asyncio.run(add_private_hospitals())
