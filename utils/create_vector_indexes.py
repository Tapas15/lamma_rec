import os
from pymongo import MongoClient
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lamma_rec")

# Collections
JOBS_COLLECTION = "jobs"
CANDIDATES_COLLECTION = "candidates"
PROJECTS_COLLECTION = "projects"

def create_vector_indexes():
    """Create vector indexes for all collections that need vector search"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        print(f"Connected to MongoDB database: {DATABASE_NAME}")
        
        # Create Atlas Search index for jobs collection
        try:
            # For Atlas Search, you need to use the Atlas UI or API to create indexes
            # This is a placeholder to remind users to create the indexes manually
            print(f"To create a vector search index for {JOBS_COLLECTION}, use the MongoDB Atlas UI:")
            print("1. Go to the Atlas UI")
            print("2. Select your cluster")
            print("3. Go to the Search tab")
            print("4. Create an index with the following JSON configuration:")
            print("""
            {
              "mappings": {
                "dynamic": false,
                "fields": {
                  "embedding": {
                    "dimensions": 4096,
                    "similarity": "cosine",
                    "type": "vector"
                  }
                }
              }
            }
            """)
            print(f"Name the index: {JOBS_COLLECTION}_vector_index")
        except Exception as e:
            print(f"Error creating vector index for {JOBS_COLLECTION}: {str(e)}")
        
        # Create regular indexes for faster lookups
        try:
            db[JOBS_COLLECTION].create_index("is_active")
            db[JOBS_COLLECTION].create_index("employer_id")
            print(f"Created regular indexes for {JOBS_COLLECTION} collection")
        except Exception as e:
            print(f"Error creating regular indexes for {JOBS_COLLECTION}: {str(e)}")
            
        # Create regular indexes for candidates collection
        try:
            db[CANDIDATES_COLLECTION].create_index("is_active")
            db[CANDIDATES_COLLECTION].create_index("profile_completed")
            db[CANDIDATES_COLLECTION].create_index("profile_visibility")
            print(f"Created regular indexes for {CANDIDATES_COLLECTION} collection")
        except Exception as e:
            print(f"Error creating regular indexes for {CANDIDATES_COLLECTION}: {str(e)}")
            
        # Create regular indexes for projects collection
        try:
            db[PROJECTS_COLLECTION].create_index("is_active")
            db[PROJECTS_COLLECTION].create_index("employer_id")
            db[PROJECTS_COLLECTION].create_index("status")
            print(f"Created regular indexes for {PROJECTS_COLLECTION} collection")
        except Exception as e:
            print(f"Error creating regular indexes for {PROJECTS_COLLECTION}: {str(e)}")
            
        print("\nRegular indexes created successfully")
        print("\nFor vector search functionality, please create Atlas Search indexes manually using the MongoDB Atlas UI.")
        print("Refer to the instructions above for each collection.")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    create_vector_indexes() 