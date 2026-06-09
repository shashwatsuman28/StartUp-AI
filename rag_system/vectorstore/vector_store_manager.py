"""Vector store management for embeddings and retrieval"""

import logging
from typing import List, Optional
from pathlib import Path

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """
    Manages vector store for document embeddings.
    Supports FAISS for local storage and retrieval.
    """

    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: Optional[str] = None,
    ):
        """
        Initialize vector store manager.

        Args:
            embedding_model: HuggingFace embedding model name
            persist_directory: Directory to persist vector store
        """
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vector_store = None

        if persist_directory and Path(persist_directory).exists():
            self._load_store()

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to vector store.

        Args:
            documents: List of Document objects to add
        """
        try:
            if self.vector_store is None:
                # Create new vector store
                self.vector_store = FAISS.from_documents(
                    documents, self.embeddings
                )
                logger.info(f"Created new vector store with {len(documents)} documents")
            else:
                # Add to existing vector store
                self.vector_store.add_documents(documents)
                logger.info(f"Added {len(documents)} documents to vector store")

            # Persist if directory specified
            if self.persist_directory:
                self.save_store()

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(
        self, query: str, k: int = 5, filter_metadata: Optional[dict] = None
    ) -> List[Document]:
        """
        Search for similar documents.

        Args:
            query: Search query
            k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of similar documents
        """
        if self.vector_store is None:
            logger.warning("Vector store is empty")
            return []

        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {str(e)}")
            return []

    def similarity_search_with_score(
        self, query: str, k: int = 5
    ) -> List[tuple]:
        """
        Search with similarity scores.

        Args:
            query: Search query
            k: Number of results

        Returns:
            List of (Document, score) tuples
        """
        if self.vector_store is None:
            return []

        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Error during similarity search with score: {str(e)}")
            return []

    def save_store(self) -> None:
        """Save vector store to disk"""
        if self.vector_store is None or not self.persist_directory:
            return

        try:
            self.vector_store.save_local(self.persist_directory)
            logger.info(f"Vector store saved to {self.persist_directory}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise

    def _load_store(self) -> None:
        """Load vector store from disk"""
        try:
            self.vector_store = FAISS.load_local(
                self.persist_directory, self.embeddings
            )
            logger.info(f"Loaded vector store from {self.persist_directory}")
        except Exception as e:
            logger.warning(f"Could not load vector store: {str(e)}")
            self.vector_store = None

    def delete_store(self) -> None:
        """Delete vector store"""
        if self.persist_directory:
            import shutil

            try:
                shutil.rmtree(self.persist_directory)
                self.vector_store = None
                logger.info("Vector store deleted")
            except Exception as e:
                logger.error(f"Error deleting vector store: {str(e)}")

    def get_store_stats(self) -> dict:
        """Get statistics about the vector store"""
        if self.vector_store is None:
            return {"total_documents": 0, "status": "empty"}

        return {
            "total_documents": self.vector_store.index.ntotal,
            "embedding_dimension": len(self.embeddings.embed_query("test")),
            "status": "active",
        }
