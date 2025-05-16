import requests
import json
from datetime import datetime

# API endpoints
BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/token"
PROFILE_URL = f"{BASE_URL}/employer/profile"

def print_step(step_num, description):
    print(f"\n{'='*50}")
    print(f"Step {step_num}: {description}")
    print(f"{'='*50}")

def print_response(response):
    print("\nResponse Status:", response.status_code)
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))

# Test data
employer_data = {
    "email": "test_employer@example.com",
    "password": "testpassword123",
    "user_type": "employer",
    "full_name": "Test Employer",
    "company_name": "Test Company",
    "company_description": "A test company for verification",
    "company_website": "https://testcompany.com",
    "company_location": "Test City, Test Country",
    "company_size": "50-100",
    "industry": "Technology",
    "contact_email": "contact@testcompany.com",
    "contact_phone": "+1234567890"
}

# Step 1: Register new employer
print_step(1, "Registering new employer")
register_response = requests.post(REGISTER_URL, json=employer_data)
print_response(register_response)

if register_response.status_code != 200:
    print("Registration failed. Exiting test.")
    exit(1)

# Step 2: Login as employer
print_step(2, "Logging in as employer")
login_data = {
    "username": employer_data["email"],
    "password": employer_data["password"]
}
login_response = requests.post(LOGIN_URL, data=login_data)
print_response(login_response)

if login_response.status_code != 200:
    print("Login failed. Exiting test.")
    exit(1)

# Get access token
access_token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}

# Step 3: Get employer profile
print_step(3, "Getting employer profile")
profile_response = requests.get(PROFILE_URL, headers=headers)
print_response(profile_response)

if profile_response.status_code != 200:
    print("Failed to get employer profile. Exiting test.")
    exit(1)

# Step 4: Update employer profile
print_step(4, "Updating employer profile")
updated_data = {
    "company_description": "Updated company description",
    "company_size": "100-200",
    "industry": "Software Development",
    "contact_phone": "+1987654321"
}
update_response = requests.put(PROFILE_URL, headers=headers, json=updated_data)
print_response(update_response)

if update_response.status_code != 200:
    print("Failed to update employer profile. Exiting test.")
    exit(1)

# Step 5: Verify updated profile
print_step(5, "Verifying updated profile")
verify_response = requests.get(PROFILE_URL, headers=headers)
print_response(verify_response)

if verify_response.status_code != 200:
    print("Failed to verify updated profile. Exiting test.")
    exit(1)

# Verify the updates
updated_profile = verify_response.json()
print("\nVerifying updates:")
for field, value in updated_data.items():
    if updated_profile.get(field) == value:
        print(f"✓ {field} updated successfully")
    else:
        print(f"✗ {field} update failed")

print("\nTest completed successfully!") 