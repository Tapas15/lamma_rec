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

def test_employer_project_posting():
    # Test account credentials - using fixed values
    test_email = "test@employer.com"
    test_password = "testpassword123"
    
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

    # Step 3: Post a new project
    project_data = {
        "title": "E-commerce Platform Development",
        "company": employer_data["company_name"],
        "description": "Develop a full-featured e-commerce platform with modern architecture",
        "requirements": [
            "Experience with React/Next.js",
            "Experience with Node.js",
            "Experience with MongoDB",
            "Good communication skills"
        ],
        "budget_range": "$15000-$25000",
        "duration": "4 months",
        "location": "Remote",
        "project_type": "Web Development",
        "skills_required": ["React", "Node.js", "MongoDB", "TypeScript"],
        "deadline": (datetime.utcnow() + timedelta(days=90)).isoformat(),
        "employer_id": employer_id
    }

    post_project_response = requests.post(
        f"{BASE_URL}/projects",
        json=project_data,
        headers=headers
    )
    print("\n3. Post Project:")
    print(f"Status: {post_project_response.status_code}")
    print(f"Response: {json.dumps(post_project_response.json(), indent=2)}")

    if post_project_response.status_code not in [200, 201]:
        print("Failed to create project. Exiting test.")
        return

    # Step 4: Get employer's projects
    get_projects_response = requests.get(
        f"{BASE_URL}/employer/projects",
        headers=headers
    )
    print("\n4. Get Employer Projects:")
    print(f"Status: {get_projects_response.status_code}")
    print(f"Response: {json.dumps(get_projects_response.json(), indent=2)}")

    # Step 5: Update project status
    project_id = post_project_response.json()["id"]
    update_data = {
        "status": "in_progress"
    }
    update_project_response = requests.patch(
        f"{BASE_URL}/projects/{project_id}",
        json=update_data,
        headers=headers
    )
    print("\n5. Update Project Status:")
    print(f"Status: {update_project_response.status_code}")
    print(f"Response: {json.dumps(update_project_response.json(), indent=2)}")

if __name__ == "__main__":
    test_employer_project_posting() 