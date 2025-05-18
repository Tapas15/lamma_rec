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
    max_retries = 3
    
    for i, project_data in enumerate(project_descriptions, 1):
        retries = 0
        while retries < max_retries:
            try:
                print(f"Creating project {i}: {project_data['title']} (Attempt {retries + 1})")
                response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
                print(f"Response status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    project = response.json()
                    # Verify project was actually created
                    verify_response = requests.get(f"{BASE_URL}/projects/{project['id']}", headers=headers)
                    if verify_response.status_code == 200:
                        created_projects.append(project)
                        print(f"✅ Created and verified project {i}/{len(project_descriptions)}: {project.get('title')}")
                        break
                    else:
                        print(f"⚠️ Project creation succeeded but verification failed. Retrying...")
                else:
                    print(f"❌ Failed to create project {i}/{len(project_descriptions)}. Status: {response.status_code}")
                    print_json("Project Creation Error", response.json() if response.content else "No content")
                
                retries += 1
                if retries < max_retries:
                    print(f"Waiting before retry {retries + 1}...")
                    time.sleep(2)  # Wait before retrying
                    
            except Exception as e:
                print(f"❌ Error creating project {i} (Attempt {retries + 1}): {str(e)}")
                retries += 1
                if retries < max_retries:
                    time.sleep(2)  # Wait before retrying
    
    if created_projects:
        print(f"✅ Successfully created {len(created_projects)} out of {len(project_descriptions)} projects")
    else:
        print("❌ Failed to create any projects")
    
    # Allow time for database consistency
    time.sleep(2)
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
        response = requests.get(f"{BASE_URL}/employer-projects", headers=headers)
        print(f"Response status code: {response.status_code}")
        
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

def view_project(token, project_id):
    """View details of a specific project"""
    print_section("VIEWING PROJECT DETAILS")
    
    if not project_id:
        print("❌ No project ID provided")
        return None
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Making request to /projects/{project_id}...")
        response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            project = response.json()
            print("✅ Retrieved project details")
            
            # Verify all required fields are present
            required_fields = ["id", "title", "company", "description", "requirements", "employer_id", "status", "project_type", "skills_required"]
            missing_fields = [field for field in required_fields if field not in project]
            if missing_fields:
                print(f"❌ WARNING: Project is missing required fields: {', '.join(missing_fields)}")
            else:
                print("✅ All required fields present in project")
                
            print_json("Project Details", project)
            return project
        elif response.status_code == 404:
            print(f"❌ Project with ID {project_id} not found")
            print_json("Error Response", response.json() if response.content else "No content")
            return None
        else:
            print(f"❌ Failed to retrieve project details. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            print(f"Raw response content: {response.text}")
            
            # Additional details if status is 500
            if response.status_code == 500:
                print("SERVER ERROR: The API returned a 500 Internal Server Error")
                print("This usually indicates an exception was raised in the server code")
                print("Check the server logs for more information")
                
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error retrieving project details: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error retrieving project details: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

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
        "status": "in_progress",
        "description": "UPDATED: Project is now in progress with additional requirements.",
        "budget_range": "$20,000 - $30,000"
    }
    
    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            print(f"Updating project {project_id} (Attempt {retries + 1})...")
            
            # First, verify the project exists
            verify_response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
            if verify_response.status_code != 200:
                print(f"❌ Project not found before update. Status: {verify_response.status_code}")
                return False
            
            # Attempt the update
            response = requests.patch(f"{BASE_URL}/projects/{project_id}", headers=headers, json=update_data)
            print(f"Update response status: {response.status_code}")
            
            if response.status_code == 200:
                # Verify the update was successful
                verify_response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
                if verify_response.status_code == 200:
                    updated_project = verify_response.json()
                    if updated_project.get("status") == "in_progress":
                        print("✅ Project status updated and verified successfully")
                        print_json("Updated Project", updated_project)
                        return True
                    else:
                        print("⚠️ Project update verification failed - status not updated correctly")
                else:
                    print(f"⚠️ Failed to verify project update. Status: {verify_response.status_code}")
            else:
                print(f"❌ Failed to update project status. Status: {response.status_code}")
                print_json("Update Error", response.json() if response.content else "No content")
            
            retries += 1
            if retries < max_retries:
                print(f"Waiting before retry {retries + 1}...")
                time.sleep(2)  # Wait before retrying
                
        except Exception as e:
            print(f"❌ Error updating project status (Attempt {retries + 1}): {str(e)}")
            retries += 1
            if retries < max_retries:
                time.sleep(2)  # Wait before retrying
    
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
    
    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            # First verify the project exists
            print(f"Verifying project {project_id} exists...")
            verify_response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
            if verify_response.status_code != 200:
                print(f"❌ Project not found before deletion. Status: {verify_response.status_code}")
                return False
            
            print(f"Deleting project {project_id} (Attempt {retries + 1})...")
            response = requests.delete(f"{BASE_URL}/projects/{project_id}", headers=headers)
            print(f"Delete response status: {response.status_code}")
            
            if response.status_code == 200:
                # Verify the project is really deleted by attempting to fetch it
                time.sleep(1)  # Brief pause to allow for deletion to complete
                verify_delete = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
                
                if verify_delete.status_code == 404:
                    print("✅ Project deleted and verified successfully")
                    result = response.json()
                    print_json("Deletion Result", result)
                    return True
                else:
                    print(f"⚠️ Project may not be fully deleted. Status: {verify_delete.status_code}")
            else:
                print(f"❌ Failed to delete project. Status: {response.status_code}")
                print_json("Deletion Error", response.json() if response.content else "No content")
            
            retries += 1
            if retries < max_retries:
                print(f"Waiting before retry {retries + 1}...")
                time.sleep(2)  # Wait before retrying
                
        except Exception as e:
            print(f"❌ Error deleting project (Attempt {retries + 1}): {str(e)}")
            retries += 1
            if retries < max_retries:
                time.sleep(2)  # Wait before retrying
    
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

def ensure_test_project(token, employer_id):
    """Ensure at least one project exists, create if needed, and return the project list."""
    projects = get_employer_projects(token)
    if not projects:
        print("No projects found, creating a test project...")
        test_project_data = {
            "title": "Test Project for Full Flow",
            "company": "Test Company",
            "description": "This project was created to ensure update/delete can be tested.",
            "requirements": ["Testing", "Debugging"],
            "budget_range": "$5,000 - $10,000",
            "duration": "1 month",
            "location": "Remote",
            "project_type": "Test",
            "skills_required": ["Testing", "Documentation"],
            "employer_id": employer_id
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            create_response = requests.post(f"{BASE_URL}/projects", headers=headers, json=test_project_data)
            if create_response.status_code in [200, 201]:
                print("✅ Created test project for update/delete")
                return get_employer_projects(token)
            else:
                print("❌ Failed to create test project for update/delete")
        except Exception as e:
            print(f"❌ Exception creating test project: {str(e)}")
    return get_employer_projects(token)

def test_get_all_projects(token):
    """Test the general projects endpoint"""
    print_section("TESTING GET ALL PROJECTS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Making request to /projects...")
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Retrieved {len(projects)} projects from /projects endpoint")
            if projects:
                print_json("First project example", projects[0])
            return projects
        else:
            print(f"❌ Failed to retrieve projects. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return []
    except Exception as e:
        print(f"❌ Error retrieving projects: {str(e)}")
        return []

def diagnose_collection_issue():
    """Helper function to diagnose potential collection issues"""
    print_section("DIAGNOSING COLLECTION ISSUES")
    
    try:
        # Let's check what collections are available in MongoDB
        # This requires pymongo to be installed
        print("Attempting to directly check MongoDB collections...")
        try:
            from pymongo import MongoClient
            
            # Use the same connection string as in the application
            # Note: In a real application, this should be retrieved from environment variables or config
            mongo_url = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
            db_name = "job_recommender"
            
            client = MongoClient(mongo_url)
            db = client[db_name]
            
            # List all collections
            collections = db.list_collection_names()
            print(f"Available collections: {collections}")
            
            # Check if projects collection exists and has documents
            if "projects" in collections:
                projects_count = db.projects.count_documents({})
                print(f"Projects collection exists with {projects_count} documents")
                
                # Sample a few documents if they exist
                if projects_count > 0:
                    print("\nSample projects:")
                    for project in db.projects.find().limit(2):
                        print(f"  - {project.get('id')}: {project.get('title')}")
            else:
                print("Projects collection does not exist!")
                
            client.close()
            
        except ImportError:
            print("pymongo is not installed. Cannot directly check MongoDB.")
        except Exception as e:
            print(f"Error connecting directly to MongoDB: {str(e)}")
    
    except Exception as e:
        print(f"Error in diagnostics: {str(e)}")

def login_existing_employer():
    """Login with existing employer account instead of registering a new one"""
    print_section("LOGGING IN WITH EXISTING EMPLOYER")
    
    token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
    if token:
        print("✅ Login with existing employer account successful")
        # Get employer profile to retrieve ID
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(f"{BASE_URL}/profile", headers=headers)
            if response.status_code == 200:
                employer = response.json()
                print(f"✅ Retrieved employer profile with ID: {employer.get('id')}")
                return employer, token
            else:
                print(f"❌ Failed to get employer profile. Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error getting employer profile: {str(e)}")
    else:
        print("❌ Failed to login with existing employer account")
    
    return None, None

def run_test():
    """Run the full employer workflow test"""
    print("\n==================================================")
    print("TESTING FULL EMPLOYER WORKFLOW".center(50))
    print("==================================================\n")
    
    # Step 1: Login with existing employer account (preferred) or register if needed
    employer, token = login_existing_employer()
    
    # If login fails, try registration
    if not employer or not token:
        print("Login failed, trying to register a new employer...")
        employer = register_employer()
        if not employer:
            print("❌ Failed to register or authenticate employer. Cannot proceed.")
            return
            
        employer_id = employer.get("id")
        if not employer_id or employer_id == "unknown":
            print("❌ Failed to get valid employer ID. Cannot proceed.")
            return
            
        # Get authentication token
        print_section("AUTHENTICATING EMPLOYER")
        token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
        if not token:
            print("❌ Failed to get employer auth token. Cannot proceed.")
            return
    else:
        employer_id = employer.get("id")
        
    print("✅ Employer authentication successful with ID:", employer_id)
    
    # Step 3: Post jobs
    jobs = post_jobs(token, employer_id)
    
    # Step 4: Post projects
    projects = post_projects(token, employer_id)
    if not projects:
        print("⚠️ No projects were created in initial attempt, trying backup project creation...")
        # Try creating a single test project as backup
        test_project = {
            "title": "Test Project",
            "company": "Acme Technologies",
            "description": "A test project for verification.",
            "requirements": ["Testing"],
            "budget_range": "$5,000 - $10,000",
            "duration": "1 month",
            "location": "Remote",
            "project_type": "Test",
            "skills_required": ["Testing"],
            "employer_id": employer_id
        }
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.post(f"{BASE_URL}/projects", headers=headers, json=test_project)
            if response.status_code in [200, 201]:
                projects = [response.json()]
                print("✅ Successfully created backup test project")
            else:
                print("❌ Failed to create backup test project")
        except Exception as e:
            print(f"❌ Error creating backup test project: {str(e)}")
    
    # Pause to allow database to update
    time.sleep(2)
    
    # Step 5: Get all projects (not just employer's)
    print_section("TESTING ALL PROJECTS VIEW")
    all_projects = test_get_all_projects(token)
    if not all_projects:
        print("⚠️ No projects found in the system. This might indicate a database issue.")
    
    # Step 6: View jobs
    employer_jobs = get_employer_jobs(token)
    
    # Step 7: View employer projects
    print("\nAttempting to view employer projects...")
    employer_projects = get_employer_projects(token)
    if not employer_projects:
        print("⚠️ No projects found in initial view, creating test project...")
        employer_projects = ensure_test_project(token, employer_id)
        time.sleep(2)  # Allow time for project creation
    
    # Step 8: View detailed project info if available
    viewed_project_details = None
    if employer_projects and len(employer_projects) > 0:
        project_to_view = employer_projects[0]
        project_id = project_to_view.get("id")
        if project_id:
            viewed_project_details = view_project(token, project_id)
            if not viewed_project_details:
                print("⚠️ Failed to view project details, waiting and retrying...")
                time.sleep(2)
                viewed_project_details = view_project(token, project_id)
    
    # If still having issues with project operations, run diagnostics
    if not viewed_project_details or not employer_projects:
        print("\n⚠️ Issues detected with project operations. Running diagnostic...")
        diagnose_collection_issue()
    
    # Step 9: Update a job if any exist
    updated_job = False
    if employer_jobs:
        job_to_update = employer_jobs[0]
        updated_job = update_job(token, job_to_update.get("id"))
    
    # Step 10: Update a project status if any exist
    updated_project = False
    if employer_projects:
        project_to_update = employer_projects[0]
        project_id = project_to_update.get("id")
        if project_id:
            print("\nAttempting to update project status...")
            updated_project = update_project_status(token, project_id)
            if not updated_project:
                print("⚠️ Project update failed, waiting and retrying...")
                time.sleep(2)
                updated_project = update_project_status(token, project_id)
    
    # Pause to allow database to update
    time.sleep(2)
    
    # Step 11: Get candidate recommendations for a job
    recommendations = []
    if employer_jobs:
        job_for_recommendations = employer_jobs[0]
        recommendations = get_candidate_recommendations(token, job_for_recommendations.get("id"))
    
    # Step 12: Delete a job if any exist
    deleted_job = False
    if len(employer_jobs) > 1:
        job_to_delete = employer_jobs[-1]
        deleted_job = delete_job(token, job_to_delete.get("id"))
    
    # Step 13: Delete a project if any exist
    deleted_project = False
    if employer_projects and len(employer_projects) > 0:
        project_to_delete = employer_projects[-1]
        project_id = project_to_delete.get("id")
        if project_id:
            print("\nAttempting to delete project...")
            deleted_project = delete_project(token, project_id)
            if not deleted_project:
                print("⚠️ Project deletion failed, waiting and retrying...")
                time.sleep(2)
                deleted_project = delete_project(token, project_id)
    
    # Pause to allow database to update
    time.sleep(2)
    
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
    print("View All Projects:", "✅ Success" if all_projects else "⚠️ No projects found")
    print("View Jobs:", "✅ Success" if employer_jobs else "⚠️ No jobs found")
    print("View Projects:", "✅ Success" if employer_projects else "⚠️ No projects found")
    print("View Project Details:", "✅ Success" if viewed_project_details else "⚠️ Skipped or Failed")
    print("Update Job:", "✅ Success" if updated_job else "⚠️ Skipped or Failed")
    print("Update Project Status:", "✅ Success" if updated_project else "⚠️ Skipped or Failed")
    print("Get Candidate Recommendations:", "✅ Success" if recommendations else "⚠️ Skipped or Failed")
    print("Delete Job:", "✅ Success" if deleted_job else "⚠️ Skipped or Failed")
    print("Delete Project:", "✅ Success" if deleted_project else "⚠️ Skipped or Failed")
    
    print("\nTest completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # If we had significant issues, suggest next steps
    if not viewed_project_details or not employer_projects:
        print("\n" + "!" * 80)
        print("TROUBLESHOOTING SUGGESTIONS:")
        print("1. Check that the MongoDB server is running and accessible")
        print("2. Verify the connection string in database.py")
        print("3. Check MongoDB permissions for the database user")
        print("4. Review server logs for any exceptions")
        print("5. Run individual tests for create, read, update, delete operations")
        print("!" * 80)

if __name__ == "__main__":
    run_test() 