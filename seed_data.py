from database import SessionLocal
from models import Applicant, Position, Application, ApplicationStatus

db = SessionLocal()

applicant = Applicant(
    full_name="Juan Dela Cruz",
    email="juan.delacruz@example.com",
    phone_number="09171234567",
)
position = Position(
    title="Junior Backend Developer",
    department="IT",
    description="Entry-level backend role focused on API development.",
    required_skills="Python, FastAPI, PostgreSQL, REST APIs",
    is_open=1,
)
db.add_all([applicant, position])
db.commit()
db.refresh(applicant)
db.refresh(position)

application = Application(
    applicant_id=applicant.id,
    position_id=position.id,
    status=ApplicationStatus.applied,
)
db.add(application)
db.commit()
db.refresh(application)

print(f"Seeded Application ID: {application.id}")
db.close()