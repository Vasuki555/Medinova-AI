"""Check user_id types in database"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import certifi
from bson import ObjectId

async def check_types():
    client = AsyncIOMotorClient(settings.MONGODB_URL, tls=True, tlsCAFile=certifi.where())
    db = client["medinova_ai"]
    
    print("=== Checking Doctor Profile user_id types ===")
    async for doc in db.doctor_profiles.find({"is_verified": True}).limit(3):
        user_id = doc.get("user_id")
        print(f"\nDoctor ID: {doc['_id']}")
        print(f"  user_id value: {user_id}")
        print(f"  user_id type: {type(user_id)}")
        
        # Try to find the user
        user = await db.users.find_one({"_id": user_id})
        print(f"  Found user by direct match: {user is not None}")
        
        if user:
            print(f"  User name: {user.get('first_name')} {user.get('last_name')}")
        else:
            # Try ObjectId conversion
            try:
                user_oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
                user = await db.users.find_one({"_id": user_oid})
                print(f"  Found user by ObjectId conversion: {user is not None}")
                if user:
                    print(f"  User name: {user.get('first_name')} {user.get('last_name')}")
            except:
                print(f"  Could not convert to ObjectId")
    
    print("\n=== Checking User _id types ===")
    async for user in db.users.find({"role": "doctor"}).limit(3):
        print(f"\nUser email: {user.get('email')}")
        print(f"  _id value: {user['_id']}")
        print(f"  _id type: {type(user['_id'])}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_types())
