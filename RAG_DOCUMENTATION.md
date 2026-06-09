# RAG System Documentation

## Overview

The RAG (Retrieval-Augmented Generation) system is the foundation of StartUp AI, designed to:
- **Ingest** documents from multiple file formats (PDF, DOCX, XLSX, TXT, MD)
- **Understand** concepts and ideas in the documents
- **Retrieve** relevant information based on queries
- **Generate** intelligent responses using LLMs

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐   ┌────────────┐   │
│  │   Document   │      │   Text       │   │ Embedding  │   │
│  │   Loader     │ ──→  │   Splitter   │──→│ Generation │   │
│  │              │      │              │   │            │   │
│  │ • PDF        │      │ • Chunks     │   │ • HuggingFace  │
│  │ • DOCX       │      │ • Metadata   │   │ • Vectors  │   │
│  │ • XLSX       │      │              │   │            │   │
│  │ • TXT, MD    │      └──────────────┘   └────────────┘   │
│  └──────────────┘                                 │           │
│                                                   ▼           │
│                                         ┌──────────────────┐ │
│                                         │ Vector Store     │ │
│                                         │ (FAISS)          │ │
│                                         │ • Persistence    │ │
│                                         │ • Similarity     │ │
│                                         └──────────────────┘ │
│                                                   │           │
│                    ┌──────────────────────────────┘           │
│                    │                                          │
│            ┌───────▼────────┐        ┌─────────────┐        │
│            │  Retriever     │        │ RAG Gen.    │        │
│            │                │   ───→ │ (GPT-4)     │        │
│            │ • Query        │        │             │        │
│            │ • Top-K Search │        │ • Analysis  │        │
│            └────────────────┘        │ • Summary   │        │
│                                      │ • Concepts  │        │
│                                      └─────────────┘        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
rag_system/
├── config/
│   └── settings.py          # Configuration constants
├── loaders/
│   ├── __init__.py
│   └── multi_format_loader.py  # Multi-format document loader
├── utils/
│   ├── __init__.py
│   └── text_splitter.py     # Text chunking utilities
├── vectorstore/
│   ├── __init__.py
│   └── vector_store_manager.py  # Vector store management
├── retrievers/
│   ├── __init__.py
│   └── retriever.py         # Document retriever
├── generators/
│   ├── __init__.py
│   └── rag_generator.py     # LLM-based response generation
└── core/
    ├── __init__.py
    └── rag_pipeline.py      # Main RAG pipeline orchestrator
```

## Features

### 1. Multi-Format Document Ingestion
- **PDF Files**: Extracts text from PDF documents
- **Word Documents**: Reads .docx and .doc files
- **Excel Files**: Processes spreadsheets (converts to text)
- **Text Files**: Handles .txt and .md files
- **Automatic Chunking**: Splits large documents into manageable chunks

### 2. Vector Embeddings
- Uses HuggingFace embeddings (all-MiniLM-L6-v2 by default)
- FAISS for efficient similarity search
- Persistent vector store for quick retrieval

### 3. Intelligent Retrieval
- Semantic similarity search
- Top-K document retrieval
- Score-based ranking
- Metadata filtering

### 4. Response Generation
- OpenAI GPT-4 integration
- Context-aware analysis
- Automatic summarization
- Concept extraction

## Installation

### 1. Clone and setup
```bash
cd /workspaces/StartUp-AI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_key_here
```

### 3. Prepare sample documents
```bash
# Place your startup documents in:
data/uploads/
```

## Quick Start

### Using the Python API

```python
from rag_system.core import RAGPipeline

# Initialize
rag = RAGPipeline()

# Ingest documents
result = rag.ingest_file("data/uploads/business_plan.pdf")
print(f"Ingested: {result['documents_loaded']} documents")

# Query the system
answer = rag.query("What is the startup's business model?")
print(answer['answer'])

# Get analysis
summary = rag.get_summary()
print(summary['summary'])

