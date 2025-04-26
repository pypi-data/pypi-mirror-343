import os
from concurrent.futures import ThreadPoolExecutor
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

from .config import DEFAULT_MODELS
from .document_loader import load_documents, chunk_documents
from .llm_interface import LLMInterface
from .response_ranker import ResponseRanker
from .aggregator import aggregate_responses
from .utils import format_documents

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class MetaRAG:
    def __init__(self, document_paths, models=None):
        self.models = models or DEFAULT_MODELS
        self.llm_interface = LLMInterface(self.models)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = self._create_vectorstore(document_paths)
        self.retrieval_prompt = PromptTemplate.from_template(
            """Answer the question based solely on the following context:

{context}

Question: {question}

Answer:""" 
        )
        self.rank = ResponseRanker(self.embeddings)

    def _create_vectorstore(self, paths):
        docs = load_documents(paths)
        if not docs:
            raise ValueError("No documents loaded.")
        chunks = chunk_documents(docs)
        return FAISS.from_documents(chunks, self.embeddings)

    def _get_context(self, query, k=5):
        docs = self.vectorstore.similarity_search(query, k)
        return docs, format_documents(docs)

    def query(self, query, k=5):
        """Main method that handles querying and returns detailed results."""
        docs, context = self._get_context(query, k)
        prompt = self.retrieval_prompt.format(context=context, question=query)

        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = {
                executor.submit(self.llm_interface.query_model, model, prompt): model
                for model in self.models
            }
            responses = [
                {"model": model, "response": future.result()} for future, model in futures.items()
            ]

        top = self.rank.score(context, responses)
        agg = aggregate_responses(top)

        return {
            "query": query,
            "aggregated_response": agg,
            "model_responses": responses,
            "top_model_responses": top,
            "retrieved_documents": [d.page_content for d in docs]
        }

    def run(self, query, k=5):
        """Simplified method to just return the final aggregated response."""
        result = self.query(query, k)
        return result["aggregated_response"]  # Return only the aggregated response
import os
from concurrent.futures import ThreadPoolExecutor
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

from .config import DEFAULT_MODELS
from .document_loader import load_documents, chunk_documents
from .llm_interface import LLMInterface
from .response_ranker import ResponseRanker
from .aggregator import aggregate_responses
from .utils import format_documents

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class MetaRAG:
    def __init__(self, document_paths, models=None):
        self.models = models or DEFAULT_MODELS
        self.llm_interface = LLMInterface(self.models)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = self._create_vectorstore(document_paths)
        self.retrieval_prompt = PromptTemplate.from_template(
            """Answer the question based solely on the following context:

{context}

Question: {question}

Answer:""" 
        )
        self.rank = ResponseRanker(self.embeddings)

    def _create_vectorstore(self, paths):
        docs = load_documents(paths)
        if not docs:
            raise ValueError("No documents loaded.")
        chunks = chunk_documents(docs)
        return FAISS.from_documents(chunks, self.embeddings)

    def _get_context(self, query, k=5):
        docs = self.vectorstore.similarity_search(query, k)
        return docs, format_documents(docs)

    def query(self, query, k=5):
        """Main method that handles querying and returns detailed results."""
        docs, context = self._get_context(query, k)
        prompt = self.retrieval_prompt.format(context=context, question=query)

        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = {
                executor.submit(self.llm_interface.query_model, model, prompt): model
                for model in self.models
            }
            responses = [
                {"model": model, "response": future.result()} for future, model in futures.items()
            ]

        top = self.rank.score(context, responses)
        agg = aggregate_responses(top)

        return {
            "query": query,
            "aggregated_response": agg,
            "model_responses": responses,
            "top_model_responses": top,
            "retrieved_documents": [d.page_content for d in docs]
        }

    def run(self, query, k=5):
        """Simplified method to just return the final aggregated response."""
        result = self.query(query, k)
        return result["aggregated_response"]  # Return only the aggregated response
import os
from concurrent.futures import ThreadPoolExecutor
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

from .config import DEFAULT_MODELS
from .document_loader import load_documents, chunk_documents
from .llm_interface import LLMInterface
from .response_ranker import ResponseRanker
from .aggregator import aggregate_responses
from .utils import format_documents

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class MetaRAG:
    def __init__(self, document_paths, models=None):
        self.models = models or DEFAULT_MODELS
        self.llm_interface = LLMInterface(self.models)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = self._create_vectorstore(document_paths)
        self.retrieval_prompt = PromptTemplate.from_template(
            """Answer the question based solely on the following context:

{context}

Question: {question}

Answer:""" 
        )
        self.rank = ResponseRanker(self.embeddings)

    def _create_vectorstore(self, paths):
        docs = load_documents(paths)
        if not docs:
            raise ValueError("No documents loaded.")
        chunks = chunk_documents(docs)
        return FAISS.from_documents(chunks, self.embeddings)

    def _get_context(self, query, k=5):
        docs = self.vectorstore.similarity_search(query, k)
        return docs, format_documents(docs)

    def query(self, query, k=5):
        """Main method that handles querying and returns detailed results."""
        docs, context = self._get_context(query, k)
        prompt = self.retrieval_prompt.format(context=context, question=query)

        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = {
                executor.submit(self.llm_interface.query_model, model, prompt): model
                for model in self.models
            }
            responses = [
                {"model": model, "response": future.result()} for future, model in futures.items()
            ]

        top = self.rank.score(context, responses)
        agg = aggregate_responses(top)

        return {
            "query": query,
            "aggregated_response": agg,
            "model_responses": responses,
            "top_model_responses": top,
            "retrieved_documents": [d.page_content for d in docs]
        }

    def run(self, query, k=5):
        """Simplified method to just return the final aggregated response."""
        result = self.query(query, k)
        return result["aggregated_response"]  # Return only the aggregated response
