import requests
import json

def delete_user():
    # API endpoint
    url = "http://localhost:8000/profile"
    
    # Get token first
    login_url = "http://localhost:8000/token"
    login_data = {
        "username": "test@example.com",  # Replace with your email
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
        
        # First, get the user profile to confirm deletion
        profile_response = requests.get(url, headers=headers)
        if profile_response.status_code == 200:
            print("Current user profile:")
            print(json.dumps(profile_response.json(), indent=2))
            
            # Ask for confirmation
            confirm = input("\nAre you sure you want to delete this user? (yes/no): ")
            if confirm.lower() != "yes":
                print("Deletion cancelled.")
                return
            
            # Delete user
            delete_response = requests.delete(url, headers=headers)
            
            if delete_response.status_code == 200:
                print("\nUser deleted successfully!")
                print("Response:", json.dumps(delete_response.json(), indent=2))
            else:
                print(f"\nError deleting user: {delete_response.status_code}")
                print("Response:", delete_response.text)
        else:
            print(f"Error getting profile: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    delete_user() 