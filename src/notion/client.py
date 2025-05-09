from notion_client import Client
from notion_client.helpers import iterate_paginated_api
from notion_client.helpers import is_full_page
import traceback

class NotionClient:
    def __init__(self, api_key: str):
        self.client = Client(auth=api_key)
        self._page_cache = {}  # Cache to store page titles by ID

    def _get_page(self, page_id: str) -> object:

        try:
            if page_id not in self._page_cache:
                self._page_cache[page_id] = self.client.pages.retrieve(page_id=page_id)
            return self._page_cache[page_id]
        except Exception as e:
            print(f"Error fetching page for {page_id}: {e}")
            return "Unknown Page"

    def _get_page_hierarchy(self, page: object) -> list:
        """Recursively get the hierarchy path for a page."""
        hierarchy = []
        current_page = page
        while current_page:
            try:
                title = self._get_page_name(current_page)
                hierarchy.insert(0, title)  # Add to beginning of list
                
                # Check if page has a parent
                if "parent" in current_page and current_page["parent"]["type"] == "page_id":
                    current_page = self._get_page(current_page["parent"]["page_id"])
                else:
                    current_page = None
            except Exception as e:
                print(f"Error fetching hierarchy for {current_page['id']}: {e}")
                print("Full traceback:")
                traceback.print_exc()
                break
        
        return hierarchy

    def fetch_and_index_all_pages(self, index_pages_callback):
        try:
            added_count = 0
            for page in iterate_paginated_api(self.client.search):
                print(f"\nPage {page['id']}:")                
                if not is_full_page(page):
                    print("Skipping page {page['id']} - not a full page")
                    continue
                if "parent" in page and page["parent"]["type"] == "database_id":
                    print("Skipping page {page['id']} - parent is a database")
                    continue
                # Get page content
                try:
                    content = self._get_page_content(page)
                    page_name = self._get_page_name(page)
                    hierarchy = self._get_page_hierarchy(page)

                    doc = {
                        "id": page["id"],
                        "title": page_name,
                        "content": "\n".join(content),
                        "url": page["url"],
                        "hierarchy": " > ".join(hierarchy)  # Join hierarchy with arrows
                    }
                except Exception as e:
                    print(f"Error fetching content for page {page['id']}: {e}")
                    continue
                # Extract nested plain_text from rich_text array
                index_pages_callback([doc])
                added_count += 1
            return added_count
        except Exception as e:
            print(f"Error fetching Notion pages: {e}")
            print("Full traceback:")
            traceback.print_exc()
            raise

    def _get_page_content(self, page):
        try:
            blocks = self.client.blocks.children.list(block_id=page["id"])
            # Extract nested plain_text from rich_text array
            content = []
            for block in blocks["results"]:
                for key, value in block.items():
                    if isinstance(value, dict) and "rich_text" in value:
                        for text in value["rich_text"]:
                            content.append(text["plain_text"])
            # Skip pages with empty content
            if not content:
                print(f"Page {page['id']} - no content found")
            
            return content
        except Exception as e:
            print(f"Error fetching Notion page contents: {e}")
            raise

    def _get_page_name(self, page):
        try:
            if "properties" not in page:
                print(f"Page {page['id']} - no properties found")
                page_name = "unknown"
            elif "Page" in page["properties"]:
                page_name = page["properties"]["Page"]["title"][0]["plain_text"]
            elif "title" in page["properties"]:
                page_name = page["properties"]["title"]["title"][0]["plain_text"]
            elif "Name" in page["properties"]:
                page_name = page["properties"]["Name"]["title"][0]["plain_text"]               # Get page hierarch
            else:
                print(page)
                print("Cannot find page name")
                page_name = "unknown"
            return page_name
        except Exception as e:
            print(f"Error getting Notion page name: {e}")
            raise