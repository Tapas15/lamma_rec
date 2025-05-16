import requests
import json

def test_employer_profile():
    # API endpoints
    login_url = "http://localhost:8000/token"
    employer_profile_url = "http://localhost:8000/employer/profile"
    
    # Login credentials
    login_data = {
        "username": "test@employer.com",
        "password": "testpassword123"
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
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful!")
        
        # Step 2: Get employer profile from employers collection
        print("\nStep 2: Getting employer profile from employers collection...")
        profile_response = requests.get(employer_profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            print("Employer profile retrieved successfully!")
            profile_data = profile_response.json()
            
            # Print employer profile information from employers collection
            print("\n" + "="*50)
            print("EMPLOYER PROFILE (FROM EMPLOYERS COLLECTION)")
            print("="*50)
            print("Basic Information:")
            print("-"*30)
            print(f"Name: {profile_data.get('full_name')}")
            print(f"Email: {profile_data.get('email')}")
            print(f"User Type: {profile_data.get('user_type')}")
            print(f"Created At: {profile_data.get('created_at')}")
            
            print("\nCompany Information:")
            print("-"*30)
            print(f"Company Name: {profile_data.get('company_name')}")
            print(f"Company Description: {profile_data.get('company_description')}")
            print(f"Company Website: {profile_data.get('company_website')}")
            print(f"Company Location: {profile_data.get('company_location')}")
            print(f"Company Size: {profile_data.get('company_size')}")
            print(f"Industry: {profile_data.get('industry')}")
            
            print("\nContact Information:")
            print("-"*30)
            print(f"Contact Email: {profile_data.get('contact_email')}")
            print(f"Contact Phone: {profile_data.get('contact_phone')}")
            print(f"Location: {profile_data.get('location')}")
            
            print("\nAdditional Information:")
            print("-"*30)
            print(f"Bio: {profile_data.get('bio')}")
            print("="*50)
            
            # Print posted jobs if available
            posted_jobs = profile_data.get('posted_jobs', [])
            print(f"\nPOSTED JOBS ({len(posted_jobs)})")
            print("="*50)
            
            if not posted_jobs:
                print("No jobs posted yet.")
            else:
                for i, job in enumerate(posted_jobs, 1):
                    print(f"\nJob #{i}")
                    print("-"*30)
                    print(f"Title: {job.get('title')}")
                    print(f"Company: {job.get('company')}")
                    print(f"Location: {job.get('location')}")
                    print(f"Status: {'Active' if job.get('is_active') else 'Inactive'}")
                    print(f"Salary Range: {job.get('salary_range')}")
                    print("\nRequirements:")
                    for req in job.get('requirements', []):
                        print(f"- {req}")
                    print("\nDescription:")
                    print(job.get('description', 'No description provided'))
                    print("-"*30)
        else:
            print(f"Error getting employer profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_profile() 