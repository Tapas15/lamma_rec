import requests
import json

def update_candidate_profile():
    # First login to get token
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
        
        # Update profile
        profile_url = "http://localhost:8000/profile"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Update data with matching skills
        update_data = {
            "skills": [
                "Python",
                "FastAPI",
                "MongoDB",
                "Problem Solving",
                "Software Development"
            ],
            "experience": "5 years of Python development experience with FastAPI and MongoDB",
            "education": "Bachelor's in Computer Science",
            "location": "New York",
            "bio": "Experienced Python developer with expertise in FastAPI and MongoDB"
        }
        
        response = requests.put(profile_url, json=update_data, headers=headers)
        if response.status_code == 200:
            print("\nProfile updated successfully!")
            print("Updated profile:", json.dumps(response.json(), indent=2))
        else:
            print(f"\nError updating profile: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    update_candidate_profile() 