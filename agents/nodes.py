from agents.states import ApplicationState
from agents.dfa import transition

def document_parsing_agent(state: ApplicationState) -> ApplicationState:
    """
    Real version (later): uses PyMuPDF/pdfplumber to extract resume text,
    then GPT-4o-mini to structure it into JSON, then pgvector for skill matching.
    Stub version (now): fakes a decent match score so we can test the pipeline flow.
    """
    state["resume_text"] = "stub extracted resume text"
    state["skill_match_score"] = 0.82  # placeholder, replace with real RAG+BM25 result later

    event = "match_success" if state["skill_match_score"] >= 0.5 else "reject_retry_eligible"
    state["current_state"] = transition(state["current_state"], event)
    state["log"].append(f"DocumentParsingAgent -> {state['current_state']}")
    return state


def assessment_agent(state: ApplicationState) -> ApplicationState:
    """Real version (later): pulls raw_exam_scores, computes percentile rank (your PR formula)."""
    state["exam_score"] = 78.5  # placeholder

    event = "exam_pass" if state["exam_score"] >= 60 else "exam_fail"
    state["current_state"] = transition(state["current_state"], event)
    state["log"].append(f"AssessmentAgent -> {state['current_state']}")
    return state


def evaluation_agent(state: ApplicationState) -> ApplicationState:
    """Real version (later): aggregates HR Director / Dept Head / VP interview scores,
    with each interview submitted separately over time.
    Stub version (now): simulates all three interviews completing back-to-back,
    so we can test the full DFA path S3 -> S4 -> S5 -> S6 in one run."""
    state["evaluation_scores"] = {"hr_director": 85, "dept_head": 88, "vp": 90}  # placeholder

    for _ in range(3):
        state["current_state"] = transition(state["current_state"], "interview_complete")
        state["log"].append(f"EvaluationAgent -> {state['current_state']}")

    return state


def reporter_agent(state: ApplicationState) -> ApplicationState:
    """Real version (later): uses Whisper to transcribe + GPT-4o-mini to synthesize a report."""
    avg_score = sum(state["evaluation_scores"].values()) / len(state["evaluation_scores"])
    state["final_rating"] = "Highly Qualified" if avg_score >= 80 else "Not Qualified"

    event = "highly_qualified" if state["final_rating"] == "Highly Qualified" else "not_qualified"
    state["current_state"] = transition(state["current_state"], event)
    state["log"].append(f"ReporterAgent -> {state['current_state']} ({state['final_rating']})")
    return state