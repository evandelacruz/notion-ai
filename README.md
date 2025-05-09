# Notion Knowledge Base Search

A Python service that indexes Notion pages in a local MeiliSearch instance and provides an intelligent search interface powered by LLMs. Includes both CLI and Slack bot interfaces.

## Features

- Fetches all pages from a Notion workspace
- Indexes content in a local MeiliSearch instance
- Continuous sync with configurable interval
- Smart content extraction including headings and paragraphs
- Parent-child page relationship tracking
- LLM-powered question answering using indexed content
- Interactive CLI for natural language queries
- Slack bot integration for team-wide access
- Context-aware responses based on indexed content

## Prerequisites

1. Python 3.8+
2. MeiliSearch installed locally
3. Notion API key with access to your workspace
4. OpenAI API key (for LLM functionality)
5. Slack Bot Token (for Slack integration)

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
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SYNC_INTERVAL_MINUTES=60
```

## Usage

### Indexing Your Notion Pages

(MeiliSearch must be running)

1. Start the sync service to index your Notion pages:
```bash
python -m src.sync.sync_service
```

2. To clear and recreate the index (if needed):
```bash
python -m src.clear_index
```

### Searching Your Knowledge Base

#### CLI Interface

Use the CLI to ask questions about your indexed content:

```bash
# Using command line argument
python -m src.cli "What is the company's policy on remote work?"

# Using stdin (for longer questions)
python -m src.cli << EOF
What is the company's policy on remote work?
Please include any specific requirements or exceptions.
EOF

# Interactive mode (just run without arguments)
python -m src.cli
```

#### Slack Bot Interface

1. Start the server:
```bash
python -m src.server
```

2. Expose the server to the internet (for testing):
```bash
ngrok http 8000
```

3. Configure your Slack app:
   - Go to your Slack App settings
   - Under "Event Subscriptions":
     - Enable events
     - Add your ngrok URL + "/slack/events" as the Request URL
     - Subscribe to the `message.im` bot event
   - Under "OAuth & Permissions":
     - Add the following bot token scopes:
       - `chat:write`
       - `im:history`
       - `im:write`

4. Users can now DM the bot with their questions, and it will respond with relevant information from your Notion knowledge base.

#### CLI Options

The CLI supports several customization options:

```bash
python -m src.cli [options] [question]

Options:
  --model MODEL           OpenAI model to use (default: gpt-3.5-turbo)
  --max-context LENGTH    Maximum context length in characters (default: 40000)
  --temperature TEMP      Temperature for LLM generation (default: 0.7)
```

### How It Works

1. **Indexing Process**:
   - The sync service fetches all pages from your Notion workspace
   - Content is extracted and processed
   - Pages are indexed in MeiliSearch with their hierarchy and relationships
   - Continuous sync keeps the index up to date

2. **Search Process**:
   - Your question is analyzed to extract key search terms
   - MeiliSearch finds relevant content from your knowledge base
   - The LLM processes the context and generates a natural language response
   - Responses are based on actual content from your Notion pages

## Development Notes

- Always ensure MeiliSearch is running in the background:
```bash
meilisearch --master-key your-master-key
```

- The service uses a combination of MeiliSearch for fast content retrieval and OpenAI's LLM for natural language understanding
- Search results are optimized for relevance using custom ranking rules and typo tolerance
- The system maintains page hierarchies to provide context-aware responses

## Future Enhancements

- Webhook-based real-time updates
- Advanced search capabilities
- Page relationship visualization
- Support for additional LLM providers
- Web interface for searching
- Batch processing for large workspaces
- Additional Slack bot features (threading, reactions, etc.)