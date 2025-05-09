from abc import ABC, abstractmethod
from typing import Optional
import os
from openai import OpenAI

class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass

class OpenAIClient(LLMClient):
    """OpenAI ChatGPT implementation of LLMClient."""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """Initialize the OpenAI client.
        
        Args:
            model: The model to use (e.g., "gpt-3.5-turbo", "gpt-4")
            api_key: Optional API key. If not provided, will use OPENAI_API_KEY env var.
        """
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response using OpenAI's API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"