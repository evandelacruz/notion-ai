#!/usr/bin/env python3

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from indexer.meilisearch_client import SearchIndexer
from config.config import config

def main():
    try:
        print("Initializing indexer...")
        indexer = SearchIndexer(config.MEILISEARCH_HOST, config.MEILISEARCH_KEY)
        
        print("Clearing and recreating index...")
        if indexer.clear_index():
            print("Successfully cleared and recreated index!")
            sys.exit(0)
        else:
            print("Failed to clear and recreate index.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
