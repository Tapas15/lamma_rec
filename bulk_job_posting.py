import requests
import json
import time
import random
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000"
EMAIL = "test@employer.com"
PASSWORD = "testpassword123"

def register_employer():
    """Register a new employer account"""
    url = f"{BASE_URL}/register/employer"
    
    employer_data = {
        "email": EMAIL,
        "password": PASSWORD,
        "full_name": "Bulk Posting Company",
        "user_type": "employer",
        "company_name": "Bulk Posting Corp",
        "company_description": "A company that posts jobs in bulk for testing",
        "company_website": "https://bulkpostingcorp.com",
        "company_location": "San Francisco, CA",
        "company_size": "500-1000",
        "industry": "Technology",
        "contact_email": "hr@bulkpostingcorp.com",
        "contact_phone": "+1-555-0123",
        "location": "San Francisco",
        "bio": "HR Department at Bulk Posting Corp - Testing job recommendations"
    }
    
    try:
        response = requests.post(url, json=employer_data)
        
        if response.status_code == 200:
            print("Employer registered successfully!")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print("Employer already exists. Proceeding to login.")
            return True
        else:
            print(f"Error registering employer: {response.status_code}")
            print("Response:", response.text)
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def login():
    """Login and get access token"""
    login_data = {
        "username": EMAIL,  # FastAPI OAuth2 uses 'username' instead of 'email'
        "password": PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token", data=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            print("Login successful")
            return token_data["access_token"]
        else:
            print(f"Login failed: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return None

def create_job(token, job_data):
    """Create a new job posting"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/jobs", headers=headers, json=job_data)
        
        if response.status_code == 200:
            job = response.json()
            print(f"Created job: {job.get('title')} (ID: {job.get('id')})")
            return job
        else:
            print(f"Error creating job: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Error during job creation: {str(e)}")
        return None

# Job templates
job_titles = [
    "Software Engineer", "Senior Software Engineer", "Principal Software Engineer", 
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Data Scientist", "Machine Learning Engineer", "AI Research Scientist",
    "DevOps Engineer", "SRE", "Cloud Engineer",
    "Product Manager", "Project Manager", "Program Manager",
    "UX Designer", "UI Designer", "Product Designer",
    "QA Engineer", "Test Engineer", "QA Automation Engineer",
    "Database Administrator", "Data Engineer", "Business Intelligence Analyst",
    "Mobile Developer", "iOS Developer", "Android Developer",
    "Security Engineer", "Penetration Tester", "Security Analyst",
    "Technical Writer", "Content Strategist", "Documentation Specialist",
    "Network Engineer", "Systems Administrator", "IT Support Specialist",
    "Blockchain Developer", "Smart Contract Engineer", "Crypto Specialist",
    "Game Developer", "3D Modeler", "Game Designer",
    "AR/VR Developer", "Computer Vision Engineer", "Graphics Programmer",
    "Marketing Specialist", "Digital Marketer", "SEO Expert",
    "Sales Representative", "Account Executive", "Business Development Manager"
]

technologies = [
    "Python", "JavaScript", "TypeScript", "Java", "C#", "Go", "Rust", "Ruby", "PHP",
    "React", "Angular", "Vue.js", "Next.js", "Node.js", "Django", "Flask", "Spring Boot",
    "AWS", "Azure", "Google Cloud", "Kubernetes", "Docker", "Terraform", "Ansible",
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "SciPy",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
    "GraphQL", "REST API", "gRPC", "WebSockets", "Kafka", "RabbitMQ",
    "Git", "GitHub", "GitLab", "CI/CD", "Jenkins", "GitHub Actions",
    "React Native", "Flutter", "Kotlin", "Swift", "Objective-C",
    "Unity", "Unreal Engine", "WebGL", "Three.js", "A-Frame"
]

locations = [
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA",
    "Chicago, IL", "Los Angeles, CA", "Denver, CO", "Atlanta, GA", "Portland, OR",
    "Remote", "Hybrid - San Francisco", "Hybrid - New York", "Hybrid - Seattle"
]

experience_levels = ["Entry-Level", "Mid-Level", "Senior", "Lead", "Principal", "Director"]
employment_types = ["Full-time", "Part-time", "Contract", "Temporary", "Internship"]

def generate_salary_range(level):
    """Generate a realistic salary range based on experience level"""
    if level == "Entry-Level":
        base = random.randint(60000, 80000)
        ceiling = base + random.randint(15000, 25000)
    elif level == "Mid-Level":
        base = random.randint(85000, 110000)
        ceiling = base + random.randint(20000, 40000)
    elif level == "Senior":
        base = random.randint(120000, 150000)
        ceiling = base + random.randint(30000, 50000)
    elif level == "Lead":
        base = random.randint(140000, 180000)
        ceiling = base + random.randint(40000, 60000)
    elif level == "Principal":
        base = random.randint(160000, 200000)
        ceiling = base + random.randint(50000, 80000)
    else:  # Director
        base = random.randint(180000, 220000)
        ceiling = base + random.randint(60000, 100000)
    
    return f"${base:,} - ${ceiling:,}"

def generate_job_description(title, tech_stack, level):
    """Generate a realistic job description"""
    company_types = ["startup", "tech giant", "industry leader", "innovative company", "growing company"]
    company_type = random.choice(company_types)
    
    intro_phrases = [
        f"We're seeking a {level} {title} to join our team.",
        f"Join our team as a {level} {title} and help us build amazing products.",
        f"Our {company_type} is looking for a talented {title} to help us scale.",
        f"Exciting opportunity for a {level} {title} to make an impact.",
        f"We need a {title} to help us innovate and grow."
    ]
    
    responsibility_phrases = [
        f"Design and implement new features using {', '.join(tech_stack[:2])}, and other technologies.",
        f"Work with cross-functional teams to deliver high-quality software solutions.",
        f"Debug and fix complex issues in our existing codebase.",
        f"Participate in code reviews and mentor other engineers.",
        f"Collaborate with product managers to define requirements and specifications.",
        f"Optimize application performance and scalability.",
        f"Write clean, maintainable, and well-tested code."
    ]
    
    qualification_phrases = [
        f"Experience with {', '.join(tech_stack)}.",
        "Strong problem-solving skills and attention to detail.",
        "Ability to work both independently and as part of a team.",
        "Excellent communication skills, both written and verbal.",
        "Bachelor's degree in Computer Science or related field, or equivalent experience."
    ]
    
    intro = random.choice(intro_phrases)
    responsibilities = "Responsibilities include: " + " ".join(random.sample(responsibility_phrases, 3))
    qualifications = "Qualifications: " + " ".join(random.sample(qualification_phrases, 3))
    
    return f"{intro} {responsibilities} {qualifications}"

def generate_job_data():
    """Generate random job data"""
    level = random.choice(experience_levels)
    title = random.choice(job_titles)
    if level != "Entry-Level":
        full_title = f"{level} {title}"
    else:
        full_title = title
        
    tech_stack = random.sample(technologies, random.randint(3, 7))
    location = random.choice(locations)
    employment_type = random.choice(employment_types)
    
    job_data = {
        "title": full_title,
        "company": "Bulk Posting Corp",
        "description": generate_job_description(title, tech_stack, level),
        "requirements": tech_stack,
        "location": location,
        "salary_range": generate_salary_range(level),
        "employment_type": employment_type
    }
    
    return job_data

def post_bulk_jobs(token, count=50):
    """Post multiple jobs"""
    print(f"Starting to post {count} jobs...")
    
    successful_jobs = 0
    for i in range(1, count + 1):
        print(f"Posting job {i}/{count}...")
        
        job_data = generate_job_data()
        job = create_job(token, job_data)
        
        if job:
            successful_jobs += 1
        
        # Add a small delay to avoid overwhelming the API
        time.sleep(0.5)
    
    print(f"Successfully posted {successful_jobs} out of {count} jobs.")
    return successful_jobs

def main():
    """Main function to register employer and post jobs"""
    print("Starting bulk job posting process...")
    
    # Step 1: Register the employer (or confirm it exists)
    if not register_employer():
        print("Failed to register employer. Exiting.")
        return
    
    # Step 2: Login and get token
    token = login()
    if not token:
        print("Failed to login. Exiting.")
        return
    
    # Step 3: Post 50 jobs
    post_bulk_jobs(token, count=50)

if __name__ == "__main__":
    main() 