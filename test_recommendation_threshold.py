import requests
import json
import time
from pprint import pprint
from datetime import datetime, timedelta

# Configuration
API_URL = "http://localhost:8001"
EMPLOYER_EMAIL = f"threshold_employer_{int(time.time())}@example.com"
EMPLOYER_PASSWORD = "password123"
CANDIDATE_EMAIL = f"threshold_candidate_{int(time.time())}@example.com" 
CANDIDATE_PASSWORD = "password123"

# Test data for employer
test_employer = {
    "email": EMPLOYER_EMAIL,
    "password": EMPLOYER_PASSWORD,
    "full_name": "Threshold Test Employer",
    "company_name": "Threshold Company",
    "company_description": "A company for testing recommendation thresholds",
    "company_website": "http://thresholdcompany.com",
    "company_location": "Threshold Location",
    "industry": "Technology",
    "contact_email": EMPLOYER_EMAIL
}

# Test data for candidates with varying skill levels
test_candidates = [
    {
        "email": f"high_match_{CANDIDATE_EMAIL}",
        "password": CANDIDATE_PASSWORD,
        "full_name": "High Match Candidate",
        "skills": ["Python", "FastAPI", "MongoDB", "React", "Docker", "AWS", "Machine Learning"],
        "experience": "7 years of software development experience with Python, FastAPI and MongoDB",
        "education": "Master's in Computer Science",
        "location": "Threshold Location",  # Same location for higher match
        "bio": "Senior developer with extensive experience in Python backends and ML"
    },
    {
        "email": f"medium_match_{CANDIDATE_EMAIL}",
        "password": CANDIDATE_PASSWORD,
        "full_name": "Medium Match Candidate",
        "skills": ["Python", "Django", "PostgreSQL", "JavaScript"],
        "experience": "3 years of web development with Python and Django",
        "education": "Bachelor's in Information Technology",
        "location": "Remote",
        "bio": "Mid-level developer with focus on web applications"
    },
    {
        "email": f"low_match_{CANDIDATE_EMAIL}",
        "password": CANDIDATE_PASSWORD,
        "full_name": "Low Match Candidate",
        "skills": ["Java", "Spring", "Oracle", "Android"],
        "experience": "4 years of Java development",
        "education": "Associate's Degree in Programming",
        "location": "Different City",
        "bio": "Java developer with mobile experience"
    }
]

# Test jobs with clear skill requirements
test_jobs = [
    {
        "title": "Senior Python Backend Developer",
        "company": "Threshold Company",
        "description": "We need a senior Python developer with extensive FastAPI and MongoDB experience.",
        "requirements": ["Python", "FastAPI", "MongoDB", "Docker", "AWS"],
        "location": "Threshold Location",
        "salary_range": "$120,000 - $150,000",
        "job_type": "Full-time",
        "is_remote": False
    },
    {
        "title": "Junior Web Developer",
        "company": "Threshold Company",
        "description": "Entry-level position for a web developer.",
        "requirements": ["HTML", "CSS", "JavaScript", "React"],
        "location": "Threshold Location",
        "salary_range": "$60,000 - $80,000",
        "job_type": "Full-time",
        "is_remote": False
    }
]

# Test projects with clear skill requirements
test_projects = [
    {
        "title": "Machine Learning Recommendation Engine",
        "company": "Threshold Company",
        "description": "Develop an advanced ML-powered recommendation system for our e-commerce platform.",
        "requirements": ["Must have ML experience", "Python expertise required", "Knowledge of recommendation algorithms"],
        "skills_required": ["Python", "Machine Learning", "TensorFlow", "MongoDB"],
        "project_type": "Development",
        "budget_range": "$15,000 - $25,000",
        "duration": "2-4 months",
        "location": "Remote"
    },
    {
        "title": "Mobile App Development",
        "company": "Threshold Company",
        "description": "Create a mobile app for our existing web platform.",
        "requirements": ["Mobile development experience", "Knowledge of React Native"],
        "skills_required": ["JavaScript", "React Native", "iOS", "Android"],
        "project_type": "Development",
        "budget_range": "$10,000 - $20,000",
        "duration": "2-3 months",
        "location": "Remote"
    }
]

def register_employer():
    response = requests.post(f"{API_URL}/register/employer", json=test_employer)
    if response.status_code != 200:
        print(f"Failed to register employer: {response.text}")
        return None
    return response.json()

def register_candidate(candidate_data):
    response = requests.post(f"{API_URL}/register/candidate", json=candidate_data)
    if response.status_code != 200:
        print(f"Failed to register candidate: {response.text}")
        return None
    return response.json()

