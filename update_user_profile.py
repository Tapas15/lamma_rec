import requests
import json

def update_user_profile():
    # API endpoint
    url = "http://localhost:8000/profile"
    
    # Get token first
    login_url = "http://localhost:8000/token"
    # login_data = {
    #     "username": "test@employer.com",  # Replace with your email
    #     "password": "testpassword123"    # Replace with your password
    # }

    login_data = {
        "username": "candidate@example.com",  # Replace with your email
        "password": "candidatepass123"    # Replace with your password
    }
    
    # Update data
    update_data = {
        "full_name": "Updated Test User ",
        "skills": ["Python", "FastAPI", "MongoDB", "Docker", "AWS"],  # Updated skills
        "experience": "5 years of software development with focus on backend systems",
        "education": "Master's in Computer Science",
        "location": "San Francisco",
        "bio": "Senior software developer with expertise in cloud technologies and microservices"
    }

    # update_data = {
    #     "full_name": "Updated Test User five ",
    #     "company_name": "Updated Tech Solutions Inc.",
    #     "company_description": "Leading technology solutions provider",
    #     "company_website": "https://techsolutions.com",
    #     "company_location": "San Francisco, CA",
    #     "company_size": "100-500",
    #     "industry": "Technology",
    #     "contact_email": "hr@techsolutions.com",
    #     "contact_phone": "+1-555-0123",
    #     "location": "San Francisco",
    #     "bio": "HR Manager at Tech Solutions Inc. with expertise in tech recruitment"   
    
    # }
    
    try:
        # Get token
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print("Response:", login_response.text)
            return
            
        token = login_response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Update profile
        update_response = requests.put(url, headers=headers, json=update_data)
        
        if update_response.status_code == 200:
            print("Profile updated successfully!")
            print("Updated Profile:", json.dumps(update_response.json(), indent=2))
        else:
            print(f"Error updating profile: {update_response.status_code}")
            print("Response:", update_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    update_user_profile() 