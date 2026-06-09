"""Configuration settings for RAG system"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# RAG Configuration
RAG_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "vector_store_type": "faiss",  # Options: faiss, chroma, pinecone
    "retrieval_top_k": 5,
}

# LLM Configuration
LLM_CONFIG = {
    "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
    "temperature": 0.7,
    "max_tokens": 2000,
    "api_key": os.getenv("OPENAI_API_KEY", ""),
}

# Supported file types
SUPPORTED_FILE_TYPES = {
    "pdf": [".pdf"],
    "word": [".docx", ".doc"],
    "excel": [".xlsx", ".xls"],
    "text": [".txt", ".md"],
}

# File size limits (in MB)
MAX_FILE_SIZE = 50

# Vector store settings
VECTOR_STORE_SETTINGS = {
    "persist_directory": str(VECTOR_STORE_DIR),
    "index_name": "startup_ai_index",
}
