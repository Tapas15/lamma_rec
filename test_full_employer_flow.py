import requests
import json
import time
from datetime import datetime
from tabulate import tabulate

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test employer credentials
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

def register_employer():
    """Register a test employer"""
    print_section("REGISTERING TEST EMPLOYER")
    
    employer_data = {
        "email": EMPLOYER_EMAIL,
        "password": EMPLOYER_PASSWORD,
        "full_name": "Test Employer",
        "user_type": "employer",
        "company_name": "Acme Technologies",
        "company_description": "Leading innovation in technology solutions",
        "company_website": "https://acmetech.example.com",
        "company_location": "New York, NY",
        "company_size": "101-500",
        "industry": "Software Development",
        "contact_email": "hr@acmetech.example.com",
        "contact_phone": "+1-555-123-4567",
        "location": "New York, NY",
        "bio": "We build technology that powers the future"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register/employer", json=employer_data)
        if response.status_code == 200:
            print("✅ Employer registered successfully")
            return response.json()
        elif response.status_code == 400 and "Email already registered" in response.json().get("detail", ""):
            print("ℹ️ Employer already registered, attempting to login...")
            token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
            if token:
                print("✅ Logged in with existing employer account")
                # Get employer profile
                headers = {"Authorization": f"Bearer {token}"}
                profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
                if profile_response.status_code == 200:
                    return profile_response.json()
                else:
                    print("❌ Failed to get employer profile")
                    return {"email": EMPLOYER_EMAIL, "id": "unknown"}
            else:
                print("❌ Failed to login with existing employer account")
                return None
        else:
            print(f"❌ Employer registration failed. Status: {response.status_code}")
            print_json("Registration Error", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error registering employer: {str(e)}")
        return None

def post_jobs(token, employer_id):
    """Post test jobs"""
    print_section("POSTING JOBS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    job_descriptions = [
        {
            "title": "Senior Frontend Developer",
            "company": "Acme Technologies",
            "description": "We're looking for a senior frontend developer with React experience to join our team.",
            "requirements": ["React", "JavaScript", "TypeScript", "CSS", "HTML5"],
            "location": "New York, NY",
            "salary_range": "$120,000 - $150,000",
            "employer_id": employer_id
        },
        {
            "title": "Backend Engineer",
            "company": "Acme Technologies",
            "description": "Join our backend team to develop scalable microservices and APIs.",
            "requirements": ["Python", "FastAPI", "MongoDB", "Docker", "Kubernetes"],
            "location": "Remote",
            "salary_range": "$110,000 - $140,000",
            "employer_id": employer_id
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Acme Technologies",
            "description": "Help us build cutting-edge machine learning models for our products.",
            "requirements": ["Python", "TensorFlow", "PyTorch", "Data Science", "NLP"],
            "location": "New York, NY",
            "salary_range": "$130,000 - $170,000",
            "employer_id": employer_id
        }
    ]
    
    created_jobs = []
    for i, job_data in enumerate(job_descriptions, 1):
        try:
            response = requests.post(f"{BASE_URL}/jobs", headers=headers, json=job_data)
            if response.status_code == 200:
                job = response.json()
                created_jobs.append(job)
                print(f"✅ Created job {i}/{len(job_descriptions)}: {job.get('title')}")
            else:
                print(f"❌ Failed to create job {i}/{len(job_descriptions)}. Status: {response.status_code}")
                print_json("Job Creation Error", response.json() if response.content else "No content")
        except Exception as e:
            print(f"❌ Error creating job {i}: {str(e)}")
    
    print(f"✅ Created {len(created_jobs)} out of {len(job_descriptions)} jobs")
    return created_jobs

def post_projects(token, employer_id):
    """Post test projects"""
    print_section("POSTING PROJECTS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    project_descriptions = [
        {
            "title": "Website Redesign",
            "company": "Acme Technologies",
            "description": "Complete redesign of our company website with modern UI/UX.",
            "requirements": ["UI/UX Design", "React", "Responsive Design"],
            "budget_range": "$15,000 - $25,000",
            "duration": "2-3 months",
            "location": "Remote",
            "project_type": "Contract",
            "skills_required": ["UI Design", "Frontend Development", "React", "CSS"],
            "employer_id": employer_id
        },
        {
            "title": "Mobile App Development",
            "company": "Acme Technologies",
            "description": "Develop a cross-platform mobile app for our product.",
            "requirements": ["React Native", "Mobile Development", "API Integration"],
            "budget_range": "$30,000 - $50,000",
            "duration": "4-6 months",
            "location": "Remote",
            "project_type": "Contract",
            "skills_required": ["React Native", "Mobile Development", "JavaScript", "API Development"],
            "employer_id": employer_id
        }
    ]
    
    created_projects = []
    for i, project_data in enumerate(project_descriptions, 1):
        try:
            response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
            if response.status_code in [200, 201]:  # Accept both 200 and 201 for success
                project = response.json()
                created_projects.append(project)
                print(f"✅ Created project {i}/{len(project_descriptions)}: {project.get('title')}")
            else:
                print(f"❌ Failed to create project {i}/{len(project_descriptions)}. Status: {response.status_code}")
                print_json("Project Creation Error", response.json() if response.content else "No content")
        except Exception as e:
            print(f"❌ Error creating project {i}: {str(e)}")
    
    print(f"✅ Created {len(created_projects)} out of {len(project_descriptions)} projects")
    return created_projects

def get_employer_jobs(token):
    """Get employer's posted jobs"""
    print_section("VIEWING POSTED JOBS")
    
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
                        job.get("location"),
                        job.get("salary_range", "Not specified"),
                        job.get("is_active", True)
                    ])
                
                print("\n" + tabulate(job_table, 
                                    headers=["#", "ID", "Title", "Location", "Salary Range", "Active"],
                                    tablefmt="grid"))
                
                return jobs
            else:
                print("ℹ️ No jobs found")
                return []
        else:
            print(f"❌ Failed to retrieve jobs. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving jobs: {str(e)}")
        return []

