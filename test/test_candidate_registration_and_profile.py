import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Hardcoded candidate credentials
CANDIDATE_EMAIL = "candidate@example.com"
CANDIDATE_PASSWORD = "candidatepass123"

def print_json(title, data):
    """Helper function to print JSON data in a formatted way"""
    print(f"\n=== {title} ===")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str))  # Use default=str for datetime objects
    else:
        print(data)
    print("-" * 80)

def register_candidate():
    """Register a new candidate"""
    print("\nStep 1: Registering new candidate...")
    
    # Candidate registration data
    candidate_data = {
        "email": CANDIDATE_EMAIL,
        "password": CANDIDATE_PASSWORD,
        "full_name": "John Smith",
        "user_type": "candidate",
        "skills": ["Python", "Data Science", "Machine Learning", "SQL", "FastAPI"],
        "experience": "5 years of experience in software development and data science",
        "education": "Master's in Computer Science, Stanford University",
        "location": "San Francisco, CA",
        "bio": "Passionate data scientist with expertise in machine learning and AI technologies"
    }
    
    try:
        # Make registration request
        register_response = requests.post(f"{BASE_URL}/register/candidate", json=candidate_data)
        print(f"Registration response status: {register_response.status_code}")
        
        if register_response.status_code != 200:
            print("Registration failed!")
            print_json("Registration Error", register_response.json() if register_response.content else "No content")
            return None
            
        registration_data = register_response.json()
        print_json("Registration Response", registration_data)
        
        candidate_id = registration_data.get("id")
        if not candidate_id:
            print("Failed to get candidate ID from registration response")
            return None
            
        print(f"Candidate registered successfully with ID: {candidate_id}")
        return candidate_id
        
    except requests.exceptions.ConnectionError:
        print(f"\nError: Could not connect to the server at {BASE_URL}. Make sure the FastAPI server is running.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred during registration: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return None

def get_auth_token():
    """Get authentication token"""
    print("\nStep 2: Authenticating candidate...")
    
    login_data = {
        "username": CANDIDATE_EMAIL,
        "password": CANDIDATE_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        
        if response.status_code != 200:
            print(f"Login failed. Status: {response.status_code}")
            print_json("Login Error Response", response.json() if response.content else "No content")
            return None
            
        token = response.json().get("access_token")
        print("Authentication successful! Token obtained.")
        return token
        
    except requests.exceptions.RequestException as e:
        print(f"Authentication request failed: {e}")
        return None

def get_candidate_profile(candidate_id, token):
    """Get candidate profile details"""
    print("\nStep 3: Fetching candidate profile...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # First get basic profile
        print("Fetching basic profile information...")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        
        if profile_response.status_code != 200:
            print(f"Error fetching basic profile. Status: {profile_response.status_code}")
            print_json("Profile Error Response", profile_response.json() if profile_response.content else "No content")
            return False
            
        basic_profile = profile_response.json()
        print_json("Basic Profile Information", basic_profile)
        
        # Then get detailed candidate profile
        print(f"Fetching detailed candidate profile for ID: {candidate_id}...")
        detailed_response = requests.get(f"{BASE_URL}/candidate/{candidate_id}", headers=headers)
        
        if detailed_response.status_code != 200:
            print(f"Error fetching detailed profile. Status: {detailed_response.status_code}")
            print_json("Detailed Profile Error Response", detailed_response.json() if detailed_response.content else "No content")
            return False
            
        candidate_details = detailed_response.json()
        
        # Print profile information in sections for better readability
        print_json("PERSONAL INFORMATION", {
            "name": candidate_details.get("full_name"),
            "email": candidate_details.get("email"),
            "id": candidate_details.get("id"),
            "user_type": candidate_details.get("user_type"),
            "created_at": candidate_details.get("created_at"),
            "location": candidate_details.get("location"),
            "bio": candidate_details.get("bio")
        })
        
        print_json("PROFESSIONAL INFORMATION", {
            "skills": candidate_details.get("skills", []),
            "experience": candidate_details.get("experience"),
            "education": candidate_details.get("education")
        })
        
        print_json("ACCOUNT STATUS", {
            "is_active": candidate_details.get("is_active"),
            "profile_completed": candidate_details.get("profile_completed"),
            "last_active": candidate_details.get("last_active")
        })
        
        # Get job recommendations for the candidate
        print("\nStep 4: Fetching job recommendations...")
        recommendations_response = requests.get(f"{BASE_URL}/recommendations/jobs", headers=headers)
        
        if recommendations_response.status_code == 200:
            recommendations = recommendations_response.json()
            if recommendations:
                print_json(f"JOB RECOMMENDATIONS ({len(recommendations)})", recommendations)
            else:
                print("\n=== JOB RECOMMENDATIONS ===")
                print("No job recommendations available at this time.")
                print("-" * 80)
        else:
            print(f"Error fetching job recommendations. Status: {recommendations_response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"\nError: Could not connect to the server at {BASE_URL}. Make sure the FastAPI server is running.")
        return False
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return False

def run_candidate_flow():
    """Run the complete candidate flow from registration to profile viewing"""
    try:
        print("=== Candidate Registration and Profile Flow ===")
        print(f"Using email: {CANDIDATE_EMAIL}")
        
        # Step 1: Register candidate
        candidate_id = register_candidate()
        if not candidate_id:
            print("Candidate registration failed. Cannot proceed.")
            return
        
        # Step 2: Get authentication token
        token = get_auth_token()
        if not token:
            print("Authentication failed. Cannot proceed.")
            return
        
        # Step 3: View candidate profile
        success = get_candidate_profile(candidate_id, token)
        if success:
            print("\nCandidate flow completed successfully!")
        else:
            print("\nCandidate flow encountered errors.")
            
    except Exception as e:
        print(f"\nAn unexpected error occurred in the main flow: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    run_candidate_flow() 