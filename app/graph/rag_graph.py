from langgraph.graph import StateGraph, END

from app.graph.nodes import generate_answer, retriving_context, rewrite_query, grade_relevance
from app.graph.state import RAGState


def decide_next_step(state: RAGState) -> str:
    """Conditional edge: retry retrieval or generate answer."""
    grade = state.get('grade')
    if grade == "yes":
        return "generate_answer"
    return "retry_retrieve"


def build_rag_graph():
    graph = StateGraph(RAGState)

    # add nodes
    graph.add_node("rewrite_query", rewrite_query)
    graph.add_node("retrive_context", retriving_context)
    graph.add_node("grade_relevance", grade_relevance)
    graph.add_node("generate_answer", generate_answer)

    # define edges
    graph.set_entry_point("rewrite_query")
    graph.add_edge("rewrite_query", "retrive_context")
    graph.add_edge("retrive_context", "grade_relevance")

    graph.add_conditional_edges(
        "grade_relevance",
        decide_next_step,
        {
            "generate_answer": "generate_answer",
            "retry_retrieve": "rewrite_query",  # loop back
        },
    )

    graph.add_edge("generate_answer", END)
    return graph.compile()


rag_graph = build_rag_graph()
