from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional, Union
import os
from dotenv import load_dotenv
from bson import ObjectId

from models import *
from database import Database, USERS_COLLECTION, JOBS_COLLECTION, RECOMMENDATIONS_COLLECTION, CANDIDATES_COLLECTION, EMPLOYERS_COLLECTION, PROJECTS_COLLECTION, JOB_APPLICATIONS_COLLECTION, SAVED_JOBS_COLLECTION, init_db
from lamma.llama_recommender import LlamaRecommender

load_dotenv()

app = FastAPI(title="Job Recommender System")
recommender = LlamaRecommender()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Add this after the token-related imports
BLACKLISTED_TOKENS = set()

# Database connection
@app.on_event("startup")
async def startup_db_client():
    await Database.connect_db()
    await init_db()
    print("Database initialized and ready for use")

@app.on_event("shutdown")
async def shutdown_db_client():
    await Database.close_db()

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Update the get_current_user function to check for blacklisted tokens
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Check if token is blacklisted
        if token in BLACKLISTED_TOKENS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been invalidated",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = await Database.get_collection(USERS_COLLECTION).find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user

from typing import Union
from fastapi import HTTPException, APIRouter
from datetime import datetime
from bson import ObjectId
from passlib.context import CryptContext

@app.post("/register/candidate", response_model=Candidate)
async def register_candidate(user: CandidateCreate):
    try:
        # Check if user already exists
        existing_user = await Database.get_collection(USERS_COLLECTION).find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
        # Generate MongoDB ObjectId
        object_id = ObjectId()
        str_id = str(object_id)
        current_time = datetime.utcnow()
    
        # Create user document
        user_dict = {
        "_id": object_id,
        "id": str_id,
        "email": user.email,
        "password": pwd_context.hash(user.password),
        "full_name": user.full_name,
        "user_type": "candidate",
        "created_at": current_time
        }
    
        # Insert into users collection
        await Database.get_collection(USERS_COLLECTION).insert_one(user_dict)
    
        # Create candidate profile with comprehensive fields
        candidate_dict = {
        "_id": object_id,
        "id": str_id,
        "email": user.email,
        "user_type": "candidate",
        "full_name": user.full_name,
        "created_at": current_time,
        "skills": user.skills or [],
        "experience": user.experience or "No experience provided",
        "education": user.education or "No education details provided",
        "location": user.location or "Location not specified",
        "bio": user.bio or "No bio provided",
        # Add additional candidate-specific fields
        "profile_completed": True,
        "is_active": True,
        "last_active": current_time,
        "resume_url": None,
        "profile_visibility": "public",
        "job_preferences": {
        "job_types": [],
        "preferred_locations": [],
        "salary_expectation": None,
        "remote_work": True
        },
        "profile_views": 0,
        "job_applications": [],
        "saved_jobs": [],
        "match_score_threshold": 70  # minimum match score for job recommendations
        }
        
        # Insert into candidates collection
        await Database.get_collection(CANDIDATES_COLLECTION).insert_one(candidate_dict)
    
        # Remove sensitive fields for response
        candidate_dict.pop("_id", None)
        
        return candidate_dict
    
    except Exception as e:
        print(f"Error in register_candidate: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to register candidate")

@app.get("/candidate/{candidate_id}", response_model=Candidate)
async def get_candidate_profile(candidate_id: str):
    try:
        # Get candidate profile from candidates collection using id
        candidate = await Database.get_collection(CANDIDATES_COLLECTION).find_one({"id": candidate_id})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate profile not found")
        
        # Remove MongoDB's _id
        candidate.pop("_id", None)
        
        return candidate
        
    except Exception as e:
        print(f"Error in get_candidate_profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/register/employer", response_model=Employer)
