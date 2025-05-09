import sys
import os
import argparse

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.indexer.meilisearch_client import SearchIndexer
from src.llm.llm_service import LLMService
from src.llm.llm_client import OpenAIClient
from src.config.config import config

def main():
    parser = argparse.ArgumentParser(description='Query your Notion knowledge base using LLM')
    parser.add_argument('prompt', nargs='?', help='The question to ask. If not provided, will read from stdin.')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='OpenAI model to use')
    parser.add_argument('--max-context', type=int, default=40000, help='Maximum context length in characters')
    parser.add_argument('--temperature', type=float, default=0.7, help='Temperature for LLM generation')
    
    args = parser.parse_args()
    
    search_indexer = SearchIndexer(host=config.MEILISEARCH_HOST, api_key=config.MEILISEARCH_KEY)
    search_indexer.configure_search_settings()
    llm_service = LLMService(
        search_indexer=search_indexer,
        llm_client=OpenAIClient(
            model=args.model,
            api_key=config.OPENAI_API_KEY
        )
    )

    # Interactive loop
    try:
        while True:
            # Get prompt from args (only first time) or input
            if args.prompt:
                prompt = args.prompt
                args.prompt = None  # Clear it after first use
            else:
                print("\nEnter your question (press Ctrl+C to exit):")
                prompt = input("> ").strip()

            if not prompt:
                print("Please enter a question")
                continue

            # Generate response
            try:
                response = llm_service.generate_response(
                    prompt,
                    max_context_length=args.max_context,
                    temperature=args.temperature
                )
                print("\nResponse:")
                print(response)
            except Exception as e:
                print(f"Error: {str(e)}", file=sys.stderr)
                continue

    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()