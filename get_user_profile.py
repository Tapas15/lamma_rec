import requests
import json

def get_user_profile():
    # API endpoint
    url = "http://localhost:8000/profile"
    
    # Get token first
    login_url = "http://localhost:8000/token"
    # login_data = {
    #     "username": "candidate@example.com",  # Replace with your email
    #     "password": "candidatepass123"    # Replace with your password
    # }
    login_data = {
        "username": "test@employer.com",  # Replace with your email
        "password": "testpassword123"    # Replace with your password
    }
    try:
        # Get token
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print("Response:", login_response.text)
            return
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get user profile
        profile_response = requests.get(url, headers=headers)
        
        if profile_response.status_code == 200:
            print("User profile retrieved successfully!")
            print("Profile:", json.dumps(profile_response.json(), indent=2))
            
            # If user is a candidate, get detailed candidate profile
            if profile_response.json()["user_type"] == "candidate":
                candidate_url = "http://localhost:8000/candidate/profile"
                candidate_response = requests.get(candidate_url, headers=headers)
                if candidate_response.status_code == 200:
                    print("\nDetailed Candidate Profile:")
                    print(json.dumps(candidate_response.json(), indent=2))
        else:
            print(f"Error getting profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    get_user_profile() 