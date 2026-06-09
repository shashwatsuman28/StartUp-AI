"""Document retriever for RAG system"""

import logging
from typing import List, Optional
from langchain.schema import Document
from rag_system.vectorstore import VectorStoreManager

logger = logging.getLogger(__name__)


class DocumentRetriever:
    """
    Retrieves relevant documents from vector store based on queries.
    Core component of the RAG system.
    """

    def __init__(self, vector_store_manager: VectorStoreManager, top_k: int = 5):
        """
        Initialize retriever.

        Args:
            vector_store_manager: VectorStoreManager instance
            top_k: Number of top results to retrieve
        """
        self.vector_store = vector_store_manager
        self.top_k = top_k

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Search query
            top_k: Override default top_k value

        Returns:
            List of relevant documents
        """
        k = top_k or self.top_k

        logger.info(f"Retrieving {k} documents for query: {query}")

        documents = self.vector_store.similarity_search(query, k=k)

        return documents

    def retrieve_with_scores(
        self, query: str, top_k: Optional[int] = None
    ) -> List[tuple]:
        """
        Retrieve documents with similarity scores.

        Args:
            query: Search query
            top_k: Override default top_k value

        Returns:
            List of (Document, score) tuples
        """
        k = top_k or self.top_k

        results = self.vector_store.similarity_search_with_score(query, k=k)

        return results

    def format_retrieval_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string.

        Args:
            documents: List of retrieved documents

        Returns:
            Formatted context string
        """
        context_parts = []

        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content[:500]  # Limit content length

            part = f"Document {i} (Source: {source}):\n{content}\n"
            context_parts.append(part)

        return "\n".join(context_parts)

    def retrieve_and_format(self, query: str, top_k: Optional[int] = None) -> str:
        """
        Retrieve documents and return formatted context.

        Args:
            query: Search query
            top_k: Override default top_k value

        Returns:
            Formatted context string
        """
        documents = self.retrieve(query, top_k=top_k)
        return self.format_retrieval_context(documents)
