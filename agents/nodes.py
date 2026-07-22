from agents.states import ApplicationState
from agents.dfa import transition
from agents.db_writer import record_stage_transition, record_skill_match, record_examination
from database import SessionLocal
from models import Application


def document_parsing_agent(state: ApplicationState) -> ApplicationState:
    db = SessionLocal()
    try:
        application = db.query(Application).filter(
            Application.id == state["application_id"]
        ).first()

        if not application:
            raise ValueError(f"No application found with id {state['application_id']}")

        applicant_name = application.applicant.full_name
        position_title = application.position.title
        required_skills = application.position.required_skills

        state["resume_text"] = f"[stub] Resume text for {applicant_name}"
        state["skill_match_score"] = 0.82  # placeholder

        state["log"].append(
            f"DocumentParsingAgent: pulled Application #{application.id} "
            f"({applicant_name} -> {position_title}, required: {required_skills})"
        )
    finally:
        db.close()

    record_skill_match(
        application_id=state["application_id"],
        score=state["skill_match_score"],
        matched_keywords=required_skills,
    )

    previous_state = state["current_state"]
    event = "match_success" if state["skill_match_score"] >= 0.5 else "reject_retry_eligible"
    state["current_state"] = transition(previous_state, event)
    record_stage_transition(state["application_id"], previous_state, state["current_state"])
    state["log"].append(f"DocumentParsingAgent -> {state['current_state']}")
    return state


def assessment_agent(state: ApplicationState) -> ApplicationState:
    state["exam_score"] = 78.5  # placeholder

    record_examination(
        application_id=state["application_id"],
        score=state["exam_score"],
    )

    previous_state = state["current_state"]
    event = "exam_pass" if state["exam_score"] >= 60 else "exam_fail"
    state["current_state"] = transition(previous_state, event)
    record_stage_transition(state["application_id"], previous_state, state["current_state"])
    state["log"].append(f"AssessmentAgent -> {state['current_state']}")
    return state


def evaluation_agent(state: ApplicationState) -> ApplicationState:
    state["evaluation_scores"] = {"hr_director": 85, "dept_head": 88, "vp": 90}  # placeholder

    for _ in range(3):
        previous_state = state["current_state"]
        state["current_state"] = transition(previous_state, "interview_complete")
        record_stage_transition(state["application_id"], previous_state, state["current_state"])
        state["log"].append(f"EvaluationAgent -> {state['current_state']}")

    return state


def reporter_agent(state: ApplicationState) -> ApplicationState:
    avg_score = sum(state["evaluation_scores"].values()) / len(state["evaluation_scores"])
    state["final_rating"] = "Highly Qualified" if avg_score >= 80 else "Not Qualified"

    previous_state = state["current_state"]
    event = "highly_qualified" if state["final_rating"] == "Highly Qualified" else "not_qualified"
    state["current_state"] = transition(previous_state, event)
    record_stage_transition(state["application_id"], previous_state, state["current_state"])
    state["log"].append(f"ReporterAgent -> {state['current_state']} ({state['final_rating']})")
    return state