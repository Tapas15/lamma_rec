import requests
import json

def test_update_employer_profile():
    # API endpoints
    login_url = "http://localhost:8000/token"
    employer_profile_url = "http://localhost:8000/employer/profile"
    
    # Login credentials
    login_data = {
        "username": "employer@techcompany.com",
        "password": "employerpass123"
    }
    
    # Updated profile data
    update_data = {
        "full_name": "Updated Tech Company",
        "company_name": "Tech Solutions Inc.",
        "company_description": "Leading technology solutions provider",
        "company_website": "https://techsolutions.com",
        "company_location": "San Francisco, CA",
        "company_size": "100-500",
        "industry": "Technology",
        "contact_email": "hr@techsolutions.com",
        "contact_phone": "+1-555-0123"
    }
    
    try:
        # Step 1: Login and get token
        print("Step 1: Logging in as employer...")
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print("Response:", login_response.text)
            return
            
        token = login_response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("Login successful!")
        
        # Step 2: Get current profile
        print("\nStep 2: Getting current employer profile...")
        profile_response = requests.get(employer_profile_url, headers=headers)
        if profile_response.status_code == 200:
            print("Current profile retrieved successfully!")
            current_profile = profile_response.json()
            print("\nCurrent Profile:")
            print(json.dumps(current_profile, indent=2))
        else:
            print(f"Error getting current profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
            return
        
        # Step 3: Update profile
        print("\nStep 3: Updating employer profile...")
        update_response = requests.put(employer_profile_url, headers=headers, json=update_data)
        
        if update_response.status_code == 200:
            print("Profile updated successfully!")
            updated_profile = update_response.json()
            
            # Print updated profile information
            print("\nUpdated Profile Information:")
            print(f"Name: {updated_profile.get('full_name')}")
            print(f"Email: {updated_profile.get('email')}")
            print(f"User Type: {updated_profile.get('user_type')}")
            print(f"Company Name: {updated_profile.get('company_name')}")
            print(f"Company Description: {updated_profile.get('company_description')}")
            print(f"Company Website: {updated_profile.get('company_website')}")
            print(f"Company Location: {updated_profile.get('company_location')}")
            print(f"Company Size: {updated_profile.get('company_size')}")
            print(f"Industry: {updated_profile.get('industry')}")
            print(f"Contact Email: {updated_profile.get('contact_email')}")
            print(f"Contact Phone: {updated_profile.get('contact_phone')}")
            
            # Print posted jobs
            posted_jobs = updated_profile.get('posted_jobs', [])
            print(f"\nPosted Jobs ({len(posted_jobs)}):")
            for job in posted_jobs:
                print("\nJob Details:")
                print(f"Title: {job.get('title')}")
                print(f"Company: {job.get('company')}")
                print(f"Location: {job.get('location')}")
                print(f"Status: {'Active' if job.get('is_active') else 'Inactive'}")
        else:
            print(f"Error updating profile: {update_response.status_code}")
            print("Response:", update_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_update_employer_profile() 