def get_employer_projects(token):
    """Get employer's posted projects"""
    print_section("VIEWING POSTED PROJECTS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/employer/projects", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            if projects:
                print(f"✅ Retrieved {len(projects)} projects")
                
                # Display projects in a table
                project_table = []
                for i, project in enumerate(projects, 1):
                    project_table.append([
                        i,
                        project.get("id"),
                        project.get("title"),
                        project.get("location"),
                        project.get("budget_range", "Not specified"),
                        project.get("status")
                    ])
                
                print("\n" + tabulate(project_table, 
                                     headers=["#", "ID", "Title", "Location", "Budget Range", "Status"],
                                     tablefmt="grid"))
                
                return projects
            else:
                print("ℹ️ No projects found")
                return []
        else:
            print(f"❌ Failed to retrieve projects. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving projects: {str(e)}")
        return []

def update_job(token, job_id):
    """Update a job"""
    print_section("UPDATING JOB")
    
    if not job_id:
        print("❌ No job ID provided for update")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    update_data = {
        "description": "UPDATED: We're looking for an exceptional frontend developer with extensive React experience to join our innovative team.",
        "requirements": ["React", "JavaScript", "TypeScript", "CSS", "HTML5", "Redux"],
        "salary_range": "$130,000 - $160,000"
    }
    
    try:
        # Use the new PATCH endpoint for direct job updates
        response = requests.patch(f"{BASE_URL}/jobs/{job_id}", headers=headers, json=update_data)
        if response.status_code == 200:
            print("✅ Job updated successfully")
            updated_job = response.json()
            print_json("Updated Job", updated_job)
            return True
        else:
            print(f"❌ Failed to update job. Status: {response.status_code}")
            print_json("Update Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error updating job: {str(e)}")
        return False

def update_project_status(token, project_id):
    """Update a project's status"""
    print_section("UPDATING PROJECT STATUS")
    
    if not project_id:
        print("❌ No project ID provided for update")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    update_data = {
        "status": "in_progress"
    }
    
    try:
        response = requests.patch(f"{BASE_URL}/projects/{project_id}", headers=headers, json=update_data)
        if response.status_code == 200:
            print("✅ Project status updated successfully")
            updated_project = response.json()
            print_json("Updated Project", updated_project)
            return True
        else:
            print(f"❌ Failed to update project status. Status: {response.status_code}")
            print_json("Update Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error updating project status: {str(e)}")
        return False

def delete_job(token, job_id):
    """Delete a job"""
    print_section("DELETING JOB")
    
    if not job_id:
        print("❌ No job ID provided for deletion")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(f"{BASE_URL}/jobs/{job_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Job deleted successfully")
            result = response.json()
            print_json("Deletion Result", result)
            return True
        else:
            print(f"❌ Failed to delete job. Status: {response.status_code}")
            print_json("Deletion Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error deleting job: {str(e)}")
        return False

def delete_project(token, project_id):
    """Delete a project"""
    print_section("DELETING PROJECT")
    
    if not project_id:
        print("❌ No project ID provided for deletion")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(f"{BASE_URL}/projects/{project_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Project deleted successfully")
            result = response.json()
            print_json("Deletion Result", result)
            return True
        else:
            print(f"❌ Failed to delete project. Status: {response.status_code}")
            print_json("Deletion Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error deleting project: {str(e)}")
        return False

def get_candidate_recommendations(token, job_id):
    """Get candidate recommendations for a job"""
    print_section("GETTING CANDIDATE RECOMMENDATIONS")
    
    if not job_id:
        print("❌ No job ID provided for recommendations")
        return []
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/recommendations/candidates/{job_id}", headers=headers)
        if response.status_code == 200:
            recommendations = response.json()
            if recommendations:
                print(f"✅ Retrieved {len(recommendations)} candidate recommendations")
                
                # Display recommendations in a table
                rec_table = []
                for i, rec in enumerate(recommendations, 1):
                    candidate = rec.get("candidate", {})
                    rec_table.append([
                        i,
                        rec.get("candidate_id"),
                        candidate.get("full_name", "Unknown"),
                        candidate.get("location", "Unknown"),
                        f"{rec.get('match_score', 0):.1f}%",
                    ])
                
                print("\n" + tabulate(rec_table, 
                                    headers=["#", "Candidate ID", "Name", "Location", "Match Score"],
                                    tablefmt="grid"))
                
                return recommendations
            else:
                print("ℹ️ No candidate recommendations found")
                return []
        else:
            print(f"❌ Failed to retrieve recommendations. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving candidate recommendations: {str(e)}")
        return []

def run_test():
    """Run the full employer workflow test"""
    print("\n==================================================")
    print("TESTING FULL EMPLOYER WORKFLOW".center(50))
    print("==================================================\n")
    
    # Step 1: Register an employer
    employer = register_employer()
    if not employer:
        print("❌ Failed to register or authenticate employer. Cannot proceed.")
        return
    
    employer_id = employer.get("id")
    if not employer_id or employer_id == "unknown":
        print("❌ Failed to get valid employer ID. Cannot proceed.")
        return
    
    # Step 2: Get employer authentication token
    print_section("AUTHENTICATING EMPLOYER")
    token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
    if not token:
        print("❌ Failed to get employer auth token. Cannot proceed.")
        return
    
    print("✅ Employer authenticated successfully")
    
    # Step 3: Post jobs
    jobs = post_jobs(token, employer_id)
    
    # Step 4: Post projects
    projects = post_projects(token, employer_id)
    
    # Pause briefly to allow database to update
    time.sleep(1)
    
    # Step 5: View jobs
    employer_jobs = get_employer_jobs(token)
    
    # Step 6: View projects
    employer_projects = get_employer_projects(token)
    
    # Step 7: Update a job if any exist
    updated_job = False
    if employer_jobs:
        job_to_update = employer_jobs[0]
        updated_job = update_job(token, job_to_update.get("id"))
    else:
        print("⚠️ No jobs available to update, skipping job update test")
    
    # Step 8: Update a project status if any exist
    updated_project = False
    if employer_projects:
        project_to_update = employer_projects[0]
        updated_project = update_project_status(token, project_to_update.get("id"))
    else:
        print("⚠️ No projects available to update, skipping project update test")
    
    # Pause briefly to allow database to update
    time.sleep(1)
    
    # Step 9: Get candidate recommendations for a job
    recommendations = []
    if employer_jobs:
        job_for_recommendations = employer_jobs[0]
        recommendations = get_candidate_recommendations(token, job_for_recommendations.get("id"))
    else:
        print("⚠️ No jobs available for getting recommendations, skipping recommendations test")
    
    # Step 10: Delete a job if any exist
    deleted_job = False
    if len(employer_jobs) > 1:
        job_to_delete = employer_jobs[-1]  # Delete the last job
        deleted_job = delete_job(token, job_to_delete.get("id"))
    else:
        print("⚠️ Not enough jobs available for deletion test, skipping job deletion")
    
    # Step 11: Delete a project if any exist
    deleted_project = False
    if employer_projects and len(employer_projects) > 0:
        project_to_delete = employer_projects[-1]  # Delete the last project
        deleted_project = delete_project(token, project_to_delete.get("id"))
    else:
        print("⚠️ No projects available for deletion test, skipping project deletion")
    
    # Pause briefly to allow database to update
    time.sleep(1)
    
    # Final view of jobs and projects after changes
    print_section("FINAL STATE - JOBS")
    final_jobs = get_employer_jobs(token)
    
    print_section("FINAL STATE - PROJECTS")
    final_projects = get_employer_projects(token)
    
    # Test summary
    print_section("TEST SUMMARY")
    print("Employer Registration:", "✅ Success" if employer else "❌ Failed")
    print("Authentication:", "✅ Success" if token else "❌ Failed")
    print("Post Jobs:", "✅ Success" if jobs else "❌ Failed")
    print("Post Projects:", "✅ Success" if projects else "❌ Failed")
    print("View Jobs:", "✅ Success" if employer_jobs else "⚠️ No jobs found")
    print("View Projects:", "✅ Success" if employer_projects else "⚠️ No projects found")
    print("Update Job:", "✅ Success" if updated_job else "⚠️ Skipped or Failed")
    print("Update Project Status:", "✅ Success" if updated_project else "⚠️ Skipped or Failed")
    print("Get Candidate Recommendations:", "✅ Success" if recommendations else "⚠️ Skipped or Failed")
    print("Delete Job:", "✅ Success" if deleted_job else "⚠️ Skipped or Failed")
    print("Delete Project:", "✅ Success" if deleted_project else "⚠️ Skipped or Failed")
    
    print("\nTest completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    run_test() 