import requests
import json

def test_employer_endpoints():
    # First login to get token
    login_url = "http://localhost:8000/token"
    login_data = {
        "username": "employer@techcompany.com",
        "password": "employerpass123"
    }
    
    try:
        # Login to get token
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print("Login failed!")
            return
            
        token = login_response.json()["access_token"]
        print("Successfully obtained access token")
        
        # Set up headers with token
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Get employer profile to get the ID
        profile_url = "http://localhost:8000/profile"
        profile_response = requests.get(profile_url, headers=headers)
        if profile_response.status_code != 200:
            print("Error getting employer profile!")
            print(f"Status code: {profile_response.status_code}")
            print(f"Response: {profile_response.text}")
            return
        
        employer_id = profile_response.json()["id"]
        print(f"Got employer ID: {employer_id}")
        
        # Test 1: Create a new job posting
        create_job_url = "http://localhost:8000/jobs"
        job_data = {
            "title": "Junior Python Developer",
            "company": "Tech Solutions Inc",
            "description": "We are looking for an experienced Python developer to join our team.",
            "requirements": [
                "2+ years of Python experience",
                "Experience with FastAPI and MongoDB",
                "Strong problem-solving skills"
            ],
            "location": "San Francisco",
            "salary_range": "$120,000 - $150,000",
            "employer_id": employer_id
        }
        
        print("\nTesting job creation...")
        job_response = requests.post(create_job_url, json=job_data, headers=headers)
        if job_response.status_code == 200:
            print("Successfully created job posting!")
            print("Job details:", json.dumps(job_response.json(), indent=2))
        else:
            print(f"Error creating job: {job_response.status_code}")
            print("Response:", job_response.text)
        
        # Test 2: Get all jobs
        print("\nTesting get all jobs...")
        jobs_response = requests.get(create_job_url, headers=headers)
        if jobs_response.status_code == 200:
            print("Successfully retrieved jobs!")
            print("Jobs:", json.dumps(jobs_response.json(), indent=2))
        else:
            print(f"Error getting jobs: {jobs_response.status_code}")
            print("Response:", jobs_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_endpoints() 