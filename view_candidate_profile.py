import requests
import json

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

def get_auth_token():
    """Get authentication token"""
    login_data = {
        "username": CANDIDATE_EMAIL,
        "password": CANDIDATE_PASSWORD
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

def view_candidate_profile():
    """View candidate profile details"""
    try:
        # Step 1: Login and get token
        print(f"\nLogging in as {CANDIDATE_EMAIL}...")
        token = get_auth_token()
        if not token:
            print("Could not authenticate. Please check credentials and server status.")
            return
        
        print("Login successful! Token obtained.")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Step 2: Get basic profile to retrieve ID
        print("\nFetching basic profile to get ID...")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        
        if profile_response.status_code != 200:
            print(f"Error fetching basic profile. Status: {profile_response.status_code}")
            print_json("Profile Error Response", profile_response.json() if profile_response.content else "No content")
            return
        
        basic_profile = profile_response.json()
        candidate_id = basic_profile.get("id")
        user_type = basic_profile.get("user_type")

        if not candidate_id:
            print_json("Error: ID not found in basic profile", basic_profile)
            return
        
        if user_type != "candidate":
            print_json(f"Error: User {CANDIDATE_EMAIL} is a '{user_type}', not a candidate.", basic_profile)
            return
            
        print(f"Candidate ID {candidate_id} obtained from basic profile.")

        # Step 3: Get detailed candidate profile
        print(f"\nFetching detailed candidate profile for ID: {candidate_id}...")
        detailed_response = requests.get(f"{BASE_URL}/candidate/{candidate_id}", headers=headers)
        
        if detailed_response.status_code != 200:
            print(f"Error fetching detailed profile. Status: {detailed_response.status_code}")
            print_json("Detailed Profile Error Response", detailed_response.json() if detailed_response.content else "No content")
            return
            
        candidate_details = detailed_response.json()
        
        # Print profile information in sections for better readability
        print_json("PERSONAL INFORMATION", {
            "name": candidate_details.get("full_name", "Not provided"),
            "email": candidate_details.get("email", "Not provided"),
            "id": candidate_details.get("id", "Not provided"),
            "user_type": candidate_details.get("user_type", "Not provided"),
            "created_at": candidate_details.get("created_at", "Not provided"),
            "location": candidate_details.get("location", "Not provided"),
            "bio": candidate_details.get("bio", "Not provided")
        })
        
        print_json("PROFESSIONAL INFORMATION", {
            "skills": candidate_details.get("skills", []),
            "experience": candidate_details.get("experience", "Not provided"),
            "education": candidate_details.get("education", "Not provided"),
            "resume_url": candidate_details.get("resume_url", "No resume uploaded")
        })
        
        # Get job preferences with fallback for each field
        job_preferences = candidate_details.get("job_preferences", {})
        if not isinstance(job_preferences, dict):
            job_preferences = {}
            
        print_json("JOB PREFERENCES", {
            "job_types": job_preferences.get("job_types", []),
            "preferred_locations": job_preferences.get("preferred_locations", []),
            "salary_expectation": job_preferences.get("salary_expectation", "Not specified"),
            "remote_work": job_preferences.get("remote_work", "Not specified"),
            "match_score_threshold": candidate_details.get("match_score_threshold", 70)
        })
        
        print_json("ACCOUNT STATUS", {
            "is_active": candidate_details.get("is_active", False),
            "profile_completed": candidate_details.get("profile_completed", False),
            "last_active": candidate_details.get("last_active", "Never"),
            "profile_visibility": candidate_details.get("profile_visibility", "private"),
            "profile_views": candidate_details.get("profile_views", 0),
            "applications_count": len(candidate_details.get("job_applications", [])),
            "saved_jobs_count": len(candidate_details.get("saved_jobs", []))
        })
        
        # Step 4: Get job recommendations
        print("\nFetching job recommendations...")
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
            
        # Display job applications if available
        job_applications = candidate_details.get("job_applications", [])
        if job_applications:
            print_json(f"JOB APPLICATIONS ({len(job_applications)})", job_applications)
        else:
            print("\n=== JOB APPLICATIONS ===")
            print("No job applications found.")
            print("-" * 80)
            
        # Display saved jobs if available
        saved_jobs = candidate_details.get("saved_jobs", [])
        if saved_jobs:
            print_json(f"SAVED JOBS ({len(saved_jobs)})", saved_jobs)
        else:
            print("\n=== SAVED JOBS ===")
            print("No saved jobs found.")
            print("-" * 80)
            
    except requests.exceptions.ConnectionError:
        print(f"\nError: Could not connect to the server at {BASE_URL}. Make sure the FastAPI server is running.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    print("=== View Candidate Profile Details ===")
    print(f"Using credentials for: {CANDIDATE_EMAIL}")
    view_candidate_profile() 