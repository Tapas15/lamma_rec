from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserType(str, Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"

class UserBase(BaseModel):
    email: EmailStr
    user_type: UserType
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class JobBase(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str]
    location: str
    salary_range: Optional[str] = None

class JobCreate(JobBase):
    employer_id: str

class Job(JobBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    employer_id: str
    is_active: bool = True

class Recommendation(BaseModel):
    id: str
    user_id: str
    job_id: Optional[str] = None
    candidate_id: Optional[str] = None
    match_score: float
    explanation: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[UserType] = None 