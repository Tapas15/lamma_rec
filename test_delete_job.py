# import requests
# import json

# def test_delete_job():
#     # API endpoints
#     login_url = "http://localhost:8000/token"
#     jobs_url = "http://localhost:8000/jobs"
    
#     # Login credentials
#     login_data = {
#         "username": "test@employer.com",
#         "password": "testpassword123"
#     }
    
#     try:
#         # Step 1: Login to get token
#         print("Step 1: Logging in...")
#         login_response = requests.post(login_url, data=login_data)
        
#         if login_response.status_code == 200:
#             print("Login successful!")
#             token = login_response.json()["access_token"]
#             headers = {"Authorization": f"Bearer {token}"}
            
#             while True:
#                 # Step 2: Get all jobs
#                 print("\nStep 2: Getting list of jobs...")
#                 get_jobs_response = requests.get(jobs_url, headers=headers)
                
#                 if get_jobs_response.status_code == 200:
#                     jobs = get_jobs_response.json()
#                     if not jobs:
#                         print("No jobs found.")
#                         break
                    
#                     # Display jobs with numbers
#                     print("\nAvailable jobs:")
#                     print("-" * 50)
#                     for i, job in enumerate(jobs, 1):
#                         print(f"{i}. Title: {job['title']}")
#                         print(f"   Company: {job['company']}")
#                         print(f"   Location: {job['location']}")
#                         print(f"   Salary: {job['salary_range']}")
#                         print("-" * 50)
                    
#                     print("\nOptions:")
#                     print("1. Delete a job")
#                     print("2. Exit")
                    
#                     choice = input("\nEnter your choice (1 or 2): ")
                    
#                     if choice == "1":
#                         job_number = input("Enter the number of the job to delete: ")
                        
#                         # Step 3: Delete the selected job
#                         print(f"\nDeleting job number {job_number}...")
#                         delete_url = f"{jobs_url}/{job_number}"
#                         delete_response = requests.delete(delete_url, headers=headers)
                        
#                         if delete_response.status_code == 200:
#                             print("Job deleted successfully!")
#                             print("Response:", json.dumps(delete_response.json(), indent=2))
#                         else:
#                             print(f"Error deleting job: {delete_response.status_code}")
#                             print("Response:", delete_response.text)
#                     elif choice == "2":
#                         print("Exiting...")
#                         break
#                     else:
#                         print("Invalid choice. Please enter 1 or 2.")
#                 else:
#                     print(f"Error getting jobs: {get_jobs_response.status_code}")
#                     print("Response:", get_jobs_response.text)
#                     break
#         else:
#             print(f"Error logging in: {login_response.status_code}")
#             print("Response:", login_response.text)
            
#     except Exception as e:
#         print(f"Error: {str(e)}")

# if __name__ == "__main__":
#     test_delete_job() 


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
                
                # Get job ID to delete
                job_id = input("\nEnter the Job ID to delete: ")
                
                # Step 3: Delete the selected job
                print(f"\nStep 3: Deleting job with ID {job_id}...")
                delete_url = f"{jobs_url}/{job_id}"
                delete_response = requests.delete(delete_url, headers=headers)
                
                if delete_response.status_code == 200:
                    print("Job deleted successfully!")
                    print("Response:", json.dumps(delete_response.json(), indent=2))
                else:
                    print(f"Error deleting job: {delete_response.status_code}")
                    print("Response:", delete_response.text)
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