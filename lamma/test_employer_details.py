import requests
import json

def test_employer_details():
    # API endpoints
    login_url = "http://localhost:8000/token"
    profile_url = "http://localhost:8000/profile"  # Changed to use profile endpoint
    
    # Login credentials
    login_data = {
        "username": "test@employer.com",
        "password": "testpassword123"
    }
    
    try:
        # Step 1: Login and get token
        print("Step 1: Logging in as employer...")
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print("Response:", login_response.text)
            return
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful!")
        
        # Step 2: Get employer details
        print("\nStep 2: Fetching employer details...")
        profile_response = requests.get(profile_url, headers=headers)
        
        if profile_response.status_code == 200:
            print("Employer details retrieved successfully!")
            employer_data = profile_response.json()
            
            # Verify if user is an employer
            if employer_data.get('user_type') != 'employer':
                print("Error: User is not an employer")
                return
            
            # Display all employer details
            print("\n" + "="*60)
            print("EMPLOYER DETAILS")
            print("="*60)
            
            # Personal Information
            print("\n1. PERSONAL INFORMATION")
            print("-"*40)
            print(f"ID: {employer_data.get('id', 'Not available')}")
            print(f"Full Name: {employer_data.get('full_name', 'Not available')}")
            print(f"Email: {employer_data.get('email', 'Not available')}")
            print(f"User Type: {employer_data.get('user_type', 'Not available')}")
            print(f"Created At: {employer_data.get('created_at', 'Not available')}")
            
            # Company Details
            print("\n2. COMPANY DETAILS")
            print("-"*40)
            print(f"Company Name: {employer_data.get('company_name', 'Not available')}")
            print(f"Company Description: {employer_data.get('company_description', 'Not available')}")
            print(f"Company Website: {employer_data.get('company_website', 'Not available')}")
            print(f"Company Location: {employer_data.get('company_location', 'Not available')}")
            print(f"Company Size: {employer_data.get('company_size', 'Not available')}")
            print(f"Industry: {employer_data.get('industry', 'Not available')}")
            
            # Contact Information
            print("\n3. CONTACT INFORMATION")
            print("-"*40)
            print(f"Contact Email: {employer_data.get('contact_email', 'Not available')}")
            print(f"Contact Phone: {employer_data.get('contact_phone', 'Not available')}")
            print(f"Location: {employer_data.get('location', 'Not available')}")
            
            # Additional Information
            print("\n4. ADDITIONAL INFORMATION")
            print("-"*40)
            print(f"Bio: {employer_data.get('bio', 'Not available')}")
            
            # Posted Jobs Summary
            posted_jobs = employer_data.get('posted_jobs', [])
            print("\n5. POSTED JOBS SUMMARY")
            print("-"*40)
            print(f"Total Jobs Posted: {len(posted_jobs)}")
            
            if posted_jobs:
                print("\nJob Titles:")
                for i, job in enumerate(posted_jobs, 1):
                    print(f"{i}. {job.get('title', 'No title')} - {job.get('company', 'No company')}")
            else:
                print("No jobs posted yet.")
            
            print("\n" + "="*60)
            
            # Print raw data for debugging
            print("\nRaw Data from Response:")
            print("-"*40)
            print(json.dumps(employer_data, indent=2))
            
        else:
            print(f"Error getting employer details: {profile_response.status_code}")
            print("Response:", profile_response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_employer_details() 