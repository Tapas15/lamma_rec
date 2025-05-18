from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection string with proper formatting
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        try:
            cls.client = AsyncIOMotorClient(MONGODB_URL)
            # Verify the connection
            await cls.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
        
    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            
    @classmethod
    def get_db(cls):
        return cls.client[DATABASE_NAME]
    
    @classmethod
    def get_collection(cls, collection_name: str):
        return cls.get_db()[collection_name]

# Collections
USERS_COLLECTION = "users"
JOBS_COLLECTION = "jobs"
RECOMMENDATIONS_COLLECTION = "recommendations"
CANDIDATES_COLLECTION = "candidates"
EMPLOYERS_COLLECTION = "employers"
PROJECTS_COLLECTION = "projects"
JOB_APPLICATIONS_COLLECTION = "job_applications"
SAVED_JOBS_COLLECTION = "saved_jobs"

async def init_db():
    """Initialize database by creating all required collections"""
    try:
        db = Database.get_db()
        
        # Get list of existing collections
        existing_collections = await db.list_collection_names()
        
        # List of all collections to ensure they exist
        collections = [
            USERS_COLLECTION,
            JOBS_COLLECTION,
            RECOMMENDATIONS_COLLECTION,
            CANDIDATES_COLLECTION,
            EMPLOYERS_COLLECTION,
            PROJECTS_COLLECTION,
            JOB_APPLICATIONS_COLLECTION,
            SAVED_JOBS_COLLECTION
        ]
        
        # Create collections if they don't exist
        for collection_name in collections:
            if collection_name not in existing_collections:
                await db.create_collection(collection_name)
                print(f"Created collection: {collection_name}")
            else:
                print(f"Collection already exists: {collection_name}")
        
        print("All collections initialized successfully")
        
        # Create indexes for better query performance
        # Users collection
        await db[USERS_COLLECTION].create_index("email", unique=True)
        await db[USERS_COLLECTION].create_index("id", unique=True)
        
        # Jobs collection
        await db[JOBS_COLLECTION].create_index("id", unique=True)
        await db[JOBS_COLLECTION].create_index("employer_id")
        
        # Candidates collection
        await db[CANDIDATES_COLLECTION].create_index("id", unique=True)
        await db[CANDIDATES_COLLECTION].create_index("email", unique=True)
        
        # Employers collection
        await db[EMPLOYERS_COLLECTION].create_index("id", unique=True)
        await db[EMPLOYERS_COLLECTION].create_index("email", unique=True)
        
        # Job applications collection
        await db[JOB_APPLICATIONS_COLLECTION].create_index("id", unique=True)
        await db[JOB_APPLICATIONS_COLLECTION].create_index("candidate_id")
        await db[JOB_APPLICATIONS_COLLECTION].create_index("job_id")
        await db[JOB_APPLICATIONS_COLLECTION].create_index([("candidate_id", 1), ("job_id", 1)], unique=True)
        
        # Saved jobs collection
        await db[SAVED_JOBS_COLLECTION].create_index("id", unique=True)
        await db[SAVED_JOBS_COLLECTION].create_index("candidate_id")
        await db[SAVED_JOBS_COLLECTION].create_index("job_id")
        await db[SAVED_JOBS_COLLECTION].create_index([("candidate_id", 1), ("job_id", 1)], unique=True)
        
        print("All indexes created successfully")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise