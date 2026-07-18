from langchain_qdrant import QdrantVectorStore

from app.config.embedding import embedding_model
from app.config.qdrant import client

vector_store = QdrantVectorStore(
    client=client, collection_name="videos", embedding=embedding_model
)
