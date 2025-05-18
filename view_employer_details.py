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

def get_auth_token(email, password):
    """Get authentication token"""
    login_data = {
        "username": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/token", data=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def view_employer_details():
    # Employer credentials
    employer_email = "test@employer.com"
    employer_password = "testpassword123"
    
    try:
        # Step 1: Login and get token
        print("\nLogging in as employer...")
        token = get_auth_token(employer_email, employer_password)
        if not token:
            print("Failed to login. Please check credentials.")
            return
        print("Login successful! Token received.")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Step 2: Get employer profile
        print("\nFetching employer profile...")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if profile_response.status_code != 200:
            print(f"Error getting profile. Status code: {profile_response.status_code}")
            print("Response:", profile_response.text)
            return
            
        profile_data = profile_response.json()
        print_json("Employer Basic Profile", profile_data)
        
        if "id" not in profile_data:
            print("Error: No ID found in profile data")
            print("Available fields:", list(profile_data.keys()))
            return
            
        # Step 3: Get detailed employer profile with posted jobs
        employer_id = profile_data["id"]
        print(f"\nFetching detailed profile for employer ID: {employer_id}")
        
        detailed_response = requests.get(f"{BASE_URL}/employer/{employer_id}", headers=headers)
        print(f"Detailed profile response status: {detailed_response.status_code}")
        
        if detailed_response.status_code != 200:
            print("Error getting detailed profile.")
            print("Response:", detailed_response.text)
            return
            
        employer_data = detailed_response.json()
        
        # Print company information
        company_info = {
            "company_name": employer_data.get("company_name", "Not found"),
            "company_description": employer_data.get("company_description", "Not found"),
            "company_website": employer_data.get("company_website", "Not found"),
            "company_location": employer_data.get("company_location", "Not found"),
            "company_size": employer_data.get("company_size", "Not found"),
            "industry": employer_data.get("industry", "Not found")
        }
        print_json("Company Information", company_info)
        
        # Print contact information
        contact_info = {
            "full_name": employer_data.get("full_name", "Not found"),
            "contact_email": employer_data.get("contact_email", "Not found"),
            "contact_phone": employer_data.get("contact_phone", "Not found"),
            "location": employer_data.get("location", "Not found")
        }
        print_json("Contact Information", contact_info)
        
        # Print account status
        account_status = {
            "id": employer_data.get("id", "Not found"),
            "email": employer_data.get("email", "Not found"),
            "user_type": employer_data.get("user_type", "Not found"),
            "created_at": employer_data.get("created_at", "Not found"),
            "is_active": employer_data.get("is_active", "Not found"),
            "profile_completed": employer_data.get("profile_completed", "Not found"),
            "verified": employer_data.get("verified", "Not found"),
            "last_active": employer_data.get("last_active", "Not found")
        }
        print_json("Account Status", account_status)
        
        # Print social links
        social_links = employer_data.get("social_links", {})
        print_json("Social Links", social_links)
        
        # Print posted jobs
        posted_jobs = employer_data.get("posted_jobs", [])
        if posted_jobs:
            print_json(f"Posted Jobs ({len(posted_jobs)} jobs)", posted_jobs)
        else:
            print("\nNo jobs posted yet.")
        
        # Step 4: Get employer's projects
        print("\nFetching employer projects...")
        projects_response = requests.get(f"{BASE_URL}/employer/projects", headers=headers)
        if projects_response.status_code == 200:
            projects = projects_response.json()
            if projects:
                print_json(f"Active Projects ({len(projects)} projects)", projects)
            else:
                print("\nNo active projects found.")
        else:
            print(f"Error getting projects. Status code: {projects_response.status_code}")
            print("Response:", projects_response.text)
                
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())

def main():
    print("=== Viewing Detailed Employer Information ===")
    view_employer_details()

if __name__ == "__main__":
    main() 