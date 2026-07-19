from sqlmodel import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.store import vector_store
from app.graph.rag_graph import rag_graph
from app.graph.state import RAGState
from app.repositories.chat import ChatRepository


class ChatService:
    def __init__(self, session: Session) -> None:
        self.repository = ChatRepository(session)

    def initiate_chat(self, video_id: int):
        snippets = self.repository.get_snippets(video_id)
        transcript = "\n".join(snippet.text for snippet in snippets)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )
        docs = splitter.create_documents(
            [transcript],
            metadatas=[{"video_id": video_id}],
        )

        vector_store.add_documents(docs)
        return

    def ask_question(self, video_id: int, question: str):
        initial_state: RAGState = {
            "video_id": video_id,
            "question": question,
            "rewritten_question": "",
            "documents": [],
            "generation": "",
            "retry_count": 0,
            "grade": "no"
        }

        result = rag_graph.invoke(initial_state)
        return result['generation']
