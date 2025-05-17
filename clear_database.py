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


async def clear_database():
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Get all collection names
        collections = await db.list_collection_names()
        
        if not collections:
            print("Database is already empty.")
            return
        
        print(f"\nFound {len(collections)} collections:")
        for collection in collections:
            print(f"- {collection}")
        
        # Drop each collection
        for collection_name in collections:
            try:
                await db[collection_name].drop()
                print(f"✓ Dropped collection: {collection_name}")
            except Exception as e:
                print(f"! Error dropping {collection_name}: {str(e)}")
        
        # Drop all indexes
        try:
            await db.command("dropAllIndexes")
            print("\n✓ Dropped all indexes")
        except Exception as e:
            print(f"\n! Error dropping indexes: {str(e)}")
        
        print("\nDatabase cleanup completed!")
        
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
    finally:
        # Close the connection
        client.close()
        print("Database connection closed.")

if __name__ == "__main__":
    # Confirm before clearing
    print("="*60)
    print("WARNING: This will COMPLETELY CLEAR the database!")
    print("All collections and their data will be permanently deleted.")
    print("="*60)
    
    confirm = input("\nType 'DELETE' to confirm database deletion: ")
    
    if confirm == "DELETE":
        # Run the async function
        asyncio.run(clear_database())
    else:
        print("Operation cancelled.") 