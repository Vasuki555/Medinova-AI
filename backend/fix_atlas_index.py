"""
Fix MongoDB Atlas Index - Force Recreation
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import certifi

async def fix_atlas_index():
    print("="*80)
    print("FIXING MONGODB ATLAS LICENSE_NUMBER INDEX")
    print("="*80)
    
    # Connect to Atlas
    print("\n[1] Connecting to MongoDB Atlas...")
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000
        )
        await client.admin.command("ping")
        db = client[settings.MONGODB_DB_NAME]
        print("    ✓ Connected successfully")
    except Exception as e:
        print(f"    ✗ Connection failed: {e}")
        return
    
    # List current indexes
    print("\n[2] Current indexes on doctor_profiles:")
    try:
        indexes = await db.doctor_profiles.list_indexes().to_list(100)
        for idx in indexes:
            print(f"    {idx}")
    except Exception as e:
        print(f"    Error: {e}")
    
    # Drop the problematic index
    print("\n[3] Dropping license_number_1 index...")
    try:
        result = await db.doctor_profiles.drop_index("license_number_1")
        print(f"    ✓ Index dropped: {result}")
    except Exception as e:
        print(f"    Note: {e}")
    
    # Recreate with correct settings
    print("\n[4] Creating license_number index with sparse=True...")
    try:
        result = await db.doctor_profiles.create_index(
            [("license_number", 1)],
            unique=True,
            sparse=True,
            name="license_number_1"
        )
        print(f"    ✓ Index created: {result}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    # Verify
    print("\n[5] Verifying final index configuration...")
    try:
        indexes = await db.doctor_profiles.list_indexes().to_list(100)
        for idx in indexes:
            if 'license_number' in idx.get('key', {}):
                print(f"    License index: {idx.get('name')}")
                print(f"      - unique: {idx.get('unique', False)}")
                print(f"      - sparse: {idx.get('sparse', False)}")
                if idx.get('unique') and idx.get('sparse'):
                    print("      ✓ INDEX IS CORRECT")
                else:
                    print("      ✗ INDEX STILL INCORRECT")
    except Exception as e:
        print(f"    Error: {e}")
    
    client.close()
    print("\n" + "="*80)
    print("INDEX FIX COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(fix_atlas_index())
