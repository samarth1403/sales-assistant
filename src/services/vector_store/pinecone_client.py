from src.services.embedding.embedder import get_embedder
from langchain_pinecone import PineconeVectorStore
from src.utils.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

def get_vectorstore():
    embedder = get_embedder()
    return PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embedder, pinecone_api_key=PINECONE_API_KEY)

def upsert_texts(texts: list[str], metadatas: list[dict], session_id: str):
    vectorstore = get_vectorstore()
    enriched_metadata = [
        {**metadata, "session_id": session_id}
        for metadata in metadatas
    ]
    vectorstore.add_texts(texts=texts, metadatas=enriched_metadata)

def search_similar_context(query: str, top_k: int = 3, session_id: str = ""):
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=top_k, filter={"session_id": session_id})
    return results