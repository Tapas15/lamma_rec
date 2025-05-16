import requests
import json

def test_logout():
    # API endpoints
    login_url = "http://localhost:8000/token"
    logout_url = "http://localhost:8000/logout/employer"  # or /logout/candidate
    
    # Login credentials
    login_data = {
        "username": "test@employer.com",
        "password": "testpassword123"
    }
    
    try:
        # Step 1: Login to get token
        print("Step 1: Logging in...")
        login_response = requests.post(login_url, data=login_data)
        
        if login_response.status_code == 200:
            print("Login successful!")
            token = login_response.json()["access_token"]
            print("\nAccess Token:", token)
            
            # Step 2: Logout using the token
            print("\nStep 2: Logging out...")
            headers = {"Authorization": f"Bearer {token}"}
            logout_response = requests.post(logout_url, headers=headers)
            
            if logout_response.status_code == 200:
                print("Logout successful!")
                print("Response:", json.dumps(logout_response.json(), indent=2))
            else:
                print(f"Error during logout: {logout_response.status_code}")
                print("Response:", logout_response.text)
        else:
            print(f"Error logging in: {login_response.status_code}")
            print("Response:", login_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_logout() 