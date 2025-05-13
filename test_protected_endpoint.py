import requests
import json

def test_protected_endpoint():
    # Get the token first
    login_url = "http://localhost:8000/token"
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Login to get token
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print("Login failed!")
            return
            
        token = login_response.json()["access_token"]
        print("Successfully obtained access token")
        
        # Test accessing protected endpoint (get jobs)
        jobs_url = "http://localhost:8000/jobs"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Make request to protected endpoint
        response = requests.get(jobs_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            print("\nSuccessfully accessed protected endpoint!")
            print("Available jobs:", json.dumps(response.json(), indent=2))
        else:
            print(f"\nError accessing protected endpoint: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_protected_endpoint() 