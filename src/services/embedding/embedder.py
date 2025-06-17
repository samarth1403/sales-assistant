from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.utils.config import GOOGLE_API_KEY

def get_embedder():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )
