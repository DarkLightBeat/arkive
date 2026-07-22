from database import SessionLocal
from models import StageHistory, Application, SkillMatch, Examination, ApplicationStatus

# Maps your fine-grained DFA states (S0-S8) to the coarser
# ApplicationStatus enum already defined on the Application table itself.
DFA_TO_STATUS = {
    "S0": ApplicationStatus.applied,
    "S1": ApplicationStatus.screening,
    "S2": ApplicationStatus.exam,
    "S3": ApplicationStatus.interview,
    "S4": ApplicationStatus.interview,
    "S5": ApplicationStatus.interview,
    "S6": ApplicationStatus.final_review,
    "S7": ApplicationStatus.hired,
    "S8": ApplicationStatus.rejected,
}


def record_stage_transition(application_id: int, from_state, to_state):
    """
    Called after every DFA transition. Writes a permanent audit row
    to stage_history, and updates the Application's overall status
    to match the new stage. This is the real, persistent version of
    what the in-memory 'log' list has been doing all along.
    """
    db = SessionLocal()
    try:
        history = StageHistory(
            application_id=application_id,
            from_stage=from_state.value,
            to_stage=to_state.value,
        )
        db.add(history)

        application = db.query(Application).filter(Application.id == application_id).first()
        if application:
            application.status = DFA_TO_STATUS[to_state.value]

        db.commit()
    finally:
        db.close()


def record_skill_match(application_id: int, score: float, matched_keywords: str):
    db = SessionLocal()
    try:
        match = SkillMatch(
            application_id=application_id,
            match_score=score,
            matched_keywords=matched_keywords,
        )
        db.add(match)
        db.commit()
    finally:
        db.close()


def record_examination(application_id: int, score: float, exam_name: str = "Online Skills Exam"):
    db = SessionLocal()
    try:
        exam = Examination(
            application_id=application_id,
            score=score,
            exam_name=exam_name,
        )
        db.add(exam)
        db.commit()
    finally:
        db.close()