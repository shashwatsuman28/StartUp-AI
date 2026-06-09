"""RAG generator - combines retrieval with generation"""

import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from rag_system.retrievers import DocumentRetriever

logger = logging.getLogger(__name__)


class RAGGenerator:
    """
    Generates responses by combining document retrieval with LLM generation.
    Implements the full RAG pipeline.
    """

    def __init__(
        self,
        retriever: DocumentRetriever,
        model_name: str = "gpt-4-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None,
    ):
        """
        Initialize RAG generator.

        Args:
            retriever: DocumentRetriever instance
            model_name: OpenAI model to use
            temperature: Temperature for generation
            api_key: OpenAI API key
        """
        self.retriever = retriever
        self.model_name = model_name
        self.temperature = temperature

        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=api_key,
        )

        self._setup_prompts()

    def _setup_prompts(self):
        """Setup prompt templates"""

        # Analysis prompt for startup documents
        self.analysis_prompt = PromptTemplate(
            input_variables=["context", "query"],
            template="""You are an expert startup analyst. Based on the following documents about a startup:

{context}

Please answer the following question: {query}

Provide a detailed analysis based on the provided documents. If the documents don't contain relevant information, clearly state that.""",
        )

        # Concept extraction prompt
        self.concept_prompt = PromptTemplate(
            input_variables=["context"],
            template="""You are an expert at understanding business concepts. Extract and explain the key concepts and ideas from the following documents:

{context}

List the main concepts with brief explanations. Focus on business model, value proposition, market opportunity, and competitive advantages.""",
        )

        # Summary prompt
        self.summary_prompt = PromptTemplate(
            input_variables=["context"],
            template="""Summarize the following documents about a startup in a concise manner:

{context}

Provide a brief executive summary (2-3 paragraphs) capturing the key points.""",
        )

    def analyze(self, query: str, top_k: int = 5) -> dict:
        """
        Analyze documents and answer a query.

        Args:
            query: Query to answer
            top_k: Number of documents to retrieve

        Returns:
            Dict with analysis results
        """
        try:
            # Retrieve relevant documents
            context = self.retriever.retrieve_and_format(query, top_k=top_k)

            if not context.strip():
                return {
                    "status": "no_context",
                    "query": query,
                    "answer": "No relevant documents found.",
                }

            # Create chain and run
            chain = LLMChain(llm=self.llm, prompt=self.analysis_prompt)
            answer = chain.run(context=context, query=query)

            return {
                "status": "success",
                "query": query,
                "answer": answer,
                "context_documents": top_k,
            }

        except Exception as e:
            logger.error(f"Error in analyze: {str(e)}")
            return {
                "status": "error",
                "query": query,
                "error": str(e),
            }

    def extract_concepts(self, top_k: int = 10) -> dict:
        """
        Extract key concepts from all documents.

        Args:
            top_k: Number of documents to process

        Returns:
            Dict with extracted concepts
        """
        try:
            # Retrieve all documents
            documents = self.retriever.retrieve("startup business model", top_k=top_k)
            context = self.retriever.format_retrieval_context(documents)

            if not context.strip():
                return {
                    "status": "no_context",
                    "concepts": [],
                }

            # Create chain and run
            chain = LLMChain(llm=self.llm, prompt=self.concept_prompt)
            concepts = chain.run(context=context)

            return {
                "status": "success",
                "concepts": concepts,
                "documents_processed": len(documents),
            }

        except Exception as e:
            logger.error(f"Error in extract_concepts: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }

    def summarize(self, top_k: int = 10) -> dict:
        """
        Generate summary of documents.

        Args:
            top_k: Number of documents to summarize

        Returns:
            Dict with summary
        """
        try:
            documents = self.retriever.retrieve("summary overview", top_k=top_k)
            context = self.retriever.format_retrieval_context(documents)

            if not context.strip():
                return {
                    "status": "no_context",
                    "summary": "",
                }

            chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
            summary = chain.run(context=context)

            return {
                "status": "success",
                "summary": summary,
                "documents_processed": len(documents),
            }

        except Exception as e:
            logger.error(f"Error in summarize: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }
