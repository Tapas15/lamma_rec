# Lamma Rec - Job Portal API with AI-Powered Recommendation System

A FastAPI-based job portal API that connects employers and candidates, featuring advanced recommendation systems, project management, semantic search, and more.

## Features

### Employer Features
- Register and manage employer profiles
- Post and manage job listings
- Post and manage project opportunities
- View and manage job applications
- Update company information
- Access AI-powered candidate recommendations for jobs and projects
- View high-scoring candidate matches (70+ scores)
- Semantic search for candidates with specific skills and experience
- Delete job and project postings
- View posted jobs statistics

### Candidate Features
- Register and manage candidate profiles
- Browse available jobs and projects
- Apply for jobs
- Update skills and experience
- View personalized job and project recommendations
- Access stored high-quality recommendations (scores 70+)
- Semantic search for jobs and projects
- Track application status
- Save interesting job postings

### AI-Powered Recommendation System
- Semantic matching using Llama 3 embeddings
- Cosine similarity scoring between job/project and candidate profiles
- Match score threshold (70+) for high-quality recommendations
- Detailed match explanations including matching and missing skills
- Automatic storage of high-quality recommendations for future access
- Recommendation viewing tracking

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MongoDB with vector search capabilities
- **Authentication**: JWT (JSON Web Tokens)
- **AI Model**: Llama 3.2 for embeddings and semantic search
- **Password Hashing**: Bcrypt
- **API Testing**: Requests

## Prerequisites

- Python 3.8+
- MongoDB
- Ollama with llama3.2 model
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Lamma_rec
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and run Ollama with the llama3.2 model:
```bash
# Follow instructions at https://ollama.ai/ to install Ollama
ollama pull llama3.2:latest
```

5. Create a `.env` file in the root directory with the following variables:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=lamma_rec
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start MongoDB service
2. Ensure Ollama is running and the llama3.2 model is available
3. Run the FastAPI application:
```bash
uvicorn main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: `http://localhost:8001/docs`
- Alternative API documentation: `http://localhost:8001/redoc`

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /register/employer` - Register new employer
- `POST /register/candidate` - Register new candidate
- `POST /logout/candidate` - Logout candidate
- `POST /logout/employer` - Logout employer

### Profile Management
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `DELETE /profile` - Delete user account

### Job Management
- `POST /jobs` - Create new job posting
- `GET /jobs` - List all active jobs
- `PATCH /jobs/{job_id}` - Update a job posting
- `DELETE /jobs/{job_id}` - Delete a job posting

### Project Management
- `POST /projects` - Create new project
- `GET /projects` - List all projects (with optional status filtering)
- `GET /employer-projects` - Get projects posted by current employer
- `GET /projects/{project_id}` - Get specific project details
- `PATCH /projects/{project_id}` - Update project details/status
- `DELETE /projects/{project_id}` - Delete a project

### Recommendation System
- `GET /recommendations/jobs` - Get job recommendations for candidate
- `GET /recommendations/projects` - Get project recommendations for candidate
- `GET /recommendations/candidates/{job_id}` - Get candidate recommendations for a job
- `GET /recommendations/candidates-for-project/{project_id}` - Get candidate recommendations for a project
- `GET /recommendations/stored` - Get stored high-quality recommendations (70+ score)
- `PATCH /recommendations/{recommendation_id}/viewed` - Mark recommendation as viewed

### Semantic Search
- `POST /jobs/search` - Search for jobs using semantic search
- `POST /projects/search` - Search for projects using semantic search
- `POST /candidates/search` - Search for candidates using semantic search

### Job Applications
- `POST /applications` - Apply for a job
- `GET /applications` - Get user's job applications
- `DELETE /applications/{application_id}` - Withdraw application
- `PATCH /applications/{application_id}` - Update application details

### Saved Jobs
- `POST /saved-jobs` - Save a job for later
- `GET /saved-jobs` - Get user's saved jobs
- `DELETE /saved-jobs/{saved_job_id}` - Remove a saved job
- `PATCH /saved-jobs/{saved_job_id}` - Update saved job notes

## Project Structure

```
Lamma_rec/
├── main.py              # Main application file
├── models.py            # Pydantic models for data validation
├── database.py          # Database connection and collection management
├── requirements.txt     # Project dependencies
├── test_recommendations.py # Test recommendation features
├── test_recommendation_threshold.py # Test threshold functionality
├── .env                # Environment variables
└── README.md           # Project documentation
```

## Recommendation Engine

The system uses Llama 3.2 embeddings to create vector representations of:
- Job listings (title, description, requirements)
- Project listings (title, description, requirements, skills)
- Candidate profiles (skills, experience, education)

These embeddings enable:
1. Accurate matching between candidates and opportunities
2. Sophisticated relevance scoring (0-100)
3. Semantic search capabilities
4. Explanation of matches including matching and missing skills

The system automatically identifies and stores high-quality matches (score >= 70) for both employers and candidates to easily access.

## Testing

The project includes two test scripts:
- `test_recommendations.py`: Tests general recommendation functionality
- `test_recommendation_threshold.py`: Tests the threshold (70+) functionality for recommendation storage

Run tests with:
```bash
python test_recommendations.py
python test_recommendation_threshold.py
```

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Token blacklisting for logout
- Role-based access control
- Input validation with Pydantic

## Error Handling

The API implements comprehensive error handling for:
- Authentication failures
- Invalid input data
- Database operations
- Resource not found
- Unauthorized access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 