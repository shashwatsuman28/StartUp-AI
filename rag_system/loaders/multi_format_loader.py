"""Multi-format document loader for various file types"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
import pandas as pd

logger = logging.getLogger(__name__)


class MultiFormatDocumentLoader:
    """
    Loads documents from multiple file formats:
    - PDF (.pdf)
    - Word (.docx, .doc)
    - Excel (.xlsx, .xls)
    - Text (.txt, .md)
    """

    SUPPORTED_FORMATS = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "docx",
        ".xlsx": "excel",
        ".xls": "excel",
        ".txt": "text",
        ".md": "text",
    }

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the loader.

        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_file(self, file_path: str) -> List[Document]:
        """
        Load a single file and return documents.

        Args:
            file_path: Path to the file

        Returns:
            List of Document objects
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = file_path.suffix.lower()

        if file_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS.keys())}"
            )

        file_type = self.SUPPORTED_FORMATS[file_ext]

        try:
            if file_type == "pdf":
                return self._load_pdf(file_path)
            elif file_type == "docx":
                return self._load_docx(file_path)
            elif file_type == "excel":
                return self._load_excel(file_path)
            elif file_type == "text":
                return self._load_text(file_path)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            raise

    def load_directory(self, directory_path: str) -> List[Document]:
        """
        Load all supported files from a directory.

        Args:
            directory_path: Path to directory

        Returns:
            List of Document objects from all files
        """
        documents = []
        directory_path = Path(directory_path)

        if not directory_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory_path}")

        for file_path in directory_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                try:
                    docs = self.load_file(str(file_path))
                    documents.extend(docs)
                    logger.info(f"Loaded {len(docs)} documents from {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to load {file_path.name}: {str(e)}")

        return documents

    def _load_pdf(self, file_path: Path) -> List[Document]:
        """Load PDF file"""
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        # Add metadata
        for doc in documents:
            doc.metadata["source"] = file_path.name
            doc.metadata["file_type"] = "pdf"
            doc.metadata["loaded_at"] = datetime.now().isoformat()

        return documents

    def _load_docx(self, file_path: Path) -> List[Document]:
        """Load Word document (.docx)"""
        loader = Docx2txtLoader(str(file_path))
        documents = loader.load()

        # Add metadata
        for doc in documents:
            doc.metadata["source"] = file_path.name
            doc.metadata["file_type"] = "docx"
            doc.metadata["loaded_at"] = datetime.now().isoformat()

        return documents

    def _load_excel(self, file_path: Path) -> List[Document]:
        """Load Excel file (.xlsx, .xls)"""
        documents = []

        try:
            xl_file = pd.ExcelFile(str(file_path))

            for sheet_name in xl_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)

                # Convert DataFrame to text
                text = f"Sheet: {sheet_name}\n"
                text += df.to_string()

                doc = Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name,
                        "sheet": sheet_name,
                        "file_type": "excel",
                        "loaded_at": datetime.now().isoformat(),
                    },
                )
                documents.append(doc)

        except Exception as e:
            logger.error(f"Error loading Excel file {file_path}: {str(e)}")
            raise

        return documents

    def _load_text(self, file_path: Path) -> List[Document]:
        """Load text file (.txt, .md)"""
        loader = TextLoader(str(file_path), encoding="utf-8")
        documents = loader.load()

        # Add metadata
        for doc in documents:
            doc.metadata["source"] = file_path.name
            doc.metadata["file_type"] = file_path.suffix.lower().strip(".")
            doc.metadata["loaded_at"] = datetime.now().isoformat()

        return documents
