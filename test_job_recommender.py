import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables if available
load_dotenv()

# API Base URL
BASE_URL = "http://localhost:8000"  # Update as needed

# User credentials - either use environment variables or hardcode them for testing
EMAIL = os.getenv("TEST_USER_EMAIL", "candidate@example.com") 
PASSWORD = os.getenv("TEST_USER_PASSWORD", "candidatepass123")

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
    
    try:
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
            # Don't return False here, we'll still try to login
            print("Attempting to login anyway in case user already exists...")
            return "try_login"
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        print("Attempting to login anyway...")
        return "try_login"

def get_job_recommendations(token):
    """Get job recommendations for the logged-in candidate"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/recommendations/jobs", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get recommendations: {response.status_code}")
        print(response.text)
        return None

def get_stored_recommendations(token):
    """Get stored job recommendations from the database"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/recommendations/stored", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get stored recommendations: {response.status_code}")
        print(response.text)
        return None

def display_recommendations(recommendations):
    """Format and display job recommendations"""
    if not recommendations:
        print("No recommendations found")
        return
    
    print("\n" + "="*50)
    print("JOB RECOMMENDATIONS")
    print("="*50)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\nRecommendation #{i}:")
        
        # Handle both direct job objects and recommendation objects
        if "job_id" in rec:
            # This is a recommendation object
            print(f"Job ID: {rec.get('job_id', 'N/A')}")
            print(f"Match Score: {rec.get('match_score', 0):.2f}")
            print(f"Explanation: {rec.get('explanation', 'N/A')}")
            
            # If the job details are embedded
            job = rec.get("job_details", {})
            if job:
                print(f"Title: {job.get('title', 'N/A')}")
                print(f"Company: {job.get('company', 'N/A')}")
                print(f"Location: {job.get('location', 'N/A')}")
        else:
            # This is a direct job object
            print(f"Title: {rec.get('title', 'N/A')}")
            print(f"Company: {rec.get('company', 'N/A')}")
            print(f"Location: {rec.get('location', 'N/A')}")
            print(f"Match Score: {rec.get('match_score', 0):.2f}")
            
        print("-"*50)

def test_candidate_for_job_recommendations(job_id, token):
    """Test getting candidate recommendations for a specific job"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/recommendations/candidates/{job_id}", headers=headers)
    
    if response.status_code == 200:
        candidates = response.json()
        print("\n" + "="*50)
        print(f"CANDIDATE RECOMMENDATIONS FOR JOB {job_id}")
        print("="*50)
        
        for i, candidate in enumerate(candidates, 1):
            print(f"\nCandidate #{i}:")
            print(f"Candidate ID: {candidate.get('candidate_id', 'N/A')}")
            print(f"Match Score: {candidate.get('match_score', 0):.2f}")
            print(f"Explanation: {candidate.get('explanation', 'N/A')}")
            print("-"*50)
    else:
        print(f"Failed to get candidate recommendations: {response.status_code}")
        print(response.text)

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

def test_job_recommender():
    """Main function to test job recommender functionality"""
    print("Starting job recommender test...")
    
    # Try registration first
    registration_result = register_candidate()
    
    # If registration failed with error other than "already exists", 
    # we still try to login
    token = None
    if registration_result == True or registration_result == "try_login":
        # Try to login regardless of registration outcome
        token = login()
    
    if not token:
        print("Failed to login. Exiting.")
        return
    
    # Test getting job recommendations
    print("\nTesting job recommendations for the current candidate...")
    recommendations = get_job_recommendations(token)
    display_recommendations(recommendations)
    
    # Test getting stored recommendations (if any)
    print("\nTesting stored recommendations...")
    stored_recommendations = get_stored_recommendations(token)
    display_recommendations(stored_recommendations)
    
    # Get list of jobs and test candidate recommendations for a job
    jobs = get_available_jobs(token)
    if jobs and len(jobs) > 0:
        job_id = jobs[0].get("id")  # Use the first job
        print(f"\nTesting candidate recommendations for job {job_id}...")
        test_candidate_for_job_recommendations(job_id, token)

if __name__ == "__main__":
    test_job_recommender() 