def login_user(email, password):
    response = requests.post(
        f"{API_URL}/token", 
        data={
            "username": email,
            "password": password
        }
    )
    if response.status_code != 200:
        print(f"Failed to login: {response.text}")
        return None
    return response.json()["access_token"]

def post_job(token, employer_id, job_data):
    headers = {"Authorization": f"Bearer {token}"}
    job_data = job_data.copy()
    job_data["employer_id"] = employer_id
    response = requests.post(f"{API_URL}/jobs", json=job_data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to post job: {response.text}")
        return None
    return response.json()

def post_project(token, employer_id, project_data):
    headers = {"Authorization": f"Bearer {token}"}
    project_data = project_data.copy()
    project_data["employer_id"] = employer_id
    response = requests.post(f"{API_URL}/projects", json=project_data, headers=headers)
    if response.status_code != 201:
        print(f"Failed to post project: {response.text}")
        return None
    return response.json()

def get_job_recommendations(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/jobs", headers=headers)
    if response.status_code != 200:
        print(f"Failed to get job recommendations: {response.text}")
        return None
    return response.json()

def get_project_recommendations(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/projects", headers=headers)
    if response.status_code != 200:
        print(f"Failed to get project recommendations: {response.text}")
        return None
    return response.json()

def get_candidate_recommendations(token, job_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/candidates/{job_id}", headers=headers)
    if response.status_code != 200:
        print(f"Failed to get candidate recommendations: {response.text}")
        return None
    return response.json()

def get_candidates_for_project(token, project_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/candidates-for-project/{project_id}", headers=headers)
    if response.status_code != 200:
        print(f"Failed to get candidate recommendations for project: {response.text}")
        return None
    return response.json()

def get_stored_recommendations(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/stored", headers=headers)
    if response.status_code != 200:
        print(f"Failed to get stored recommendations: {response.text}")
        return None
    return response.json()

def run_threshold_test():
    print("\n===== RECOMMENDATION THRESHOLD TESTING =====\n")
    
    # Step 1: Register employer
    print("\n----- REGISTERING EMPLOYER -----")
    employer = register_employer()
    if not employer:
        print("TEST FAILED: Could not register employer")
        return
    print(f"Employer registered successfully: {employer['full_name']}")
    
    # Step 2: Register candidates with different match potentials
    print("\n----- REGISTERING CANDIDATES -----")
    registered_candidates = []
    for candidate_data in test_candidates:
        print(f"Registering candidate: {candidate_data['full_name']}")
        candidate = register_candidate(candidate_data)
        if candidate:
            registered_candidates.append({
                "data": candidate_data,
                "profile": candidate
            })
            print(f"Candidate registered successfully: {candidate['full_name']}")
        else:
            print(f"Failed to register candidate: {candidate_data['full_name']}")
    
    if not registered_candidates:
        print("TEST FAILED: Could not register any candidates")
        return
        
    # Step 3: Login as employer
    print("\n----- LOGIN AS EMPLOYER -----")
    employer_token = login_user(EMPLOYER_EMAIL, EMPLOYER_PASSWORD)
    if not employer_token:
        print("TEST FAILED: Could not login as employer")
        return
    print("Employer logged in successfully")
    
    # Step 4: Post jobs and projects
    print("\n----- POSTING JOBS -----")
    posted_jobs = []
    for job_data in test_jobs:
        print(f"Posting job: {job_data['title']}")
        job = post_job(employer_token, employer['id'], job_data)
        if job:
            posted_jobs.append(job)
            print(f"Job posted successfully: {job['title']}")
        else:
            print(f"Failed to post job: {job_data['title']}")
            
    print("\n----- POSTING PROJECTS -----")
    posted_projects = []
    for project_data in test_projects:
        print(f"Posting project: {project_data['title']}")
        project = post_project(employer_token, employer['id'], project_data)
        if project:
            posted_projects.append(project)
            print(f"Project posted successfully: {project['title']}")
        else:
            print(f"Failed to post project: {project_data['title']}")
    
    if not posted_jobs or not posted_projects:
        print("TEST FAILED: Could not post required jobs or projects")
        return
    
    # Give the system a moment to process embeddings
    print("\nWaiting for embeddings to be processed...")
    time.sleep(3)
    
    # Step 5: Login as each candidate and check recommendations
    print("\n----- CHECKING CANDIDATE RECOMMENDATIONS -----")
    
    for candidate in registered_candidates:
        print(f"\nTesting recommendations for: {candidate['data']['full_name']}")
        
        # Login as this candidate
        candidate_token = login_user(candidate['data']['email'], CANDIDATE_PASSWORD)
        if not candidate_token:
            print(f"Could not login as {candidate['data']['full_name']}")
            continue
            
        # Get job recommendations
        job_recommendations = get_job_recommendations(candidate_token)
        if job_recommendations:
            print(f"Job Recommendations for {candidate['data']['full_name']}:")
            for i, rec in enumerate(job_recommendations, 1):
                print(f"  Job {i}: {rec.get('job_id', 'Unknown')} - Score: {rec.get('match_score', 'Unknown')}")
        else:
            print(f"No job recommendations for {candidate['data']['full_name']}")
            
        # Get project recommendations
        project_recommendations = get_project_recommendations(candidate_token)
        if project_recommendations:
            print(f"Project Recommendations for {candidate['data']['full_name']}:")
            for i, rec in enumerate(project_recommendations, 1):
                print(f"  Project {i}: {rec.get('project_id', 'Unknown')} - Score: {rec.get('match_score', 'Unknown')}")
        else:
            print(f"No project recommendations for {candidate['data']['full_name']}")
            
        # Check stored recommendations (should only contain scores >= 70)
        stored_recommendations = get_stored_recommendations(candidate_token)
        if stored_recommendations is not None:
            print(f"Stored Recommendations for {candidate['data']['full_name']}: {len(stored_recommendations)}")
            if stored_recommendations:
                below_threshold = [r for r in stored_recommendations if r.get('match_score', 0) < 70]
                if below_threshold:
                    print(f"ERROR: Found {len(below_threshold)} recommendations below threshold!")
                    for r in below_threshold:
                        print(f"  Score: {r.get('match_score')}, Type: {r.get('type')}")
                else:
                    print(f"SUCCESS: All {len(stored_recommendations)} stored recommendations are above threshold")
                    
                # Print the stored recommendations
                for i, rec in enumerate(stored_recommendations[:3], 1):  # Show up to 3
                    print(f"  Stored {i}: Type={rec.get('type', 'Unknown')}, Score={rec.get('match_score', 'Unknown')}")
    
    # Step 6: Check candidate recommendations for jobs and projects
    print("\n----- CHECKING EMPLOYER CANDIDATE RECOMMENDATIONS -----")
    
    # Check candidate recommendations for each job
    for job in posted_jobs:
        print(f"\nCandidate recommendations for job: {job['title']}")
        
        candidate_recommendations = get_candidate_recommendations(employer_token, job['id'])
        if candidate_recommendations:
            print(f"Found {len(candidate_recommendations)} candidate recommendations")
            for i, rec in enumerate(candidate_recommendations, 1):
                print(f"  Candidate {i}: {rec.get('candidate_id', 'Unknown')} - Score: {rec.get('match_score', 'Unknown')}")
        else:
            print("No candidate recommendations found")
            
    # Check candidate recommendations for each project
    for project in posted_projects:
        print(f"\nCandidate recommendations for project: {project['title']}")
        
        candidate_recommendations = get_candidates_for_project(employer_token, project['id'])
        if candidate_recommendations:
            print(f"Found {len(candidate_recommendations)} candidate recommendations")
            for i, rec in enumerate(candidate_recommendations, 1):
                print(f"  Candidate {i}: {rec.get('candidate_id', 'Unknown')} - Score: {rec.get('match_score', 'Unknown')}")
        else:
            print("No candidate recommendations found")
    
    # Step 7: Check employer's stored recommendations (should only contain scores >= 70)
    print("\n----- CHECKING EMPLOYER'S STORED RECOMMENDATIONS -----")
    
    employer_recommendations = get_stored_recommendations(employer_token)
    if employer_recommendations is not None:
        print(f"Found {len(employer_recommendations)} stored recommendations for employer")
        
        # Check for recommendations below threshold
        below_threshold = [r for r in employer_recommendations if r.get('match_score', 0) < 70]
        if below_threshold:
            print(f"ERROR: Found {len(below_threshold)} recommendations below threshold!")
            for r in below_threshold:
                print(f"  Score: {r.get('match_score')}, Type: {r.get('type')}")
        else:
            print(f"SUCCESS: All {len(employer_recommendations)} stored recommendations are above threshold")
            
        # Print stored recommendations
        for i, rec in enumerate(employer_recommendations[:5], 1):  # Show up to 5
            print(f"  Recommendation {i}:")
            print(f"    Type: {rec.get('type', 'Unknown')}")
            print(f"    Score: {rec.get('match_score', 'Unknown')}")
            if 'candidate_details' in rec:
                print(f"    Candidate: {rec['candidate_details'].get('full_name', 'Unknown')}")
    
    print("\n===== THRESHOLD TEST SUMMARY =====")
    print(f"Candidates tested: {len(registered_candidates)}")
    print(f"Jobs posted: {len(posted_jobs)}")
    print(f"Projects posted: {len(posted_projects)}")
    
    print("\nThreshold Test Completed!")

if __name__ == "__main__":
    run_threshold_test() 