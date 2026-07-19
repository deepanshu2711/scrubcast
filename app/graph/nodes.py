from app.config.llm import llm
from qdrant_client.models import FieldCondition, Filter, MatchValue
from app.graph.state import RAGState
from app.config.store import vector_store


def rewrite_query(state: RAGState):
    """Rewrite the user question into a better search query."""

    question = state["question"]

    prompt = f"""
    You are a query rewriting assistant. Given the user's question,
    rewrite it into a concise, effective search query for vector similarity search.

    Original question: {question}

    Rewritten query:
    """

    response = llm.invoke(prompt)

    return {
        "rewritten_question": response.content,
        "retry_count": 0,
    }


def retriving_context(state: RAGState):
    """Retrive relevant transcript chunks from Qdrant."""
    search_query = state.get("rewritten_question") or state.get('question')

    docs = vector_store.similarity_search(
        query=search_query,
        k=3,
        filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.video_id",
                    match=MatchValue(value=state['video_id'])
                )
            ]
        )
    )

    return {'documents': docs}


def grade_relevance(state: RAGState):
    """Check if retrieved documents are relevant to the question."""

    question = state["question"]
    docs = state["documents"]
    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""You are a relevance grader. Given the question and the retrieved context,
    determine if the context is relevant enough to answer the question.

    Question: {question}
    Context: {context}

    Is the context relevant? Answer only "yes" or "no"."""  # noqa: E501

    response = llm.invoke(prompt)
    answer = response.content

    retry_count = state.get("retry_count", 0)

    if answer == "yes" or retry_count >= 2:
        return {"grade": "yes"}
    return {
        "grade": "no",
        "retry_count": retry_count + 1,
    }


def generate_answer(state: RAGState) -> dict:
    """Generate an answer using the retrieved context."""
    question = state["question"]
    docs = state["documents"]
    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""Answer the question based on the context below.
    If the context doesn't contain enough information, say so.

    Context: {context}
    Question: {question}
    Answer:"""

    response = llm.invoke(prompt)

    return {"generation": response.content}
