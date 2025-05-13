import asyncio
from database import Database, USERS_COLLECTION, JOBS_COLLECTION, RECOMMENDATIONS_COLLECTION

async def init_database():
    try:
        # Connect to MongoDB
        await Database.connect_db()
        print("Connected to MongoDB successfully!")

        # Get database instance
        db = Database.get_db()
        
        # List all collections
        collections = await db.list_collection_names()
        print(f"Existing collections: {collections}")

        # Create collections if they don't exist
        if USERS_COLLECTION not in collections:
            await db.create_collection(USERS_COLLECTION)
            print(f"Created collection: {USERS_COLLECTION}")
            
            # Create indexes for users collection
            await db[USERS_COLLECTION].create_index("email", unique=True)
            print("Created unique index on email field in users collection")

        if JOBS_COLLECTION not in collections:
            await db.create_collection(JOBS_COLLECTION)
            print(f"Created collection: {JOBS_COLLECTION}")
            
            # Create indexes for jobs collection
            await db[JOBS_COLLECTION].create_index("title")
            await db[JOBS_COLLECTION].create_index("company")
            print("Created indexes on title and company fields in jobs collection")

        if RECOMMENDATIONS_COLLECTION not in collections:
            await db.create_collection(RECOMMENDATIONS_COLLECTION)
            print(f"Created collection: {RECOMMENDATIONS_COLLECTION}")
            
            # Create indexes for recommendations collection
            await db[RECOMMENDATIONS_COLLECTION].create_index("user_id")
            await db[RECOMMENDATIONS_COLLECTION].create_index("job_id")
            print("Created indexes on user_id and job_id fields in recommendations collection")

        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        # Close the database connection
        await Database.close_db()

if __name__ == "__main__":
    asyncio.run(init_database()) 