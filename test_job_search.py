import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()

# API Base URL
BASE_URL = "http://localhost:8000"  # Update as needed

# User credentials - either use environment variables or hardcode them for testing
EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com") 
PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")

def login():
    """Login and get access token"""
    login_data = {
        "username": EMAIL,  # Note: FastAPI OAuth2 uses 'username' instead of 'email'
        "password": PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/token", data=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Login successful")
        return token_data["access_token"]
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def register_candidate():
    """Register a test candidate if needed"""
    register_data = {
        "email": EMAIL,
        "password": PASSWORD,
        "user_type": "candidate",
        "full_name": "Test User",
        "skills": ["Python", "Machine Learning", "FastAPI", "Data Analysis"],
        "experience": "5 years of experience in software development",
        "education": "MSc Computer Science",
        "location": "New York",
        "bio": "Software engineer specializing in AI and machine learning applications"
    }
    
    response = requests.post(f"{BASE_URL}/register/candidate", json=register_data)
    
    if response.status_code == 200:
        print(f"Registration successful")
        return True
    elif response.status_code == 400 and "already exists" in response.text:
        print("User already exists, trying to log in instead")
        return True
    else:
        print(f"Registration failed: {response.status_code}")
        print(response.text)
        return False

def search_jobs(token, query, top_k=5):
    """Search for jobs using vector search"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    search_data = {
        "query": query
    }
    
    response = requests.post(
        f"{BASE_URL}/jobs/search?top_k={top_k}", 
        headers=headers,
        json=search_data
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Search failed: {response.status_code}")
        print(response.text)
        return None

def display_search_results(results, query):
    """Format and display search results"""
    if not results:
        print(f"No results found for query: '{query}'")
        return
    
    print("\n" + "="*50)
    print(f"SEARCH RESULTS FOR: '{query}'")
    print("="*50)
    
    for i, job in enumerate(results, 1):
        print(f"\nResult #{i}:")
        print(f"Title: {job.get('title', 'N/A')}")
        print(f"Company: {job.get('company', 'N/A')}")
        print(f"Location: {job.get('location', 'N/A')}")
        if 'requirements' in job and job['requirements']:
            print(f"Requirements: {', '.join(job['requirements'])}")
        print(f"Description: {job.get('description', 'N/A')[:150]}...")
        print("-"*50)

def test_job_search():
    """Main function to test job search functionality"""
    print("Starting job search test...")
    
    # Try registration (if user doesn't already exist)
    if not register_candidate():
        print("Failed to register or user already exists.")
        return
    
    # Login to get token
    token = login()
    if not token:
        print("Failed to login. Exiting.")
        return
    
    # Test vector search with different queries
    test_queries = [
        "Python developer with machine learning experience",
        "Frontend developer with React experience",
        "Data scientist with statistical analysis skills",
        "DevOps engineer with AWS experience",
        "Software engineer with API development skills"
    ]
    
    for query in test_queries:
        print(f"\nTesting search with query: '{query}'")
        results = search_jobs(token, query)
        display_search_results(results, query)

if __name__ == "__main__":
    test_job_search() 