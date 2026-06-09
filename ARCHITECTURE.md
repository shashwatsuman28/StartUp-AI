"""
                    ╔═════════════════════════════════════════════╗
                    ║   STARTUP AI - RAG SYSTEM ARCHITECTURE      ║
                    ╚═════════════════════════════════════════════╝


┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERACTION LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │   Python API         │  │   Interactive CLI    │  │   Example Scripts │  │
│  │                      │  │                      │  │                   │  │
│  │ from rag_system... │  │  $ python cli.py     │  │  example_usage.py │  │
│  │ rag = RAGPipeline()  │  │                      │  │                   │  │
│  │ rag.ingest_file()    │  │  1. Ingest          │  │  • Copy-paste    │  │
│  │ rag.query()          │  │  2. Query           │  │  • Educational   │  │
│  │ rag.get_summary()    │  │  3. Analyze         │  │  • Template      │  │
│  │                      │  │  4. Statistics      │  │                   │  │
│  └──────────┬───────────┘  └──────────┬──────────┘  └────────────┬──────┘  │
│             │                         │                          │          │
│             └─────────────────────────┼──────────────────────────┘          │
│                                       │                                      │
└───────────────────────────────────────┼──────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RAG PIPELINE (ORCHESTRATOR)                          │
│                      [rag_system/core/rag_pipeline.py]                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  • Ingest Files/Directories                                                 │
│  • Coordinate all components                                                │
│  • Query processing                                                         │
│  • Statistics management                                                    │
│  • Store lifecycle                                                          │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                          │              │              │
            ┌─────────────┼──────────────┼──────────────┘
            │             │              │
            ▼             ▼              ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ DOCUMENT LOADER  │ │ VECTOR STORE     │ │ RETRIEVER        │
│                  │ │                  │ │                  │
│ Multi-Format:    │ │ VectorStore      │ │ Similarity       │
│ • PDF            │ │ Manager          │ │ Search           │
│ • DOCX           │ │ (FAISS)          │ │ • Top-K          │
│ • XLSX           │ │ • Add documents  │ │ • Scoring        │
│ • TXT            │ │ • Save/Load      │ │ • Formatting     │
│ • MD             │ │ • Search         │ │ • Context        │
│                  │ │ • Statistics     │ │                  │
│ ┌──────────────┐ │ │                  │ │ ┌──────────────┐ │
│ │ MultiFormat  │ │ │ ┌──────────────┐ │ │ │ Document     │ │
│ │ DocumentLoader│ │ │ │ HuggingFace  │ │ │ │ Retriever    │ │
│ │              │ │ │ │ Embeddings   │ │ │ │              │ │
│ │ [multi_..    │ │ │ │ all-MiniLM-L6│ │ │ │ [retriever.py│ │
│ │  loader.py]  │ │ │ └──────────────┘ │ │ │              │ │
│ └──────────────┘ │ │ ┌──────────────┐ │ │ └──────────────┘ │
│                  │ │ │ FAISS Index  │ │ │                  │
│ Documents output:│ │ │ Vector Store │ │ │ Returns:         │
│ - page_content  │ │ │ (Persistent) │ │ │ - Top-K docs    │
│ - metadata      │ │ │              │ │ │ - Scores        │
│ - source        │ │ │ [vector_     │ │ │ - Formatted ctx │
│                  │ │ │  store_...   │ │ │                  │
│                  │ │ │  py]         │ │ │                  │
│                  │ │ └──────────────┘ │ │                  │
│                  │ │                  │ │                  │
│                  │ │ data/vector_store│ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                            │
                ┌───────────┼───────────┐
                │                       │
            ┌───▼──────────────────────▼──┐
            │   TEXT SPLITTER              │
            │   (TextSplitter)             │
            │                              │
            │ • RecursiveCharacter split  │
            │ • Chunk size: 1000 chars    │
            │ • Overlap: 200 chars        │
            │ • Semantic boundaries       │
            │                              │
            │ [text_splitter.py]          │
            └────────────────────────────┘
                           │
                           │ Split Chunks
                           ▼
                ┌──────────────────────┐
                │  EMBEDDING & VECTOR  │
                │  STORAGE             │
                │                      │
                │ HuggingFace Embedder │
                │ ↓                    │
                │ FAISS Index          │
                │ ↓                    │
                │ Vector Store         │
                │ (data/vector_store/) │
                └──────────────────────┘
                           │
                           │ Similarity Search
                           ▼
            ┌──────────────────────────────┐
            │   RESPONSE GENERATOR         │
            │   (RAG Generator)            │
            │                              │
            │ LLM-Powered Analysis:       │
            │ • Q&A with documents        │
            │ • Summarization             │
            │ • Concept extraction        │
            │ • Context synthesis         │
            │                              │
            │ ┌──────────────────────┐    │
            │ │ OpenAI GPT-4 Turbo  │    │
            │ │                      │    │
            │ │ - Temperature: 0.7  │    │
            │ │ - Max tokens: 2000  │    │
            │ │ - Context-aware     │    │
            │ └──────────────────────┘    │
            │                              │
            │ [rag_generator.py]          │
            └──────────┬───────────────────┘
                       │
                       │ Analysis Result
                       ▼
        ┌──────────────────────────────┐
        │   RESPONSE FORMATTING        │
        │                              │
        │ • Answer/Analysis            │
        │ • Summary                    │
        │ • Concepts                   │
        │ • Metadata                   │
        │ • Status indicators          │
        └──────────┬───────────────────┘
                   │
                   │ Final Output
                   ▼
        ┌──────────────────────────────┐
        │   USER RESPONSE              │
        │                              │
        │ Dict with:                   │
        │ - status                     │
        │ - answer/analysis            │
        │ - metadata                   │
        │ - error (if any)             │
        └──────────────────────────────┘


═════════════════════════════════════════════════════════════════════════════

DATA FLOW EXAMPLE:

User Query: "What is the startup's business model?"
    │
    └─→ RAGPipeline.query()
         │
         ├─→ DocumentRetriever.retrieve()
         │    │
         │    └─→ VectorStore.similarity_search()
         │         │
         │         └─→ Returns Top-5 matching documents
         │
         ├─→ Format context
         │
         └─→ RAGGenerator.analyze()
              │
              ├─→ OpenAI GPT-4
              │    │
              │    └─→ "Based on the documents, the business model..."
              │
              └─→ Return formatted answer


═════════════════════════════════════════════════════════════════════════════

COMPONENT INTERACTION MATRIX:

                  │ Loader │ Splitter │ VectorStore │ Retriever │ Generator
              ────┼────────┼──────────┼─────────────┼───────────┼──────────
  Loader        │   -    │    ✓     │      -      │     -     │    -
  Splitter      │    -   │    -     │      ✓      │     -     │    -
  VectorStore   │    -   │    -     │      -      │     ✓     │    -
  Retriever     │    -   │    -     │      ✓      │     -     │    ✓
  Generator     │    -   │    -     │      -      │     ✓     │    -


═════════════════════════════════════════════════════════════════════════════

CONFIGURATION HIERARCHY:

settings.py (rag_system/config/settings.py)
    │
    ├─→ RAG_CONFIG
    │   ├─ chunk_size: 1000
    │   ├─ chunk_overlap: 200
    │   ├─ embedding_model
    │   └─ retrieval_top_k: 5
    │
    ├─→ LLM_CONFIG
    │   ├─ model: "gpt-4-turbo"
    │   ├─ temperature: 0.7
    │   └─ max_tokens: 2000
    │
    ├─→ SUPPORTED_FILE_TYPES
    │   ├─ pdf, docx, xlsx, txt, md
    │
    └─→ VECTOR_STORE_SETTINGS
        └─ persist_directory


═════════════════════════════════════════════════════════════════════════════

EXECUTION SEQUENCE:

1️⃣  INITIALIZATION
    RAGPipeline() → Initialize all components

2️⃣  DOCUMENT INGESTION
    ingest_file/ingest_directory() → Load documents

3️⃣  PROCESSING
    MultiFormatDocumentLoader → Extracts content

4️⃣  CHUNKING
    TextSplitter → Creates overlapping chunks

5️⃣  EMBEDDING
    HuggingFace embeddings → Vector representations

6️⃣  STORAGE
    FAISS vector store → Saves embeddings

7️⃣  QUERYING
    similarity_search() → Retrieves top-K documents

8️⃣  CONTEXT FORMATTING
    format_retrieval_context() → Prepares for LLM

9️⃣  GENERATION
    OpenAI GPT-4 → Generates response

🔟 RESPONSE
    Return formatted answer with metadata


═════════════════════════════════════════════════════════════════════════════

KEY PERFORMANCE METRICS:

⏱️  Document Loading:      <5 seconds per document
⏱️  Embedding Generation:  <10 seconds per 10 chunks
⏱️  Vector Storage:        <100 milliseconds per add
⏱️  Similarity Search:     <100 milliseconds per query
⏱️  LLM Response:          1-5 seconds (depends on token count)

📦 Storage Footprint:
    • Empty index:        ~1 MB
    • Per 100 documents:  ~2-5 MB
    • Per 1000 documents: ~20-50 MB


═════════════════════════════════════════════════════════════════════════════

ERROR HANDLING:

┌─ DOCUMENT LOADING
│  ├─ File not found → Custom FileNotFoundError
│  ├─ Unsupported format → ValueError
│  └─ Parse error → Logged and reported
│
├─ EMBEDDING
│  ├─ Model not found → Auto-download from HuggingFace
│  └─ OOM → Reduce chunk size
│
├─ VECTOR STORAGE
│  ├─ Persistence error → Logged warning
│  └─ Corruption → Automatic rebuild
│
├─ RETRIEVAL
│  ├─ Empty store → Returns empty list
│  └─ Search error → Logged and reported
│
└─ GENERATION
   ├─ API key missing → Clear error message
   ├─ API error → Caught and reported
   └─ Context too long → Auto-truncation


═════════════════════════════════════════════════════════════════════════════

NEXT PHASE: ANALYSIS ENGINE

Current: ✅ RAG System
Next:    📊 ML Analysis Models
         📈 Dashboard
         🔐 Full Application
"""
