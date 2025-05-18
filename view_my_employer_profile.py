import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Hardcoded employer credentials
EMPLOYER_EMAIL = "test@employer.com"
EMPLOYER_PASSWORD = "testpassword123"

def print_json(title, data):
    """Helper function to print JSON data in a formatted way"""
    print(f"\n=== {title} ===")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str)) # Use default=str for datetime etc.
    else:
        print(data)
    print("-" * 80)

def get_auth_token(email, password):
    """Get authentication token"""
    login_data = {
        "username": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Login failed. Status: {response.status_code}")
            print_json("Login Error Response", response.json() if response.content else "No content")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Login request failed: {e}")
        return None

def view_own_employer_details():
    try:
        # Step 1: Login and get token using predefined credentials
        print(f"\nLogging in as {EMPLOYER_EMAIL}...")
        token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
        if not token:
            print("Could not authenticate. Please check credentials and server status.")
            return
        
        print("Login successful! Token obtained.")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Step 2: Get basic user profile to retrieve the employer ID
        print("\nFetching basic profile to get ID...")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        
        if profile_response.status_code != 200:
            print(f"Error fetching basic profile. Status: {profile_response.status_code}")
            print_json("Profile Error Response", profile_response.json() if profile_response.content else "No content")
            return
        
        basic_profile_data = profile_response.json()
        employer_id = basic_profile_data.get("id")
        user_type = basic_profile_data.get("user_type")

        if not employer_id:
            print_json("Error: ID not found in basic profile", basic_profile_data)
            return
        
        if user_type != "employer":
            print_json(f"Error: User {EMPLOYER_EMAIL} is a '{user_type}', not an employer.", basic_profile_data)
            return
            
        print(f"Employer ID {employer_id} obtained from basic profile.")

        # Step 3: Get detailed employer profile using the obtained ID
        print(f"\nFetching detailed employer profile for ID: {employer_id}...")
        detailed_response = requests.get(f"{BASE_URL}/employer/{employer_id}", headers=headers)
        
        if detailed_response.status_code == 200:
            employer_details = detailed_response.json()
            
            # Print sections of the profile for better readability
            print_json("BASIC INFORMATION", {
                "name": employer_details.get("full_name"),
                "email": employer_details.get("email"),
                "id": employer_details.get("id"),
                "user_type": employer_details.get("user_type"),
                "created_at": employer_details.get("created_at")
            })
            
            print_json("COMPANY INFORMATION", {
                "company_name": employer_details.get("company_name"),
                "industry": employer_details.get("industry"),
                "company_size": employer_details.get("company_size"),
                "company_description": employer_details.get("company_description"),
                "company_website": employer_details.get("company_website"),
                "company_location": employer_details.get("company_location")
            })
            
            print_json("CONTACT INFORMATION", {
                "contact_email": employer_details.get("contact_email"),
                "contact_phone": employer_details.get("contact_phone"),
                "location": employer_details.get("location")
            })
            
            print_json("ACCOUNT STATUS", {
                "is_active": employer_details.get("is_active"),
                "profile_completed": employer_details.get("profile_completed"),
                "verified": employer_details.get("verified"),
                "last_active": employer_details.get("last_active"),
                "account_type": employer_details.get("account_type"),
                "profile_views": employer_details.get("profile_views"),
                "total_jobs_posted": employer_details.get("total_jobs_posted"),
                "total_active_jobs": employer_details.get("total_active_jobs")
            })
            
            print_json("SOCIAL LINKS", employer_details.get("social_links", {}))
            
            # Print posted jobs if any
            posted_jobs = employer_details.get("posted_jobs", [])
            if posted_jobs:
                print_json(f"POSTED JOBS ({len(posted_jobs)})", posted_jobs)
            else:
                print("\n=== POSTED JOBS ===\nNo jobs posted yet.")
                print("-" * 80)
        else:
            print(f"Error fetching detailed employer profile. Status: {detailed_response.status_code}")
            print_json("Detailed Profile Error Response", detailed_response.json() if detailed_response.content else "No content")
                
    except requests.exceptions.ConnectionError:
        print(f"\nError: Could not connect to the server at {BASE_URL}. Make sure the FastAPI server is running.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    print("=== View Employer Profile Details ===")
    print(f"Using credentials for: {EMPLOYER_EMAIL}")
    view_own_employer_details() 