import requests
import json
import time
from datetime import datetime
from pprint import pprint
import sys
import random

# Configuration
API_URL = "http://localhost:8003"
TIMESTAMP = int(time.time())
EMPLOYER_EMAIL = f"e2e_employer_{TIMESTAMP}@example.com"
EMPLOYER_PASSWORD = "password123"
CANDIDATE1_EMAIL = f"e2e_candidate1_{TIMESTAMP}@example.com"
CANDIDATE2_EMAIL = f"e2e_candidate2_{TIMESTAMP}@example.com"
CANDIDATE_PASSWORD = "password123"

# Test data
test_employer = {
    "email": EMPLOYER_EMAIL,
    "password": EMPLOYER_PASSWORD,
    "full_name": "E2E Test Employer",
    "company_name": "E2E Test Company",
    "company_description": "A company for end-to-end testing of the recommendation system",
    "company_website": "http://e2etestcompany.com",
    "company_location": "E2E Test Location",
    "industry": "Technology",
    "contact_email": EMPLOYER_EMAIL
}

test_candidate1 = {
    "email": CANDIDATE1_EMAIL,
    "password": CANDIDATE_PASSWORD,
    "full_name": "E2E Test Candidate 1",
    "skills": ["Python", "FastAPI", "MongoDB", "React", "JavaScript", "Docker", "AWS", "Machine Learning"],
    "experience": "7 years of software development experience with Python, FastAPI and MongoDB",
    "education": "Master's in Computer Science",
    "location": "E2E Test Location",
    "bio": "Senior developer with extensive experience in Python backends and ML"
}

test_candidate2 = {
    "email": CANDIDATE2_EMAIL,
    "password": CANDIDATE_PASSWORD,
    "full_name": "E2E Test Candidate 2",
    "skills": ["Java", "Spring", "Oracle", "Android", "Kotlin"],
    "experience": "5 years of mobile app development",
    "education": "Bachelor's in Computer Engineering",
    "location": "Remote",
    "bio": "Mobile developer specializing in Android applications"
}

test_job1 = {
    "title": "Senior Python Developer",
    "company": "E2E Test Company",
    "description": "We are looking for a Senior Python Developer with experience in FastAPI, MongoDB, and AWS.",
    "requirements": ["Python", "FastAPI", "MongoDB", "Docker", "AWS"],
    "location": "E2E Test Location",
    "salary_range": "$120,000 - $150,000",
    "job_type": "Full-time",
    "is_remote": True
}

test_job2 = {
    "title": "Mobile App Developer",
    "company": "E2E Test Company",
    "description": "Seeking an experienced mobile developer for our Android team.",
    "requirements": ["Java", "Kotlin", "Android", "Firebase", "REST APIs"],
    "location": "Remote",
    "salary_range": "$100,000 - $130,000",
    "job_type": "Full-time",
    "is_remote": True
}

test_project1 = {
    "title": "AI Recommendation Engine",
    "company": "E2E Test Company",
    "description": "Build an advanced AI recommendation system using Python and machine learning techniques.",
    "requirements": ["Must have experience with recommendation systems", "Strong Python skills", "ML knowledge"],
    "skills_required": ["Python", "Machine Learning", "TensorFlow", "NLP", "MongoDB"],
    "project_type": "Development",
    "budget_range": "$15,000 - $25,000",
    "duration": "2-4 months",
    "location": "Remote"
}

test_project2 = {
    "title": "Android E-commerce App",
    "company": "E2E Test Company",
    "description": "Develop a mobile e-commerce application for Android.",
    "requirements": ["Mobile development experience", "Knowledge of e-commerce platforms"],
    "skills_required": ["Java", "Kotlin", "Android", "Firebase", "Payment APIs"],
    "project_type": "Development",
    "budget_range": "$10,000 - $20,000",
    "duration": "2-3 months",
    "location": "Remote"
}

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
    
    def pass_test(self, message):
        self.passed += 1
        self.total += 1
        print(f"✅ PASS: {message}")
    
    def fail_test(self, message, details=None):
        self.failed += 1
        self.total += 1
        print(f"❌ FAIL: {message}")
        if details:
            print(f"     Details: {details}")
    
    def summary(self):
        print("\n===== TEST SUMMARY =====")
        print(f"Total tests: {self.total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Pass rate: {(self.passed / self.total * 100):.2f}%")
        return self.failed == 0

