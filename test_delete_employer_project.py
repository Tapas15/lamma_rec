import requests
import json
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

def cleanup_test_account(email, password):
    """Clean up the test account if it exists"""
    # Login
    login_data = {
        "username": email,
        "password": password
    }
    login_response = requests.post(
        f"{BASE_URL}/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if login_response.status_code == 200:
        # If login successful, delete the account
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        requests.delete(f"{BASE_URL}/profile", headers=headers)

def test_delete_employer_project():
    # Test account credentials - using fixed values
    test_email = "projectmanager@testcompany.com"
    test_password = "test123456"
    
    # Clean up any existing test account
    cleanup_test_account(test_email, test_password)
    
    # Test data for employer registration
    employer_data = {
        "email": test_email,
        "password": test_password,
        "full_name": "Project Manager",
        "user_type": "employer",
        "company_name": "Test Company",
        "company_description": "A test company for project management",
        "company_website": "https://testcompany.com",
        "company_location": "Test City",
        "company_size": "10-50",
        "industry": "Technology",
        "contact_email": test_email,
        "contact_phone": "+1-555-0123",
        "location": "Test City",
        "bio": "Test account for project management"
    }

    # Step 1: Register employer
    print("\n1. Registering employer...")
    register_response = requests.post(
        f"{BASE_URL}/register/employer",
        json=employer_data
    )
    print(f"Status: {register_response.status_code}")
    print(f"Response: {json.dumps(register_response.json(), indent=2)}")

    if register_response.status_code != 200:
        print("Failed to register employer. Exiting test.")
        return

    employer_id = register_response.json()["id"]

    # Step 2: Login employer
    print("\n2. Logging in employer...")
    login_data = {
        "username": test_email,
        "password": test_password
    }
    login_response = requests.post(
        f"{BASE_URL}/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Status: {login_response.status_code}")
    print(f"Response: {json.dumps(login_response.json(), indent=2)}")

    if login_response.status_code != 200:
        print("Failed to login. Exiting test.")
        return

    # Get access token
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Step 3: Create multiple projects
    print("\n3. Creating projects...")
    projects = []
    project_names = ["Website Redesign", "Mobile App Development", "API Integration"]
    project_descriptions = [
        "Complete website redesign with modern UI/UX",
        "Develop a cross-platform mobile application",
        "Integrate third-party APIs and create documentation"
    ]
    
    for i in range(3):
        project_data = {
            "title": project_names[i],
            "company": employer_data["company_name"],
            "description": project_descriptions[i],
            "requirements": [
                "Python",
                "FastAPI",
                "MongoDB"
            ],
            "budget_range": f"${5000*(i+1)}-${8000*(i+1)}",
            "duration": f"{i+2} months",
            "location": "Remote",
            "project_type": "Software Development",
            "skills_required": ["Python", "FastAPI", "MongoDB"],
            "deadline": (datetime.utcnow() + timedelta(days=30*(i+1))).isoformat(),
            "employer_id": employer_id
        }
        
        create_response = requests.post(
            f"{BASE_URL}/projects",
            json=project_data,
            headers=headers
        )
        print(f"\nCreated Project {i+1}: {project_names[i]}")
        print(f"Status: {create_response.status_code}")
        print(f"Response: {json.dumps(create_response.json(), indent=2)}")
        
        if create_response.status_code in [200, 201]:
            projects.append(create_response.json())
        else:
            print(f"Failed to create project {i+1}")

    if not projects:
        print("No projects were created. Exiting test.")
        return

    # Step 4: List all projects before deletion
    print("\n4. Listing all projects before deletion...")
    list_response = requests.get(
        f"{BASE_URL}/employer/projects",
        headers=headers
    )
    print(f"Status: {list_response.status_code}")
    print(f"Projects before deletion: {json.dumps(list_response.json(), indent=2)}")

    # Step 5: Delete projects one by one
    print("\n5. Deleting projects...")
    for project in projects:
        project_id = project["id"]
        project_title = project["title"]
        delete_response = requests.delete(
            f"{BASE_URL}/projects/{project_id}",
            headers=headers
        )
        print(f"\nDeleting project: {project_title}")
        print(f"Status: {delete_response.status_code}")
        print(f"Response: {json.dumps(delete_response.json(), indent=2)}")

    # Step 6: Verify all projects are deleted
    print("\n6. Verifying projects are deleted...")
    final_list_response = requests.get(
        f"{BASE_URL}/employer/projects",
        headers=headers
    )
    print(f"Status: {final_list_response.status_code}")
    print(f"Projects after deletion: {json.dumps(final_list_response.json(), indent=2)}")

    # Step 7: Try to delete a non-existent project (should fail)
    print("\n7. Testing deletion of non-existent project...")
    non_existent_id = "non_existent_id"
    error_delete_response = requests.delete(
        f"{BASE_URL}/projects/{non_existent_id}",
        headers=headers
    )
    print(f"Status: {error_delete_response.status_code}")
    print(f"Response: {json.dumps(error_delete_response.json(), indent=2)}")

    # Clean up: Delete the test account
    print("\n8. Cleaning up test account...")
    cleanup_response = requests.delete(
        f"{BASE_URL}/profile",
        headers=headers
    )
    print(f"Cleanup Status: {cleanup_response.status_code}")

if __name__ == "__main__":
    test_delete_employer_project() 