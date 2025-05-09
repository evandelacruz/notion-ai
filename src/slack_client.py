import aiohttp
from typing import Optional
from src.config.config import config

class SlackClient:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base_url = "https://slack.com/api"
    
    async def post_message(self, channel: str, text: str, thread_ts: Optional[str] = None) -> bool:
        """
        Post a message to a Slack channel.
        
        Args:
            channel: The channel ID to post to
            text: The message text
            thread_ts: Optional thread timestamp to reply in a thread
            
        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.base_url}/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": channel,
            "text": text
        }
        
        if thread_ts:
            payload["thread_ts"] = thread_ts
            
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                result = await response.json()
                return result.get("ok", False) 