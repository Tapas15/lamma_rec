import requests
import json

def register_candidate():
    # API endpoint
    url = "http://localhost:8000/register/candidate"
    
    # Candidate data
    candidate_data = {
        "email": "candidate@example.com",
        "password": "candidatepass123",
        "full_name": "John Doe",
        "skills": ["Python", "FastAPI", "MongoDB", "Docker"],
        "experience": "3 years of software development",
        "education": "Bachelor's in Computer Science",
        "location": "New York",
        "bio": "Passionate software developer looking for new opportunities"
    }
    
    try:
        # Make POST request to register endpoint
        response = requests.post(url, json=candidate_data)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Candidate registered successfully!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"Error registering candidate: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    register_candidate() 