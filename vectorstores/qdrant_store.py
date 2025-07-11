from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

def get_qdrant_vectorstore(collection_name: str):
    client = QdrantClient(url="http://localhost:6543")
    return Qdrant(client, collection_name, embeddings=get_embeddings())