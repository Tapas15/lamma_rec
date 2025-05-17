import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration

# MongoDB connection string with proper formatting
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"


# Collection names
COLLECTIONS = [
    "users",
    "employers",
    "candidates",
    "jobs",
    "applications",
    "blacklisted_tokens"
]

async def clear_collections():
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Clear each collection
        for collection_name in COLLECTIONS:
            try:
                # Check if collection exists
                if collection_name in await db.list_collection_names():
                    # Delete all documents
                    result = await db[collection_name].delete_many({})
                    print(f"✓ Cleared {collection_name}: {result.deleted_count} documents deleted")
                else:
                    print(f"! Collection {collection_name} does not exist")
            except Exception as e:
                print(f"! Error clearing {collection_name}: {str(e)}")
        
        print("\nDatabase cleanup completed!")
        
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
    finally:
        # Close the connection
        client.close()
        print("Database connection closed.")

if __name__ == "__main__":
    # Confirm before clearing
    print("WARNING: This will delete ALL data from the following collections:")
    for collection in COLLECTIONS:
        print(f"- {collection}")
    
    confirm = input("\nAre you sure you want to proceed? (yes/no): ")
    
    if confirm.lower() == "yes":
        # Run the async function
        asyncio.run(clear_collections())
    else:
        print("Operation cancelled.") 