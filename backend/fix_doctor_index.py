"""
Fix Doctor Profile Index Issue
Removes incorrect license_number index and recreates with sparse=True
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def inspect_and_fix_indexes():
    print("="*80)
    print("DOCTOR PROFILE INDEX FIX")
    print("="*80)
    
    # Connect to MongoDB
    print("\n[1] Connecting to MongoDB...")
    try:
        import certifi
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        await client.admin.command("ping")
        db = client[settings.MONGODB_DB_NAME]
        print("    ✓ Connected to MongoDB Atlas")
    except Exception as e:
        print(f"    ✗ Failed to connect to MongoDB Atlas: {e}")
        print("    Using mongomock for testing...")
        import mongomock
        mock_client = mongomock.MongoClient()
        db = mock_client[settings.MONGODB_DB_NAME]
        client = None
    
    # Inspect current indexes
    print("\n[2] Inspecting current doctor_profiles indexes...")
    try:
        if client:
            indexes = await db.doctor_profiles.list_indexes().to_list(100)
        else:
            indexes = list(db.doctor_profiles.list_indexes())
        
        print(f"    Found {len(indexes)} indexes:")
        for idx in indexes:
            idx_name = idx.get('name', 'unknown')
            idx_key = idx.get('key', {})
            idx_unique = idx.get('unique', False)
            idx_sparse = idx.get('sparse', False)
            print(f"      - {idx_name}: key={idx_key}, unique={idx_unique}, sparse={idx_sparse}")
            
    except Exception as e:
        print(f"    ✗ Error listing indexes: {e}")
        indexes = []
    
    # Check if problematic index exists
    license_index = None
    for idx in indexes:
        if 'license_number' in idx.get('key', {}):
            license_index = idx
            break
    
    if license_index:
        idx_name = license_index.get('name')
        is_sparse = license_index.get('sparse', False)
        is_unique = license_index.get('unique', False)
        
        print(f"\n[3] Found license_number index: {idx_name}")
        print(f"    Unique: {is_unique}, Sparse: {is_sparse}")
        
        if is_unique and not is_sparse:
            print("    ⚠ INDEX IS INCORRECT - unique but not sparse")
            print(f"    Dropping index: {idx_name}...")
            
            try:
                if client:
                    await db.doctor_profiles.drop_index(idx_name)
                else:
                    db.doctor_profiles.drop_index(idx_name)
                print(f"    ✓ Dropped index: {idx_name}")
            except Exception as e:
                print(f"    ✗ Error dropping index: {e}")
        else:
            print("    ✓ Index is correct (sparse=True)")
            print("    No changes needed")
            if client:
                client.close()
            return
    else:
        print("\n[3] No license_number index found")
    
    # Create correct index
    print("\n[4] Creating correct license_number index...")
    try:
        if client:
            result = await db.doctor_profiles.create_index(
                "license_number",
                unique=True,
                sparse=True,
                name="license_number_1"
            )
        else:
            result = db.doctor_profiles.create_index(
                "license_number",
                unique=True,
                sparse=True,
                name="license_number_1"
            )
        print(f"    ✓ Created index: {result}")
        print("    Configuration: unique=True, sparse=True")
    except Exception as e:
        print(f"    ✗ Error creating index: {e}")
    
    # Verify new indexes
    print("\n[5] Verifying indexes after fix...")
    try:
        if client:
            indexes = await db.doctor_profiles.list_indexes().to_list(100)
        else:
            indexes = list(db.doctor_profiles.list_indexes())
        
        print(f"    Current indexes ({len(indexes)}):")
        for idx in indexes:
            idx_name = idx.get('name', 'unknown')
            idx_key = idx.get('key', {})
            idx_unique = idx.get('unique', False)
            idx_sparse = idx.get('sparse', False)
            print(f"      - {idx_name}: key={idx_key}, unique={idx_unique}, sparse={idx_sparse}")
            
            if 'license_number' in idx_key:
                if idx_unique and idx_sparse:
                    print("        ✓ LICENSE INDEX CORRECT")
                else:
                    print("        ✗ LICENSE INDEX STILL INCORRECT")
    except Exception as e:
        print(f"    ✗ Error verifying indexes: {e}")
    
    # Check existing documents
    print("\n[6] Checking existing doctor documents...")
    try:
        if client:
            count = await db.doctor_profiles.count_documents({})
        else:
            count = db.doctor_profiles.count_documents({})
        print(f"    Found {count} doctor profiles")
        
        if count > 0:
            print("    ✓ Existing doctor documents intact")
    except Exception as e:
        print(f"    ✗ Error checking documents: {e}")
    
    if client:
        client.close()
    
    print("\n" + "="*80)
    print("INDEX FIX COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(inspect_and_fix_indexes())
