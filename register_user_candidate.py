import requests
import json

def register_user():
    # API endpoint
    url = "http://localhost:8000/register"
    
    # User data
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "user_type": "candidate",
        "full_name": "Test User",
        "skills": ["Python", "FastAPI", "MongoDB"],
        "experience": "3 years of software development",
        "education": "Bachelor's in Computer Science",
        "location": "New York",
        "bio": "Passionate software developer looking for new opportunities",
        "bios": "Passionate software developer looking for new opportunities"
    }
    
    try:
        # Make POST request to register endpoint
        response = requests.post(url, json=user_data)
        
        # Check if request was successful
        if response.status_code == 200:
            print("User registered successfully!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"Error registering user: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    register_user() 