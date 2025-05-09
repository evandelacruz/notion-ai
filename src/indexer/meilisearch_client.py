from meilisearch import Client

class SearchIndexer:
    def __init__(self, host: str, api_key: str):
        self.client = Client(host, api_key)
        self.index_name = "notion_pages"

    def configure_search_settings(self):
        """Configure search settings for better relevancy."""
        try:
            index = self.client.index(self.index_name)
            
            # Update settings
            index.update_settings({
                # Add common English stop words
                'stopWords': [
                    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                    'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
                ],
                
                # Configure typo tolerance
                'typoTolerance': {
                    'enabled': True,
                    'minWordSizeForTypos': {
                        'oneTypo': 5,    # Words must be at least 5 chars for 1 typo
                        'twoTypos': 9    # Words must be at least 9 chars for 2 typos
                    },
                    'disableOnWords': [], # Add specific words where typos should be disabled
                    'disableOnAttributes': [] # Add attributes where typos should be disabled
                },                
                # Customize ranking rules if needed
                'rankingRules': [
                    'words',
                    'typo',
                    'proximity',
                    'attribute',
                    'exactness'
                ],
                
                # Maybe add synonyms for common terms in your domain
                'synonyms': {
                    'api': ['endpoint', 'service'],
                    'database': ['db', 'storage']
                },
                
                # Configure searchable attributes
                'searchableAttributes': [
                    'title^2',
                    'content',
                    'hierarchy'
                ]
            })
            print("Search settings updated successfully")
            return True
        except Exception as e:
            print(f"Error updating search settings: {e}")
            return False

    def index_pages(self, pages):
        try:
            # Add documents and wait for the operation to complete
            task = self.client.index(self.index_name).add_documents(pages)
            # Check if documents were actually indexed
            stats = self.client.index(self.index_name).get_stats()
            print(f"Number of documents: {stats.number_of_documents}")
            return True
        except Exception as e:
            print(f"Error during indexing: {e}")
            return False

    def search(self, query: str, limit: int = 10):
        return self.client.index(self.index_name).search(query, {"limit": limit}) 
    
    def clear_index(self):
        try:
            # Delete the existing index
            self.client.index(self.index_name).delete()
            print("Index deleted successfully")
            
            # Create a new index
            self.client.create_index(self.index_name)
            print("Index recreated successfully")
            
            # Apply search settings to the new index
            self.configure_search_settings()
            
            return True
        except Exception as e:
            print(f"Error clearing and recreating index: {e}")
            return False