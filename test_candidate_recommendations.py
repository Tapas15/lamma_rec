import requests
import json

def test_candidate_recommendations():
    # Candidate login
    login_url = "http://localhost:8000/token"
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        # Login to get token
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print("Candidate login failed!")
            print(login_response.text)
            return
        token = login_response.json()["access_token"]
        print("Candidate login successful! Token obtained.")
        
        # Get job recommendations
        rec_url = "http://localhost:8000/recommendations/jobs"
        headers = {"Authorization": f"Bearer {token}"}
        rec_response = requests.get(rec_url, headers=headers)
        if rec_response.status_code == 200:
            print("\nJob recommendations for candidate:")
            print(json.dumps(rec_response.json(), indent=2))
        else:
            print(f"Error fetching recommendations: {rec_response.status_code}")
            print(rec_response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_candidate_recommendations() 