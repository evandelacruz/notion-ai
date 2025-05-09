import time
import logging
from datetime import datetime
from ..config.config import config
from ..notion.client import NotionClient
from ..indexer.meilisearch_client import SearchIndexer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self):
        self.notion_client = NotionClient(config.NOTION_API_KEY)
        self.indexer = SearchIndexer(config.MEILISEARCH_HOST, config.MEILISEARCH_KEY)
        self.sync_interval = config.SYNC_INTERVAL_MINUTES * 60  # Convert to seconds
        # Configure search settings
        self.indexer.configure_search_settings()

    def sync(self):
        """Perform a single sync operation."""
        try:
            logger.info("Starting sync operation...")
            
            # Fetch pages from Notion
            logger.info("Fetching pages from Notion...")
            added_count = self.notion_client.fetch_and_index_all_pages(self.indexer.index_pages)
            logger.info(f"Added {added_count} pages to the index")
            
            # Index the pages
            # logger.info(f"Found {len(pages)} pages. Indexing...")
            # success = self.indexer.index_pages(pages)
            
            logger.info("Sync completed successfully!")
            return True
        except Exception as e:
            logger.error(f"Error during sync: {e}")
            return False

    def run_continuous_sync(self):
        """Run sync operations continuously with the configured interval."""
        logger.info(f"Starting continuous sync service (interval: {config.SYNC_INTERVAL_MINUTES} minutes)")
        
        while True:
            try:
                self.sync()
            except Exception as e:
                logger.error(f"Error in sync loop: {e}")
            
            # Wait for the next sync interval
            time.sleep(self.sync_interval)

if __name__ == "__main__":
    service = SyncService()
    service.run_continuous_sync() 