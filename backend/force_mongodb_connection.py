"""
Force MongoDB Atlas connection and verify user exists
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = "medinova_ai"

async def test_connection():
    print("="*60)
    print("TESTING MONGODB ATLAS CONNECTION")
    print("="*60)
    
    try:
        # Create SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        print("\n1. Connecting to MongoDB Atlas...")
        client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            tls=True,
            tlsCAFile=certifi.where(),
        )
        
        # Test connection
        print("2. Pinging server...")
        await client.admin.command("ping")
        print("   ✅ Connection successful!")
        
        # Get database
        db = client[DB_NAME]
        
        # Check users collection
        print("\n3. Checking users collection...")
        user_count = await db.users.count_documents({})
        print(f"   ✅ Found {user_count} users in database")
        
        # Find the test user
        print("\n4. Looking for sharma333@test.com...")
        user = await db.users.find_one({"email": "sharma333@test.com"})
        
        if user:
            print(f"   ✅ User found!")
            print(f"   - ID: {user['_id']}")
            print(f"   - Name: {user.get('first_name')} {user.get('last_name')}")
            print(f"   - Role: {user.get('role')}")
        else:
            print(f"   ❌ User NOT found in database")
            print(f"   Available users:")
            async for u in db.users.find({}, {"email": 1, "first_name": 1, "last_name": 1}).limit(5):
                print(f"      - {u.get('email')} ({u.get('first_name')} {u.get('last_name')})")
        
        print("\n" + "="*60)
        print("✅ MONGODB CONNECTION IS WORKING!")
        print("="*60)
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n" + "="*60)
        print("SOLUTION:")
        print("1. Check MongoDB Atlas IP whitelist")
        print("2. Verify network connectivity")
        print("3. Confirm MongoDB URL in .env is correct")
        print("="*60)
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
