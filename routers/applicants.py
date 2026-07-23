from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Applicant
from schemas.applicant import ApplicantCreate, ApplicantUpdate, ApplicantResponse

router = APIRouter(prefix="/applicants", tags=["Applicants"])


@router.post("/", response_model=ApplicantResponse)
def create_applicant(applicant: ApplicantCreate, db: Session = Depends(get_db)):
    existing = db.query(Applicant).filter(Applicant.email == applicant.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_applicant = Applicant(**applicant.model_dump())
    db.add(new_applicant)
    db.commit()
    db.refresh(new_applicant)
    return new_applicant


@router.get("/", response_model=list[ApplicantResponse])
def list_applicants(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Applicant).offset(skip).limit(limit).all()


@router.get("/{applicant_id}", response_model=ApplicantResponse)
def get_applicant(applicant_id: int, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant


@router.put("/{applicant_id}", response_model=ApplicantResponse)
def update_applicant(applicant_id: int, updates: ApplicantUpdate, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(applicant, field, value)

    db.commit()
    db.refresh(applicant)
    return applicant


@router.delete("/{applicant_id}")
def delete_applicant(applicant_id: int, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    db.delete(applicant)
    db.commit()
    return {"message": f"Applicant {applicant_id} deleted successfully"}