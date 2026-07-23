from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ApplicantBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None

class ApplicantCreate(ApplicantBase):
    """Used when someone submits a new applicant — no id/created_at yet."""
    pass

class ApplicantUpdate(BaseModel):
    """All fields optional — lets you update just one field without resending everything."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

class ApplicantResponse(ApplicantBase):
    """What gets sent back to the client — includes db-generated fields."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic read directly from SQLAlchemy objects