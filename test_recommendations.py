import requests
import json
import time
import random
from datetime import datetime
from pprint import pprint

# Configuration
API_URL = "http://localhost:8001"
EMPLOYER_EMAIL = f"test_employer_{int(time.time())}@example.com"
EMPLOYER_PASSWORD = "password123"
CANDIDATE_EMAIL = f"test_candidate_{int(time.time())}@example.com" 
CANDIDATE_PASSWORD = "password123"

# Test data
test_employer = {
    "email": EMPLOYER_EMAIL,
    "password": EMPLOYER_PASSWORD,
    "full_name": "Test Employer",
    "company_name": "Test Company",
    "company_description": "A company for testing",
    "company_website": "http://testcompany.com",
    "company_location": "Test Location",
    "industry": "Technology",
    "contact_email": EMPLOYER_EMAIL
}

test_candidate = {
    "email": CANDIDATE_EMAIL,
    "password": CANDIDATE_PASSWORD,
    "full_name": "Test Candidate",
    "skills": ["Python", "FastAPI", "MongoDB", "React", "JavaScript", "Docker"],
    "experience": "5 years of software development experience",
    "education": "Bachelor's in Computer Science",
    "location": "Test Location",
    "bio": "A test candidate for testing the recommendation system"
}

test_job = {
    "title": "Senior Python Developer",
    "company": "Test Company",
    "description": "We are looking for a Senior Python Developer with experience in FastAPI and MongoDB.",
    "requirements": ["Python", "FastAPI", "MongoDB", "Docker"],
    "location": "Test Location",
    "salary_range": "$100,000 - $120,000",
    "job_type": "Full-time",
    "is_remote": True
}

test_project = {
    "title": "AI Recommendation System",
    "company": "Test Company",
    "description": "Develop an AI-powered recommendation system using Python and machine learning.",
    "requirements": ["Must have experience with recommendation systems", "Strong Python skills", "Machine learning knowledge"],
    "skills_required": ["Python", "Machine Learning", "MongoDB", "FastAPI"],
    "project_type": "Development",
    "budget_range": "$5,000 - $10,000",
    "duration": "1-3 months",
    "location": "Remote"
}

# Helper functions
def register_employer():
    response = requests.post(f"{API_URL}/register/employer", json=test_employer)
    if response.status_code != 200:
        print(f"Failed to register employer: {response.text}")
        return None
    return response.json()

def register_candidate():
    response = requests.post(f"{API_URL}/register/candidate", json=test_candidate)
    if response.status_code != 200:
        print(f"Failed to register candidate: {response.text}")
        return None
    return response.json()

def login_employer():
    response = requests.post(
        f"{API_URL}/token", 
        data={
            "username": EMPLOYER_EMAIL,
            "password": EMPLOYER_PASSWORD
        }
    )
    if response.status_code != 200:
        print(f"Failed to login as employer: {response.text}")
        return None
    return response.json()["access_token"]

def login_candidate():
    response = requests.post(
        f"{API_URL}/token", 
        data={
            "username": CANDIDATE_EMAIL,
            "password": CANDIDATE_PASSWORD
        }
    )
    if response.status_code != 200:
        print(f"Failed to login as candidate: {response.text}")
        return None
    return response.json()["access_token"]

