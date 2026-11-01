"""
Mark all doctors as verified in MongoDB Atlas
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import Database
from datetime import datetime, timezone


async def verify_all_doctors():
    """Mark all doctor profiles as verified"""
    
    await Database.connect_to_database()
    print("✅ Connected to MongoDB Atlas")
    
    db = Database.get_database()
    doctor_profiles = db["doctor_profiles"]
    
    # Update all doctor profiles to be verified and available
    result = await doctor_profiles.update_many(
        {},
        {
            "$set": {
                "is_verified": True,
                "is_available": True,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    print(f"\n✅ Updated {result.modified_count} doctor profiles")
    print("   All doctors are now verified and available for appointments")
    
    # Count total doctors
    count = await doctor_profiles.count_documents({})
    print(f"   Total doctors in database: {count}")
    
    await Database.close_database_connection()


if __name__ == "__main__":
    asyncio.run(verify_all_doctors())