async def register_employer(user: EmployerCreate):
    try:
        # Check if user already exists
        existing_user = await Database.get_collection(USERS_COLLECTION).find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
        # Generate MongoDB ObjectId
        object_id = ObjectId()
        str_id = str(object_id)
        current_time = datetime.utcnow()
    
        # Create user document
        user_dict = {
        "_id": object_id,
        "id": str_id,
        "email": user.email,
        "password": pwd_context.hash(user.password),
        "full_name": user.full_name,
        "user_type": "employer",
        "created_at": current_time
        }
    
        # Insert into users collection
        await Database.get_collection(USERS_COLLECTION).insert_one(user_dict)
    
        # Create employer profile with all fields
        employer_dict = {
        "_id": object_id,
        "id": str_id,
        "email": user.email,
        "user_type": "employer",
        "full_name": user.full_name,
        "company_name": user.company_name,
        "company_description": user.company_description or "Company description not provided",
        "company_website": user.company_website or "Website not provided",
        "company_location": user.company_location or "Location not specified",
        "company_size": user.company_size or "Company size not specified",
        "industry": user.industry or "Industry not specified",
        "contact_email": user.contact_email or user.email,
        "contact_phone": user.contact_phone or "Phone not provided",
        "location": user.location or user.company_location or "Location not specified",
        "bio": user.bio or "Bio not provided",
        "created_at": current_time,
        # Add additional employer-specific fields with default values
        "profile_completed": True,
        "is_active": True,
        "last_active": current_time,
        "verified": False,  # Default to False, can be verified later
        "total_jobs_posted": 0,
        "total_active_jobs": 0,
        "account_type": "standard",  # Can be used for different subscription levels
        "profile_views": 0,
        "rating": None,  # Can be used for employer ratings
        "social_links": {
        "linkedin": user.linkedin or "",
        "twitter": user.twitter or "",
        "website": user.company_website or ""
        },
        "posted_jobs": []
        }
    
        # Insert into employers collection
        await Database.get_collection(EMPLOYERS_COLLECTION).insert_one(employer_dict)
    
        # Remove sensitive fields for response
        # Password is not in employer_dict, it's in user_dict which is not directly returned.
        # _id is specific to MongoDB and usually not exposed directly if 'id' (string version) is used.
        clean_employer_dict = employer_dict.copy()
        clean_employer_dict.pop("_id", None) 
        
        return clean_employer_dict
    
    except Exception as e:
        print(f"Error in register_employer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to register employer")

