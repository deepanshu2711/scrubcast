from qdrant_client.models import FieldCondition, Filter, MatchValue
from sqlmodel import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.llm import llm
from app.config.store import vector_store
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
        result = vector_store.similarity_search(
            query=question,
            k=3,
            filter=Filter(
                must=[
                    FieldCondition(
                        key="metadata.video_id",
                        match=MatchValue(value=video_id)
                    )
                ]
            )
        )

        context = "\n".join([doc.page_content for doc in result])
        prompt = f"""Answer the question based on the context below:
        Context: {context}
        Question: {question}
        Answer:"""

        response = llm.invoke(prompt)
        return response.content


#
