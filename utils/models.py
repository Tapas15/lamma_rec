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
    company_description: str
    company_website: str
    company_location: str
    company_size: str
    industry: str
    contact_email: str
    contact_phone: str
    location: str
    bio: str
    profile_completed: bool = True
    is_active: bool = True
    last_active: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = False
    total_jobs_posted: int = 0
    total_active_jobs: int = 0
    account_type: str = "standard"
    profile_views: int = 0
    rating: Optional[float] = None
    social_links: dict = Field(default_factory=lambda: {"linkedin": "", "twitter": "", "website": ""})
    posted_jobs: Optional[List[dict]] = []

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
    linkedin: Optional[str] = None
    twitter: Optional[str] = None

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

class JobApplication(BaseModel):
    id: str
    candidate_id: str
    job_id: str
    employer_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "applied"  # applied, reviewed, interview, rejected, accepted
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    notes: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
class JobApplicationCreate(BaseModel):
    job_id: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    notes: Optional[str] = None

class SavedJob(BaseModel):
    id: str
    candidate_id: str
    job_id: str
    employer_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    
class SavedJobCreate(BaseModel):
    job_id: str
    notes: Optional[str] = None

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