import requests
import json

def register_employer():
    # API endpoint
    url = "http://localhost:8000/register"
    
    # Employer data
    employer_data = {
        "email": "employer@techcompany.com",
        "password": "employerpass123",
        "user_type": "employer",
        "full_name": "Updated Tech Company",
        "company_name": "Tech Solutions Inc.",
        "company_description": "Leading technology solutions provider",
        "company_website": "https://techsolutions.com",
        "company_location": "San Francisco, CA",
        "company_size": "100-500",
        "industry": "Technology",
        "contact_email": "hr@techsolutions.com",
        "contact_phone": "+1-555-0123",
        "location": "San Francisco",
        "bio": "Leading technology company looking for talented professionals"
        
    }
    
    try:
        # Make POST request to register endpoint
        response = requests.post(url, json=employer_data)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Employer registered successfully!")
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"Error registering employer: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    register_employer() 