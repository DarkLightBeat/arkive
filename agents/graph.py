from langgraph.graph import StateGraph, END
from agents.states import ApplicationState, DFAState
from agents.nodes import document_parsing_agent, assessment_agent, evaluation_agent, reporter_agent

def build_graph():
    workflow = StateGraph(ApplicationState)

    # Register each agent as a node
    workflow.add_node("document_parsing", document_parsing_agent)
    workflow.add_node("assessment", assessment_agent)
    workflow.add_node("evaluation", evaluation_agent)
    workflow.add_node("reporter", reporter_agent)

    # Define the flow — this mirrors your S0 -> S2 -> S3/4/5 -> S6 pipeline
    workflow.set_entry_point("document_parsing")
    workflow.add_edge("document_parsing", "assessment")
    workflow.add_edge("assessment", "evaluation")
    workflow.add_edge("evaluation", "reporter")
    workflow.add_edge("reporter", END)

    return workflow.compile()


# Quick manual test — no API key needed since everything's stubbed
if __name__ == "__main__":
    graph = build_graph()

    initial_state: ApplicationState = {
        "application_id": 1,  # <- use the ID printed by seed_data.py
        "current_state": DFAState.S0_RESUME_SUBMITTED,
        "resume_text": None,
        "skill_match_score": None,
        "exam_score": None,
        "interview_notes": None,
        "evaluation_scores": None,
        "final_rating": None,
        "log": [],
    }

    result = graph.invoke(initial_state)

    print("Final state:", result["current_state"])
    print("Final rating:", result["final_rating"])
    print("\nAudit log:")
    for entry in result["log"]:
        print(" -", entry)