# Helper functions
def register_employer(test_results):
    response = requests.post(f"{API_URL}/register/employer", json=test_employer)
    if response.status_code != 200:
        test_results.fail_test("Register employer", response.text)
        return None
    test_results.pass_test("Register employer")
    return response.json()

def register_candidate(candidate_data, test_results, test_name="Register candidate"):
    response = requests.post(f"{API_URL}/register/candidate", json=candidate_data)
    if response.status_code != 200:
        test_results.fail_test(test_name, response.text)
        return None
    test_results.pass_test(test_name)
    return response.json()

def login_user(email, password, test_results, test_name="Login user"):
    response = requests.post(
        f"{API_URL}/token", 
        data={
            "username": email,
            "password": password
        }
    )
    if response.status_code != 200:
        test_results.fail_test(test_name, response.text)
        return None
    test_results.pass_test(test_name)
    return response.json()["access_token"]

def create_job(token, job_data, employer_id, test_results, test_name="Create job"):
    headers = {"Authorization": f"Bearer {token}"}
    job_payload = job_data.copy()
    job_payload["employer_id"] = employer_id
    response = requests.post(f"{API_URL}/jobs", json=job_payload, headers=headers)
    if response.status_code != 200:
        test_results.fail_test(test_name, response.text)
        return None
    test_results.pass_test(test_name)
    return response.json()

def create_project(token, project_data, employer_id, test_results, test_name="Create project"):
    headers = {"Authorization": f"Bearer {token}"}
    project_payload = project_data.copy()
    project_payload["employer_id"] = employer_id
    response = requests.post(f"{API_URL}/projects", json=project_payload, headers=headers)
    if response.status_code != 201:
        test_results.fail_test(test_name, response.text)
        return None
    test_results.pass_test(test_name)
    return response.json()

def get_job_recommendations(token, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/jobs", headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Get job recommendations", response.text)
        return None
    test_results.pass_test("Get job recommendations")
    return response.json()

def get_project_recommendations(token, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/projects", headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Get project recommendations", response.text)
        return None
    test_results.pass_test("Get project recommendations")
    return response.json()

def get_candidate_recommendations(token, job_id, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/candidates/{job_id}", headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Get candidate recommendations for job", response.text)
        return None
    test_results.pass_test("Get candidate recommendations for job")
    return response.json()

def get_candidates_for_project(token, project_id, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/candidates-for-project/{project_id}", headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Get candidate recommendations for project", response.text)
        return None
    test_results.pass_test("Get candidate recommendations for project")
    return response.json()

def search_jobs(token, query, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/jobs/search", json={"query": query}, headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Search jobs", response.text)
        return None
    test_results.pass_test("Search jobs")
    return response.json()

def search_projects(token, query, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/projects/search", json={"query": query}, headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Search projects", response.text)
        return None
    test_results.pass_test("Search projects")
    return response.json()

def search_candidates(token, query, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/candidates/search", json={"query": query}, headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Search candidates", response.text)
        return None
    test_results.pass_test("Search candidates")
    return response.json()

def get_stored_recommendations(token, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/recommendations/stored", headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Get stored recommendations", response.text)
        return None
    test_results.pass_test("Get stored recommendations")
    return response.json()

