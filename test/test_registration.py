import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_response(response):
    """Helper function to print responses in a formatted way"""
    print("\nStatus Code:", response.status_code)
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 80)

def test_candidate_registration():
    print("\n=== Testing Candidate Registration and Profile ===")
    
    # Test candidate registration
    candidate_data = {
        "email": "candidate@example.com",
        "password": "candidatepass123",
        "full_name": "John Doe",
        "user_type": "candidate",
        "skills": ["Python", "FastAPI", "MongoDB", "React"],
        "experience": "5 years of full-stack development",
        "education": "Master's in Computer Science",
        "location": "New York",
        "bio": "Passionate developer with focus on web technologies"
    }
    
    # Register candidate
    print("\nRegistering candidate...")
    response = requests.post(f"{BASE_URL}/register/candidate", json=candidate_data)
    print_response(response)
    
    if response.status_code == 200:
        candidate_id = response.json()["id"]
        
        # Get candidate profile
        print("\nRetrieving candidate profile...")
        response = requests.get(f"{BASE_URL}/candidate/{candidate_id}")
        print_response(response)
        
        # Test candidate login
        print("\nTesting candidate login...")
        login_data = {
            "username": candidate_data["email"],
            "password": candidate_data["password"]
        }
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        print_response(response)

def test_employer_registration():
    print("\n=== Testing Employer Registration and Profile ===")
    
    # Test employer registration with complete data
    employer_data = {
        "email": "test@employer.com",
        "password": "testpassword123",
        "full_name": "Jane Smith",
        "user_type": "employer",
        "company_name": "Tech Innovations Inc.",
        "company_description": "Leading software development and AI solutions provider",
        "company_website": "https://techinnovations.com",
        "company_location": "Silicon Valley, CA",
        "company_size": "100-500",
        "industry": "Information Technology",
        "contact_email": "hr@techinnovations.com",
        "contact_phone": "+1-555-123-4567",
        "location": "San Francisco Bay Area",
        "bio": "Global technology company specializing in AI and machine learning solutions",
        # Additional fields to ensure complete profile
        "is_active": True,
        "profile_completed": True,
        "verified": True,
        "last_active": datetime.utcnow().isoformat()
    }
    
    # Register employer
    print("\nRegistering employer...")
    response = requests.post(f"{BASE_URL}/register/employer", json=employer_data)
    print_response(response)
    
    if response.status_code == 200:
        employer_id = response.json()["id"]
        
        # Get employer profile
        print("\nRetrieving employer profile...")
        response = requests.get(f"{BASE_URL}/employer/{employer_id}")
        print_response(response)
        
        # Test employer login
        print("\nTesting employer login...")
        login_data = {
            "username": employer_data["email"],
            "password": employer_data["password"]
        }
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        print_response(response)

def main():
    try:
        # Test candidate functionality
        #test_candidate_registration()
        
        # Test employer functionality
        test_employer_registration()
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main() 