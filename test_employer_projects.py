import requests
import json
import time

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

def get_auth_token():
    """Get authentication token"""
    login_data = {
        "username": EMPLOYER_EMAIL,
        "password": EMPLOYER_PASSWORD
    }
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Login failed for {EMPLOYER_EMAIL}. Status: {response.status_code}")
            print_json("Login Error Response", response.json() if response.content else "No content")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Authentication request failed: {e}")
        return None

def get_profile(token):
    """Get user profile to get employer ID"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Retrieved profile with ID: {profile.get('id')}")
            return profile
        else:
            print(f"Failed to get profile. Status: {response.status_code}")
            print_json("Profile Error Response", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return None

def create_test_project(token, employer_id):
    """Create a test project"""
    print_section("CREATING TEST PROJECT")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    project_data = {
        "title": "Test Project for Employer Projects",
        "company": "Test Company",
        "description": "This is a test project to debug the employer projects endpoint.",
        "requirements": ["Testing", "Debugging"],
        "budget_range": "$5,000 - $10,000",
        "duration": "1 month",
        "location": "Remote",
        "project_type": "Test",
        "skills_required": ["Testing", "Debugging"],
        "employer_id": employer_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
        print(f"Response status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            project = response.json()
            print("✅ Created test project successfully")
            print_json("Created Project", project)
            return project
        else:
            print(f"❌ Failed to create project. Status: {response.status_code}")
            print_json("Project Creation Error", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error creating project: {str(e)}")
        return None

def get_all_projects(token):
    """Get all projects"""
    print_section("GETTING ALL PROJECTS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Retrieved {len(projects)} projects")
            if projects:
                print_json("First Project", projects[0])
            return projects
        else:
            print(f"❌ Failed to retrieve projects. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error retrieving projects: {str(e)}")
        return None

def get_employer_projects(token):
    """Get employer projects"""
    print_section("GETTING EMPLOYER PROJECTS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Making request to /employer-projects...")
        response = requests.get(f"{BASE_URL}/employer-projects", headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Raw response: {response.text}")
        
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Retrieved {len(projects)} employer projects")
            if projects:
                print_json("First Employer Project", projects[0])
            return projects
        else:
            print(f"❌ Failed to retrieve employer projects. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error retrieving employer projects: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

def get_project_by_id(token, project_id):
    """Get a project by ID"""
    print_section(f"GETTING PROJECT BY ID: {project_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            project = response.json()
            print("✅ Retrieved project successfully")
            print_json("Project Details", project)
            return project
        else:
            print(f"❌ Failed to retrieve project. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error retrieving project: {str(e)}")
        return None

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
                    for project in db.projects.find().limit(5):
                        print(f"  - {project.get('id')}: {project.get('title')} (employer_id: {project.get('employer_id')})")
                        
                    # Check projects for a specific employer
                    employer_id = "68299cd7ba887372c513711f"  # From our test
                    employer_projects = list(db.projects.find({"employer_id": employer_id}))
                    print(f"\nFound {len(employer_projects)} projects for employer {employer_id}")
                    for project in employer_projects:
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

def run_test():
    """Run the test"""
    print("\n==================================================")
    print("TESTING EMPLOYER PROJECTS ENDPOINT".center(50))
    print("==================================================\n")
    
    # Step 1: Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token. Cannot proceed.")
        return
    
    print("✅ Authentication successful")
    
    # Step 2: Get employer profile
    profile = get_profile(token)
    if not profile:
        print("❌ Failed to get employer profile. Cannot proceed.")
        return
    
    employer_id = profile.get("id")
    print(f"✅ Got employer ID: {employer_id}")
    
    # Step 3: Create a test project
    project = create_test_project(token, employer_id)
    if not project:
        print("❌ Failed to create test project. Continuing with existing projects...")
    
    # Allow time for database consistency
    time.sleep(1)
    
    # Step 4: Get all projects
    all_projects = get_all_projects(token)
    
    # Step 5: Get employer projects
    employer_projects = get_employer_projects(token)
    
    # If we have a project ID from the created project, try to get it directly
    if project:
        project_id = project.get("id")
        if project_id:
            project_details = get_project_by_id(token, project_id)
    
    # Run diagnostics
    diagnose_collection_issue()
    
    # Test summary
    print_section("TEST SUMMARY")
    print("Authentication:", "✅ Success" if token else "❌ Failed")
    print("Get Profile:", "✅ Success" if profile else "❌ Failed")
    print("Create Project:", "✅ Success" if project else "❌ Failed")
    print("Get All Projects:", "✅ Success" if all_projects else "❌ Failed")
    print("Get Employer Projects:", "✅ Success" if employer_projects else "❌ Failed")

if __name__ == "__main__":
    run_test() 