import requests
import json
import time
from datetime import datetime
from tabulate import tabulate

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test candidate credentials
CANDIDATE_EMAIL = "candidate@example.com"
CANDIDATE_PASSWORD = "candidatepass123"

# Test employer credentials (to create jobs that the candidate can apply for)
EMPLOYER_EMAIL = "test@employer.com"
EMPLOYER_PASSWORD = "testpassword123"

def print_json(title, data):
    """Helper function to print JSON data in a formatted way"""
    print(f"\n=== {title} ===")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str))  # Use default=str for datetime objects
    else:
        print(data)
    print("-" * 80)

def print_section(title):
    """Print a section title for better readability"""
    print("\n")
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def get_auth_token(email, password):
    """Get authentication token"""
    login_data = {
        "username": email,
        "password": password
    }
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Login failed for {email}. Status: {response.status_code}")
            print_json("Login Error Response", response.json() if response.content else "No content")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Authentication request failed: {e}")
        return None

def register_candidate():
    """Register a test candidate"""
    print_section("REGISTERING TEST CANDIDATE")
    
    candidate_data = {
        "email": CANDIDATE_EMAIL,
        "password": CANDIDATE_PASSWORD,
        "full_name": "Test Candidate Flow",
        "user_type": "candidate",
        "skills": ["Python", "React", "MongoDB", "FastAPI", "Data Analysis"],
        "experience": "6 years in software development and data science",
        "education": "MS in Computer Science, BS in Statistics",
        "location": "San Francisco, CA",
        "bio": "Experienced full-stack developer with a passion for data-driven applications"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register/candidate", json=candidate_data)
        if response.status_code == 200:
            print("✅ Candidate registered successfully")
            return response.json()
        # If the candidate already exists, try to log in instead
        elif response.status_code == 400 and "Email already registered" in response.json().get("detail", ""):
            print("ℹ️ Candidate already registered, attempting to login...")
            token = get_auth_token(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
            if token:
                print("✅ Logged in with existing candidate account")
                return {"id": "existing", "email": CANDIDATE_EMAIL}
            else:
                print("❌ Failed to login with existing account")
                return None
        else:
            print(f"❌ Candidate registration failed. Status: {response.status_code}")
            print_json("Registration Error", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error registering candidate: {str(e)}")
        return None

def register_employer_and_create_jobs():
    """Register an employer and create test jobs for the candidate to apply to"""
    print_section("REGISTERING TEST EMPLOYER AND CREATING JOBS")
    
    employer_data = {
        "email": EMPLOYER_EMAIL,
        "password": EMPLOYER_PASSWORD,
        "full_name": "Test Employer Flow",
        "user_type": "employer",
        "company_name": "Flow Tech Solutions",
        "company_description": "Innovative tech company focused on AI solutions",
        "company_website": "https://flowtech.example.com",
        "company_location": "Austin, TX",
        "company_size": "50-200",
        "industry": "Technology",
        "contact_email": "hr@flowtech.example.com",
        "contact_phone": "+1-555-987-6543",
        "location": "Austin, TX",
        "bio": "Building the future with innovative technologies"
    }
    
    try:
        # Register employer
        response = requests.post(f"{BASE_URL}/register/employer", json=employer_data)
        
        employer_id = None
        
        if response.status_code == 200:
            print("✅ Employer registered successfully")
            employer_id = response.json().get("id")
        elif response.status_code == 400 and "Email already registered" in response.json().get("detail", ""):
            print("ℹ️ Employer already registered, attempting to login...")
            token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
            if token:
                print("✅ Logged in with existing employer account")
                # Get employer profile to retrieve ID
                headers = {"Authorization": f"Bearer {token}"}
                profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
                if profile_response.status_code == 200:
                    employer_id = profile_response.json().get("id")
                    print(f"✅ Retrieved employer ID: {employer_id}")
                else:
                    print("❌ Failed to get employer profile")
            else:
                print("❌ Failed to login with existing employer account")
                return None
        else:
            print(f"❌ Employer registration failed. Status: {response.status_code}")
            print_json("Registration Error", response.json() if response.content else "No content")
            return None
        
        if not employer_id:
            print("❌ Failed to obtain employer ID")
            return None
        
        # Get auth token for employer
        token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
        if not token:
            print("❌ Failed to get employer auth token")
            return None
        
        # Create test jobs
        print("\nCreating test jobs...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        job_descriptions = [
            {
                "title": "Senior Data Scientist",
                "company": "Flow Tech Solutions",
                "description": "Looking for an experienced data scientist to lead our AI initiatives and develop cutting-edge machine learning models.",
                "requirements": ["Python", "Machine Learning", "TensorFlow", "Data Analysis", "Statistics"],
                "location": "Austin, TX",
                "salary_range": "$130,000 - $160,000",
                "employer_id": employer_id
            },
            {
                "title": "Full Stack Developer",
                "company": "Flow Tech Solutions",
                "description": "Join our development team to build scalable web applications using modern technologies.",
                "requirements": ["JavaScript", "React", "Node.js", "MongoDB", "FastAPI"],
                "location": "Remote",
                "salary_range": "$110,000 - $140,000",
                "employer_id": employer_id
            },
            {
                "title": "DevOps Engineer",
                "company": "Flow Tech Solutions",
                "description": "Help us optimize our CI/CD pipeline and cloud infrastructure for maximum efficiency and reliability.",
                "requirements": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
                "location": "Austin, TX",
                "salary_range": "$120,000 - $150,000",
                "employer_id": employer_id
            }
        ]
        
        created_jobs = []
        
        for i, job_data in enumerate(job_descriptions, 1):
            job_response = requests.post(f"{BASE_URL}/jobs", headers=headers, json=job_data)
            if job_response.status_code == 200:
                job = job_response.json()
                created_jobs.append(job)
                print(f"✅ Created job {i}/{len(job_descriptions)}: {job.get('title')}")
            else:
                print(f"❌ Failed to create job {i}/{len(job_descriptions)}. Status: {job_response.status_code}")
        
        print(f"✅ Created {len(created_jobs)} out of {len(job_descriptions)} jobs")
        return created_jobs
        
    except Exception as e:
        print(f"❌ Error in employer registration or job creation: {str(e)}")
        return None

def test_candidate_view_jobs(token):
    """Test candidate viewing available jobs"""
    print_section("CANDIDATE VIEWING JOBS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/jobs", headers=headers)
        if response.status_code == 200:
            jobs = response.json()
            if jobs:
                print(f"✅ Retrieved {len(jobs)} jobs")
                
                # Display jobs in a table
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
                
                return jobs
            else:
                print("ℹ️ No jobs available")
                return []
        else:
            print(f"❌ Failed to retrieve jobs. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving jobs: {str(e)}")
        return []

def test_candidate_apply_for_jobs(token, jobs):
    """Test candidate applying for jobs"""
    print_section("CANDIDATE APPLYING FOR JOBS")
    
    if not jobs:
        print("❌ No jobs available to apply for")
        return []
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Apply for the first job
    job_to_apply = jobs[0]
    print(f"Applying for: {job_to_apply['title']} at {job_to_apply['company']}")
    
    application_data = {
        "job_id": job_to_apply["id"],
        "cover_letter": "I am excited to apply for this position and believe my skills in data science and machine learning make me an excellent candidate.",
        "notes": "Available for immediate start"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/applications", 
                               headers=headers, 
                               json=application_data)
        if response.status_code == 200:
            print("✅ Application submitted successfully")
            application = response.json()
            print_json("Application Details", application)
            return application
        else:
            print(f"❌ Failed to apply for job. Status: {response.status_code}")
            print_json("Application Error", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error applying for job: {str(e)}")
        return None

def test_candidate_save_jobs(token, jobs):
    """Test candidate saving jobs"""
    print_section("CANDIDATE SAVING JOBS")
    
    if not jobs or len(jobs) < 2:
        print("❌ Not enough jobs available to save")
        return None
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Save the second job
    job_to_save = jobs[1]
    print(f"Saving job: {job_to_save['title']} at {job_to_save['company']}")
    
    saved_job_data = {
        "job_id": job_to_save["id"],
        "notes": "Interesting role to consider after gaining more experience"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/saved-jobs", 
                               headers=headers, 
                               json=saved_job_data)
        if response.status_code == 200:
            print("✅ Job saved successfully")
            saved_job = response.json()
            print_json("Saved Job Details", saved_job)
            return saved_job
        else:
            print(f"❌ Failed to save job. Status: {response.status_code}")
            print_json("Save Job Error", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error saving job: {str(e)}")
        return None

def test_candidate_view_applications(token):
    """Test candidate viewing job applications"""
    print_section("CANDIDATE VIEWING APPLICATIONS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/applications", headers=headers)
        if response.status_code == 200:
            applications = response.json()
            if applications:
                print(f"✅ Retrieved {len(applications)} applications")
                
                # Display applications in a table
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
                
                return applications
            else:
                print("ℹ️ No applications found")
                return []
        else:
            print(f"❌ Failed to retrieve applications. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving applications: {str(e)}")
        return []

def test_candidate_view_saved_jobs(token):
    """Test candidate viewing saved jobs"""
    print_section("CANDIDATE VIEWING SAVED JOBS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/saved-jobs", headers=headers)
        if response.status_code == 200:
            saved_jobs = response.json()
            if saved_jobs:
                print(f"✅ Retrieved {len(saved_jobs)} saved jobs")
                
                # Display saved jobs in a table
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
                
                return saved_jobs
            else:
                print("ℹ️ No saved jobs found")
                return []
        else:
            print(f"❌ Failed to retrieve saved jobs. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving saved jobs: {str(e)}")
        return []

def test_candidate_update_application(token, applications):
    """Test candidate updating an application"""
    print_section("CANDIDATE UPDATING APPLICATION")
    
    if not applications:
        print("❌ No applications to update")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    application_to_update = applications[0]
    job_title = application_to_update.get("job_details", {}).get("title", "Unknown Job")
    
    print(f"Updating application for: {job_title}")
    
    update_data = {
        "cover_letter": "I am extremely excited to apply for this position and have recently completed additional training in advanced machine learning techniques.",
        "notes": "Available for immediate start. Can also work evenings if needed."
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/applications/{application_to_update['id']}", 
                                headers=headers, 
                                json=update_data)
        
        # If successful (200-299 status code range)
        if 200 <= response.status_code < 300:
            print("✅ Application updated successfully")
            try:
                updated_application = response.json()
                print_json("Updated Application", updated_application)
            except:
                print("Note: Response was successful but couldn't parse JSON response")
            return True
        elif response.status_code == 405:
            # Method Not Allowed - This means the PATCH endpoint might not be implemented yet
            print("❌ PATCH method not allowed. The endpoint might not be implemented.")
            print("Attempting fallback to PUT endpoint...")
            
            # Try PUT instead as a fallback
            put_response = requests.put(f"{BASE_URL}/applications/{application_to_update['id']}", 
                                      headers=headers, 
                                      json=update_data)
            if 200 <= put_response.status_code < 300:
                print("✅ Application updated successfully using PUT method")
                return True
            else:
                print(f"❌ Failed to update application with PUT method. Status: {put_response.status_code}")
                return False
        else:
            print(f"❌ Failed to update application. Status: {response.status_code}")
            print_json("Update Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error updating application: {str(e)}")
        return False

def test_candidate_update_saved_job(token, saved_jobs):
    """Test candidate updating a saved job"""
    print_section("CANDIDATE UPDATING SAVED JOB")
    
    if not saved_jobs:
        print("❌ No saved jobs to update")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    saved_job_to_update = saved_jobs[0]
    job_title = saved_job_to_update.get("job_details", {}).get("title", "Unknown Job")
    
    print(f"Updating saved job: {job_title}")
    
    update_data = {
        "notes": "Very interesting position. Planning to apply next month after completing my certification."
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/saved-jobs/{saved_job_to_update['id']}", 
                                headers=headers, 
                                json=update_data)
        
        # If successful (200-299 status code range)
        if 200 <= response.status_code < 300:
            print("✅ Saved job updated successfully")
            try:
                updated_saved_job = response.json()
                print_json("Updated Saved Job", updated_saved_job)
            except:
                print("Note: Response was successful but couldn't parse JSON response")
            return True
        elif response.status_code == 405:
            # Method Not Allowed - This means the PATCH endpoint might not be implemented yet
            print("❌ PATCH method not allowed. The endpoint might not be implemented.")
            print("Attempting fallback to PUT endpoint...")
            
            # Try PUT instead as a fallback
            put_response = requests.put(f"{BASE_URL}/saved-jobs/{saved_job_to_update['id']}", 
                                      headers=headers, 
                                      json=update_data)
            if 200 <= put_response.status_code < 300:
                print("✅ Saved job updated successfully using PUT method")
                return True
            else:
                print(f"❌ Failed to update saved job with PUT method. Status: {put_response.status_code}")
                return False
        else:
            print(f"❌ Failed to update saved job. Status: {response.status_code}")
            print_json("Update Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error updating saved job: {str(e)}")
        return False

def test_candidate_withdraw_application(token, applications):
    """Test candidate withdrawing an application"""
    print_section("CANDIDATE WITHDRAWING APPLICATION")
    
    if not applications:
        print("❌ No applications to withdraw")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    application_to_withdraw = applications[0]
    job_title = application_to_withdraw.get("job_details", {}).get("title", "Unknown Job")
    
    print(f"Withdrawing application for: {job_title}")
    
    try:
        response = requests.delete(f"{BASE_URL}/applications/{application_to_withdraw['id']}", 
                                 headers=headers)
        if response.status_code == 200:
            print("✅ Application withdrawn successfully")
            withdrawal_result = response.json()
            print_json("Withdrawal Result", withdrawal_result)
            return True
        else:
            print(f"❌ Failed to withdraw application. Status: {response.status_code}")
            print_json("Withdrawal Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error withdrawing application: {str(e)}")
        return False

def test_candidate_remove_saved_job(token, saved_jobs):
    """Test candidate removing a saved job"""
    print_section("CANDIDATE REMOVING SAVED JOB")
    
    if not saved_jobs:
        print("❌ No saved jobs to remove")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    saved_job_to_remove = saved_jobs[0]
    job_title = saved_job_to_remove.get("job_details", {}).get("title", "Unknown Job")
    
    print(f"Removing saved job: {job_title}")
    
    try:
        response = requests.delete(f"{BASE_URL}/saved-jobs/{saved_job_to_remove['id']}", 
                                 headers=headers)
        if response.status_code == 200:
            print("✅ Saved job removed successfully")
            removal_result = response.json()
            print_json("Removal Result", removal_result)
            return True
        else:
            print(f"❌ Failed to remove saved job. Status: {response.status_code}")
            print_json("Removal Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error removing saved job: {str(e)}")
        return False

def test_candidate_recommendations(token):
    """Test candidate getting job recommendations"""
    print_section("CANDIDATE GETTING JOB RECOMMENDATIONS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/recommendations/jobs", headers=headers)
        if response.status_code == 200:
            recommendations = response.json()
            if recommendations:
                print(f"✅ Retrieved {len(recommendations)} job recommendations")
                
                # Display recommendations in a table
                rec_table = []
                for i, rec in enumerate(recommendations, 1):
                    # Handle different possible response formats
                    job_id = rec.get("job_id")
                    title = rec.get("title") or rec.get("job", {}).get("title", "Unknown")
                    company = rec.get("company") or rec.get("job", {}).get("company", "Unknown")
                    
                    # Handle different score formats
                    match_score = rec.get("match_score", 0)
                    # If match_score is already a string with a % sign
                    if isinstance(match_score, str) and "%" in match_score:
                        score_display = match_score
                    else:
                        # Format as percentage
                        score_display = f"{float(match_score):.1f}%"
                    
                    rec_table.append([
                        i,
                        job_id,
                        title,
                        company,
                        score_display,
                    ])
                
                print("\n" + tabulate(rec_table, 
                                    headers=["#", "Job ID", "Title", "Company", "Match Score"],
                                    tablefmt="grid"))
                
                return recommendations
            else:
                print("ℹ️ No job recommendations found")
                return []
        else:
            print(f"❌ Failed to retrieve recommendations. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving recommendations: {str(e)}")
        return []

def run_test():
    """Run the full candidate flow test"""
    print("\n==================================================")
    print("TESTING FULL CANDIDATE FLOW".center(50))
    print("==================================================\n")
    
    # Step 1: Register a test candidate
    candidate = register_candidate()
    if not candidate:
        print("❌ Failed to register or authenticate candidate. Cannot proceed.")
        return
    
    # Step 2: Register an employer and create jobs
    jobs = register_employer_and_create_jobs()
    if not jobs:
        print("❌ Failed to register employer or create jobs. Cannot fully test candidate flow.")
        # We can still proceed with existing jobs if available
    
    # Step 3: Get candidate authentication token
    print_section("AUTHENTICATING CANDIDATE")
    token = get_auth_token(CANDIDATE_EMAIL, CANDIDATE_PASSWORD)
    if not token:
        print("❌ Failed to get candidate auth token. Cannot proceed.")
        return
    
    print("✅ Candidate authenticated successfully")
    
    # Step 4: View available jobs
    available_jobs = test_candidate_view_jobs(token)
    
    # Step 5: Apply for a job only if jobs are available
    applied_job = None
    if available_jobs:
        applied_job = test_candidate_apply_for_jobs(token, available_jobs)
    else:
        print("⚠️ No jobs available to apply for, skipping application tests")
    
    # Step 6: Save a job only if multiple jobs are available
    saved_job = None
    if available_jobs and len(available_jobs) >= 2:
        saved_job = test_candidate_save_jobs(token, available_jobs)
    else:
        print("⚠️ Not enough jobs available to save, skipping save job tests")
    
    # Pause briefly to allow database to update
    time.sleep(1)
    
    # Step 7: View applications
    applications = test_candidate_view_applications(token)
    
    # Step 8: View saved jobs
    saved_jobs = test_candidate_view_saved_jobs(token)
    
    # Step 9: Update an application if any exist
    updated_application = False
    if applications:
        updated_application = test_candidate_update_application(token, applications)
    else:
        print("⚠️ No applications to update, skipping update application test")
    
    # Step 10: Update a saved job if any exist
    updated_saved_job = False
    if saved_jobs:
        updated_saved_job = test_candidate_update_saved_job(token, saved_jobs)
    else:
        print("⚠️ No saved jobs to update, skipping update saved job test")
    
    # Pause briefly to allow database to update
    time.sleep(1)
    
    # Step 11: Get job recommendations
    recommendations = test_candidate_recommendations(token)
    
    # Step 12: Withdraw an application if any exist
    withdrawn_application = False
    if applications:
        withdrawn_application = test_candidate_withdraw_application(token, applications)
    else:
        print("⚠️ No applications to withdraw, skipping withdrawal test")
    
    # Step 13: Remove a saved job if any exist
    removed_saved_job = False
    if saved_jobs:
        removed_saved_job = test_candidate_remove_saved_job(token, saved_jobs)
    else:
        print("⚠️ No saved jobs to remove, skipping removal test")
    
    # Final view of applications and saved jobs after changes
    print_section("FINAL STATE - APPLICATIONS")
    final_applications = test_candidate_view_applications(token)
    
    print_section("FINAL STATE - SAVED JOBS")
    final_saved_jobs = test_candidate_view_saved_jobs(token)
    
    # Test summary
    print_section("TEST SUMMARY")
    print("Candidate Registration:", "✅ Success" if candidate else "❌ Failed")
    print("Employer Registration and Job Creation:", "✅ Success" if jobs else "⚠️ Used existing jobs")
    print("View Jobs:", "✅ Success" if available_jobs else "❌ Failed")
    print("Apply for Job:", "✅ Success" if applied_job else "⚠️ Skipped or Failed")
    print("Save Job:", "✅ Success" if saved_job else "⚠️ Skipped or Failed")
    print("View Applications:", "✅ Success" if applications else "⚠️ No applications found")
    print("View Saved Jobs:", "✅ Success" if saved_jobs else "⚠️ No saved jobs found")
    print("Update Application:", "✅ Success" if updated_application else "⚠️ Skipped or Failed")
    print("Update Saved Job:", "✅ Success" if updated_saved_job else "⚠️ Skipped or Failed")
    print("Get Recommendations:", "✅ Success" if recommendations else "❌ Failed")
    print("Withdraw Application:", "✅ Success" if withdrawn_application else "⚠️ Skipped or Failed")
    print("Remove Saved Job:", "✅ Success" if removed_saved_job else "⚠️ Skipped or Failed")

if __name__ == "__main__":
    run_test() 