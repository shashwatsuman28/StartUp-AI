"""
StartUp AI - RAG System - QUICK REFERENCE GUIDE
"""

# ============================================================================
# INSTALLATION & SETUP
# ============================================================================

## 1. Install Dependencies
pip install -r requirements.txt

## 2. Configure Environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

## 3. Add Your Documents
# Place startup documents in: data/uploads/
# Supported formats: PDF, DOCX, XLSX, TXT, MD


# ============================================================================
# BASIC USAGE - PYTHON API
# ============================================================================

from rag_system.core import RAGPipeline

# Initialize
rag = RAGPipeline()

# Option 1: Ingest a single file
result = rag.ingest_file("data/uploads/business_plan.pdf")
print(result['documents_loaded'])  # Number of documents loaded

# Option 2: Ingest entire directory
result = rag.ingest_directory("data/uploads/")
print(f"Loaded: {result['documents_loaded']} documents")
print(f"Created: {result['chunks_created']} chunks")

# Query the system
answer = rag.query("What is the startup's business model?", top_k=5)
print(answer['answer'])

# Get analysis
summary = rag.get_summary()
print(summary['summary'])

concepts = rag.get_concepts()
print(concepts['concepts'])

# Get statistics
stats = rag.get_stats()
print(stats)


# ============================================================================
# INTERACTIVE CLI
# ============================================================================

python examples/cli.py

# Menu options:
# 1. Ingest file
# 2. Ingest directory
# 3. Query documents
# 4. Get summary
# 5. Extract concepts
# 6. System statistics
# 7. Clear store
# 8. Exit


# ============================================================================
# EXAMPLE WORKFLOWS
# ============================================================================

## Workflow 1: Analyze Single Startup
rag = RAGPipeline()
rag.ingest_file("startup_pitch.pdf")

queries = [
    "What problem does this startup solve?",
    "What is the target market size?",
    "What are the competitive advantages?",
    "What is the business model?",
    "What are the key metrics?",
]

for query in queries:
    result = rag.query(query)
    print(f"Q: {query}")
    print(f"A: {result['answer']}\n")


## Workflow 2: Batch Analysis
import os

rag = RAGPipeline()
startups_dir = "data/startups/"

for startup_name in os.listdir(startups_dir):
    startup_path = os.path.join(startups_dir, startup_name)
    if os.path.isdir(startup_path):
        result = rag.ingest_directory(startup_path)
        print(f"\n{startup_name}:")
        print(f"  Documents: {result['documents_loaded']}")
        print(f"  Chunks: {result['chunks_created']}")
        
        # Analysis
        summary = rag.get_summary()
        print(f"  Summary: {summary['summary'][:200]}...")


## Workflow 3: Custom Questions
rag = RAGPipeline()
rag.ingest_directory("data/uploads/")

while True:
    question = input("\nAsk a question (or 'quit'): ")
    if question.lower() == 'quit':
        break
    
    result = rag.query(question)
    print(f"\nAnswer: {result['answer']}\n")


# ============================================================================
# CONFIGURATION
# ============================================================================

# Edit: rag_system/config/settings.py

# Chunk settings
RAG_CONFIG = {
    "chunk_size": 1000,        # Increase for more context
    "chunk_overlap": 200,      # Overlap between chunks
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "retrieval_top_k": 5,      # Number of docs to retrieve
}

# LLM settings
LLM_CONFIG = {
    "model": "gpt-4-turbo",    # OpenAI model
    "temperature": 0.7,         # 0 = factual, 1 = creative
    "max_tokens": 2000,        # Response length
}

# File formats supported
SUPPORTED_FILE_TYPES = {
    "pdf": [".pdf"],
    "word": [".docx", ".doc"],
    "excel": [".xlsx", ".xls"],
    "text": [".txt", ".md"],
}


# ============================================================================
# ADVANCED USAGE
# ============================================================================

## Direct Component Access
from rag_system.loaders import MultiFormatDocumentLoader
from rag_system.vectorstore import VectorStoreManager
from rag_system.retrievers import DocumentRetriever
from rag_system.generators import RAGGenerator

# Load documents
loader = MultiFormatDocumentLoader(chunk_size=1000)
documents = loader.load_directory("data/uploads/")

# Create vector store
vector_store = VectorStoreManager()
vector_store.add_documents(documents)

# Retrieve
retriever = DocumentRetriever(vector_store, top_k=5)
docs = retriever.retrieve("business model")

# Generate
generator = RAGGenerator(retriever, model_name="gpt-4-turbo")
analysis = generator.analyze("What is the business model?")


## Custom Retrieval
rag = RAGPipeline()
rag.ingest_directory("data/uploads/")

# Retrieve with scores
results = rag.retriever.retrieve_with_scores(
    "market opportunity",
    top_k=10
)
for doc, score in results:
    print(f"Score: {score:.3f} | {doc.metadata['source']}")


## Error Handling
try:
    result = rag.ingest_file("document.pdf")
    if result['status'] == 'error':
        print(f"Error: {result['error']}")
    else:
        print(f"Success: {result['documents_loaded']} docs")
except Exception as e:
    print(f"Exception: {str(e)}")


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Issue: "No module named 'rag_system'"
export PYTHONPATH=$PYTHONPATH:/workspaces/StartUp-AI

# Issue: "OPENAI_API_KEY not found"
# Make sure .env file exists and has correct key

# Issue: Vector store is slow
# - Reduce top_k value
# - Clear store: rag.clear_store()
# - Use smaller documents

# Issue: Out of memory
# - Reduce chunk_size
# - Process files one at a time
# - Clear vector store periodically


# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

# For SPEED:
# - Use smaller chunk_size (500)
# - Lower top_k (3)
# - Use faster embedding model

# For ACCURACY:
# - Use larger chunk_size (1500)
# - Higher top_k (10)
# - Use larger embedding model

# For MEMORY:
# - Clear vector store periodically
# - Process large documents in batches
# - Delete old vector store files


# ============================================================================
# NEXT STEPS
# ============================================================================

# 1. Add your startup documents to data/uploads/
# 2. Test with: python examples/cli.py
# 3. Integrate into your application
# 4. Check RAG_DOCUMENTATION.md for advanced features

# See README.md for full documentation
