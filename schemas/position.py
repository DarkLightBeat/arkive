from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PositionBase(BaseModel):
    title: str
    department: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    education_requirement: Optional[str] = None
    min_experience_years: Optional[int] = None
    certifications_required: Optional[str] = None
    is_open: Optional[int] = 1

class PositionCreate(PositionBase):
    pass

class PositionUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    required_skills: Optional[str] = None
    preferred_skills: Optional[str] = None
    education_requirement: Optional[str] = None
    min_experience_years: Optional[int] = None
    certifications_required: Optional[str] = None
    is_open: Optional[int] = None

class PositionResponse(PositionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True