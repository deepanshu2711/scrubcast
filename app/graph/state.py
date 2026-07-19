from operator import add
from typing import Annotated, TypedDict
from langchain_core.documents import Document


class RAGState(TypedDict):

    video_id: int
    question: str
    rewritten_question: str
    documents: Annotated[list[Document], add]
    generation: str
    grade: str
    retry_count: int
