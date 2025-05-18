import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from datetime import datetime
import uuid
import json
from bson import ObjectId

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net")
DB_NAME = os.getenv("DB_NAME", "job_recommendation")
JOBS_COLLECTION = "jobs"
USERS_COLLECTION = "users"
EMPLOYERS_COLLECTION = "employers"

# Ollama endpoint for embeddings
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434/api/embeddings")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
jobs_collection = db[JOBS_COLLECTION]
users_collection = db[USERS_COLLECTION]
employers_collection = db[EMPLOYERS_COLLECTION]

def get_embedding(text: str) -> list:
    """Get embedding from Ollama API"""
    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json={
                "model": OLLAMA_MODEL,
                "prompt": text
            }
        )
        
        if response.status_code != 200:
            print(f"Error from Ollama API: {response.status_code}")
            print(response.text)
            return []
            
        data = response.json()
        return data['embedding']
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []

def create_job_embedding(job_data):
    """Create a searchable text from job data and get its embedding"""
    searchable_text = f"{job_data.get('title', '')} {job_data.get('company', '')} {job_data.get('description', '')} {' '.join(job_data.get('requirements', []))} {job_data.get('location', '')}"
    return get_embedding(searchable_text)

def create_sample_jobs(employer_id=None):
    """Create sample jobs for testing"""
    
    # Check if employer_id is valid
    if employer_id:
        employer = employers_collection.find_one({"_id": ObjectId(employer_id)})
        if not employer:
            print(f"Employer with ID {employer_id} not found")
            return False
    else:
        # Look for any employer in the system
        employer = employers_collection.find_one({"user_type": "employer"})
        if employer:
            employer_id = str(employer["_id"])
            print(f"Using existing employer with ID: {employer_id}")
        else:
            # Create a sample employer if none exists
            employer_id = create_sample_employer()
            if not employer_id:
                print("Failed to create sample employer")
                return False
    
    sample_jobs = [
        {
            "title": "Python Developer",
            "company": "TechCorp",
            "description": "We're looking for a Python developer to join our team. You'll work on building and maintaining web applications using Django and Flask. The ideal candidate has experience with RESTful APIs, database design, and cloud services.",
            "requirements": ["Python", "Django", "Flask", "REST API", "SQL", "AWS"],
            "location": "New York, NY",
            "salary_range": "$80,000 - $120,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Solutions",
            "description": "Join our ML team to develop cutting-edge machine learning models for various business applications. You'll work with large datasets and implement ML algorithms to solve complex problems.",
            "requirements": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Data Analysis", "Mathematics"],
            "location": "San Francisco, CA",
            "salary_range": "$100,000 - $150,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Frontend Developer",
            "company": "WebDesign Co",
            "description": "We're seeking a talented frontend developer to create beautiful and responsive user interfaces. You'll work with designers to implement pixel-perfect web applications using modern frameworks.",
            "requirements": ["JavaScript", "React", "HTML", "CSS", "Responsive Design", "UI/UX"],
            "location": "Remote",
            "salary_range": "$70,000 - $110,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Data Scientist",
            "company": "Data Insights Inc",
            "description": "We're looking for a data scientist to analyze complex datasets and extract meaningful insights. You'll work on predictive modeling, statistical analysis, and data visualization.",
            "requirements": ["Python", "R", "Statistics", "Machine Learning", "SQL", "Data Visualization"],
            "location": "Boston, MA",
            "salary_range": "$90,000 - $130,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudTech",
            "description": "Join our DevOps team to build and maintain our cloud infrastructure. You'll work on automation, CI/CD pipelines, and ensure the reliability of our services.",
            "requirements": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Terraform"],
            "location": "Seattle, WA",
            "salary_range": "$95,000 - $140,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Full Stack Developer",
            "company": "SoftwareSolutions",
            "description": "We need a versatile full-stack developer who can work across the entire software stack. You'll develop both frontend and backend components of our web applications.",
            "requirements": ["JavaScript", "Node.js", "React", "MongoDB", "Express", "RESTful API"],
            "location": "Austin, TX",
            "salary_range": "$85,000 - $125,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Mobile App Developer",
            "company": "AppWorks",
            "description": "Join our mobile development team to create engaging mobile applications for iOS and Android platforms. You'll work with UI/UX designers to implement features and ensure a smooth user experience.",
            "requirements": ["React Native", "iOS", "Android", "JavaScript", "Mobile UI Design"],
            "location": "Chicago, IL",
            "salary_range": "$80,000 - $120,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Database Administrator",
            "company": "DataSystems",
            "description": "We're looking for a database administrator to manage our database systems. You'll be responsible for database design, optimization, security, and backup procedures.",
            "requirements": ["SQL", "MongoDB", "Database Design", "Performance Tuning", "Data Security"],
            "location": "Denver, CO",
            "salary_range": "$85,000 - $130,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "UI/UX Designer",
            "company": "DesignStudio",
            "description": "We're seeking a creative UI/UX designer to create intuitive and engaging user experiences. You'll work on wireframes, prototypes, and collaborate with developers to implement your designs.",
            "requirements": ["UI Design", "UX Research", "Figma", "Adobe XD", "Wireframing", "Prototyping"],
            "location": "Los Angeles, CA",
            "salary_range": "$75,000 - $115,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "title": "QA Engineer",
            "company": "QualityTech",
            "description": "Join our QA team to ensure the quality of our software products. You'll develop and execute test cases, identify bugs, and collaborate with developers to improve our applications.",
            "requirements": ["Test Planning", "Automated Testing", "Selenium", "JIRA", "Bug Tracking", "Quality Assurance"],
            "location": "Portland, OR",
            "salary_range": "$70,000 - $100,000",
            "employer_id": employer_id,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Add unique ID and embeddings to each job
    for job in sample_jobs:
        job["_id"] = ObjectId()
        print(f"Creating embedding for job: {job['title']}")
        job["embedding"] = create_job_embedding(job)
        
        # Insert job
        jobs_collection.insert_one(job)
        print(f"Created job: {job['title']}")
    
    print(f"Created {len(sample_jobs)} sample jobs")
    return True

def create_sample_employer():
    """Create a sample employer if none exists"""
    sample_email = "employer@example.com"
    existing_user = users_collection.find_one({"email": sample_email})
    
    if existing_user:
        print(f"Employer with email {sample_email} already exists")
        employer = employers_collection.find_one({"email": sample_email})
        return str(employer["_id"]) if employer else None
    
    # Create sample employer user
    employer_data = {
        "email": sample_email,
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password" hashed
        "user_type": "employer",
        "full_name": "Sample Employer",
        "created_at": datetime.utcnow()
    }
    
    # Insert into users collection
    user_result = users_collection.insert_one(employer_data)
    user_id = str(user_result.inserted_id)
    
    # Create employer profile
    employer_profile = {
        "_id": ObjectId(user_id),
        "email": sample_email,
        "user_type": "employer",
        "full_name": "Sample Employer",
        "company_name": "Sample Company",
        "company_description": "A sample company for testing purposes",
        "company_website": "https://example.com",
        "company_location": "New York, NY",
        "company_size": "50-100",
        "industry": "Technology",
        "contact_email": "contact@example.com",
        "contact_phone": "123-456-7890",
        "location": "New York, NY",
        "bio": "We are a technology company focused on innovation.",
        "profile_completed": True,
        "is_active": True,
        "last_active": datetime.utcnow(),
        "verified": True,
        "created_at": datetime.utcnow()
    }
    
    # Insert into employers collection
    employers_collection.insert_one(employer_profile)
    print(f"Created sample employer with ID: {user_id}")
    
    return user_id

if __name__ == "__main__":
    # Check if jobs already exist
    existing_jobs_count = jobs_collection.count_documents({})
    if existing_jobs_count > 0:
        print(f"Database already contains {existing_jobs_count} jobs.")
        user_input = input("Do you want to add more sample jobs anyway? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without adding jobs.")
            exit(0)
    
    print("Creating sample jobs...")
    success = create_sample_jobs()
    
    if success:
        print("Sample jobs created successfully!")
    else:
        print("Failed to create sample jobs.") 