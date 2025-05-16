import requests
import json

def test_employer_profile():
    # API endpoints
    login_url = "http://localhost:8000/token"
    employer_profile_url = "http://localhost:8000/employer/profile"
    
        # Login credentials
    login_data = {
        "username": "test@employer.com",  # Replace with your email
        "password": "testpassword123"    # Replace with your password
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
        
        # Step 2: Get employer profile
        print("\nStep 2: Getting employer profile...")
        profile_response = requests.get(employer_profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            print("Employer profile retrieved successfully!")
            profile_data = profile_response.json()
            
            # Print basic profile information
            print("\nBasic Profile Information:")
            print(f"Name: {profile_data.get('full_name')}")
            print(f"Email: {profile_data.get('email')}")
            print(f"User Type: {profile_data.get('user_type')}")
            
            # Print posted jobs
            posted_jobs = profile_data.get('posted_jobs', [])
            print(f"\nPosted Jobs ({len(posted_jobs)}):")
            for job in posted_jobs:
                print("\nJob Details:")
                print(f"Title: {job.get('title')}")
                print(f"Company: {job.get('company')}")
                print(f"Location: {job.get('location')}")
                print(f"Status: {'Active' if job.get('is_active') else 'Inactive'}")
                print("Requirements:", ", ".join(job.get('requirements', [])))
                if job.get('salary_range'):
                    print(f"Salary Range: {job.get('salary_range')}")
        else:
            print(f"Error getting employer profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_profile() 