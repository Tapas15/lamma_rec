import requests
import json
from pymongo import MongoClient
import numpy as np
from tabulate import tabulate
import uuid
import time

# MongoDB connection details
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"
CANDIDATES_COLLECTION = "candidates"
USERS_COLLECTION = "users"

# API endpoints
BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/register/candidate"
LOGIN_URL = f"{BASE_URL}/token"
SEARCH_URL = f"{BASE_URL}/candidates/search"

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

def generate_unique_email():
    """Generate a unique email for testing"""
    unique_id = str(int(time.time()))
    return f"test_candidate_{unique_id}@example.com"

def register_candidate():
    """Register a new test candidate"""
    email = generate_unique_email()
    
    candidate_data = {
        "email": email,
        "password": "Test@password123",
        "full_name": "Test Candidate",
        "user_type": "candidate",
        "skills": [
            "Python", 
            "Machine Learning", 
            "Data Analysis", 
            "TensorFlow", 
            "Docker",
            "Cloud Computing"
        ],
        "experience": "5+ years of experience in data science and machine learning, specializing in computer vision and natural language processing. Implemented several production ML systems.",
        "education": "Master's degree in Computer Science with focus on AI/ML. Bachelor's in Mathematics.",
        "location": "San Francisco, CA",
        "bio": "Passionate data scientist and ML engineer with expertise in building scalable AI solutions. Interest in deep learning, reinforcement learning, and deploying models to production."
    }
    
    try:
        print(f"Registering candidate with email: {email}")
        response = requests.post(REGISTER_URL, json=candidate_data)
        
        if response.status_code == 200:
            print("✅ Candidate registered successfully!")
            return response.json(), candidate_data["password"]
        else:
            print(f"❌ Error registering candidate: {response.status_code}")
            print("Response:", response.text)
            return None, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

def get_auth_token(email, password):
    """Get authentication token"""
    login_data = {
        "username": email,
        "password": password
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

def get_candidate_with_embedding(candidate_id):
    """Directly access MongoDB to get candidate with embedding"""
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        candidates_collection = db[CANDIDATES_COLLECTION]
        
        candidate = candidates_collection.find_one({"id": candidate_id})
        client.close()
        return candidate
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

def test_semantic_search(token, query="Data scientist with machine learning and Python experience"):
    """Test semantic search functionality for candidates"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        # The server expects the query parameter in the URL
        params = {"query": query, "top_k": 5}
        response = requests.post(
            SEARCH_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            print(f"✅ Semantic search for candidates '{query}' completed successfully!")
            return response.json()
        else:
            print(f"❌ Error with semantic search: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def update_candidate_profile(token, profile_updates):
    """Update candidate profile"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        response = requests.put(f"{BASE_URL}/profile", headers=headers, json=profile_updates)
        
        if response.status_code == 200:
            print("✅ Candidate profile updated successfully!")
            return response.json()
        else:
            print(f"❌ Error updating profile: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def run_test():
    print_section("TESTING CANDIDATE EMBEDDINGS")
    
    # Step 1: Register a new candidate
    print_section("REGISTERING NEW CANDIDATE")
    candidate, password = register_candidate()
    if not candidate:
        print("❌ Failed to register candidate. Cannot proceed.")
        return
    
    # Print candidate details
    print_json("Registered Candidate", candidate)
    
    # Step 2: Get candidate with embedding from MongoDB
    print_section("RETRIEVING EMBEDDINGS FROM MONGODB")
    candidate_with_embedding = get_candidate_with_embedding(candidate["id"])
    if not candidate_with_embedding:
        print("❌ Failed to retrieve candidate from MongoDB.")
        return
    
    # Step 3: Analyze and print embedding information
    embedding = candidate_with_embedding.get("embedding")
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
        print("❌ No embedding found in the candidate document.")
    
    # Step 4: Get auth token for the newly registered candidate
    token = get_auth_token(candidate["email"], password)
    if not token:
        print("❌ Failed to get auth token. Cannot proceed with profile update test.")
        return
    
    # Step 5: Update the candidate profile
    print_section("UPDATING CANDIDATE PROFILE")
    profile_updates = {
        "bio": "Experienced ML engineer and data scientist with a focus on NLP and computer vision. I enjoy working on challenging AI problems and building production-ready machine learning systems that deliver business value.",
        "skills": candidate["skills"] + ["NLP", "Computer Vision", "AWS", "Azure ML"]
    }
    
    updated_candidate = update_candidate_profile(token, profile_updates)
    if updated_candidate:
        print_json("Updated Candidate Profile", updated_candidate)
        
        # Step 6: Check if the embedding was updated
        print_section("CHECKING FOR EMBEDDING UPDATE")
        updated_embedding = get_candidate_with_embedding(candidate["id"]).get("embedding")
        
        if updated_embedding:
            updated_analysis = analyze_embedding(updated_embedding)
            print("\n📊 Updated Embedding Analysis:")
            updated_table_data = [
                ["Dimension", updated_analysis["dimension"]],
                ["L2 Norm", updated_analysis["norm"]]  # Just show dimension and norm to confirm it changed
            ]
            print(tabulate(updated_table_data, headers=["Property", "Value"], tablefmt="grid"))
            
            # Compare norms to see if embedding changed
            if "norm" in analysis and abs(analysis["norm"] - updated_analysis["norm"]) > 0.01:
                print("✅ Embedding was successfully updated (norm changed)")
            else:
                print("❓ Embedding may not have been updated (norm unchanged)")
        else:
            print("❌ No updated embedding found.")
    
    # Step 7: Login as an employer to test candidate search
    # You'd need valid employer credentials or create a new employer here
    # For this test, we'll create a simplified version
    print_section("TESTING SEMANTIC SEARCH (SIMPLIFIED)")
    print("Note: For a full semantic search test, login as an existing employer")
    print("Semantic search would match candidates based on skill requirements and job descriptions")
    
    # Get a valid MongoDB vector index before enabling this test
    # uncomment the following line if you have set up a vector index for candidates in MongoDB
    # search_results = test_semantic_search("<employer_token>", "Machine learning engineer with Python and data science skills")

if __name__ == "__main__":
    run_test() 