def post_job(token, employer_id):
    headers = {"Authorization": f"Bearer {token}"}
    job_data = test_job.copy()
    job_data["employer_id"] = employer_id
    response = requests.post(f"{API_URL}/jobs", json=job_data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to post job: {response.text}")
        return None
    return response.json()

def post_project(token, employer_id):
    headers = {"Authorization": f"Bearer {token}"}
    project_data = test_project.copy()
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

def mark_recommendation_as_viewed(token, recommendation_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{API_URL}/recommendations/{recommendation_id}/viewed", headers=headers)
    if response.status_code != 200:
        print(f"Failed to mark recommendation as viewed: {response.text}")
        return None
    return response.json()

def search_jobs(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/jobs/search", json={"query": query}, headers=headers)
    if response.status_code != 200:
        print(f"Failed to search jobs: {response.text}")
        return None
    return response.json()

def search_projects(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/projects/search", json={"query": query}, headers=headers)
    if response.status_code != 200:
        print(f"Failed to search projects: {response.text}")
        return None
    return response.json()

def search_candidates(token, query):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/candidates/search", json={"query": query}, headers=headers)
    if response.status_code != 200:
        print(f"Failed to search candidates: {response.text}")
        return None
    return response.json()

def run_tests():
    print("\n===== RECOMMENDATION SYSTEM TESTING =====\n")
    
    # Step 1: Register employer and candidate
    print("\n----- STEP 1: REGISTERING TEST ACCOUNTS -----")
    print(f"Registering employer: {EMPLOYER_EMAIL}")
    employer = register_employer()
    if not employer:
        print("TEST FAILED: Could not register employer")
        return
    print(f"Employer registered successfully: {employer['full_name']}")
    
    print(f"Registering candidate: {CANDIDATE_EMAIL}")
    candidate = register_candidate()
    if not candidate:
        print("TEST FAILED: Could not register candidate")
        return
    print(f"Candidate registered successfully: {candidate['full_name']}")
    
    # Step 2: Login as employer and candidate
    print("\n----- STEP 2: LOGIN -----")
    employer_token = login_employer()
    if not employer_token:
        print("TEST FAILED: Could not login as employer")
        return
    print("Employer logged in successfully")
    
    candidate_token = login_candidate()
    if not candidate_token:
        print("TEST FAILED: Could not login as candidate")
        return
    print("Candidate logged in successfully")
    
    # Step 3: Employer posts job and project
    print("\n----- STEP 3: CREATING JOB AND PROJECT -----")
    job = post_job(employer_token, employer['id'])
    if not job:
        print("TEST FAILED: Could not create job")
        return
    print(f"Job created successfully: {job['title']}")
    
    project = post_project(employer_token, employer['id'])
    if not project:
        print("TEST FAILED: Could not create project")
        return
    print(f"Project created successfully: {project['title']}")
    
    # Give the system a moment to process embeddings
    print("\nWaiting for embeddings to be processed...")
    time.sleep(2)
    
    # Step 4: Test job recommendations for candidate
    print("\n----- STEP 4: TESTING JOB RECOMMENDATIONS -----")
    job_recommendations = get_job_recommendations(candidate_token)
    if not job_recommendations:
        print("TEST FAILED: Could not get job recommendations")
        return
    
    print(f"Received {len(job_recommendations)} job recommendations")
    for i, rec in enumerate(job_recommendations[:3], 1):  # Show top 3
        print(f"Recommendation {i}:")
        print(f"  Job ID: {rec['job_id']}")
        print(f"  Match Score: {rec['match_score']}")
        print(f"  Explanation: {rec['explanation'][:100]}...")
    
    # Step 5: Test project recommendations for candidate
    print("\n----- STEP 5: TESTING PROJECT RECOMMENDATIONS -----")
    project_recommendations = get_project_recommendations(candidate_token)
    if not project_recommendations:
        print("TEST FAILED: Could not get project recommendations")
        return
    
    print(f"Received {len(project_recommendations)} project recommendations")
    for i, rec in enumerate(project_recommendations[:3], 1):  # Show top 3
        print(f"Recommendation {i}:")
        print(f"  Project ID: {rec['project_id']}")
        print(f"  Match Score: {rec['match_score']}")
        print(f"  Explanation: {rec['explanation'][:100]}...")
    
    # Step 6: Test candidate recommendations for employer (jobs)
    print("\n----- STEP 6: TESTING CANDIDATE RECOMMENDATIONS FOR JOB -----")
    candidate_recommendations = get_candidate_recommendations(employer_token, job['id'])
    if not candidate_recommendations:
        print("TEST FAILED: Could not get candidate recommendations for job")
        return
    
    print(f"Received {len(candidate_recommendations)} candidate recommendations for job")
    for i, rec in enumerate(candidate_recommendations[:3], 1):  # Show top 3
        print(f"Recommendation {i}:")
        print(f"  Candidate ID: {rec['candidate_id']}")
        print(f"  Match Score: {rec['match_score']}")
        print(f"  Explanation: {rec['explanation'][:100]}...")
    
    # Step 7: Test candidate recommendations for employer (projects)
    print("\n----- STEP 7: TESTING CANDIDATE RECOMMENDATIONS FOR PROJECT -----")
    project_candidate_recommendations = get_candidates_for_project(employer_token, project['id'])
    if not project_candidate_recommendations:
        print("TEST FAILED: Could not get candidate recommendations for project")
        return
    
    print(f"Received {len(project_candidate_recommendations)} candidate recommendations for project")
    for i, rec in enumerate(project_candidate_recommendations[:3], 1):  # Show top 3
        print(f"Recommendation {i}:")
        print(f"  Candidate ID: {rec['candidate_id']}")
        print(f"  Match Score: {rec['match_score']}")
        print(f"  Explanation: {rec['explanation'][:100]}...")
    
    # Step 8: Check stored recommendations for candidate
    print("\n----- STEP 8: CHECKING STORED RECOMMENDATIONS FOR CANDIDATE -----")
    candidate_stored_recommendations = get_stored_recommendations(candidate_token)
    if candidate_stored_recommendations is None:  # Could be empty list, which is valid
        print("TEST FAILED: Could not get stored recommendations for candidate")
        return
    
    print(f"Found {len(candidate_stored_recommendations)} stored recommendations for candidate")
    high_score_count = len([r for r in candidate_stored_recommendations if r['match_score'] >= 70])
    print(f"Of which {high_score_count} have scores >= 70")
    
    if len(candidate_stored_recommendations) > 0:
        for i, rec in enumerate(candidate_stored_recommendations[:3], 1):  # Show top 3
            print(f"Stored Recommendation {i}:")
            print(f"  Type: {rec['type']}")
            print(f"  ID: {rec['id']}")
            print(f"  Match Score: {rec['match_score']}")
            
            # If we have a recommendation with details, mark it as viewed
            if i == 1 and 'id' in rec:
                print("\nMarking a recommendation as viewed...")
                result = mark_recommendation_as_viewed(candidate_token, rec['id'])
                if result:
                    print("Recommendation marked as viewed successfully")
                else:
                    print("Failed to mark recommendation as viewed")
    
    # Step 9: Check stored recommendations for employer
    print("\n----- STEP 9: CHECKING STORED RECOMMENDATIONS FOR EMPLOYER -----")
    employer_stored_recommendations = get_stored_recommendations(employer_token)
    if employer_stored_recommendations is None:  # Could be empty list, which is valid
        print("TEST FAILED: Could not get stored recommendations for employer")
        return
    
    print(f"Found {len(employer_stored_recommendations)} stored recommendations for employer")
    high_score_count = len([r for r in employer_stored_recommendations if r['match_score'] >= 70])
    print(f"Of which {high_score_count} have scores >= 70")
    
    if len(employer_stored_recommendations) > 0:
        for i, rec in enumerate(employer_stored_recommendations[:3], 1):  # Show top 3
            print(f"Stored Recommendation {i}:")
            print(f"  Type: {rec['type']}")
            print(f"  ID: {rec['id']}")
            print(f"  Match Score: {rec['match_score']}")
    
    # Step 10: Test semantic search
    print("\n----- STEP 10: TESTING SEMANTIC SEARCH -----")
    
    # Job search
    print("\nSearching for Python jobs...")
    job_search_results = search_jobs(candidate_token, "Python developer with FastAPI experience")
    if job_search_results is None:
        print("TEST FAILED: Could not search for jobs")
    else:
        print(f"Found {len(job_search_results)} matching jobs")
        if len(job_search_results) > 0:
            for i, job_result in enumerate(job_search_results[:2], 1):
                print(f"Job Result {i}: {job_result['title']}")
    
    # Project search
    print("\nSearching for AI projects...")
    project_search_results = search_projects(candidate_token, "AI machine learning projects")
    if project_search_results is None:
        print("TEST FAILED: Could not search for projects")
    else:
        print(f"Found {len(project_search_results)} matching projects")
        if len(project_search_results) > 0:
            for i, project_result in enumerate(project_search_results[:2], 1):
                print(f"Project Result {i}: {project_result['title']}")
    
    # Candidate search (employer only)
    print("\nSearching for candidates with Python skills...")
    candidate_search_results = search_candidates(employer_token, "Python developer with FastAPI experience")
    if candidate_search_results is None:
        print("TEST FAILED: Could not search for candidates")
    else:
        print(f"Found {len(candidate_search_results)} matching candidates")
        if len(candidate_search_results) > 0:
            for i, candidate_result in enumerate(candidate_search_results[:2], 1):
                print(f"Candidate Result {i}: {candidate_result['full_name']}")
    
    print("\n===== TEST COMPLETED =====")
    print("Summary:")
    print(f"- Job recommendations for candidate: {len(job_recommendations) if job_recommendations else 'Failed'}")
    print(f"- Project recommendations for candidate: {len(project_recommendations) if project_recommendations else 'Failed'}")
    print(f"- Candidate recommendations for employer's job: {len(candidate_recommendations) if candidate_recommendations else 'Failed'}")
    print(f"- Candidate recommendations for employer's project: {len(project_candidate_recommendations) if project_candidate_recommendations else 'Failed'}")
    print(f"- Stored recommendations for candidate: {len(candidate_stored_recommendations) if candidate_stored_recommendations is not None else 'Failed'}")
    print(f"- Stored recommendations for employer: {len(employer_stored_recommendations) if employer_stored_recommendations is not None else 'Failed'}")

if __name__ == "__main__":
    run_tests() 