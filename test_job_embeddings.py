import requests
import json
from pymongo import MongoClient
import numpy as np
from tabulate import tabulate

# MongoDB connection details
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"
JOBS_COLLECTION = "jobs"

# API endpoints
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/token"
JOBS_URL = f"{BASE_URL}/jobs"
SEARCH_URL = f"{BASE_URL}/jobs/search"

# Employer credentials
EMPLOYER_EMAIL = "test@employer.com"
EMPLOYER_PASSWORD = "testpassword123"

def print_section(title):
    """Print a section title for better readability"""
    print("\n")
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def print_json(title, data):
    """Print JSON data in a formatted way"""
    print(f"\n--- {title} ---")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str))
    else:
        print(data)

def get_auth_token():
    """Get authentication token"""
    login_data = {
        "username": EMPLOYER_EMAIL,
        "password": EMPLOYER_PASSWORD
    }
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()["access_token"]
        else:
            print(f"❌ Error logging in: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def get_profile(token):
    """Get user profile to get employer ID"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def create_job(token, employer_id):
    """Create a test job"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Create a unique job title to avoid duplicates
    import time
    job_title = f"AI Engineer (Test {int(time.time())})"
    
    job_data = {
        "title": job_title,
        "company": "Tech Innovations",
        "description": "We are seeking a talented AI Engineer to join our cutting-edge research team. You will work on developing and implementing machine learning models and advanced NLP applications.",
        "requirements": [
            "Strong background in machine learning",
            "Experience with PyTorch or TensorFlow",
            "NLP expertise",
            "Python programming",
            "Vector databases"
        ],
        "location": "Remote",
        "salary_range": "$130,000 - $170,000",
        "employer_id": employer_id
    }
    
    try:
        response = requests.post(JOBS_URL, headers=headers, json=job_data)
        if response.status_code == 200:
            print(f"✅ Job '{job_title}' created successfully!")
            return response.json()
        else:
            print(f"❌ Error creating job: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def get_job_with_embedding(job_id):
    """Directly access MongoDB to get job with embedding"""
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        jobs_collection = db[JOBS_COLLECTION]
        
        job = jobs_collection.find_one({"id": job_id})
        client.close()
        return job
    except Exception as e:
        print(f"❌ Error accessing MongoDB: {str(e)}")
        return None

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

def test_semantic_search(token, query="AI engineer with Python and machine learning"):
    """Test semantic search functionality"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        # The server expects the query parameter in the URL, not in the JSON body
        params = {"query": query, "top_k": 5}
        response = requests.post(
            SEARCH_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            print(f"✅ Semantic search for '{query}' completed successfully!")
            return response.json()
        else:
            print(f"❌ Error with semantic search: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def run_test():
    print_section("TESTING JOB EMBEDDINGS")
    
    # Step 1: Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token. Cannot proceed.")
        return
    
    # Step 2: Get employer profile
    profile = get_profile(token)
    if not profile:
        print("❌ Failed to get profile. Cannot proceed.")
        return
    employer_id = profile["id"]
    print(f"✅ Employer ID: {employer_id}")
    
    # Step 3: Create a new job
    print_section("CREATING A NEW JOB")
    job = create_job(token, employer_id)
    if not job:
        print("❌ Failed to create job. Cannot proceed.")
        return
    
    # Print job details
    print_json("Created Job Details", job)
    
    # Step 4: Get job with embedding from MongoDB
    print_section("RETRIEVING EMBEDDINGS FROM MONGODB")
    job_with_embedding = get_job_with_embedding(job["id"])
    if not job_with_embedding:
        print("❌ Failed to retrieve job from MongoDB.")
        return
    
    # Step 5: Analyze and print embedding information
    embedding = job_with_embedding.get("embedding")
    if embedding:
        analysis = analyze_embedding(embedding)
        
        # Create a table to display embedding properties
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
        
        embedding_size_kb = len(str(embedding)) * 2 / 1024  # Approximate size
        print(f"\n💾 Embedding size: ~{embedding_size_kb:.2f} KB")
    else:
        print("❌ No embedding found in the job document.")
    
    # Step 6: Test semantic search
    print_section("TESTING SEMANTIC SEARCH")
    search_query = "AI engineer with Python and machine learning"
    search_results = test_semantic_search(token, search_query)
    
    if search_results:
        print(f"\n🔍 Found {len(search_results)} results for query: '{search_query}'")
        for i, result in enumerate(search_results):
            print(f"\nResult #{i+1}: {result['title']}")
            print(f"Description: {result['description'][:100]}...")

if __name__ == "__main__":
    run_test() 