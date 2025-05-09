from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    MEILISEARCH_HOST = os.getenv("MEILISEARCH_HOST", "http://localhost:7700")
    MEILISEARCH_KEY = os.getenv("MEILISEARCH_KEY")
    SYNC_INTERVAL_MINUTES = int(os.getenv("SYNC_INTERVAL_MINUTES", "60"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = Config()
