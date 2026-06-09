"""Example: Using the RAG Pipeline for Startup Analysis"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_system.core import RAGPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Example usage of RAG pipeline"""

    # Initialize RAG pipeline
    print("=" * 60)
    print("StartUp AI - RAG System Demo")
    print("=" * 60)

    rag = RAGPipeline()

    # Example 1: Ingest sample documents
    print("\n1. Ingesting documents...")
    print("-" * 60)

    sample_data_dir = Path(__file__).parent.parent / "data" / "uploads"

    if sample_data_dir.exists() and any(sample_data_dir.iterdir()):
        result = rag.ingest_directory(str(sample_data_dir))
        print(f"Ingestion Result: {result}")
    else:
        print(f"Note: Place sample documents in {sample_data_dir}")
        print("Supported formats: PDF, DOCX, XLSX, TXT, MD")

    # Example 2: Get system statistics
    print("\n2. System Statistics:")
    print("-" * 60)
    stats = rag.get_stats()
    print(f"Vector Store Stats: {stats['vector_store']}")
    print(f"Embedding Model: {stats['embedding_model']}")

    # Example 3: Query the system
    print("\n3. Querying the RAG system...")
    print("-" * 60)

    sample_queries = [
        "What is the business model of this startup?",
        "What market opportunities are identified?",
        "Who are the key competitors?",
    ]

    for query in sample_queries:
        print(f"\nQuery: {query}")
        print("-" * 40)

        result = rag.query(query)

        if result["status"] == "success":
            print(f"Answer: {result['answer'][:500]}...")
        else:
            print(f"Status: {result['status']}")
            if "error" in result:
                print(f"Error: {result['error']}")

    # Example 4: Get summary and concepts
    print("\n4. Document Analysis:")
    print("-" * 60)

    summary_result = rag.get_summary()
    print(f"\nSummary Status: {summary_result['status']}")
    if summary_result["status"] == "success":
        print(f"Summary:\n{summary_result['summary'][:500]}...")

    concepts_result = rag.get_concepts()
    print(f"\nConcepts Status: {concepts_result['status']}")
    if concepts_result["status"] == "success":
        print(f"Concepts:\n{concepts_result['concepts'][:500]}...")

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
