from sqlmodel import Session
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from app.config.qdrant import client

from app.config.embedding import embedding_model
from app.repositories.chat import ChatRepository


class ChatService:
    def __init__(self, session: Session) -> None:
        self.repository = ChatRepository(session)

    def initiate_chat(self, video_id: int):
        snippets = self.repository.get_snippets(video_id)

        docs = []

        for snippet in snippets:
            docs.append(
                Document(
                    page_content=snippet.text,
                    metadata={
                        "video_id": snippet.video_id,
                        "start": snippet.start,
                        "duration": snippet.duration,
                    }
                )
            )
        print('docs:', docs)

        vector_store = QdrantVectorStore(
            client=client, collection_name="videos", embedding=embedding_model
        )

        vector_store.add_documents(docs)

        return
