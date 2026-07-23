from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from database import Base
import enum

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    screening = "screening"
    exam = "exam"
    interview = "interview"
    final_review = "final_review"
    hired = "hired"
    rejected = "rejected"

class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="applicant")


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    department = Column(String)
    employment_type = Column(String)  # full-time, OJT, contractual
    description = Column(Text)
    responsibilities = Column(Text)
    required_skills = Column(Text)
    preferred_skills = Column(Text)
    education_requirement = Column(String)
    min_experience_years = Column(Integer)
    certifications_required = Column(Text)
    is_open = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    applications = relationship("Application", back_populates="position")


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    applicant = relationship("Applicant", back_populates="applications")
    position = relationship("Position", back_populates="applications")
    documents = relationship("Document", back_populates="application")
    skill_matches = relationship("SkillMatch", back_populates="application")
    examinations = relationship("Examination", back_populates="application")
    interviews = relationship("Interview", back_populates="application")
    stage_history = relationship("StageHistory", back_populates="application")


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    doc_type = Column(String)  # e.g. "resume", "compliance_file"
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="documents")


class SkillMatch(Base):
    __tablename__ = "skill_matches"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    matched_keywords = Column(Text)
    embedding = Column(Vector(1536))  # adjust dimension to match your embedding model
    match_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="skill_matches")


class Examination(Base):
    __tablename__ = "examinations"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    exam_name = Column(String)
    score = Column(Float)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="examinations")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String)  # e.g. "HR Director", "Interviewer"
    hashed_password = Column(String, nullable=False)

    evaluations = relationship("Evaluation", back_populates="evaluator")


class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    state = Column(String)  # e.g. "scheduled", "completed"
    summary = Column(Text)
    scheduled_at = Column(DateTime(timezone=True))

    application = relationship("Application", back_populates="interviews")
    evaluations = relationship("Evaluation", back_populates="interview")


class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interview = relationship("Interview", back_populates="evaluations")
    evaluator = relationship("User", back_populates="evaluations")


class StageHistory(Base):
    __tablename__ = "stage_history"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    from_stage = Column(String)
    to_stage = Column(String)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="stage_history")