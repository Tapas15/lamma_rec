import requests
import json

def test_employer_recommendations():
    # Employer login
    login_url = "http://localhost:8000/token"
    login_data = {
        "username": "test@employer.com",
        "password": "testpassword123"
    }
    
    try:
        # Login to get token
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print("Employer login failed!")
            print(login_response.text)
            return
        token = login_response.json()["access_token"]
        print("Employer login successful! Token obtained.")
        
        # Get all jobs
        jobs_url = "http://localhost:8000/jobs"
        headers = {"Authorization": f"Bearer {token}"}
        jobs_response = requests.get(jobs_url, headers=headers)
        if jobs_response.status_code != 200:
            print("Error fetching jobs!")
            print(jobs_response.text)
            return
        jobs = jobs_response.json()
        if not jobs:
            print("No jobs found for employer.")
            return
        job_id = jobs[0]["id"]
        print(f"Using job ID: {job_id}")
        
        # Get candidate recommendations for the first job
        rec_url = f"http://localhost:8000/recommendations/candidates/{job_id}"
        rec_response = requests.get(rec_url, headers=headers)
        if rec_response.status_code == 200:
            print("\nCandidate recommendations for job:")
            print(json.dumps(rec_response.json(), indent=2))
            print(f"Comparing candidate IDs: rec['candidate_id']={rec_response.json()[0]['candidate_id']} vs candidates:")
            for c in rec_response.json():
                print(f"  candidate['_id']={c['candidate_id']} (type: {type(c['candidate_id'])})")
        else:
            print(f"Error fetching recommendations: {rec_response.status_code}")
            print(rec_response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_recommendations() 