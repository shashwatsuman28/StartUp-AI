"""Main RAG pipeline orchestrating all components"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from rag_system.loaders import MultiFormatDocumentLoader
from rag_system.utils import TextSplitter
from rag_system.vectorstore import VectorStoreManager
from rag_system.retrievers import DocumentRetriever
from rag_system.generators import RAGGenerator
from rag_system.config.settings import RAG_CONFIG, LLM_CONFIG, VECTOR_STORE_SETTINGS

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Complete RAG pipeline for startup analysis.
    Handles document loading, embedding, retrieval, and generation.
    """

    def __init__(
        self,
        vector_store_dir: Optional[str] = None,
        embedding_model: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        """
        Initialize RAG pipeline.

        Args:
            vector_store_dir: Directory for vector store persistence
            embedding_model: Embedding model name
            openai_api_key: OpenAI API key
        """
        # Use provided settings or defaults
        self.vector_store_dir = vector_store_dir or VECTOR_STORE_SETTINGS[
            "persist_directory"
        ]
        self.embedding_model = embedding_model or RAG_CONFIG["embedding_model"]

        # Initialize components
        self.loader = MultiFormatDocumentLoader(
            chunk_size=RAG_CONFIG["chunk_size"],
            chunk_overlap=RAG_CONFIG["chunk_overlap"],
        )

        self.text_splitter = TextSplitter(
            chunk_size=RAG_CONFIG["chunk_size"],
            chunk_overlap=RAG_CONFIG["chunk_overlap"],
        )

        self.vector_store = VectorStoreManager(
            embedding_model=self.embedding_model,
            persist_directory=self.vector_store_dir,
        )

        self.retriever = DocumentRetriever(
            vector_store_manager=self.vector_store,
            top_k=RAG_CONFIG["retrieval_top_k"],
        )

        self.generator = RAGGenerator(
            retriever=self.retriever,
            model_name=LLM_CONFIG["model"],
            temperature=LLM_CONFIG["temperature"],
            api_key=openai_api_key or LLM_CONFIG["api_key"],
        )

        logger.info("RAG Pipeline initialized successfully")

    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """
        Ingest a single file into the RAG system.

        Args:
            file_path: Path to the file

        Returns:
            Dict with ingestion results
        """
        try:
            logger.info(f"Ingesting file: {file_path}")

            # Load document
            documents = self.loader.load_file(file_path)
            logger.info(f"Loaded {len(documents)} documents from file")

            # Split documents
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Split into {len(split_docs)} chunks")

            # Add to vector store
            self.vector_store.add_documents(split_docs)

            return {
                "status": "success",
                "file": Path(file_path).name,
                "documents_loaded": len(documents),
                "chunks_created": len(split_docs),
            }

        except Exception as e:
            logger.error(f"Error ingesting file: {str(e)}")
            return {
                "status": "error",
                "file": Path(file_path).name,
                "error": str(e),
            }

    def ingest_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Ingest all supported files from a directory.

        Args:
            directory_path: Path to directory

        Returns:
            Dict with ingestion results
        """
        try:
            logger.info(f"Ingesting directory: {directory_path}")

            # Load all documents
            documents = self.loader.load_directory(directory_path)
            logger.info(f"Loaded {len(documents)} documents from directory")

            # Split documents
            split_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Split into {len(split_docs)} chunks")

            # Add to vector store
            self.vector_store.add_documents(split_docs)

            return {
                "status": "success",
                "directory": directory_path,
                "documents_loaded": len(documents),
                "chunks_created": len(split_docs),
            }

        except Exception as e:
            logger.error(f"Error ingesting directory: {str(e)}")
            return {
                "status": "error",
                "directory": directory_path,
                "error": str(e),
            }

    def query(self, question: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """
        Query the RAG system with a question.

        Args:
            question: Question to answer
            top_k: Number of documents to retrieve

        Returns:
            Dict with query results and answer
        """
        logger.info(f"Processing query: {question}")
        return self.generator.analyze(question, top_k=top_k or RAG_CONFIG["retrieval_top_k"])

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all ingested documents"""
        return self.generator.summarize()

    def get_concepts(self) -> Dict[str, Any]:
        """Extract key concepts from documents"""
        return self.generator.extract_concepts()

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system"""
        return {
            "vector_store": self.vector_store.get_store_stats(),
            "embedding_model": self.embedding_model,
            "retrieval_top_k": RAG_CONFIG["retrieval_top_k"],
        }

    def clear_store(self) -> Dict[str, str]:
        """Clear all data from vector store"""
        try:
            self.vector_store.delete_store()
            return {"status": "success", "message": "Vector store cleared"}
        except Exception as e:
            logger.error(f"Error clearing store: {str(e)}")
            return {"status": "error", "error": str(e)}
