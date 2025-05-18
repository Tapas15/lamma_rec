import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_json(title, data):
    """Helper function to print JSON data in a formatted way"""
    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2))
    print("-" * 80)

def test_full_employer_flow():
    try:
        # Step 1: Register a new employer
        print("\nStep 1: Registering new employer...")
        
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
            "linkedin": "https://linkedin.com/company/techinnovations",
            "twitter": "@techinnovations"
        }
        
        register_response = requests.post(f"{BASE_URL}/register/employer", json=employer_data)
        print(f"Registration response status: {register_response.status_code}")
        
        if register_response.status_code != 200:
            print("Registration failed!")
            print("Response:", register_response.text)
            return
            
        registration_data = register_response.json()
        print_json("Registration Response", registration_data)
        employer_id = registration_data["id"]
        print(f"Employer ID: {employer_id}")
        
        # Step 2: Login with new credentials
        print("\nStep 2: Testing login...")
        login_data = {
            "username": employer_data["email"],
            "password": employer_data["password"]
        }
        
        login_response = requests.post(f"{BASE_URL}/token", data=login_data)
        if login_response.status_code != 200:
            print("Login failed!")
            print("Response:", login_response.text)
            return
            
        token = login_response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("Login successful!")
        
        # Step 3: Get profile using token
        print("\nStep 3: Getting profile...")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if profile_response.status_code == 200:
            print_json("Profile Data", profile_response.json())
        else:
            print(f"Error getting profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
        
        # Step 4: Get detailed profile using ID
        print("\nStep 4: Getting detailed profile...")
        detailed_response = requests.get(f"{BASE_URL}/employer/{employer_id}", headers=headers)
        if detailed_response.status_code == 200:
            print_json("Detailed Profile", detailed_response.json())
        else:
            print(f"Error getting detailed profile: {detailed_response.status_code}")
            print("Response:", detailed_response.text)
        
        # Step 5: Create a test job posting
        print("\nStep 5: Creating a test job posting...")
        job_data = {
            "title": "Senior Python Developer",
            "company": "Tech Innovations Inc.",
            "description": "Looking for an experienced Python developer to join our AI team.",
            "requirements": ["Python", "FastAPI", "MongoDB", "AI/ML"],
            "location": "San Francisco Bay Area",
            "salary_range": "$150,000 - $200,000",
            "employer_id": employer_id
        }
        
        job_response = requests.post(f"{BASE_URL}/jobs", headers=headers, json=job_data)
        if job_response.status_code == 200:
            print_json("Created Job", job_response.json())
        else:
            print(f"Error creating job: {job_response.status_code}")
            print("Response:", job_response.text)
        
        # Step 6: Get updated profile with jobs
        print("\nStep 6: Getting final profile with jobs...")
        final_response = requests.get(f"{BASE_URL}/employer/{employer_id}", headers=headers)
        if final_response.status_code == 200:
            print_json("Final Profile with Jobs", final_response.json())
        else:
            print(f"Error getting final profile: {final_response.status_code}")
            print("Response:", final_response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    print("=== Testing Full Employer Flow ===")
    test_full_employer_flow() 