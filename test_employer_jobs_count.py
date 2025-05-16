import requests
import json

def test_employer_jobs_count():
    # API endpoints
    login_url = "http://localhost:8000/token"
    employer_profile_url = "http://localhost:8000/employer/profile"
    jobs_url = "http://localhost:8000/jobs"
    
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
        
        # Step 2: Get employer profile
        print("\nStep 2: Getting employer profile...")
        profile_response = requests.get(employer_profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            print("Employer profile retrieved successfully!")
            profile_data = profile_response.json()
            
            # Print employer profile information
            print("\n" + "="*50)
            print("EMPLOYER PROFILE")
            print("="*50)
            print(f"Name: {profile_data.get('full_name')}")
            print(f"Email: {profile_data.get('email')}")
            print(f"Company: {profile_data.get('company_name')}")
            print(f"Location: {profile_data.get('location')}")
            print(f"Industry: {profile_data.get('industry')}")
            print("="*50)
            
            # Step 3: Get all jobs from jobs collection
            print("\nStep 3: Getting jobs from jobs collection...")
            jobs_response = requests.get(jobs_url, headers=headers)
            
            if jobs_response.status_code == 200:
                all_jobs = jobs_response.json()
                employer_jobs = [job for job in all_jobs if job.get('employer_id') == profile_data.get('id')]
                
                print("\n" + "="*50)
                print("JOBS STATISTICS")
                print("="*50)
                print(f"Total jobs posted: {len(employer_jobs)}")
                
                if employer_jobs:
                    print("\nJob List:")
                    print("-"*30)
                    for i, job in enumerate(employer_jobs, 1):
                        print(f"\nJob #{i}")
                        print(f"Title: {job.get('title')}")
                        print(f"Status: {'Active' if job.get('is_active') else 'Inactive'}")
                        print(f"Posted on: {job.get('created_at', 'N/A')}")
                        print("-"*30)
                else:
                    print("\nNo jobs found in jobs collection.")
            else:
                print(f"Error getting jobs: {jobs_response.status_code}")
                print("Response:", jobs_response.text)
        else:
            print(f"Error getting employer profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_jobs_count() 