def apply_for_job(token, job_id, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    application_data = {
        "job_id": job_id,
        "cover_letter": "I am very interested in this position and believe my skills match your requirements.",
        "resume_url": "https://example.com/resume.pdf"
    }
    response = requests.post(f"{API_URL}/applications", json=application_data, headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Apply for job", response.text)
        return None
    test_results.pass_test("Apply for job")
    return response.json()

def save_job(token, job_id, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    saved_job_data = {
        "job_id": job_id,
        "notes": "This job looks interesting, will apply later"
    }
    response = requests.post(f"{API_URL}/saved-jobs", json=saved_job_data, headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Save job", response.text)
        return None
    test_results.pass_test("Save job")
    return response.json()

def mark_recommendation_as_viewed(token, recommendation_id, test_results):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{API_URL}/recommendations/{recommendation_id}/viewed", headers=headers)
    if response.status_code != 200:
        test_results.fail_test("Mark recommendation as viewed", response.text)
        return None
    test_results.pass_test("Mark recommendation as viewed")
    return response.json()

def run_end_to_end_tests():
    print("\n===== STARTING END-TO-END TESTS =====\n")
    start_time = time.time()
    test_results = TestResult()
    
    # Step 1: Register users
    print("\n----- STEP 1: REGISTERING TEST USERS -----")
    employer = register_employer(test_results)
    if not employer:
        print("Failed to register employer, aborting tests")
        return False
    
    candidate1 = register_candidate(test_candidate1, test_results, "Register candidate 1")
    if not candidate1:
        print("Failed to register candidate 1, aborting tests")
        return False
    
    candidate2 = register_candidate(test_candidate2, test_results, "Register candidate 2")
    if not candidate2:
        print("Failed to register candidate 2, aborting tests")
        return False
    
    # Step 2: Login with all users
    print("\n----- STEP 2: LOGIN TESTS -----")
    employer_token = login_user(EMPLOYER_EMAIL, EMPLOYER_PASSWORD, test_results, "Employer login")
    if not employer_token:
        print("Failed to login as employer, aborting tests")
        return False
    
    candidate1_token = login_user(CANDIDATE1_EMAIL, CANDIDATE_PASSWORD, test_results, "Candidate 1 login")
    if not candidate1_token:
        print("Failed to login as candidate 1, aborting tests")
        return False
    
    candidate2_token = login_user(CANDIDATE2_EMAIL, CANDIDATE_PASSWORD, test_results, "Candidate 2 login")
    if not candidate2_token:
        print("Failed to login as candidate 2, aborting tests")
        return False
    
    # Step 3: Employer creates jobs and projects
    print("\n----- STEP 3: CREATING JOBS AND PROJECTS -----")
    job1 = create_job(employer_token, test_job1, employer['id'], test_results, "Create Python job")
    if not job1:
        print("Failed to create job 1, aborting tests")
        return False
    
    job2 = create_job(employer_token, test_job2, employer['id'], test_results, "Create Mobile job")
    if not job2:
        print("Failed to create job 2, aborting tests")
        return False
    
    project1 = create_project(employer_token, test_project1, employer['id'], test_results, "Create AI project")
    if not project1:
        print("Failed to create project 1, aborting tests")
        return False
    
    project2 = create_project(employer_token, test_project2, employer['id'], test_results, "Create Android project")
    if not project2:
        print("Failed to create project 2, aborting tests")
        return False
    
    # Wait for embeddings to be processed
    print("\nWaiting for embeddings to be processed...")
    time.sleep(3)
    
    # Step 4: Test job recommendations for candidates
    print("\n----- STEP 4: TESTING JOB RECOMMENDATIONS -----")
    candidate1_job_recommendations = get_job_recommendations(candidate1_token, test_results)
    if candidate1_job_recommendations:
        # Verify recommendations exist
        if len(candidate1_job_recommendations) > 0:
            test_results.pass_test("Candidate 1 received job recommendations")
            # Check if the Python job has a higher score for candidate 1 (Python developer)
            python_job_rec = next((rec for rec in candidate1_job_recommendations if rec["job_id"] == job1["id"]), None)
            mobile_job_rec = next((rec for rec in candidate1_job_recommendations if rec["job_id"] == job2["id"]), None)
            if python_job_rec and mobile_job_rec and python_job_rec["match_score"] > mobile_job_rec["match_score"]:
                test_results.pass_test("Candidate 1 (Python dev) has higher match score for Python job")
            else:
                test_results.fail_test("Candidate 1 (Python dev) should have higher match score for Python job")
        else:
            test_results.fail_test("Candidate 1 received no job recommendations")
    
    candidate2_job_recommendations = get_job_recommendations(candidate2_token, test_results)
    if candidate2_job_recommendations:
        # Verify recommendations exist
        if len(candidate2_job_recommendations) > 0:
            test_results.pass_test("Candidate 2 received job recommendations")
            # Check if the Mobile job has a higher score for candidate 2 (Mobile developer)
            python_job_rec = next((rec for rec in candidate2_job_recommendations if rec["job_id"] == job1["id"]), None)
            mobile_job_rec = next((rec for rec in candidate2_job_recommendations if rec["job_id"] == job2["id"]), None)
            if python_job_rec and mobile_job_rec and mobile_job_rec["match_score"] > python_job_rec["match_score"]:
                test_results.pass_test("Candidate 2 (Mobile dev) has higher match score for Mobile job")
            else:
                test_results.fail_test("Candidate 2 (Mobile dev) should have higher match score for Mobile job")
        else:
            test_results.fail_test("Candidate 2 received no job recommendations")
    
    # Step 5: Test project recommendations for candidates
    print("\n----- STEP 5: TESTING PROJECT RECOMMENDATIONS -----")
    candidate1_project_recommendations = get_project_recommendations(candidate1_token, test_results)
    if candidate1_project_recommendations:
        # Verify recommendations exist
        if len(candidate1_project_recommendations) > 0:
            test_results.pass_test("Candidate 1 received project recommendations")
            # Check if the AI project has a higher score for candidate 1 (Python developer)
            ai_project_rec = next((rec for rec in candidate1_project_recommendations if rec["project_id"] == project1["id"]), None)
            android_project_rec = next((rec for rec in candidate1_project_recommendations if rec["project_id"] == project2["id"]), None)
            if ai_project_rec and android_project_rec and ai_project_rec["match_score"] > android_project_rec["match_score"]:
                test_results.pass_test("Candidate 1 (Python dev) has higher match score for AI project")
            else:
                test_results.fail_test("Candidate 1 (Python dev) should have higher match score for AI project")
        else:
            test_results.fail_test("Candidate 1 received no project recommendations")
    
    candidate2_project_recommendations = get_project_recommendations(candidate2_token, test_results)
    if candidate2_project_recommendations:
        # Verify recommendations exist
        if len(candidate2_project_recommendations) > 0:
            test_results.pass_test("Candidate 2 received project recommendations")
            # Check if the Android project has a higher score for candidate 2 (Mobile developer)
            ai_project_rec = next((rec for rec in candidate2_project_recommendations if rec["project_id"] == project1["id"]), None)
            android_project_rec = next((rec for rec in candidate2_project_recommendations if rec["project_id"] == project2["id"]), None)
            if ai_project_rec and android_project_rec and android_project_rec["match_score"] > ai_project_rec["match_score"]:
                test_results.pass_test("Candidate 2 (Mobile dev) has higher match score for Android project")
            else:
                test_results.fail_test("Candidate 2 (Mobile dev) should have higher match score for Android project")
        else:
            test_results.fail_test("Candidate 2 received no project recommendations")
    
    # Step 6: Test candidate recommendations for employer
    print("\n----- STEP 6: TESTING CANDIDATE RECOMMENDATIONS -----")
    python_job_candidates = get_candidate_recommendations(employer_token, job1["id"], test_results)
    if python_job_candidates:
        # Verify recommendations exist
        if len(python_job_candidates) > 0:
            test_results.pass_test("Employer received candidate recommendations for Python job")
            # Check if candidate 1 (Python developer) has higher score for Python job
            candidate1_rec = next((rec for rec in python_job_candidates if rec["candidate_id"] == candidate1["id"]), None)
            candidate2_rec = next((rec for rec in python_job_candidates if rec["candidate_id"] == candidate2["id"]), None)
            if candidate1_rec and candidate2_rec and candidate1_rec["match_score"] > candidate2_rec["match_score"]:
                test_results.pass_test("Candidate 1 (Python dev) has higher match score for Python job in employer view")
            else:
                test_results.fail_test("Candidate 1 (Python dev) should have higher match score for Python job in employer view")
        else:
            test_results.fail_test("Employer received no candidate recommendations for Python job")
    
    mobile_job_candidates = get_candidate_recommendations(employer_token, job2["id"], test_results)
    if mobile_job_candidates:
        # Verify recommendations exist
        if len(mobile_job_candidates) > 0:
            test_results.pass_test("Employer received candidate recommendations for Mobile job")
            # Check if candidate 2 (Mobile developer) has higher score for Mobile job
            candidate1_rec = next((rec for rec in mobile_job_candidates if rec["candidate_id"] == candidate1["id"]), None)
            candidate2_rec = next((rec for rec in mobile_job_candidates if rec["candidate_id"] == candidate2["id"]), None)
            if candidate1_rec and candidate2_rec and candidate2_rec["match_score"] > candidate1_rec["match_score"]:
                test_results.pass_test("Candidate 2 (Mobile dev) has higher match score for Mobile job in employer view")
            else:
                test_results.fail_test("Candidate 2 (Mobile dev) should have higher match score for Mobile job in employer view")
        else:
            test_results.fail_test("Employer received no candidate recommendations for Mobile job")
    
    # Step 7: Test project candidate recommendations for employer
    print("\n----- STEP 7: TESTING PROJECT CANDIDATE RECOMMENDATIONS -----")
    ai_project_candidates = get_candidates_for_project(employer_token, project1["id"], test_results)
    if ai_project_candidates:
        # Verify recommendations exist
        if len(ai_project_candidates) > 0:
            test_results.pass_test("Employer received candidate recommendations for AI project")
            # Check if candidate 1 (Python developer) has higher score for AI project
            candidate1_rec = next((rec for rec in ai_project_candidates if rec["candidate_id"] == candidate1["id"]), None)
            candidate2_rec = next((rec for rec in ai_project_candidates if rec["candidate_id"] == candidate2["id"]), None)
            if candidate1_rec and candidate2_rec and candidate1_rec["match_score"] > candidate2_rec["match_score"]:
                test_results.pass_test("Candidate 1 (Python dev) has higher match score for AI project in employer view")
            else:
                test_results.fail_test("Candidate 1 (Python dev) should have higher match score for AI project in employer view")
        else:
            test_results.fail_test("Employer received no candidate recommendations for AI project")
    
    android_project_candidates = get_candidates_for_project(employer_token, project2["id"], test_results)
    if android_project_candidates:
        # Verify recommendations exist
        if len(android_project_candidates) > 0:
            test_results.pass_test("Employer received candidate recommendations for Android project")
            # Check if candidate 2 (Mobile developer) has higher score for Android project
            candidate1_rec = next((rec for rec in android_project_candidates if rec["candidate_id"] == candidate1["id"]), None)
            candidate2_rec = next((rec for rec in android_project_candidates if rec["candidate_id"] == candidate2["id"]), None)
            if candidate1_rec and candidate2_rec and candidate2_rec["match_score"] > candidate1_rec["match_score"]:
                test_results.pass_test("Candidate 2 (Mobile dev) has higher match score for Android project in employer view")
            else:
                test_results.fail_test("Candidate 2 (Mobile dev) should have higher match score for Android project in employer view")
        else:
            test_results.fail_test("Employer received no candidate recommendations for Android project")
    
    # Step 8: Test semantic search
    print("\n----- STEP 8: TESTING SEMANTIC SEARCH -----")
    # Candidate searching for jobs
    python_search_results = search_jobs(candidate1_token, "Python backend developer with AWS experience", test_results)
    if python_search_results:
        if len(python_search_results) > 0:
            test_results.pass_test("Candidate 1 found jobs through semantic search")
            # Check if Python job is returned in search results
            if any(job["id"] == job1["id"] for job in python_search_results):
                test_results.pass_test("Python job found in semantic search results")
            else:
                test_results.fail_test("Python job not found in semantic search results")
        else:
            test_results.fail_test("No jobs found in semantic search")
    
    # Candidate searching for projects
    ai_search_results = search_projects(candidate1_token, "AI machine learning project", test_results)
    if ai_search_results:
        if len(ai_search_results) > 0:
            test_results.pass_test("Candidate 1 found projects through semantic search")
            # Check if AI project is returned in search results
            if any(project["id"] == project1["id"] for project in ai_search_results):
                test_results.pass_test("AI project found in semantic search results")
            else:
                test_results.fail_test("AI project not found in semantic search results")
        else:
            test_results.fail_test("No projects found in semantic search")
    
    # Employer searching for candidates
    python_candidate_search = search_candidates(employer_token, "Python machine learning developer", test_results)
    if python_candidate_search:
        if len(python_candidate_search) > 0:
            test_results.pass_test("Employer found candidates through semantic search")
            # Check if Python developer is returned in search results
            if any(candidate["id"] == candidate1["id"] for candidate in python_candidate_search):
                test_results.pass_test("Python developer found in semantic search results")
            else:
                test_results.fail_test("Python developer not found in semantic search results")
        else:
            test_results.fail_test("No candidates found in semantic search")
    
    # Step 9: Test job application functionality
    print("\n----- STEP 9: TESTING JOB APPLICATION -----")
    # Candidate 1 applies for Python job
    application = apply_for_job(candidate1_token, job1["id"], test_results)
    
    # Candidate 2 saves Mobile job for later
    saved_job = save_job(candidate2_token, job2["id"], test_results)
    
    # Step 10: Test stored recommendations
    print("\n----- STEP 10: TESTING STORED RECOMMENDATIONS -----")
    candidate1_stored_recs = get_stored_recommendations(candidate1_token, test_results)
    if candidate1_stored_recs is not None:
        if len(candidate1_stored_recs) > 0:
            test_results.pass_test("Candidate has stored recommendations")
            
            # Try to mark one recommendation as viewed if available
            if len(candidate1_stored_recs) > 0 and 'id' in candidate1_stored_recs[0]:
                mark_recommendation_as_viewed(candidate1_token, candidate1_stored_recs[0]['id'], test_results)
        else:
            # Note: Not failing the test here as there might be no recommendations with score >= 70
            print("Note: No stored recommendations found for candidate 1")
    
    employer_stored_recs = get_stored_recommendations(employer_token, test_results)
    if employer_stored_recs is not None:
        if len(employer_stored_recs) > 0:
            test_results.pass_test("Employer has stored recommendations")
            
            # Try to mark one recommendation as viewed if available
            if len(employer_stored_recs) > 0 and 'id' in employer_stored_recs[0]:
                mark_recommendation_as_viewed(employer_token, employer_stored_recs[0]['id'], test_results)
        else:
            # Note: Not failing the test here as there might be no recommendations with score >= 70
            print("Note: No stored recommendations found for employer")
    
    # Calculate test duration
    end_time = time.time()
    duration = end_time - start_time
    
    # Print test summary
    print(f"\n===== END-TO-END TESTS COMPLETED IN {duration:.2f} SECONDS =====")
    success = test_results.summary()
    
    return success

if __name__ == "__main__":
    try:
        success = run_end_to_end_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"\nUnexpected error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(3) 