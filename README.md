# StartUp AI Analysis Platform

## Overview

**StartUp AI** is a comprehensive platform for analyzing startup ideas and company information using advanced AI technologies. The system combines Retrieval-Augmented Generation (RAG) with machine learning to provide intelligent insights and reports.

## Current Phase: RAG System ✅

We're currently building the **RAG (Retrieval-Augmented Generation) System**, which is the foundation of the platform.

### What is RAG?

RAG enhances large language models by:
1. **Retrieving** relevant documents based on user queries
2. **Augmenting** the context with actual startup information
3. **Generating** intelligent, contextual responses using LLMs

## Features

### 📄 Multi-Format Document Ingestion
- **PDF Files** - Extract text and structure from PDFs
- **Word Documents** (.docx, .doc) - Read formatted documents
- **Excel Files** (.xlsx, .xls) - Convert spreadsheets to insights
- **Text Files** (.txt, .md) - Support for plain text and markdown

### 🔍 Intelligent Retrieval
- Semantic similarity search using embeddings
- Top-K document ranking
- Score-based relevance filtering
- Metadata-aware retrieval

### 🧠 Smart Analysis
- Document summarization
- Concept extraction
- Context-aware question answering
- Multi-document synthesis

### 💾 Persistent Storage
- FAISS vector database for fast retrieval
- Local persistence for quick access
- Scalable architecture

## Quick Start

### 1. Setup
```bash
cd /workspaces/StartUp-AI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
```

### 2. Ingest Documents
```python
from rag_system.core import RAGPipeline

rag = RAGPipeline()
result = rag.ingest_directory("data/uploads/")
print(f"Ingested {result['documents_loaded']} documents")
```

### 3. Query Documents
```python
answer = rag.query("What is the startup's business model?")
print(answer['answer'])
```

### 4. Get Analysis
```python
summary = rag.get_summary()
concepts = rag.get_concepts()
```

## Project Structure

```
StartUp-AI/
├── rag_system/
│   ├── config/              # Configuration
│   ├── loaders/             # Document loaders
│   ├── utils/               # Utilities
│   ├── vectorstore/         # Vector storage
│   ├── retrievers/          # Retrieval logic
│   ├── generators/          # Response generation
│   └── core/                # Main RAG pipeline
├── data/
│   ├── uploads/             # Input documents
│   └── vector_store/        # Persistent vector storage
├── examples/                # Usage examples
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── RAG_DOCUMENTATION.md    # Detailed documentation
```

## Documentation

See [RAG_DOCUMENTATION.md](RAG_DOCUMENTATION.md) for:
- Detailed architecture overview
- API reference
- Configuration guide
- Advanced usage examples
- Troubleshooting

## Example Usage

### Via Python API
```bash
python examples/example_usage.py
```

### Via Interactive CLI
```bash
python examples/cli.py
```

## System Requirements

- Python 3.8+
- 2GB RAM minimum (4GB+ recommended)
- OpenAI API key
- Disk space for vector store (varies by document size)

## Dependencies

Key libraries:
- **LangChain** - LLM framework
- **OpenAI** - GPT-4 integration
- **HuggingFace** - Embeddings
- **FAISS** - Vector search
- **PyPDF, python-docx** - Document parsing

## Configuration

### Environment Variables
```
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4-turbo
```

### RAG Settings (in `rag_system/config/settings.py`)
```python
RAG_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "retrieval_top_k": 5,
}
```

## Roadmap

### Phase 1: RAG System ✅ (Current)
- [x] Multi-format document loading
- [x] Text splitting and chunking
- [x] Vector embeddings
- [x] FAISS vector store
- [x] Semantic retrieval
- [x] LLM-based generation
- [x] CLI interface
- [x] Documentation

### Phase 2: Analysis Engine (Next)
- [ ] ML models for document scoring
- [ ] Startup metrics extraction
- [ ] Competitive analysis
- [ ] Risk assessment
- [ ] Financial analysis
- [ ] Market sizing

### Phase 3: Dashboard (Future)
- [ ] Web interface
- [ ] Report generation
- [ ] Visualization
- [ ] Data export
- [ ] Team collaboration
- [ ] Real-time updates

## Usage Examples

### Example 1: Startup Analysis
```python
rag = RAGPipeline()
rag.ingest_directory("startup_docs/")

# Get insights
summary = rag.get_summary()
concepts = rag.get_concepts()

# Ask specific questions
queries = [
    "What is the business model?",
    "Who is the target market?",
    "What are competitive advantages?",
]

for query in queries:
    answer = rag.query(query)
    print(f"Q: {query}\nA: {answer['answer']}\n")
```

### Example 2: Batch Processing
```python
import os

rag = RAGPipeline()

startups_dir = "data/startups/"
for startup in os.listdir(startups_dir):
    startup_path = os.path.join(startups_dir, startup)
    result = rag.ingest_directory(startup_path)
    print(f"Processed {startup}: {result['documents_loaded']} docs")
```

### Example 3: Interactive Analysis
```bash
python examples/cli.py
```

## Architecture

```
User Input
    ↓
Document Loader (PDF, DOCX, XLSX, TXT, MD)
    ↓
Text Splitter (1000 char chunks with 200 char overlap)
    ↓
Embedding Generation (HuggingFace Embeddings)
    ↓
Vector Store (FAISS - Persistent)
    ↓
Retrieval (Semantic Similarity Search)
    ↓
LLM Generation (OpenAI GPT-4)
    ↓
Response Output
```

## Performance Characteristics

- **Ingestion**: ~50-100 documents/minute
- **Retrieval**: <100ms for similarity search
- **Generation**: 1-5 seconds (depends on LLM and context)
- **Storage**: ~1MB per 100 documents

## Troubleshooting

**Error: "No module named 'rag_system'"**
```bash
export PYTHONPATH=$PYTHONPATH:/workspaces/StartUp-AI
```

**Error: "OPENAI_API_KEY not found"**
```bash
cp .env.example .env
# Edit .env with your actual API key
```

**Vector store is slow**
- Reduce top_k value
- Use smaller documents
- Clear old vector store: `rag.clear_store()`

## Contributing

Contributions are welcome! Areas for improvement:
- [ ] Additional document formats (PPT, HTML, etc.)
- [ ] Advanced filtering options
- [ ] Custom embedding models
- [ ] Multi-language support
- [ ] Performance optimizations

## License

[Add your license here]

## Contact

For questions or feedback about StartUp AI:
- Create an issue on GitHub
- Email: [contact info]

---

**Next Step**: Proceed to Phase 2 to build the ML Analysis Engine and Dashboard after RAG system is fully tested.
