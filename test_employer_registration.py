import requests
import json

BASE_URL = "http://localhost:8000"

def test_employer_registration():
    print("\nTesting Employer Registration...")
    
    # Test data for employer registration
    employer_data = {
        "email": "employer@test.com",
        "password": "Test@123",
        "user_type": "employer",
        "full_name": "Test Employer",
        "company_name": "Test Company",
        "company_description": "A test company for API testing",
        "industry": "Technology",
        "location": "Test City"
    }
    
    try:
        # Make the registration request
        response = requests.post(
            f"{BASE_URL}/register",
            json=employer_data
        )
        
        # Print response details
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        
        # Check if registration was successful
        if response.status_code == 201:
            print("\n✅ Employer registration successful!")
            return response.json()
        else:
            print("\n❌ Employer registration failed!")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error during registration: {str(e)}")
        return None

if __name__ == "__main__":
    test_employer_registration() 