import requests
import json

def test_employer_jobs():
    # API endpoints
    login_url = "http://localhost:8000/token"
    jobs_url = "http://localhost:8000/jobs"
    
    # Login credentials
    login_data = {
        "username": "test@employer.com",
        "password": "testpassword123"
    }
    
    try:
        # Step 1: Login to get token
        print("Step 1: Logging in...")
        login_response = requests.post(login_url, data=login_data)
        
        if login_response.status_code == 200:
            print("Login successful!")
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get employer profile to get employer_id
            profile_url = "http://localhost:8000/profile"
            profile_response = requests.get(profile_url, headers=headers)
            if profile_response.status_code != 200:
                print("Error getting employer profile")
                return
                
            employer_id = profile_response.json()["id"]
            
            # Job data for posting
            job_data = {
                "title": "Senior Python Developer",
                "company": "Tech Solutions Inc.",
                "description": "We are looking for an experienced Python developer to join our team.",
                "requirements": [
                    "5+ years of Python experience",
                    "Experience with FastAPI",
                    "Knowledge of MongoDB",
                    "Strong problem-solving skills"
                ],
                "location": "San Francisco, CA",
                "salary_range": "$120,000 - $150,000",
                "employer_id": employer_id
            }
            
            # Step 2: Post a new job
            print("\nStep 2: Posting a new job...")
            post_response = requests.post(jobs_url, headers=headers, json=job_data)
            
            if post_response.status_code == 200:
                print("Job posted successfully!")
                job = post_response.json()
                print("Job details:", json.dumps(job, indent=2))
            else:
                print(f"Error posting job: {post_response.status_code}")
                print("Response:", post_response.text)
        else:
            print(f"Error logging in: {login_response.status_code}")
            print("Response:", login_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_jobs() 