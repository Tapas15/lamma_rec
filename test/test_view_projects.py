import requests
import json
import sys
from datetime import datetime
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test employer credentials
EMPLOYER_EMAIL = "test@employer.com"
EMPLOYER_PASSWORD = "testpassword123"

def print_json(title, data):
    """Helper function to print JSON data in a formatted way"""
    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2, default=str))  # Use default=str for datetime objects
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

def get_employer_profile(token):
    """Get the employer profile to retrieve the employer ID"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print("✅ Retrieved employer profile")
            return profile
        else:
            print(f"❌ Failed to get employer profile. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error getting employer profile: {str(e)}")
        return None

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

def test_get_employer_projects(token):
    """Test the employer's projects endpoint"""
    print_section("TESTING GET EMPLOYER PROJECTS")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("Making request to /employer/projects...")
        response = requests.get(f"{BASE_URL}/employer/projects", headers=headers)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Retrieved {len(projects)} employer projects")
            if projects:
                print_json("First employer project example", projects[0])
                # Check for required fields
                required_fields = ["id", "title", "company", "description", "requirements"]
                missing_fields = [field for field in required_fields if field not in projects[0]]
                if missing_fields:
                    print(f"❌ WARNING: Project is missing required fields: {', '.join(missing_fields)}")
                else:
                    print("✅ All required fields present in project")
            else:
                print("ℹ️ No projects found for this employer")
                # We'll create a test project later in the flow
            return projects
        else:
            print(f"❌ Failed to retrieve employer projects. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            # For debugging: try to get the raw response
            print(f"Raw response: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error retrieving employer projects: {str(e)}")
        return []
    except Exception as e:
        print(f"❌ Error retrieving employer projects: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return []

def test_project_details(token, project_id):
    """Test viewing details of a specific project"""
    print_section(f"TESTING VIEW PROJECT DETAILS: {project_id}")
    
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

def create_test_project(token, employer_id):
    """Create a test project for later viewing"""
    print_section("CREATING TEST PROJECT")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    project_data = {
        "title": "Test Project for Viewing",
        "company": "Test Company",
        "description": "This is a test project created to test the viewing endpoint.",
        "requirements": ["Python", "FastAPI", "Testing"],
        "budget_range": "$5,000 - $10,000",
        "duration": "1-2 weeks",
        "location": "Remote",
        "project_type": "Testing",
        "skills_required": ["Python", "API Testing", "Documentation"],
        "employer_id": employer_id
    }
    
    try:
        print("Creating test project...")
        response = requests.post(f"{BASE_URL}/projects", headers=headers, json=project_data)
        print(f"Response status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            project = response.json()
            print("✅ Created test project successfully")
            print_json("Created Project", project)
            return project
        else:
            print(f"❌ Failed to create test project. Status: {response.status_code}")
            print_json("Error Response", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error creating test project: {str(e)}")
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

def update_project(token, project_id):
    """Update a project's status and description"""
    print_section(f"UPDATING PROJECT: {project_id}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    update_data = {
        "status": "in_progress",
        "description": "UPDATED: Project is now in progress for testing update endpoint.",
        "budget_range": "$10,000 - $15,000"
    }
    try:
        response = requests.patch(f"{BASE_URL}/projects/{project_id}", headers=headers, json=update_data)
        print(f"Update response status: {response.status_code}")
        if response.status_code == 200:
            updated_project = response.json()
            print("✅ Project updated successfully")
            print_json("Updated Project", updated_project)
            return updated_project
        else:
            print(f"❌ Failed to update project. Status: {response.status_code}")
            print_json("Update Error", response.json() if response.content else "No content")
            return None
    except Exception as e:
        print(f"❌ Error updating project: {str(e)}")
        return None

def delete_project(token, project_id):
    """Delete a project and verify deletion"""
    print_section(f"DELETING PROJECT: {project_id}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.delete(f"{BASE_URL}/projects/{project_id}", headers=headers)
        print(f"Delete response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Project deleted successfully")
            # Verify deletion
            verify_response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
            if verify_response.status_code == 404:
                print("✅ Verified project deletion - project no longer exists")
            else:
                print(f"❌ Project still exists after deletion. Status: {verify_response.status_code}")
            return True
        else:
            print(f"❌ Failed to delete project. Status: {response.status_code}")
            print_json("Delete Error", response.json() if response.content else "No content")
            return False
    except Exception as e:
        print(f"❌ Error deleting project: {str(e)}")
        return False

def run_test():
    """Run all project view tests"""
    print("\n==================================================")
    print("TESTING PROJECT VIEWING ENDPOINTS".center(50))
    print("==================================================\n")
    
    # Step 1: Get authentication token
    print_section("AUTHENTICATING")
    token = get_auth_token(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
    if not token:
        print("❌ Failed to get auth token. Cannot proceed.")
        return
    
    print("✅ Authentication successful")
    
    # Step 2: Get employer profile to retrieve ID
    employer = get_employer_profile(token)
    if not employer or "id" not in employer:
        print("❌ Failed to get valid employer profile. Cannot proceed.")
        return
    
    employer_id = employer["id"]
    print(f"✅ Got employer ID: {employer_id}")
    
    # Step 3: Test general projects endpoint
    all_projects = test_get_all_projects(token)
    
    # Step 4: Test employer projects endpoint
    employer_projects = test_get_employer_projects(token)
    
    # Step 5: Create a test project regardless of whether there are existing projects
    # This ensures we have at least one project that we know is valid for testing
    print("Creating a fresh test project for complete testing...")
    new_project = create_test_project(token, employer_id)
    
    if new_project and "id" in new_project:
        project_id = new_project["id"]
        print(f"Created test project with ID: {project_id}")
        
        # Wait a moment to ensure the project is fully saved in the database
        print("Waiting 1 second for database consistency...")
        time.sleep(1)
        
        # Now test viewing this specific project
        project_details = test_project_details(token, project_id)
        
        if project_details:
            # Step 6: Update the project if we retrieved it successfully
            print("\n--- Testing update for the viewed project ---")
            updated = update_project(token, project_id)
            if updated:
                print("✅ Update project test passed.")
            else:
                print("❌ Update project test failed.")
                
            # Wait a moment to ensure update is fully processed
            time.sleep(1)
            
            # Step 7: Delete the project
            print("\n--- Testing delete for the viewed project ---")
            deleted = delete_project(token, project_id)
            if deleted:
                print("✅ Delete project test passed.")
            else:
                print("❌ Delete project test failed.")
        else:
            print("❌ Could not retrieve the test project details, skipping update/delete tests")
    else:
        print("❌ Failed to create test project, cannot proceed with view/update/delete tests.")
    
    # Run diagnostics if we had issues
    if not all_projects or not employer_projects or not new_project:
        print("\nDetected potential issues with project collections. Running diagnostics...")
        diagnose_collection_issue()
    
    print("\nTest completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    run_test() 