from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional, Union
import os
from dotenv import load_dotenv
from bson import ObjectId

from models import *
from database import Database, USERS_COLLECTION, JOBS_COLLECTION, RECOMMENDATIONS_COLLECTION, CANDIDATES_COLLECTION
from llama_recommender import LlamaRecommender

load_dotenv()

app = FastAPI(title="Job Recommender System")
recommender = LlamaRecommender()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database connection
@app.on_event("startup")
async def startup_db_client():
    await Database.connect_db()

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

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
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

# Authentication endpoints
@app.post("/register", response_model=User)
async def register_user(user: Union[CandidateCreate, EmployerCreate]):
    # Check if user already exists
    existing_user = await Database.get_collection(USERS_COLLECTION).find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user document
    user_dict = user.dict()
    user_dict["id"] = str(ObjectId())
    user_dict["created_at"] = datetime.utcnow()
    user_dict["password"] = pwd_context.hash(user.password)
    
    # Insert into users collection
    await Database.get_collection(USERS_COLLECTION).insert_one(user_dict)
    
    # If user is a candidate, create candidate profile
    if user.user_type == UserType.CANDIDATE:
        candidate_dict = {
            "id": user_dict["id"],
            "email": user.email,
            "user_type": user.user_type,
            "full_name": user.full_name,
            "created_at": datetime.utcnow(),
            "skills": user_dict["skills"],  # Directly use the skills from the input
            "experience": user_dict.get("experience"),
            "education": user_dict.get("education"),
            "location": user_dict.get("location"),
            "bio": user_dict.get("bio")
        }
        await Database.get_collection(CANDIDATES_COLLECTION).insert_one(candidate_dict)
    
    # Remove password from response
    del user_dict["password"]
    return user_dict

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
    
    candidates = await Database.get_collection(CANDIDATES_COLLECTION).find().to_list(length=None)
    if not candidates:
        return []
    
    recommendations = recommender.get_job_candidate_matches(job, candidates)
    
    # Fetch full candidate details for each recommendation
    detailed_recommendations = []
    for rec in recommendations:
        candidate = next((c for c in candidates if c["id"] == rec["candidate_id"]), None)
        if candidate:
            rec_with_details = rec.copy()
            rec_with_details["candidate"] = candidate
            detailed_recommendations.append(rec_with_details)
    
    return detailed_recommendations

# User profile endpoints
@app.put("/profile", response_model=User)
async def update_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    if current_user["user_type"] == UserType.CANDIDATE:
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
        # Update employer profile
        await Database.get_collection(USERS_COLLECTION).update_one(
            {"email": current_user["email"]},
            {"$set": profile_data}
        )
        # Get updated user profile
        updated_profile = await Database.get_collection(USERS_COLLECTION).find_one(
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
        
        return {"message": "User and associated profiles deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 