"""Text splitting utilities"""

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class TextSplitter:
    """Splits documents into chunks for embedding"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text splitter.

        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.

        Args:
            documents: List of Document objects

        Returns:
            List of split Document objects
        """
        return self.splitter.split_documents(documents)

    def split_text(self, text: str) -> List[str]:
        """
        Split plain text into chunks.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        return self.splitter.split_text(text)
