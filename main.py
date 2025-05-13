from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional
import os
from dotenv import load_dotenv
from bson import ObjectId

from models import *
from database import Database, USERS_COLLECTION, JOBS_COLLECTION, RECOMMENDATIONS_COLLECTION
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
async def register(user: UserCreate):
    if await Database.get_collection(USERS_COLLECTION).find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    user_dict["id"] = str(ObjectId())
    
    await Database.get_collection(USERS_COLLECTION).insert_one(user_dict)
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
    
    jobs = await Database.get_collection(JOBS_COLLECTION).find({"is_active": True}).to_list(length=None)
    recommendations = recommender.get_candidate_job_matches(current_user, jobs)
    return recommendations

@app.get("/recommendations/candidates/{job_id}", response_model=List[dict])
async def get_candidate_recommendations(job_id: str, current_user: dict = Depends(get_current_user)):
    try:
        if current_user["user_type"] != UserType.EMPLOYER:
            raise HTTPException(status_code=403, detail="Only employers can get candidate recommendations")
        
        print(f"Fetching job with ID: {job_id}")
        try:
            job = await Database.get_collection(JOBS_COLLECTION).find_one({"id": job_id})
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            print(f"Found job: {job}")
        except Exception as e:
            print(f"Error finding job: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error finding job: {str(e)}")
        
        print("Fetching candidates...")
        try:
            candidates = await Database.get_collection(USERS_COLLECTION).find(
                {"user_type": UserType.CANDIDATE}
            ).to_list(length=None)
            # Convert _id to string for all candidates
            for c in candidates:
                c["id"] = str(c["_id"])
            print(f"Found {len(candidates)} candidates")
        except Exception as e:
            print(f"Error fetching candidates: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching candidates: {str(e)}")
        
        if not candidates:
            return []
        
        print("Getting job-candidate matches...")
        try:
            recommendations = recommender.get_job_candidate_matches(job, candidates)
            print(f"Generated {len(recommendations)} recommendations")
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
        
        # Fetch full candidate details for each recommendation
        detailed_recommendations = []
        for rec in recommendations:
            try:
                print(f"rec['candidate_id']: {rec['candidate_id']}, candidate ids: {[c['id'] for c in candidates]}")
                candidate = next((c for c in candidates if c["id"] == rec["candidate_id"]), None)
                if candidate:
                    rec_with_details = rec.copy()
                    # Remove sensitive information
                    if "password" in candidate:
                        del candidate["password"]
                    rec_with_details["candidate"] = candidate
                    detailed_recommendations.append(rec_with_details)
            except Exception as e:
                print(f"Error processing recommendation: {str(e)}")
                continue
        
        print(f"Returning {len(detailed_recommendations)} detailed recommendations")
        return detailed_recommendations
    except Exception as e:
        print(f"Error in get_candidate_recommendations: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# User profile endpoints
@app.put("/profile", response_model=User)
async def update_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    await Database.get_collection(USERS_COLLECTION).update_one(
        {"email": current_user["email"]},
        {"$set": profile_data}
    )
    updated_user = await Database.get_collection(USERS_COLLECTION).find_one(
        {"email": current_user["email"]}
    )
    return updated_user

@app.get("/profile", response_model=User)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 