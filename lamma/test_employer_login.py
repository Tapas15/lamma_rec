import requests
import json

def test_employer_login():
    # API endpoint
    url = "http://localhost:8000/token"
    
    # Login credentials
    login_data = {
        "username": "test@employer.com",
        "password": "testpassword123"
    }
    
    try:
        # Make POST request to login endpoint
        response = requests.post(url, data=login_data)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Employer login successful!")
            print("Response:", json.dumps(response.json(), indent=2))
            
            # Save the token for future use
            token = response.json()["access_token"]
            print("\nAccess Token:", token)
            print("\nYou can use this token in the Authorization header for protected endpoints:")
            print("Authorization: Bearer", token)
        else:
            print(f"Error logging in: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_login() 