import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Milvus Config
    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
    MILVUS_COLLECTION_NAME = os.getenv("MILVUS_COLLECTION_NAME", "dspy_rag_collection")
    
    # Embedding Model
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    @staticmethod
    def validate():
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")
