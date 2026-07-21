from enum import Enum
from typing import TypedDict, Optional

class DFAState(str, Enum):
    S0_RESUME_SUBMITTED = "S0"
    S1_SHORTLISTED = "S1"
    S2_ONLINE_EXAM = "S2"
    S3_HR_DIRECTOR_INTERVIEW = "S3"
    S4_DEPT_HEAD_INTERVIEW = "S4"
    S5_VP_INTERVIEW = "S5"
    S6_FINAL_DECISION = "S6"
    S7_HIRED = "S7"
    S8_REJECTED = "S8"


class ApplicationState(TypedDict):
    """
    This is the shared object every agent reads from and writes to
    as it moves through the LangGraph pipeline. Think of it as the
    single 'case file' that gets passed from agent to agent.
    """
    application_id: int
    current_state: DFAState
    resume_text: Optional[str]
    skill_match_score: Optional[float]
    exam_score: Optional[float]
    interview_notes: Optional[str]
    evaluation_scores: Optional[dict]
    final_rating: Optional[str]  # e.g. "Highly Qualified", "Rejected"
    log: list  # audit trail of what happened at each step