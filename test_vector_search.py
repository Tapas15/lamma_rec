import asyncio
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
import numpy as np
from bson import ObjectId
import json

# Load environment variables
load_dotenv()

# MongoDB connection details
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net")
DB_NAME = os.getenv("DB_NAME", "job_recommender")
JOBS_COLLECTION = "jobs"  # Collection name for jobs

# Ollama endpoint for embeddings
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434/api/embeddings")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
jobs_collection = db[JOBS_COLLECTION]

def get_embedding(text: str) -> list:
    """Get embedding from Ollama API"""
    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json={
                "model": OLLAMA_MODEL,
                "prompt": text
            }
        )
        
        if response.status_code != 200:
            print(f"Error from Ollama API: {response.status_code}")
            print(response.text)
            return []
            
        data = response.json()
        return data['embedding']
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    if not vec1 or not vec2:
        return 0.0
    
    try:
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
            
        return dot_product / (norm_vec1 * norm_vec2)
    except Exception as e:
        print(f"Error in cosine similarity calculation: {str(e)}")
        return 0.0

def calculate_job_similarity(query_embedding, job_data):
    """Calculate similarity between query and job"""
    job_embedding = job_data.get('embedding', [])
    
    # If job doesn't have embedding, return low similarity
    if not job_embedding:
        return 0.0
        
    return cosine_similarity(query_embedding, job_embedding)

def vector_search(query: str, top_k=5):
    """Perform vector search in jobs collection"""
    print(f"Searching for: '{query}'")
    
    # Get embedding for the query
    query_embedding = get_embedding(query)
    if not query_embedding:
        print("Failed to get embedding for query")
        return []
    
    print(f"Generated embedding vector with {len(query_embedding)} dimensions")
    
    # Try MongoDB's $vectorSearch if available
    try:
        # Check if we have a vector index - using list_indexes on the collection object
        try:
            indexes = list(jobs_collection.list_indexes())
            has_vector_index = any("jobs_vector_index" == idx.get("name") for idx in indexes)
        except Exception as e:
            print(f"Failed to list indexes: {e}")
            has_vector_index = False
        
        if has_vector_index:
            print("Using MongoDB vector search")
            # Use MongoDB Atlas vector search
            pipeline = [
                {
                    "$search": {
                        "index": "jobs_vector_index",
                        "vectorSearch": {
                            "queryVector": query_embedding,
                            "path": "embedding",
                            "numCandidates": 100,
                            "limit": top_k
                        }
                    }
                },
                {
                    "$project": {
                        "score": {"$meta": "searchScore"},
                        "title": 1,
                        "company": 1,
                        "location": 1,
                        "description": 1,
                        "requirements": 1,
                        "embedding": 1
                    }
                }
            ]
            
            results = list(jobs_collection.aggregate(pipeline))
            print(f"Found {len(results)} results using MongoDB vector search")
            return results
    except Exception as e:
        print(f"MongoDB vector search not available or failed: {e}")
    
    # Fallback: Manual vector search
    print("Using manual vector search")
    jobs = list(jobs_collection.find({"is_active": True}))
    print(f"Retrieved {len(jobs)} jobs for comparison")
    
    # Calculate similarity for each job
    job_scores = []
    for job in jobs:
        similarity = calculate_job_similarity(query_embedding, job)
        job_scores.append({
            "job": job,
            "similarity": similarity
        })
    
    # Sort by similarity (descending)
    job_scores.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Get top_k results
    top_results = job_scores[:top_k]
    
    # Format results similar to MongoDB's $vectorSearch
    results = []
    for item in top_results:
        job = item["job"]
        job["score"] = item["similarity"]
        # Remove embedding from results for cleaner output
        if "embedding" in job:
            del job["embedding"]
        results.append(job)
    
    print(f"Found {len(results)} results using manual vector search")
    return results

def display_results(results):
    """Format and display search results"""
    if not results:
        print("No results found")
        return
        
    print("\nSearch Results:")
    print("=" * 60)
    
    for i, job in enumerate(results, 1):
        print(f"Result #{i}:")
        print(f"Title: {job.get('title', 'N/A')}")
        print(f"Company: {job.get('company', 'N/A')}")
        print(f"Location: {job.get('location', 'N/A')}")
        print(f"Score: {job.get('score', 0):.4f}")
        
        if 'requirements' in job and job['requirements']:
            print(f"Requirements: {', '.join(job['requirements'])}")
            
        if 'description' in job:
            print(f"Description: {job['description'][:150]}...")
            
        print("-" * 60)

def test_search_queries():
    """Test vector search with multiple queries"""
    test_queries = [
        "Python developer with machine learning experience",
        "Frontend developer with React experience",
        "Data scientist with statistical analysis skills",
        "DevOps engineer with AWS experience",
        "Software engineer with API development skills"
    ]
    
    for query in test_queries:
        print("\n" + "=" * 80)
        print(f"TESTING QUERY: {query}")
        print("=" * 80)
        
        results = vector_search(query)
        display_results(results)
        print("\n")

if __name__ == "__main__":
    # Test vector search
    test_search_queries() 