import pymongo
import time
from pymongo.errors import OperationFailure

# MongoDB connection details
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"

# Collections that need vector indexes
COLLECTIONS_CONFIG = [
    {
        "name": "jobs",
        "index_name": "vector_index",
        "field": "embedding",
        "dimension": 3072  # This is the dimension for llama3.2 embeddings
    },
    {
        "name": "projects",
        "index_name": "project_vector_index",
        "field": "embedding",
        "dimension": 3072
    },
    {
        "name": "candidates",
        "index_name": "candidate_vector_index",
        "field": "embedding",
        "dimension": 3072
    }
]

def print_section(title):
    """Print a section title for better readability"""
    print("\n")
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def create_vector_indexes():
    """Create vector indexes for all collections if they don't exist"""
    client = pymongo.MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    for config in COLLECTIONS_CONFIG:
        collection_name = config["name"]
        index_name = config["index_name"]
        field = config["field"]
        dimension = config["dimension"]
        
        print_section(f"CHECKING {collection_name.upper()} COLLECTION")
        
        collection = db[collection_name]
        
        # Check if any documents have embeddings
        sample_doc = collection.find_one({field: {"$exists": True}})
        if not sample_doc:
            print(f"❌ No documents with '{field}' field found in {collection_name} collection")
            print("   Make sure you have documents with embeddings before creating index")
            continue
        
        # Check if the embeddings are in the correct format (list of numbers)
        embedding = sample_doc.get(field)
        if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
            print(f"❌ The embedding format is incorrect in {collection_name} collection")
            print(f"   Embedding type: {type(embedding)}")
            print(f"   First few elements: {embedding[:5] if isinstance(embedding, list) else 'Not a list'}")
            continue
        
        actual_dimension = len(embedding) if isinstance(embedding, list) else 0
        if actual_dimension != dimension:
            print(f"⚠️ Warning: Expected dimension {dimension}, but found {actual_dimension}")
            print(f"   Updating dimension from {dimension} to {actual_dimension}")
            dimension = actual_dimension
        
        # Check existing indexes
        try:
            indexes = list(collection.list_indexes())
            index_exists = False
            for idx in indexes:
                if idx.get("name") == index_name:
                    index_exists = True
                    print(f"✅ Vector index '{index_name}' already exists for {collection_name}")
                    break
                
            if not index_exists:
                print(f"Creating vector index '{index_name}' for {collection_name}...")
                
                # Create the vector index
                index_model = {
                    "name": index_name,
                    "fields": [
                        {
                            "numDimensions": dimension,
                            "path": field,
                            "similarity": "cosine"  # cosine similarity is good for embeddings
                        }
                    ]
                }
                
                try:
                    # MongoDB Atlas requires a different approach than local MongoDB
                    # This is the Atlas command format
                    result = db.command({
                        "createSearchIndex": collection_name,
                        "definition": {
                            "name": index_name,
                            "mappings": {
                                "dynamic": False,
                                "fields": {
                                    field: {
                                        "dimensions": dimension,
                                        "similarity": "cosine",
                                        "type": "vector"
                                    }
                                }
                            }
                        }
                    })
                    
                    print(f"✅ Vector index created for {collection_name}!")
                    print(f"   Response: {result}")
                    
                except OperationFailure as e:
                    if "already exists" in str(e):
                        print(f"✅ Vector index '{index_name}' already exists (detected during creation)")
                    else:
                        print(f"❌ Failed to create vector index for {collection_name}: {str(e)}")
                        print("   You might need to use MongoDB Atlas UI to create the index")
        
        except Exception as e:
            print(f"❌ Error checking indexes for {collection_name}: {str(e)}")
    
    client.close()
    print("\nDone checking and creating vector indexes!")

if __name__ == "__main__":
    create_vector_indexes() 