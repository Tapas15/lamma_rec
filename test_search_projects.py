import requests
import json
import time

# API endpoints
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/token"
SEARCH_URL = f"{BASE_URL}/projects/search"

# Test credentials
EMAIL = "test@employer.com"
PASSWORD = "testpassword123"

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
        "username": EMAIL,
        "password": PASSWORD
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

def test_search(token, queries):
    """Test semantic search functionality with multiple queries"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for i, query in enumerate(queries, 1):
        print_section(f"SEARCH TEST #{i}: '{query}'")
        
        # Prepare request
        params = {
            "query": query,
            "top_k": 10  # Retrieve up to 10 results
        }
        
        try:
            # Make the search request
            response = requests.post(SEARCH_URL, headers=headers, params=params)
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ Search successful! Found {len(results)} projects")
                
                # Display results
                if results:
                    for j, result in enumerate(results, 1):
                        print(f"\nResult #{j}:")
                        print(f"  Title: {result.get('title', 'N/A')}")
                        print(f"  Type: {result.get('project_type', 'N/A')}")
                        
                        # Show first 100 chars of description
                        description = result.get('description', '')
                        if description:
                            if len(description) > 100:
                                description = description[:100] + "..."
                            print(f"  Description: {description}")
                        
                        # Show skills if available
                        skills = result.get('skills_required', [])
                        if skills:
                            print(f"  Skills: {', '.join(skills[:5])}" + (" + more" if len(skills) > 5 else ""))
                else:
                    print("No matching projects found")
            else:
                print(f"❌ Search failed with status code: {response.status_code}")
                print("Response:", response.text)
        
        except Exception as e:
            print(f"❌ Error during search: {str(e)}")
        
        print("\n" + "-" * 80)
        
        # Add a small delay between requests to avoid rate limiting
        time.sleep(1)

def run_test():
    # Step 1: Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Failed to get auth token. Cannot proceed.")
        return
    
    # Step 2: Define search queries to test
    test_queries = [
        "Web development project with React and Node.js",
        "Mobile app development for iOS and Android",
        "Data science project with machine learning",
        "Front-end development with responsive design",
        "API integration project"
    ]
    
    # Step 3: Run search tests
    test_search(token, test_queries)

if __name__ == "__main__":
    run_test() 