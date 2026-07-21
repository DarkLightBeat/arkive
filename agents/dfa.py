from agents.states import DFAState

# This is the mathematical transition matrix from your proposal (δ: Q × Σ → Q)
# Each key is (current_state, event), and the value is the only legal next state.
VALID_TRANSITIONS = {
    (DFAState.S0_RESUME_SUBMITTED, "reject_retry_eligible"): DFAState.S1_SHORTLISTED,
    (DFAState.S0_RESUME_SUBMITTED, "match_success"): DFAState.S2_ONLINE_EXAM,
    (DFAState.S1_SHORTLISTED, "recontacted"): DFAState.S2_ONLINE_EXAM,
    (DFAState.S2_ONLINE_EXAM, "exam_fail"): DFAState.S1_SHORTLISTED,
    (DFAState.S2_ONLINE_EXAM, "exam_pass"): DFAState.S3_HR_DIRECTOR_INTERVIEW,
    (DFAState.S3_HR_DIRECTOR_INTERVIEW, "interview_complete"): DFAState.S4_DEPT_HEAD_INTERVIEW,
    (DFAState.S4_DEPT_HEAD_INTERVIEW, "interview_complete"): DFAState.S5_VP_INTERVIEW,
    (DFAState.S5_VP_INTERVIEW, "interview_complete"): DFAState.S6_FINAL_DECISION,
    (DFAState.S6_FINAL_DECISION, "highly_qualified"): DFAState.S7_HIRED,
    (DFAState.S6_FINAL_DECISION, "not_qualified"): DFAState.S8_REJECTED,
}


class DFAPermissionError(Exception):
    """Raised when an agent attempts an illegal state transition."""
    pass


def transition(current_state: DFAState, event: str) -> DFAState:
    """
    This is the actual DFA governance check — the 'hallucination guard'
    described in your proposal. Every agent MUST call this function
    instead of setting state directly.
    """
    key = (current_state, event)
    if key not in VALID_TRANSITIONS:
        raise DFAPermissionError(
            f"Illegal transition attempted: {current_state} --({event})--> blocked. "
            f"This move is not defined in the DFA transition matrix."
        )
    return VALID_TRANSITIONS[key]