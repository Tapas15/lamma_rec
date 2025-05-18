import requests
import json
from pymongo import MongoClient
import numpy as np
from tabulate import tabulate

# MongoDB connection details
MONGODB_URL = "mongodb+srv://tapu199824:1234567890@cluster0.5q7vyy1.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "job_recommender"
PROJECTS_COLLECTION = "projects"

# API endpoints
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/token"
PROJECTS_URL = f"{BASE_URL}/projects"
SEARCH_URL = f"{BASE_URL}/projects/search"

# Employer credentials
EMPLOYER_EMAIL = "test@employer.com"
EMPLOYER_PASSWORD = "testpassword123"

def print_section(title):
    """Print a section title for better readability"""
    print("\n")
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def print_json(title, data):
    """Print JSON data in a formatted way"""
    print(f"\n--- {title} ---")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str))
    else:
        print(data)

def get_auth_token():
    """Get authentication token"""
    login_data = {
        "username": EMPLOYER_EMAIL,
        "password": EMPLOYER_PASSWORD
    }
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()["access_token"]
        else:
            print(f"❌ Error logging in: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def get_profile(token):
    """Get user profile to get employer ID"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def create_project(token, employer_id):
    """Create a test project"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Create a unique project title to avoid duplicates
    import time
    project_title = f"Web Development Project (Test {int(time.time())})"
    
    project_data = {
        "title": project_title,
        "company": "Innovate Tech",
        "description": "We need a modern responsive web application built using React and Node.js with MongoDB backend. The application should include user authentication, dashboard analytics, and real-time features.",
        "requirements": [
            "Strong frontend development skills",
            "Experience with React and state management",
            "Node.js backend development",
            "MongoDB database design",
            "Responsive design"
        ],
        "project_type": "Web Development",
        "skills_required": [
            "React", 
            "Node.js", 
            "MongoDB", 
            "JavaScript", 
            "CSS", 
            "Responsive Design"
        ],
        "budget_range": "$5,000 - $10,000",
        "duration": "2 months",
        "location": "Remote",
        "employer_id": employer_id
    }
    
    try:
        response = requests.post(PROJECTS_URL, headers=headers, json=project_data)
        if response.status_code == 201:
            print(f"✅ Project '{project_title}' created successfully!")
            return response.json()
        else:
            print(f"❌ Error creating project: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def get_project_with_embedding(project_id):
    """Directly access MongoDB to get project with embedding"""
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        projects_collection = db[PROJECTS_COLLECTION]
        
        project = projects_collection.find_one({"id": project_id})
        client.close()
        return project
    except Exception as e:
        print(f"❌ Error accessing MongoDB: {str(e)}")
        return None

def analyze_embedding(embedding):
    """Analyze embedding vector properties"""
    if not embedding or not isinstance(embedding, list):
        return "Invalid embedding"
    
    embedding_array = np.array(embedding)
    return {
        "dimension": len(embedding),
        "min": float(np.min(embedding_array)),
        "max": float(np.max(embedding_array)),
        "mean": float(np.mean(embedding_array)),
        "std": float(np.std(embedding_array)),
        "norm": float(np.linalg.norm(embedding_array)),
        "first_5": embedding[:5],
        "last_5": embedding[-5:]
    }

def test_semantic_search(token, query="Web development project with React and Node.js"):
    """Test semantic search functionality"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        # The server expects the query parameter in the URL, not in the JSON body
        params = {"query": query, "top_k": 5}
        response = requests.post(
            SEARCH_URL,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            print(f"✅ Semantic search for '{query}' completed successfully!")
            return response.json()
        else:
            print(f"❌ Error with semantic search: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def run_test():
    print_section("TESTING PROJECT EMBEDDINGS")
    
    # Step 1: Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token. Cannot proceed.")
        return
    
    # Step 2: Get employer profile
    profile = get_profile(token)
    if not profile:
        print("❌ Failed to get profile. Cannot proceed.")
        return
    employer_id = profile["id"]
    print(f"✅ Employer ID: {employer_id}")
    
    # Step 3: Create a new project
    print_section("CREATING A NEW PROJECT")
    project = create_project(token, employer_id)
    if not project:
        print("❌ Failed to create project. Cannot proceed.")
        return
    
    # Print project details
    print_json("Created Project Details", project)
    
    # Step 4: Get project with embedding from MongoDB
    print_section("RETRIEVING EMBEDDINGS FROM MONGODB")
    project_with_embedding = get_project_with_embedding(project["id"])
    if not project_with_embedding:
        print("❌ Failed to retrieve project from MongoDB.")
        return
    
    # Step 5: Analyze and print embedding information
    embedding = project_with_embedding.get("embedding")
    if embedding:
        analysis = analyze_embedding(embedding)
        
        # Create a table to display embedding properties
        print("\n📊 Embedding Analysis:")
        table_data = [
            ["Dimension", analysis["dimension"]],
            ["Min value", analysis["min"]],
            ["Max value", analysis["max"]],
            ["Mean value", analysis["mean"]],
            ["Standard deviation", analysis["std"]],
            ["L2 Norm", analysis["norm"]]
        ]
        print(tabulate(table_data, headers=["Property", "Value"], tablefmt="grid"))
        
        print("\n🔢 First 5 dimensions:")
        print(analysis["first_5"])
        print("\n🔢 Last 5 dimensions:")
        print(analysis["last_5"])
        
        embedding_size_kb = len(str(embedding)) * 2 / 1024  # Approximate size
        print(f"\n💾 Embedding size: ~{embedding_size_kb:.2f} KB")
    else:
        print("❌ No embedding found in the project document.")
    
    # Step 6: Test semantic search
    print_section("TESTING SEMANTIC SEARCH")
    search_query = "Web development project with React and Node.js"
    search_results = test_semantic_search(token, search_query)
    
    if search_results:
        print(f"\n🔍 Found {len(search_results)} results for query: '{search_query}'")
        for i, result in enumerate(search_results):
            print(f"\nResult #{i+1}: {result['title']}")
            print(f"Description: {result['description'][:100]}...")

if __name__ == "__main__":
    run_test() 