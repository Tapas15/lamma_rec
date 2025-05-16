import requests
import json

def test_delete_job_endpoint():
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
            
            # Step 2: Get all jobs posted by the employer
            print("\nStep 2: Getting posted jobs...")
            get_jobs_response = requests.get(jobs_url, headers=headers)
            
            if get_jobs_response.status_code == 200:
                jobs = get_jobs_response.json()
                if not jobs:
                    print("No jobs found to delete.")
                    return
                
                # Display jobs with numbers
                print("\nAvailable jobs:")
                print("-" * 50)
                for i, job in enumerate(jobs, 1):
                    print(f"{i}. Title: {job['title']}")
                    print(f"   Company: {job['company']}")
                    print(f"   Location: {job['location']}")
                    print(f"   Salary: {job['salary_range']}")
                    print(f"   Job ID: {job['id']}")
                    print("-" * 50)
                
                # Get job number to delete
                job_number = int(input("\nEnter the number (1, 2, 3, etc.) of the job to delete: "))
                if 1 <= job_number <= len(jobs):
                    job_to_delete = jobs[job_number - 1]
                    job_id = job_to_delete['id']
                    
                    # Step 3: Delete the selected job
                    print(f"\nStep 3: Deleting job '{job_to_delete['title']}'...")
                    delete_url = f"{jobs_url}/{job_id}"
                    delete_response = requests.delete(delete_url, headers=headers)
                    
                    if delete_response.status_code == 200:
                        print("Job deleted successfully!")
                        print("Response:", json.dumps(delete_response.json(), indent=2))
                    else:
                        print(f"Error deleting job: {delete_response.status_code}")
                        print("Response:", delete_response.text)
                else:
                    print("Invalid job number selected.")
            else:
                print(f"Error getting jobs: {get_jobs_response.status_code}")
                print("Response:", get_jobs_response.text)
        else:
            print(f"Error logging in: {login_response.status_code}")
            print("Response:", login_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_delete_job_endpoint() 