concepts = rag.get_concepts()
print(concepts['concepts'])
```

### Using the CLI

```bash
python examples/cli.py
```

Follow the interactive menu to:
1. Ingest files or directories
2. Query documents
3. Generate summaries
4. Extract concepts
5. View statistics

### Run Example Script

```bash
python examples/example_usage.py
```

## Core Components

### RAGPipeline
Main orchestrator that manages all components.

**Methods:**
- `ingest_file(file_path)` - Ingest a single file
- `ingest_directory(dir_path)` - Ingest all files in directory
- `query(question, top_k)` - Ask a question
- `get_summary()` - Get document summary
- `get_concepts()` - Extract key concepts
- `get_stats()` - Get system statistics
- `clear_store()` - Clear vector store

### MultiFormatDocumentLoader
Loads documents from various file formats.

**Supported formats:**
- PDF, DOCX, DOC, XLSX, XLS, TXT, MD

### TextSplitter
Splits documents into optimized chunks.

**Default settings:**
- Chunk size: 1000 characters
- Overlap: 200 characters

### VectorStoreManager
Manages embeddings and vector storage.

**Features:**
- Add/retrieve documents
- Similarity search with scores
- Persistent storage
- Statistics

### DocumentRetriever
Retrieves relevant documents for queries.

**Methods:**
- `retrieve(query, top_k)` - Get documents
- `retrieve_with_scores(query, top_k)` - Get with scores
- `format_retrieval_context(documents)` - Format for LLM

### RAGGenerator
Generates responses using LLM.

**Methods:**
- `analyze(query, top_k)` - Answer a question
- `extract_concepts(top_k)` - Extract key concepts
- `summarize(top_k)` - Summarize documents

## Configuration

Edit `rag_system/config/settings.py` to customize:

```python
RAG_CONFIG = {
    "chunk_size": 1000,           # Character size of chunks
    "chunk_overlap": 200,          # Character overlap between chunks
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "vector_store_type": "faiss",
    "retrieval_top_k": 5,         # Number of docs to retrieve
}

LLM_CONFIG = {
    "model": "gpt-4-turbo",       # OpenAI model
    "temperature": 0.7,            # Response creativity (0-1)
    "max_tokens": 2000,
}
```

## Example Workflows

### Workflow 1: Basic Document Analysis

```python
rag = RAGPipeline()

# 1. Ingest startup documents
rag.ingest_directory("startup_docs/")

# 2. Get overview
summary = rag.get_summary()
print("Startup Overview:", summary['summary'])

# 3. Extract concepts
concepts = rag.get_concepts()
print("Key Concepts:", concepts['concepts'])
```

### Workflow 2: Specific Queries

```python
rag = RAGPipeline()
rag.ingest_file("business_plan.pdf")

# Ask specific questions
queries = [
    "What is the target market?",
    "What are the revenue streams?",
    "Who are the competitors?",
    "What is the competitive advantage?",
]

for query in queries:
    result = rag.query(query)
    print(f"Q: {query}")
    print(f"A: {result['answer']}\n")
```

### Workflow 3: Batch Processing

```python
import os
from pathlib import Path

rag = RAGPipeline()

# Process all documents in startup data
startup_dir = "data/startups/startup_name/"
result = rag.ingest_directory(startup_dir)

print(f"Processed {result['documents_loaded']} documents")
print(f"Created {result['chunks_created']} chunks")
```

## Performance Tips

1. **Chunk Size**: Increase for longer context, decrease for precision
2. **Top-K**: Use 3-5 for specific queries, 10-15 for broad analysis
3. **Embedding Model**: all-MiniLM-L6-v2 is fast; use larger models for accuracy
4. **Temperature**: Lower (0.3) for factual, higher (0.8) for creative

## Error Handling

The system includes robust error handling:

```python
result = rag.ingest_file("document.pdf")
if result['status'] == 'error':
    print(f"Error: {result['error']}")
else:
    print(f"Successfully ingested {result['documents_loaded']} documents")
```

## Next Steps (Future Features)

- [ ] Dashboard for visualization
- [ ] ML model for document analysis/scoring
- [ ] Advanced filtering and metadata queries
- [ ] Multi-language support
- [ ] Real-time streaming responses
- [ ] Document versioning and updates
- [ ] Custom embedding models
- [ ] Fine-tuned LLMs for startup analysis

## Troubleshooting

**Issue: "No module named 'rag_system'"**
- Add project root to PYTHONPATH: `export PYTHONPATH=$PYTHONPATH:/workspaces/StartUp-AI`

**Issue: "OPENAI_API_KEY not set"**
- Create `.env` file with your API key
- Or pass `openai_api_key` to RAGPipeline()

**Issue: Slow similarity search**
- Reduce top_k value
- Use smaller embedding model
- Check vector store size

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [HuggingFace Models](https://huggingface.co/models)
