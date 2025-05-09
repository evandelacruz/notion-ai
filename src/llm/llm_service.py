from typing import List, Dict, Optional
from ..indexer.meilisearch_client import SearchIndexer
from .llm_client import LLMClient, OpenAIClient
from ..config.config import config

class LLMService:
    def __init__(self, search_indexer: SearchIndexer, llm_client: Optional[LLMClient] = None):
        self.search_indexer = search_indexer
        self.llm_client = llm_client or OpenAIClient(api_key=config.OPENAI_API_KEY)

    def get_context_for_llm(self, query: str, max_context_length: int = 40000) -> str:
        """Get relevant context from MeiliSearch for the LLM."""

        #translate the query into searchable terms
        terms = self.llm_client.generate(prompt=f"Note that your output will be consumed by a machine. You must only return the requested data as a csv or list, without any comentary whatsoever.Translate the following query into searchable terms prioritizing words will yield results that get to the heart of what is being asked: {query}")
        # Get more results than needed to ensure we have enough content
        results = self.search_indexer.search(terms, limit=5)
        context = []
        current_length = 0
        for hit in results['hits']:
            content = hit['content']

            if current_length + len(content) > max_context_length:
                break
                
            context.append(content)
            current_length += len(content)
        
        return "\n\n---\n\n".join(context)

    def generate_response(self, user_prompt: str, max_context_length: int = 40000, **kwargs) -> str:
        """Generate a response using the LLM with context from MeiliSearch."""
        # Get relevant context from MeiliSearch
        context = self.get_context_for_llm(user_prompt, max_context_length)
        # Format the prompt with context
        prompt = f"""Context from knowledge base:
{context}

User question: {user_prompt}

Please answer the question based on the context provided above. If the context doesn't contain enough information to answer the question, please say so."""
        
        # Generate response using the LLM client
        return self.llm_client.generate(prompt, **kwargs) 