@app.get("/employer/{employer_id}", response_model=Employer)
async def get_employer_profile(employer_id: str):
    try:
        employer = await Database.get_collection(EMPLOYERS_COLLECTION).find_one({"id": employer_id})
        if not employer:
            raise HTTPException(status_code=404, detail="Employer profile not found")
        
        # Get jobs posted by this employer
        raw_jobs_from_db = await Database.get_collection(JOBS_COLLECTION).find(
            {"employer_id": employer_id, "is_active": True}
        ).to_list(length=None)
        
        # Process jobs to remove _id and ensure they are suitable for the response model
        processed_jobs_list = []
        for job_doc in raw_jobs_from_db:
            job_doc.pop("_id", None)  # Remove MongoDB's _id from each job document
            # Potentially, here you could also validate/convert job_doc fields if needed,
            # e.g., ensuring datetime objects are handled as expected by Pydantic if not using a Job model for them.
            processed_jobs_list.append(job_doc)
            
        employer["posted_jobs"] = processed_jobs_list

        # Remove MongoDB's _id from the main employer document before returning
        employer.pop("_id", None)
        
        return employer
        
    except Exception as e:
        # Log the actual exception for debugging on the server
        import traceback
        print(f"Error in get_employer_profile for employer_id {employer_id}: {{str(e)}}\n{{traceback.format_exc()}}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await Database.get_collection(USERS_COLLECTION).find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Job endpoints
@app.post("/jobs", response_model=Job)
async def create_job(job: JobCreate, current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(status_code=403, detail="Only employers can post jobs")
    
    job_dict = job.dict()
    job_dict["id"] = str(ObjectId())
    job_dict["is_active"] = True
    await Database.get_collection(JOBS_COLLECTION).insert_one(job_dict)
    return job_dict

@app.get("/jobs", response_model=List[Job])
async def get_jobs(current_user: dict = Depends(get_current_user)):
    jobs = await Database.get_collection(JOBS_COLLECTION).find({"is_active": True}).to_list(length=None)
    return jobs

@app.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    # Verify user is an employer
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(
            status_code=403,
            detail="Only employers can delete jobs"
        )
    
    # Get the job
    job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": job_id})
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    # Verify the job belongs to this employer
    if str(job["employer_id"]) != str(current_user["id"]):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own jobs"
        )
    
    # Delete the job
    result = await Database.get_collection(JOBS_COLLECTION).delete_one({"id": job_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete job"
        )
    
    return {"message": "Job deleted successfully"}

@app.patch("/jobs/{job_id}", response_model=Job)
async def update_job(
    job_id: str,
    update_data: dict,
    current_user: dict = Depends(get_current_user)
):
    # Verify user is an employer
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(
            status_code=403,
            detail="Only employers can update jobs"
        )
    
    # Get the job
    job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": job_id})
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    # Verify the job belongs to this employer
    if str(job["employer_id"]) != str(current_user["id"]):
        raise HTTPException(
            status_code=403,
            detail="You can only update your own jobs"
        )
    
    # Update the job
    result = await Database.get_collection(JOBS_COLLECTION).update_one(
        {"id": job_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to update job or no changes made"
        )
    
    # Return updated job
    updated_job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": job_id})
    if not updated_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found after update"
        )
    
    # Remove MongoDB's _id
    updated_job.pop("_id", None)
    
    return updated_job

# Project endpoints
@app.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(status_code=403, detail="Only employers can post projects")
    
    try:
        # Convert project to dict and add required fields
        project_dict = project.dict()
        
        # Generate a unique ID
        project_id = str(ObjectId())
        project_dict["id"] = project_id
        project_dict["created_at"] = datetime.utcnow()
        project_dict["is_active"] = True
        project_dict["status"] = "open"
        project_dict["employer_id"] = current_user["id"]
        
        print(f"DEBUG - Creating project: employer_id={current_user['id']}, title={project_dict['title']}, id={project_id}")
        
        # Validate required fields
        required_fields = ["title", "company", "description", "requirements", "project_type", "skills_required"]
        missing_fields = [field for field in required_fields if field not in project_dict or not project_dict[field]]
        
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
            
        # Ensure list fields are actually lists
        list_fields = ["requirements", "skills_required"]
        for field in list_fields:
            if field in project_dict and not isinstance(project_dict[field], list):
                project_dict[field] = [project_dict[field]]  # Convert to list if it's not already
        
        # Remove any None values to prevent null constraints
        project_dict = {k: v for k, v in project_dict.items() if v is not None}
        
        # Insert the project
        await Database.get_collection(PROJECTS_COLLECTION).insert_one(project_dict)
        
        # Fetch and return the created project
        created_project = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_dict["id"]})
        if not created_project:
            print("DEBUG - Project not found after creation!")
            # Try using ObjectId directly as a fallback
            created_project = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
            if not created_project:
                raise HTTPException(status_code=500, detail="Failed to create project - cannot find it after creation")
            
        # Remove MongoDB's _id
        if "_id" in created_project:
            created_project.pop("_id", None)
            
        print(f"DEBUG - Project created successfully: id={created_project['id']}")
        return created_project
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating project: {str(e)}")  # Log the error
        import traceback
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )

