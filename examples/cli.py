"""Interactive CLI for RAG system"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_system.core import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGCli:
    """Command-line interface for RAG system"""

    def __init__(self):
        """Initialize CLI and RAG pipeline"""
        print("\n" + "=" * 70)
        print("StartUp AI - RAG System CLI")
        print("=" * 70)
        print("\nInitializing RAG pipeline...")

        try:
            self.rag = RAGPipeline()
            print("✓ RAG Pipeline initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing RAG: {str(e)}")
            sys.exit(1)

    def show_menu(self):
        """Display main menu"""
        print("\n" + "-" * 70)
        print("MENU:")
        print("-" * 70)
        print("1. Ingest file")
        print("2. Ingest directory")
        print("3. Query documents")
        print("4. Get summary")
        print("5. Extract concepts")
        print("6. System statistics")
        print("7. Clear store")
        print("8. Exit")
        print("-" * 70)

    def ingest_file(self):
        """Ingest a single file"""
        file_path = input("\nEnter file path: ").strip()

        if not file_path:
            print("Cancelled.")
            return

        result = self.rag.ingest_file(file_path)
        self._print_result(result)

    def ingest_directory(self):
        """Ingest all files from directory"""
        dir_path = input("\nEnter directory path: ").strip()

        if not dir_path:
            print("Cancelled.")
            return

        result = self.rag.ingest_directory(dir_path)
        self._print_result(result)

    def query(self):
        """Query the RAG system"""
        question = input("\nEnter your question: ").strip()

        if not question:
            print("Cancelled.")
            return

        top_k = input("Number of documents to retrieve (default: 5): ").strip()
        top_k = int(top_k) if top_k.isdigit() else 5

        print("\nProcessing query...")
        result = self.rag.query(question, top_k=top_k)

        if result["status"] == "success":
            print("\n" + "-" * 70)
            print("ANSWER:")
            print("-" * 70)
            print(result["answer"])
        else:
            self._print_result(result)

    def get_summary(self):
        """Get document summary"""
        print("\nGenerating summary...")
        result = self.rag.get_summary()

        if result["status"] == "success":
            print("\n" + "-" * 70)
            print("SUMMARY:")
            print("-" * 70)
            print(result["summary"])
        else:
            self._print_result(result)

    def get_concepts(self):
        """Extract key concepts"""
        print("\nExtracting concepts...")
        result = self.rag.get_concepts()

        if result["status"] == "success":
            print("\n" + "-" * 70)
            print("KEY CONCEPTS:")
            print("-" * 70)
            print(result["concepts"])
        else:
            self._print_result(result)

    def show_stats(self):
        """Show system statistics"""
        stats = self.rag.get_stats()
        print("\n" + "-" * 70)
        print("SYSTEM STATISTICS:")
        print("-" * 70)
        print(f"Vector Store: {stats['vector_store']}")
        print(f"Embedding Model: {stats['embedding_model']}")

    def clear_store(self):
        """Clear vector store"""
        confirm = input("\nAre you sure? (y/n): ").strip().lower()

        if confirm == "y":
            result = self.rag.clear_store()
            self._print_result(result)
        else:
            print("Cancelled.")

    def _print_result(self, result):
        """Pretty print result dict"""
        print("\n" + "-" * 70)
        for key, value in result.items():
            print(f"{key}: {value}")

    def run(self):
        """Run CLI main loop"""
        while True:
            self.show_menu()
            choice = input("\nEnter choice (1-8): ").strip()

            if choice == "1":
                self.ingest_file()
            elif choice == "2":
                self.ingest_directory()
            elif choice == "3":
                self.query()
            elif choice == "4":
                self.get_summary()
            elif choice == "5":
                self.get_concepts()
            elif choice == "6":
                self.show_stats()
            elif choice == "7":
                self.clear_store()
            elif choice == "8":
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    cli = RAGCli()
    cli.run()
