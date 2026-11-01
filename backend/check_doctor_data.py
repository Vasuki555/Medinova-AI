"""
Check doctor profile data for null license_numbers
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import certifi

async def check_doctors():
    print("Checking doctor profiles...")
    
    client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )
    await client.admin.command("ping")
    db = client[settings.MONGODB_DB_NAME]
    
    # Find doctors with null license_number
    docs = await db.doctor_profiles.find({"license_number": None}).to_list(100)
    print(f"Found {len(docs)} doctors with null license_number")
    
    # Find doctors with non-null license_number  
    docs2 = await db.doctor_profiles.find({"license_number": {"$ne": None}}).to_list(100)
    print(f"Found {len(docs2)} doctors with non-null license_number")
    
    # Count total
    total = await db.doctor_profiles.count_documents({})
    print(f"Total doctor profiles: {total}")
    
    # Show first few
    if docs:
        print("\nDoctors with null license:")
        for doc in docs[:3]:
            print(f"  - user_id: {doc['user_id']}, license: {doc.get('license_number')}")
    
    if docs2:
        print("\nDoctors with license:")
        for doc in docs2[:3]:
            print(f"  - user_id: {doc['user_id']}, license: {doc.get('license_number')}")
    
    client.close()

asyncio.run(check_doctors())
