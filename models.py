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

class User(UserBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Candidate(UserBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class CandidateCreate(UserBase):
    user_type: UserType = UserType.CANDIDATE
    password: str
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class Employer(UserBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    company_name: str
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    company_location: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None

class EmployerCreate(UserBase):
    user_type: UserType = UserType.EMPLOYER
    password: str
    company_name: str
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    company_location: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
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

class ProjectBase(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str]
    budget_range: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    project_type: str
    skills_required: List[str]
    deadline: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    employer_id: str

class Project(ProjectBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    employer_id: str
    is_active: bool = True
    status: str = "open"  # open, in_progress, completed, cancelled

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