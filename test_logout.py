import requests
import json
import time

def test_logout():
    # API endpoints
    login_url = "http://localhost:8000/token"
    profile_url = "http://localhost:8000/profile"
    logout_url = "http://localhost:8000/logout"
    
    # Login credentials
    login_data = {
        "username": "test@example.com",  # Replace with your email
        "password": "testpassword123"    # Replace with your password
    }
    
    try:
        # Step 1: Login and get token
        print("Step 1: Logging in...")
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print("Response:", login_response.text)
            return
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful!")
        
        # Step 2: Try to access profile (should work)
        print("\nStep 2: Testing profile access before logout...")
        profile_response = requests.get(profile_url, headers=headers)
        if profile_response.status_code == 200:
            print("Profile access successful!")
            print("Profile:", json.dumps(profile_response.json(), indent=2))
        else:
            print(f"Profile access failed: {profile_response.status_code}")
            print("Response:", profile_response.text)
            return
        
        # Step 3: Logout
        print("\nStep 3: Logging out...")
        logout_response = requests.post(logout_url, headers=headers)
        if logout_response.status_code == 200:
            print("Logout successful!")
            print("Response:", json.dumps(logout_response.json(), indent=2))
        else:
            print(f"Logout failed: {logout_response.status_code}")
            print("Response:", logout_response.text)
            return
        
        # Add a small delay to ensure token invalidation is processed
        time.sleep(1)
        
        # Step 4: Try to access profile again (should fail)
        print("\nStep 4: Testing profile access after logout...")
        profile_response = requests.get(profile_url, headers=headers)
        if profile_response.status_code == 401:
            print("Profile access failed as expected (token invalidated)")
            print("Response:", profile_response.text)
        else:
            print(f"Unexpected response: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
        # Step 5: Try to logout again (should fail)
        print("\nStep 5: Testing logout with invalidated token...")
        logout_response = requests.post(logout_url, headers=headers)
        if logout_response.status_code == 401:
            print("Second logout failed as expected (token already invalidated)")
            print("Response:", logout_response.text)
        else:
            print(f"Unexpected response: {logout_response.status_code}")
            print("Response:", logout_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_logout() 