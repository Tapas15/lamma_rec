# Lamma Rec - Job Portal API

A FastAPI-based job portal API that connects employers and candidates, featuring job posting, application management, and profile management.

## Features

### Employer Features
- Register and manage employer profiles
- Post and manage job listings
- View and manage job applications
- Update company information
- Delete job postings
- View posted jobs statistics

### Candidate Features
- Register and manage candidate profiles
- Browse available jobs
- Apply for jobs
- Update skills and experience
- View job recommendations
- Track application status

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt
- **API Testing**: Requests

## Prerequisites

- Python 3.8+
- MongoDB
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

4. Create a `.env` file in the root directory with the following variables:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=lamma_rec
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start MongoDB service
2. Run the FastAPI application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /register/employer` - Register new employer
- `POST /register/candidate` - Register new candidate

### Profile Management
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `DELETE /profile` - Delete user account

### Job Management
- `POST /jobs` - Create new job posting
- `GET /jobs` - List all active jobs
- `DELETE /jobs/{job_id}` - Delete a job posting

### Employer Specific
- `GET /employer/profile` - Get employer profile with posted jobs
- `GET /employer/applications` - Get job applications

### Candidate Specific
- `GET /candidate/profile` - Get candidate profile
- `GET /recommendations/jobs` - Get job recommendations

## Project Structure

```
Lamma_rec/
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
├── .env                # Environment variables
└── README.md           # Project documentation
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