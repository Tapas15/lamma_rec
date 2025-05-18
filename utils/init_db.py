from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from database import MONGODB_URL, DATABASE_NAME, USERS_COLLECTION, JOBS_COLLECTION, PROJECTS_COLLECTION, CANDIDATES_COLLECTION, EMPLOYERS_COLLECTION

async def init_database():
    print("Initializing database...")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Drop existing indexes to clean up
        print("\nDropping existing indexes...")
        collections = [USERS_COLLECTION, JOBS_COLLECTION, PROJECTS_COLLECTION, CANDIDATES_COLLECTION, EMPLOYERS_COLLECTION]
        for collection in collections:
            try:
                await db[collection].drop_indexes()
                print(f"Dropped indexes for {collection}")
            except Exception as e:
                print(f"No indexes to drop for {collection}: {str(e)}")

        # Create proper indexes
        print("\nCreating new indexes...")
        
        # Users collection - email should be unique
        await db[USERS_COLLECTION].create_index("email", unique=True)
        print(f"Created unique index on email for {USERS_COLLECTION}")
        
        # Employers collection - email should be unique
        await db[EMPLOYERS_COLLECTION].create_index("email", unique=True)
        print(f"Created unique index on email for {EMPLOYERS_COLLECTION}")
        
        # Candidates collection - email should be unique
        await db[CANDIDATES_COLLECTION].create_index("email", unique=True)
        print(f"Created unique index on email for {CANDIDATES_COLLECTION}")
        
        # Jobs collection - no unique constraint needed
        await db[JOBS_COLLECTION].create_index([("employer_id", 1), ("created_at", -1)])
        print(f"Created index on employer_id and created_at for {JOBS_COLLECTION}")
        
        # Projects collection - no unique constraint needed
        await db[PROJECTS_COLLECTION].create_index([("employer_id", 1), ("created_at", -1)])
        print(f"Created index on employer_id and created_at for {PROJECTS_COLLECTION}")
        
        print("\nDatabase initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(init_database()) 