@app.get("/projects", response_model=List[Project])
async def get_projects(status: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    print(f"DEBUG: get_projects called with status={status}")
    try:
        # Start with a base query
        query = {}
        
        # Only add filters if provided
        if status:
            print(f"DEBUG: Filtering by status: {status}")
            # Validate status
            valid_statuses = ["open", "in_progress", "completed", "cancelled"]
            if status not in valid_statuses:
                raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            query["status"] = status
        
        # Get all projects
        print(f"DEBUG: Query for all projects = {query}")
        projects = await Database.get_collection(PROJECTS_COLLECTION).find(query).to_list(length=None)
        print(f"DEBUG: Found {len(projects)} projects")
        
        # Process projects - remove _id and handle missing fields
        clean_projects = []
        required_fields = ["id", "title", "company", "description", "requirements", "employer_id", "is_active", "status", "project_type", "skills_required"]
        
        for project in projects:
            # Remove MongoDB's _id
            if "_id" in project:
                project.pop("_id", None)
                
            # Fill in any missing required fields
            for field in required_fields:
                if field not in project:
                    print(f"DEBUG: Project {project.get('id')} missing required field '{field}'")
                    if field in ["requirements", "skills_required"]:
                        project[field] = []
                    elif field in ["is_active"]:
                        project[field] = True
                    elif field in ["status"]:
                        project[field] = "open"
                    else:
                        project[field] = f"[Missing {field}]"
                        
            clean_projects.append(project)
            
        print(f"DEBUG: Returning {len(clean_projects)} projects")
        return clean_projects
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in get_projects: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to retrieve projects: {str(e)}")

@app.get("/employer-projects", response_model=List[Project])
async def get_current_employer_projects(current_user: dict = Depends(get_current_user)):
    """Get projects posted by the current employer using a different endpoint path"""
    try:
        # Check if user is an employer
        if current_user.get("user_type") != "employer":
            raise HTTPException(status_code=403, detail="Only employers can view their projects")
        
        employer_id = current_user.get("id")
        if not employer_id:
            raise HTTPException(status_code=400, detail="Invalid employer ID")
        
        print(f"DEBUG: Finding projects for employer_id: {employer_id}")
        
        # Find all projects for this employer
        projects_cursor = Database.get_collection(PROJECTS_COLLECTION).find({"employer_id": employer_id})
        projects = await projects_cursor.to_list(length=None)
        
        print(f"DEBUG: Found {len(projects)} projects")
        
        # Clean up projects before returning
        result_projects = []
        for project in projects:
            if "_id" in project:
                project.pop("_id", None)
            result_projects.append(project)
        
        return result_projects
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in get_current_employer_projects: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    """Get details of a specific project"""
    print(f"DEBUG: get_project called for project_id={project_id}, user={current_user.get('id')}")
    try:
        # Get the project
        print(f"DEBUG: Attempting to find project with id={project_id}")
        project = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
        print(f"DEBUG: Project found? {'Yes' if project else 'No'}")
        print(f"DEBUG: Project data: {project}")
        
        if not project:
            print(f"DEBUG: Project with id={project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Remove MongoDB's _id
        if "_id" in project:
            project.pop("_id", None)
            print("DEBUG: Removed _id from project")
            
        # Ensure all required fields are present
        required_fields = ["id", "title", "company", "description", "requirements", "employer_id", "is_active", "status", "project_type", "skills_required"]
        for field in required_fields:
            if field not in project:
                print(f"DEBUG: Required field '{field}' missing from project")
                if field in ["requirements", "skills_required"]:
                    project[field] = []
                elif field in ["is_active"]:
                    project[field] = True
                elif field in ["status"]:
                    project[field] = "open"
                else:
                    project[field] = f"[Missing {field}]"
            
        print(f"DEBUG: Project details: id={project.get('id')}, title={project.get('title')}")
        
        # If user is an employer, verify they own this project or return limited info
        if current_user["user_type"] == UserType.EMPLOYER:
            # Allow full access for project owners
            if project["employer_id"] == current_user["id"]:
                print("DEBUG: User is the project owner")
                return project
            else:
                print(f"DEBUG: User is not owner. Project owner={project.get('employer_id')}, User={current_user.get('id')}")
        
        # For non-owner employers and candidates, only return project if it's active
        if not project.get("is_active", False):
            print(f"DEBUG: Project is not active, returning 404")
            raise HTTPException(status_code=404, detail="Project not found or inactive")
        
        print("DEBUG: Returning project to non-owner")
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in get_project: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.patch("/projects/{project_id}", response_model=Project)
async def update_project_status(
    project_id: str,
    update_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update a project's details or status"""
    print(f"DEBUG: update_project_status called for project_id={project_id}, user={current_user.get('id')}")
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(status_code=403, detail="Only employers can update projects")
    
    try:
        # Get the project
        print(f"DEBUG: Attempting to find project with id={project_id}")
        project = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
        print(f"DEBUG: Project data: {project}")
        
        if not project:
            print(f"DEBUG: Project with id={project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Verify the project belongs to this employer
        if project["employer_id"] != current_user["id"]:
            print(f"DEBUG: User is not project owner. Project owner={project.get('employer_id')}, User={current_user.get('id')}")
            raise HTTPException(status_code=403, detail="You can only update your own projects")
        
        # Validate status if it's being updated
        if "status" in update_data:
            print(f"DEBUG: Validating status: {update_data['status']}")
            valid_statuses = ["open", "in_progress", "completed", "cancelled"]
            if update_data["status"] not in valid_statuses:
                raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        # Remove any invalid fields from update_data
        allowed_fields = ["status", "description", "title", "requirements", "budget_range", "duration", "location", "skills_required", "is_active"]
        invalid_fields = [key for key in update_data.keys() if key not in allowed_fields]
        for field in invalid_fields:
            print(f"DEBUG: Removing invalid field from update: {field}")
            update_data.pop(field, None)
            
        # Don't allow updating employer_id
        if "employer_id" in update_data:
            update_data.pop("employer_id", None)
            
        # Add updated timestamp
        update_data["last_updated"] = datetime.utcnow()
        print(f"DEBUG: Update data: {update_data}")
        
        # Update the project
        result = await Database.get_collection(PROJECTS_COLLECTION).update_one(
            {"id": project_id},
            {"$set": update_data}
        )
        print(f"DEBUG: Update result: matched={result.matched_count}, modified={result.modified_count}")
        
        if result.matched_count == 0:
            print("DEBUG: No documents were matched")
            raise HTTPException(status_code=404, detail="Project not found") 
        
        # Return updated project
        updated_project = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
        if not updated_project:
            print("DEBUG: Could not find updated project")
            raise HTTPException(status_code=404, detail="Project not found after update")
        
        if "_id" in updated_project:
            updated_project.pop("_id", None)
        
        print(f"DEBUG: Project updated successfully: {project_id}")    
        return updated_project
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in update_project_status: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")

@app.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a project"""
    print(f"DEBUG: delete_project called for project_id={project_id}, user={current_user.get('id')}")
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(status_code=403, detail="Only employers can delete projects")
    
    try:
        # Get the project
        print(f"DEBUG: Attempting to find project with id={project_id}")
        project = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
        print(f"DEBUG: Project found? {'Yes' if project else 'No'}")
        
        if not project:
            print(f"DEBUG: Project with id={project_id} not found")
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Verify the project belongs to this employer
        if project["employer_id"] != current_user["id"]:
            print(f"DEBUG: User is not project owner. Project owner={project.get('employer_id')}, User={current_user.get('id')}")
            raise HTTPException(status_code=403, detail="You can only delete your own projects")
        
        # Delete the project
        print(f"DEBUG: Deleting project with id={project_id}")
        result = await Database.get_collection(PROJECTS_COLLECTION).delete_one({"id": project_id})
        print(f"DEBUG: Delete result: deleted count={result.deleted_count}")
        
        if result.deleted_count == 0:
            print("DEBUG: No documents were deleted")
            # Even though we found it earlier, it might have been deleted concurrently or there might be an issue with the ID format
            # Check again to differentiate between "project doesn't exist" and "failed to delete"
            exists_check = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
            if exists_check:
                # It still exists, so deletion failed
                raise HTTPException(status_code=500, detail="Failed to delete project")
            else:
                # It's already gone
                return {"message": "Project already deleted", "id": project_id}
        
        print(f"DEBUG: Project deleted successfully: {project_id}")
        
        # Verify the project is really gone
        verify = await Database.get_collection(PROJECTS_COLLECTION).find_one({"id": project_id})
        if verify:
            print(f"WARNING: Project still exists after deletion: {project_id}")
            
        return {"message": "Project deleted successfully", "id": project_id}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in delete_project: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")

# Recommendation endpoints
@app.get("/recommendations/jobs", response_model=List[dict])
async def get_job_recommendations(current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] != UserType.CANDIDATE:
        raise HTTPException(status_code=403, detail="Only candidates can get job recommendations")
    
    # Get candidate profile
    candidate = await Database.get_collection(CANDIDATES_COLLECTION).find_one(
        {"email": current_user["email"]}
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    
    jobs = await Database.get_collection(JOBS_COLLECTION).find({"is_active": True}).to_list(length=None)
    recommendations = recommender.get_candidate_job_matches(candidate, jobs)
    return recommendations

@app.get("/recommendations/candidates/{job_id}", response_model=List[dict])
async def get_candidate_recommendations(job_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] != UserType.EMPLOYER:
        raise HTTPException(status_code=403, detail="Only employers can get candidate recommendations")
    
    job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Make sure to only get active candidates with complete profiles
    candidates = await Database.get_collection(CANDIDATES_COLLECTION).find({
        "is_active": True,
        "profile_completed": True
    }).to_list(length=None)
    
    if not candidates:
        print(f"No active candidates found for job {job_id}")
        return []
    
    recommendations = recommender.get_job_candidate_matches(job, candidates)
    
    # Fetch full candidate details for each recommendation
    detailed_recommendations = []
    for rec in recommendations:
        candidate = next((c for c in candidates if c["id"] == rec["candidate_id"]), None)
        if candidate:
            # Remove MongoDB's _id from candidate
            if "_id" in candidate:
                candidate.pop("_id", None)
                
            rec_with_details = rec.copy()
            rec_with_details["candidate"] = candidate
            detailed_recommendations.append(rec_with_details)
    
    return detailed_recommendations

# User profile endpoints
@app.put("/profile", response_model=User)
async def update_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] == UserType.CANDIDATE:
        # Update both user and candidate profiles
        # Update user profile
        await Database.get_collection(USERS_COLLECTION).update_one(
            {"email": current_user["email"]},
            {"$set": profile_data}
        )
        
        # Update candidate profile
        await Database.get_collection(CANDIDATES_COLLECTION).update_one(
            {"email": current_user["email"]},
            {"$set": profile_data}
        )
        
        # Get updated candidate profile
        updated_profile = await Database.get_collection(CANDIDATES_COLLECTION).find_one(
            {"email": current_user["email"]}
        )
        return updated_profile
    else:
        # Update both user and employer profiles
        # Update user profile
        await Database.get_collection(USERS_COLLECTION).update_one(
            {"email": current_user["email"]},
            {"$set": profile_data}
        )
        
        # Update employer profile
        await Database.get_collection(EMPLOYERS_COLLECTION).update_one(
            {"email": current_user["email"]},
            {"$set": profile_data}
        )
        
        # Get updated employer profile
        updated_profile = await Database.get_collection(EMPLOYERS_COLLECTION).find_one(
            {"email": current_user["email"]}
        )
        return updated_profile

@app.get("/profile", response_model=User)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@app.delete("/profile", response_model=dict)
async def delete_user(current_user: dict = Depends(get_current_user)):
    try:
        # Delete from users collection
        user_result = await Database.get_collection(USERS_COLLECTION).delete_one(
            {"email": current_user["email"]}
        )
        
        if user_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        # If user is a candidate, also delete from candidates collection
        if current_user["user_type"] == UserType.CANDIDATE:
            candidate_result = await Database.get_collection(CANDIDATES_COLLECTION).delete_one(
                {"email": current_user["email"]}
            )
            if candidate_result.deleted_count == 0:
                print(f"Warning: Candidate profile not found for user {current_user['email']}")
        
        # If user is an employer, delete from employers collection and their posted jobs
        elif current_user["user_type"] == UserType.EMPLOYER:
            # Delete employer profile
            employer_result = await Database.get_collection(EMPLOYERS_COLLECTION).delete_one(
                {"email": current_user["email"]}
            )
            if employer_result.deleted_count == 0:
                print(f"Warning: Employer profile not found for user {current_user['email']}")
            
            # Delete all jobs posted by this employer
            jobs_result = await Database.get_collection(JOBS_COLLECTION).delete_many(
                {"employer_id": current_user["id"]}
            )
            if jobs_result.deleted_count > 0:
                print(f"Deleted {jobs_result.deleted_count} jobs posted by employer {current_user['email']}")
            
            # Delete all projects posted by this employer
            projects_result = await Database.get_collection(PROJECTS_COLLECTION).delete_many(
                {"employer_id": current_user["id"]}
            )
            if projects_result.deleted_count > 0:
                print(f"Deleted {projects_result.deleted_count} projects posted by employer {current_user['email']}")
        
        return {"message": "User and associated profiles deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logout/candidate")
async def logout_candidate(token: str = Depends(oauth2_scheme), current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(
                status_code=403,
                detail="Only candidates can use this endpoint"
            )
        # Add token to blacklist
        BLACKLISTED_TOKENS.add(token)
        return {"message": "Candidate successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logout/employer")
async def logout_employer(token: str = Depends(oauth2_scheme), current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.EMPLOYER:
            raise HTTPException(
                status_code=403,
                detail="Only employers can use this endpoint"
            )
        # Add token to blacklist
        BLACKLISTED_TOKENS.add(token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Job application endpoints
@app.post("/applications", response_model=JobApplication)
async def apply_for_job(application: JobApplicationCreate, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can apply for jobs")
        
        # Check if the job exists
        job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": application.job_id})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Check if the candidate has already applied for this job
        existing_application = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).find_one({
            "candidate_id": current_user["id"],
            "job_id": application.job_id
        })
        
        if existing_application:
            raise HTTPException(status_code=400, detail="You have already applied for this job")
        
        # Create a new application
        application_dict = application.dict()
        application_dict["id"] = str(ObjectId())
        application_dict["candidate_id"] = current_user["id"]
        application_dict["employer_id"] = job["employer_id"]
        application_dict["created_at"] = datetime.utcnow()
        application_dict["status"] = "applied"
        application_dict["last_updated"] = datetime.utcnow()
        
        # Insert into job applications collection
        await Database.get_collection(JOB_APPLICATIONS_COLLECTION).insert_one(application_dict)
        
        # Remove MongoDB's _id
        application_dict.pop("_id", None)
        
        return application_dict
    
    except Exception as e:
        print(f"Error in apply_for_job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to apply for job")

@app.get("/applications", response_model=List[JobApplication])
async def get_job_applications(current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can view their job applications")
        
        # Get all applications for this candidate
        applications = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).find({
            "candidate_id": current_user["id"]
        }).to_list(length=None)
        
        # Get job details for each application
        for application in applications:
            application.pop("_id", None)
            job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": application["job_id"]})
            if job:
                application["job_details"] = {
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "location": job.get("location")
                }
        
        return applications
    
    except Exception as e:
        print(f"Error in get_job_applications: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get job applications")

@app.delete("/applications/{application_id}")
async def withdraw_application(application_id: str, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can withdraw applications")
        
        # Check if the application exists and belongs to this candidate
        application = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).find_one({
            "id": application_id,
            "candidate_id": current_user["id"]
        })
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found or does not belong to you")
        
        # Delete the application
        result = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).delete_one({
            "id": application_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to withdraw application")
        
        return {"message": "Application withdrawn successfully"}
    
    except Exception as e:
        print(f"Error in withdraw_application: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to withdraw application")

@app.patch("/applications/{application_id}", response_model=JobApplication)
async def update_application(
    application_id: str, 
    update_data: dict, 
    current_user: dict = Depends(get_current_user)
):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can update applications")
        
        # Check if the application exists and belongs to this candidate
        application = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).find_one({
            "id": application_id,
            "candidate_id": current_user["id"]
        })
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found or does not belong to you")
        
        # Only allow updating certain fields
        allowed_fields = ["cover_letter", "notes", "resume_url"]
        update_dict = {k: v for k, v in update_data.items() if k in allowed_fields}
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        # Add last_updated timestamp
        update_dict["last_updated"] = datetime.utcnow()
        
        # Update the application
        result = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).update_one(
            {"id": application_id},
            {"$set": update_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update application")
        
        # Get updated application
        updated_application = await Database.get_collection(JOB_APPLICATIONS_COLLECTION).find_one({"id": application_id})
        if not updated_application:
            raise HTTPException(status_code=404, detail="Application not found after update")
        
        # Remove MongoDB's _id
        updated_application.pop("_id", None)
        
        # Get job details
        job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": updated_application["job_id"]})
        if job:
            updated_application["job_details"] = {
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location")
            }
        
        return updated_application
    
    except Exception as e:
        print(f"Error in update_application: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update application")

# Saved jobs endpoints
@app.post("/saved-jobs", response_model=SavedJob)
async def save_job(saved_job: SavedJobCreate, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can save jobs")
        
        # Check if the job exists
        job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": saved_job.job_id})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
    
        # Check if the job is already saved
        existing_saved_job = await Database.get_collection(SAVED_JOBS_COLLECTION).find_one({
            "candidate_id": current_user["id"],
            "job_id": saved_job.job_id
        })
        
        if existing_saved_job:
            raise HTTPException(status_code=400, detail="You have already saved this job")
        
        # Create a new saved job
        saved_job_dict = saved_job.dict()
        saved_job_dict["id"] = str(ObjectId())
        saved_job_dict["candidate_id"] = current_user["id"]
        saved_job_dict["employer_id"] = job["employer_id"]
        saved_job_dict["created_at"] = datetime.utcnow()
        
        # Insert into saved jobs collection
        await Database.get_collection(SAVED_JOBS_COLLECTION).insert_one(saved_job_dict)
        
        # Remove MongoDB's _id
        saved_job_dict.pop("_id", None)
        
        return saved_job_dict
    
    except Exception as e:
        print(f"Error in save_job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save job")

@app.get("/saved-jobs", response_model=List[SavedJob])
async def get_saved_jobs(current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can view their saved jobs")
        
        # Get all saved jobs for this candidate
        saved_jobs = await Database.get_collection(SAVED_JOBS_COLLECTION).find({
            "candidate_id": current_user["id"]
        }).to_list(length=None)
    
        # Get job details for each saved job
        for saved_job in saved_jobs:
            saved_job.pop("_id", None)
            job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": saved_job["job_id"]})
            if job:
                saved_job["job_details"] = {
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "location": job.get("location")
                }
        
        return saved_jobs
    
    except Exception as e:
        print(f"Error in get_saved_jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get saved jobs")

@app.delete("/saved-jobs/{saved_job_id}")
async def remove_saved_job(saved_job_id: str, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can remove saved jobs")
        
        # Check if the saved job exists and belongs to this candidate
        saved_job = await Database.get_collection(SAVED_JOBS_COLLECTION).find_one({
            "id": saved_job_id,
            "candidate_id": current_user["id"]
        })
        
        if not saved_job:
            raise HTTPException(status_code=404, detail="Saved job not found or does not belong to you")
        
        # Delete the saved job
        result = await Database.get_collection(SAVED_JOBS_COLLECTION).delete_one({
            "id": saved_job_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to remove saved job")
        
        return {"message": "Saved job removed successfully"}
    
    except Exception as e:
        print(f"Error in remove_saved_job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to remove saved job")

@app.patch("/saved-jobs/{saved_job_id}", response_model=SavedJob)
async def update_saved_job(
    saved_job_id: str, 
    update_data: dict, 
    current_user: dict = Depends(get_current_user)
):
    try:
        if current_user["user_type"] != UserType.CANDIDATE:
            raise HTTPException(status_code=403, detail="Only candidates can update saved jobs")
        
        # Check if the saved job exists and belongs to this candidate
        saved_job = await Database.get_collection(SAVED_JOBS_COLLECTION).find_one({
            "id": saved_job_id,
            "candidate_id": current_user["id"]
        })
        
        if not saved_job:
            raise HTTPException(status_code=404, detail="Saved job not found or does not belong to you")
        
        # Only allow updating notes field
        if "notes" not in update_data:
            raise HTTPException(status_code=400, detail="Notes field is required for update")
        
        update_dict = {"notes": update_data["notes"]}
        
        # Update the saved job
        result = await Database.get_collection(SAVED_JOBS_COLLECTION).update_one(
            {"id": saved_job_id},
            {"$set": update_dict}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update saved job")
        
        # Get updated saved job
        updated_saved_job = await Database.get_collection(SAVED_JOBS_COLLECTION).find_one({"id": saved_job_id})
        if not updated_saved_job:
            raise HTTPException(status_code=404, detail="Saved job not found after update")
        
        # Remove MongoDB's _id
        updated_saved_job.pop("_id", None)
        
        # Get job details
        job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": updated_saved_job["job_id"]})
        if job:
            updated_saved_job["job_details"] = {
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location")
            }
        
        return updated_saved_job
    
    except Exception as e:
        print(f"Error in update_saved_job: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update saved job")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
    #uvicorn.run(app, host="0.0.0.0", port=8000) 
