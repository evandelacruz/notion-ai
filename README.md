# Notion Page Indexer

A Python service that indexes Notion pages in a local MeiliSearch instance for fast, local search capabilities.

## Features

- Fetches all pages from a Notion workspace
- Indexes content in a local MeiliSearch instance
- Continuous sync with configurable interval
- Smart content extraction including headings and paragraphs
- Parent-child page relationship tracking
- LLM-powered question answering using indexed content

## Prerequisites

1. Python 3.8+
2. MeiliSearch installed locally
3. Notion API key with access to your workspace
4. OpenAI API key (for LLM functionality)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd trr-notion-index
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install MeiliSearch:
- Download from [MeiliSearch website](https://www.meilisearch.com/download)
- Start the server:
```bash
./meilisearch --master-key your_master_key_here
```

5. Create a `.env` file with your configuration:
```plaintext
NOTION_API_KEY=your_notion_api_key_here
NOTION_WORKSPACE_ID=your_workspace_id_here
MEILISEARCH_HOST=http://localhost:7700
MEILISEARCH_KEY=your_master_key_here
OPENAI_API_KEY=your_openai_api_key_here
SYNC_INTERVAL_MINUTES=60
```

## Usage

1. Start the sync service to index your Notion pages:
```bash
python -m src.sync.sync_service
```

2. Query your knowledge base using the CLI:
```bash
# Using command line argument
python -m src.cli "What is the company's policy on remote work?"

# Using stdin (for longer questions)
python -m src.cli << EOF
What is the company's policy on remote work?
Please include any specific requirements or exceptions.
EOF

# With custom parameters
python -m src.cli --model gpt-4 --max-context 8000 --temperature 0.5 "Your question here"
```

The service will:
- Initialize the MeiliSearch index
- Fetch all pages from your Notion workspace
- Index them in MeiliSearch
- Continue syncing at the configured interval

## Future Enhancements

This module is designed to be extended with:
- Webhook-based real-time updates
- Advanced search capabilities
- Page relationship visualization
- Support for additional LLM providers

When testing and developing etc remember you need meilisearch running in background

`meilisearch --master-key your-master-key`