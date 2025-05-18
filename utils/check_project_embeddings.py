import pymongo
from bson import ObjectId
from tabulate import tabulate
import numpy as np

# MongoDB connection details
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"
PROJECTS_COLLECTION = "projects"

def print_section(title):
    """Print a section title for better readability"""
    print("\n")
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def analyze_embedding(embedding):
    """Analyze embedding vector properties"""
    if not embedding or not isinstance(embedding, list):
        return "Invalid embedding"
    
    embedding_array = np.array(embedding)
    return {
        "dimension": len(embedding),
        "min": float(np.min(embedding_array)),
        "max": float(np.max(embedding_array)),
        "mean": float(np.mean(embedding_array)),
        "std": float(np.std(embedding_array)),
        "norm": float(np.linalg.norm(embedding_array)),
        "first_5": embedding[:5],
        "last_5": embedding[-5:]
    }

def check_project_embeddings():
    client = pymongo.MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db[PROJECTS_COLLECTION]
    
    print_section("PROJECT COLLECTION STATISTICS")
    total_count = collection.count_documents({})
    with_embedding_count = collection.count_documents({"embedding": {"$exists": True}})
    without_embedding_count = collection.count_documents({"embedding": {"$exists": False}})
    
    print(f"Total projects: {total_count}")
    print(f"Projects with embeddings: {with_embedding_count}")
    print(f"Projects without embeddings: {without_embedding_count}")
    
    if with_embedding_count == 0:
        print("\n❌ No projects have embeddings! This is the main issue.")
        print("   The embedding generation during project creation might not be working.")
        client.close()
        return
    
    print_section("EXAMINING EMBEDDINGS")
    
    # Get a sample project with embedding
    sample_project = collection.find_one({"embedding": {"$exists": True}})
    
    if sample_project:
        print(f"Sample project title: {sample_project.get('title', 'Unknown title')}")
        print(f"Project ID: {sample_project.get('id', 'No ID')}")
        print(f"Project Type: {sample_project.get('project_type', 'Unknown type')}")
        
        embedding = sample_project.get('embedding')
        if embedding:
            # Check embedding format
            if isinstance(embedding, list):
                analysis = analyze_embedding(embedding)
                
                print("\n📊 Embedding Analysis:")
                table_data = [
                    ["Dimension", analysis["dimension"]],
                    ["Min value", analysis["min"]],
                    ["Max value", analysis["max"]],
                    ["Mean value", analysis["mean"]],
                    ["Standard deviation", analysis["std"]],
                    ["L2 Norm", analysis["norm"]]
                ]
                print(tabulate(table_data, headers=["Property", "Value"], tablefmt="grid"))
                
                print("\n🔢 First 5 dimensions:")
                print(analysis["first_5"])
                print("\n🔢 Last 5 dimensions:")
                print(analysis["last_5"])
                
                if analysis["dimension"] != 3072:
                    print(f"\n⚠️ Warning: Expected embedding dimension 3072, but found {analysis['dimension']}")
                    print("   This may cause issues with vector search")
            else:
                print(f"\n❌ Embedding is not a list! Type: {type(embedding)}")
                print("   This will prevent vector search from working")
        else:
            print("\n❌ Embedding is None or empty!")
    else:
        print("\n❌ Could not find any projects with embeddings")
    
    print_section("CHECKING MONGODB INDEXES")
    indexes = list(collection.list_indexes())
    
    vector_index_exists = False
    for idx in indexes:
        if idx.get("name") == "project_vector_index":
            vector_index_exists = True
            print("✅ Vector index found in projects collection")
            break
    
    if not vector_index_exists:
        print("❌ No vector index found in projects collection")
        print("   Run 'python create_vector_indexes.py' to create the required indexes")
    
    # Show some projects that don't have embeddings (if any)
    if without_embedding_count > 0:
        print_section("PROJECTS MISSING EMBEDDINGS")
        projects_without_embedding = collection.find(
            {"embedding": {"$exists": False}}
        ).limit(5)  # Show at most 5 examples
        
        for i, project in enumerate(projects_without_embedding):
            print(f"\nProject {i+1}:")
            print(f"  Title: {project.get('title', 'Unknown')}")
            print(f"  ID: {project.get('id', 'Unknown')}")
            print(f"  Type: {project.get('project_type', 'Unknown')}")
            print(f"  Created at: {project.get('created_at', 'Unknown')}")
    
    client.close()

if __name__ == "__main__":
    check_project_embeddings() 