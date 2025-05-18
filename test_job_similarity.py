import requests
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import numpy as np
from bson import ObjectId
from datetime import datetime

# Load environment variables
load_dotenv()

# API Base URL
BASE_URL = "http://localhost:8000"

# MongoDB connection details - use the same connection as the test_vector_search.py
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net")
DB_NAME = os.getenv("DB_NAME", "job_recommendation")
JOBS_COLLECTION = "jobs"

# User credentials
EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")

# Connect to MongoDB directly to calculate similarity
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
jobs_collection = db[JOBS_COLLECTION]

def login():
    """Login and get access token"""
    login_data = {
        "username": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/token", data=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print("Login successful")
        return token_data["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

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

def get_available_jobs(token):
    """Get list of available jobs to use for testing"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/jobs", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get jobs: {response.status_code}")
        print(response.text)
        return []

def find_similar_jobs(job_id, top_k=5):
    """Find jobs similar to the given job using their embeddings"""
    # Get the source job
    try:
        source_job = jobs_collection.find_one({"_id": ObjectId(job_id)})
        if not source_job:
            print(f"Job with ID {job_id} not found")
            return []
        
        # Get the embedding of the source job
        source_embedding = source_job.get("embedding", [])
        if not source_embedding:
            print(f"Job with ID {job_id} doesn't have an embedding")
            return []
        
        # Get all other jobs
        all_jobs = list(jobs_collection.find({"_id": {"$ne": ObjectId(job_id)}, "is_active": True}))
        print(f"Found {len(all_jobs)} other jobs for comparison")
        
        # Calculate similarity scores
        job_similarities = []
        for job in all_jobs:
            job_embedding = job.get("embedding", [])
            if job_embedding:
                similarity = cosine_similarity(source_embedding, job_embedding)
                job_similarities.append({
                    "job": job,
                    "similarity": similarity
                })
        
        # Sort by similarity (descending)
        job_similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Get top_k results
        top_results = job_similarities[:top_k]
        
        # Format results
        results = []
        for item in top_results:
            job = item["job"]
            similarity = item["similarity"]
            
            # Create a result object without the embedding
            result = {
                "job_id": str(job["_id"]),
                "title": job.get("title", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "N/A"),
                "similarity_score": similarity,
                "requirements": job.get("requirements", [])
            }
            
            results.append(result)
        
        return results
    except Exception as e:
        print(f"Error finding similar jobs: {e}")
        return []

def display_job_details(job):
    """Display details of a job"""
    print(f"Job ID: {job.get('id', 'N/A')}")
    print(f"Title: {job.get('title', 'N/A')}")
    print(f"Company: {job.get('company', 'N/A')}")
    print(f"Location: {job.get('location', 'N/A')}")
    
    if "requirements" in job and job["requirements"]:
        print(f"Requirements: {', '.join(job['requirements'])}")
    
    print(f"Description: {job.get('description', 'N/A')[:150]}...")
    print("-" * 50)

def display_similar_jobs(source_job, similar_jobs):
    """Display similar job recommendations"""
    print("\n" + "="*60)
    print(f"SIMILAR JOBS TO: {source_job.get('title', 'N/A')} at {source_job.get('company', 'N/A')}")
    print("="*60)
    
    print("\nSOURCE JOB:")
    display_job_details(source_job)
    
    print("\nSIMILAR JOBS:")
    if not similar_jobs:
        print("No similar jobs found")
        return
    
    for i, job in enumerate(similar_jobs, 1):
        print(f"\nSimilar Job #{i}:")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Similarity Score: {job['similarity_score']:.4f}")
        
        if "requirements" in job and job["requirements"]:
            print(f"Requirements: {', '.join(job['requirements'])}")
        
        print("-"*50)

def test_job_similarity():
    """Main function to test job similarity recommendations"""
    print("Starting job similarity test...")
    
    # Login to get token
    token = login()
    if not token:
        print("Failed to login. Exiting.")
        return
    
    # Get list of available jobs
    print("Getting list of available jobs...")
    jobs = get_available_jobs(token)
    
    if not jobs or len(jobs) == 0:
        print("No jobs found. Please run populate_sample_jobs.py first.")
        return
    
    # Test similarity for each job
    for i, job in enumerate(jobs[:3], 1):  # Test only the first 3 jobs to avoid too much output
        job_id = job.get("id")
        print(f"\nTesting job similarity for job #{i}: {job.get('title')} (ID: {job_id})")
        
        similar_jobs = find_similar_jobs(job_id)
        display_similar_jobs(job, similar_jobs)

if __name__ == "__main__":
    test_job_similarity() 