# Job Recommender System

A personalized job recommendation system that matches candidates with jobs and vice versa using semantic matching and LLM-based explanations.

## Features

- User registration and authentication (candidates and employers)
- Job posting and management
- Semantic matching between jobs and candidates
- Percentage match score with LLM-generated explanations
- RESTful API endpoints for all operations

## Prerequisites

- Python 3.8+
- MongoDB
- Llama API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd job-recommender
```

2. Create a virtual environment and activate it:
```bash
python3.10 -m venv venv 
py -3.10 -m venv myenv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key
LLAMA_API_KEY=your-llama-api-key
```

5. Start MongoDB service on your machine

6. Run the application:
```bash
uvicorn main:app --reload
uvicorn llama_recommender:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for the interactive API documentation.

### Key Endpoints

1. Authentication:
   - POST `/register` - Register a new user (candidate or employer)
   - POST `/token` - Login and get access token

2. Jobs:
   - POST `/jobs` - Create a new job posting (employers only)
   - GET `/jobs` - List all active jobs

3. Recommendations:
   - GET `/recommendations/jobs` - Get job recommendations for candidates
   - GET `/recommendations/candidates/{job_id}` - Get candidate recommendations for a job

4. Profile:
   - PUT `/profile` - Update user profile

## Testing with Postman

1. Register a new user:
```http
POST http://localhost:8000/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "yourpassword",
    "user_type": "candidate",
    "full_name": "John Doe"
}
```

2. Login to get access token:
```http
POST http://localhost:8000/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

3. Use the access token in subsequent requests:
```http
GET http://localhost:8000/jobs
Authorization: Bearer <your-access-token>
```

## Recommendation System

The system uses:
- Sentence Transformers for semantic matching
- Llama 3.2 for generating match explanations
- Cosine similarity for calculating match scores

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Role-based access control for endpoints

## Contributing

Feel free to submit issues and enhancement requests! 