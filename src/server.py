from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn
import json
import os
from typing import Dict, Any

from src.indexer.meilisearch_client import SearchIndexer
from src.llm.llm_service import LLMService
from src.llm.llm_client import OpenAIClient
from src.slack_client import SlackClient
from src.config.config import config

app = FastAPI()

# Initialize services
search_indexer = SearchIndexer(host=config.MEILISEARCH_HOST, api_key=config.MEILISEARCH_KEY)
search_indexer.configure_search_settings()
llm_service = LLMService(
    search_indexer=search_indexer,
    llm_client=OpenAIClient(
        model='gpt-3.5-turbo',  # Default model
        api_key=config.OPENAI_API_KEY
    )
)
slack_client = SlackClient(bot_token=config.SLACK_BOT_TOKEN)

# This is the new function that contains all the message processing logic
async def process_message(event: Dict[str, Any]):
    """Process the message in the background."""
    try:
        user_message = event.get("text", "").strip()
        if not user_message:
            return

        response = llm_service.generate_response(
            user_message,
            max_context_length=40000,
            temperature=0.7
        )
        
        # Send response back to Slack
        channel = event.get("channel")
        thread_ts = event.get("thread_ts") if event.get("thread_ts") else None
        
        success = await slack_client.post_message(
            channel=channel,
            text=response,
            thread_ts=thread_ts
        )
        
        if not success:
            print(f"Failed to send response to Slack for user {event.get('user')}")
            
    except Exception as e:
        print(f"Error processing message: {str(e)}")

@app.post("/slack/events")
async def handle_slack_event(request: Request, background_tasks: BackgroundTasks):
    try:
        # Parse the request body
        body = await request.json()
        
        # Handle URL verification challenge
        if body.get("type") == "url_verification":
            return {"challenge": body["challenge"]}
        
        # Handle message events
        if body.get("event", {}).get("type") == "message" and body.get("event", {}).get("channel_type") == "im":
            event = body["event"]
            
            # Ignore bot messages and message edits/deletions
            if event.get("subtype") in ["bot_message", "message_changed", "message_deleted"]:
                return JSONResponse(content={"ok": True})
            
            # Ignore messages from the bot itself
            if event.get("bot_id") or event.get("user") == body.get("authorizations", [{}])[0].get("user_id"):
                return JSONResponse(content={"ok": True})
            
            # Process the message in the background
            background_tasks.add_task(process_message, event)
                    
        return JSONResponse(content={"ok": True})
        
    except Exception as e:
        print(f"Error handling Slack event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server."""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server() 