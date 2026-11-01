"""
Fix doctor profiles with null license_number
Set them to PENDING-{user_id} pattern
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import certifi

async def fix_null_licenses():
    print("="*80)
    print("FIXING NULL LICENSE NUMBERS")
    print("="*80)
    
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
    print(f"\nFound {len(docs)} doctors with null license_number")
    
    for doc in docs:
        user_id = doc['user_id']
        new_license = f"PENDING-{user_id[-6:]}"
        
        print(f"  Updating user_id {user_id}...")
        print(f"    Old: null")
        print(f"    New: {new_license}")
        
        result = await db.doctor_profiles.update_one(
            {"_id": doc["_id"]},
            {"$set": {"license_number": new_license}}
        )
        print(f"    ✓ Updated: {result.modified_count} document")
    
    # Verify
    remaining = await db.doctor_profiles.count_documents({"license_number": None})
    print(f"\nRemaining doctors with null license: {remaining}")
    
    if remaining == 0:
        print("✓ All null licenses fixed!")
    
    client.close()
    print("="*80)

asyncio.run(fix_null_licenses())
