import requests
import json
import sys
from tabulate import tabulate
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

class CandidatePortal:
    def __init__(self):
        self.token = None
        self.headers = None
    
    def login(self):
        login_data = {
            "username": "candidate@gmail.com",
            "password": 'candidatepass123'
        }
        try:
            response = requests.post(f"{BASE_URL}/token", data=login_data)
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                return True
            else:
                print(f"Login failed. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    def get_jobs(self):
        if not self.token:
            print("Please login first.")
            return []
        
        try:
            response = requests.get(f"{BASE_URL}/jobs", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get jobs. Status: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting jobs: {str(e)}")
            return []
    
    def apply_for_job(self, job_id, cover_letter=None, resume_url=None, notes=None):
        if not self.token:
            print("Please login first.")
            return False
        
        application_data = {
            "job_id": job_id,
            "cover_letter": cover_letter,
            "resume_url": resume_url,
            "notes": notes
        }
        
        try:
            response = requests.post(f"{BASE_URL}/applications", 
                                    headers=self.headers, 
                                    json=application_data)
            if response.status_code == 200:
                print("Application submitted successfully!")
                return True
            else:
                print(f"Failed to apply for job. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error applying for job: {str(e)}")
            return False
    
    def update_application(self, application_id, cover_letter=None, notes=None):
        if not self.token:
            print("Please login first.")
            return False
        
        update_data = {}
        if cover_letter is not None:
            update_data["cover_letter"] = cover_letter
        if notes is not None:
            update_data["notes"] = notes
        
        try:
            # Using PATCH to update only specified fields
            response = requests.patch(f"{BASE_URL}/applications/{application_id}", 
                                    headers=self.headers, 
                                    json=update_data)
            if response.status_code == 200:
                print("Application updated successfully!")
                return True
            else:
                print(f"Failed to update application. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error updating application: {str(e)}")
            return False
    
    def delete_application(self, application_id):
        if not self.token:
            print("Please login first.")
            return False
        
        try:
            response = requests.delete(f"{BASE_URL}/applications/{application_id}", 
                                      headers=self.headers)
            if response.status_code == 200:
                print("Application withdrawn successfully!")
                return True
            else:
                print(f"Failed to withdraw application. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error withdrawing application: {str(e)}")
            return False
    
    def save_job(self, job_id, notes=None):
        if not self.token:
            print("Please login first.")
            return False
        
        saved_job_data = {
            "job_id": job_id,
            "notes": notes
        }
        
        try:
            response = requests.post(f"{BASE_URL}/saved-jobs", 
                                    headers=self.headers, 
                                    json=saved_job_data)
            if response.status_code == 200:
                print("Job saved successfully!")
                return True
            else:
                print(f"Failed to save job. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error saving job: {str(e)}")
            return False
    
    def update_saved_job(self, saved_job_id, notes):
        if not self.token:
            print("Please login first.")
            return False
        
        update_data = {"notes": notes}
        
        try:
            # Using PATCH to update only specified fields
            response = requests.patch(f"{BASE_URL}/saved-jobs/{saved_job_id}", 
                                     headers=self.headers, 
                                     json=update_data)
            if response.status_code == 200:
                print("Saved job updated successfully!")
                return True
            else:
                print(f"Failed to update saved job. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error updating saved job: {str(e)}")
            return False
    
    def delete_saved_job(self, saved_job_id):
        if not self.token:
            print("Please login first.")
            return False
        
        try:
            response = requests.delete(f"{BASE_URL}/saved-jobs/{saved_job_id}", 
                                      headers=self.headers)
            if response.status_code == 200:
                print("Saved job removed successfully!")
                return True
            else:
                print(f"Failed to remove saved job. Status: {response.status_code}")
                print(f"Error: {response.json().get('detail', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Error removing saved job: {str(e)}")
            return False
    
    def get_applications(self):
        if not self.token:
            print("Please login first.")
            return []
        
        try:
            response = requests.get(f"{BASE_URL}/applications", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get applications. Status: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting applications: {str(e)}")
            return []
    
    def get_saved_jobs(self):
        if not self.token:
            print("Please login first.")
            return []
        
        try:
            response = requests.get(f"{BASE_URL}/saved-jobs", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get saved jobs. Status: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting saved jobs: {str(e)}")
            return []

def display_jobs(jobs):
    if not jobs:
        print("No jobs available.")
        return
    
    job_table = []
    for i, job in enumerate(jobs, 1):
        job_table.append([
            i,
            job.get("id"),
            job.get("title"),
            job.get("company"),
            job.get("location"),
            job.get("salary_range", "Not specified")
        ])
    
    print("\n" + tabulate(job_table, 
                        headers=["#", "ID", "Title", "Company", "Location", "Salary Range"],
                        tablefmt="grid"))

def display_applications(applications):
    if not applications:
        print("No job applications found.")
        return
    
    app_table = []
    for i, app in enumerate(applications, 1):
        job_details = app.get("job_details", {})
        app_table.append([
            i,
            app.get("id"),
            job_details.get("title", "Unknown"),
            job_details.get("company", "Unknown"),
            app.get("status"),
            app.get("created_at")
        ])
    
    print("\n" + tabulate(app_table, 
                        headers=["#", "ID", "Job Title", "Company", "Status", "Applied Date"],
                        tablefmt="grid"))

def display_saved_jobs(saved_jobs):
    if not saved_jobs:
        print("No saved jobs found.")
        return
    
    saved_table = []
    for i, saved in enumerate(saved_jobs, 1):
        job_details = saved.get("job_details", {})
        saved_table.append([
            i,
            saved.get("id"),
            job_details.get("title", "Unknown"),
            job_details.get("company", "Unknown"),
            job_details.get("location", "Unknown"),
            saved.get("created_at")
        ])
    
    print("\n" + tabulate(saved_table, 
                        headers=["#", "ID", "Job Title", "Company", "Location", "Saved Date"],
                        tablefmt="grid"))

def main():
    portal = CandidatePortal()
    
    print("=== Candidate Job Portal ===")
    
    # Login using hardcoded credentials
    if not portal.login():
        print("Login failed. Exiting...")
        sys.exit(1)
    
    print("\nLogin successful!")
    
    while True:
        print("\n=== Candidate Job Portal Menu ===")
        print("1. View Available Jobs")
        print("2. Apply for a Job")
        print("3. Save a Job")
        print("4. View My Applications")
        print("5. Update an Application")
        print("6. Withdraw an Application")
        print("7. View My Saved Jobs")
        print("8. Update a Saved Job")
        print("9. Remove a Saved Job")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-9): ")
        
        if choice == "1":
            jobs = portal.get_jobs()
            display_jobs(jobs)
        
        elif choice == "2":
            jobs = portal.get_jobs()
            display_jobs(jobs)
            
            job_index = input("\nEnter job number to apply for (or 0 to cancel): ")
            if job_index.isdigit() and 0 < int(job_index) <= len(jobs):
                job = jobs[int(job_index) - 1]
                print(f"\nApplying for: {job['title']} at {job['company']}")
                
                cover_letter = input("Enter cover letter (optional): ")
                notes = input("Enter additional notes (optional): ")
                
                portal.apply_for_job(
                    job_id=job["id"], 
                    cover_letter=cover_letter if cover_letter else None,
                    notes=notes if notes else None
                )
            elif job_index == "0":
                print("Application cancelled.")
            else:
                print("Invalid job number.")
        
        elif choice == "3":
            jobs = portal.get_jobs()
            display_jobs(jobs)
            
            job_index = input("\nEnter job number to save (or 0 to cancel): ")
            if job_index.isdigit() and 0 < int(job_index) <= len(jobs):
                job = jobs[int(job_index) - 1]
                print(f"\nSaving job: {job['title']} at {job['company']}")
                
                notes = input("Enter notes (optional): ")
                
                portal.save_job(
                    job_id=job["id"],
                    notes=notes if notes else None
                )
            elif job_index == "0":
                print("Save cancelled.")
            else:
                print("Invalid job number.")
        
        elif choice == "4":
            applications = portal.get_applications()
            display_applications(applications)
        
        elif choice == "5":
            applications = portal.get_applications()
            display_applications(applications)
            
            if not applications:
                continue
                
            app_index = input("\nEnter application number to update (or 0 to cancel): ")
            if app_index.isdigit() and 0 < int(app_index) <= len(applications):
                app = applications[int(app_index) - 1]
                print(f"\nUpdating application for: {app['job_details'].get('title', 'Unknown Job')}")
                
                cover_letter = input("Enter new cover letter (leave blank to keep current): ")
                notes = input("Enter new notes (leave blank to keep current): ")
                
                portal.update_application(
                    application_id=app["id"],
                    cover_letter=cover_letter if cover_letter else None,
                    notes=notes if notes else None
                )
            elif app_index == "0":
                print("Update cancelled.")
            else:
                print("Invalid application number.")
        
        elif choice == "6":
            applications = portal.get_applications()
            display_applications(applications)
            
            if not applications:
                continue
                
            app_index = input("\nEnter application number to withdraw (or 0 to cancel): ")
            if app_index.isdigit() and 0 < int(app_index) <= len(applications):
                app = applications[int(app_index) - 1]
                
                confirm = input(f"Are you sure you want to withdraw application for {app['job_details'].get('title', 'Unknown Job')}? (y/n): ")
                if confirm.lower() == 'y':
                    portal.delete_application(app["id"])
                else:
                    print("Withdrawal cancelled.")
            elif app_index == "0":
                print("Withdrawal cancelled.")
            else:
                print("Invalid application number.")
        
        elif choice == "7":
            saved_jobs = portal.get_saved_jobs()
            display_saved_jobs(saved_jobs)
        
        elif choice == "8":
            saved_jobs = portal.get_saved_jobs()
            display_saved_jobs(saved_jobs)
            
            if not saved_jobs:
                continue
                
            saved_index = input("\nEnter saved job number to update (or 0 to cancel): ")
            if saved_index.isdigit() and 0 < int(saved_index) <= len(saved_jobs):
                saved = saved_jobs[int(saved_index) - 1]
                print(f"\nUpdating saved job: {saved['job_details'].get('title', 'Unknown Job')}")
                
                notes = input("Enter new notes: ")
                
                portal.update_saved_job(
                    saved_job_id=saved["id"],
                    notes=notes
                )
            elif saved_index == "0":
                print("Update cancelled.")
            else:
                print("Invalid saved job number.")
        
        elif choice == "9":
            saved_jobs = portal.get_saved_jobs()
            display_saved_jobs(saved_jobs)
            
            if not saved_jobs:
                continue
                
            saved_index = input("\nEnter saved job number to remove (or 0 to cancel): ")
            if saved_index.isdigit() and 0 < int(saved_index) <= len(saved_jobs):
                saved = saved_jobs[int(saved_index) - 1]
                
                confirm = input(f"Are you sure you want to remove saved job {saved['job_details'].get('title', 'Unknown Job')}? (y/n): ")
                if confirm.lower() == 'y':
                    portal.delete_saved_job(saved["id"])
                else:
                    print("Removal cancelled.")
            elif saved_index == "0":
                print("Removal cancelled.")
            else:
                print("Invalid saved job number.")
        
        elif choice == "0":
            print("Thank you for using the Candidate Job Portal. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 