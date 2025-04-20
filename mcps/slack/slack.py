import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi_mcp import FastApiMCP

# It's recommended to use environment variables for tokens in production
# For example: SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "xoxb-8781267142452-8781487338914-B1mnssUNt1A7PAaZvZuU981x") # Replace with your actual token or load from env
# SLACK_TEAM_ID = "T08NZ7V46DA" # Team ID is often not needed for basic operations

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Initialize WebClient
try:
    client = WebClient(token=SLACK_BOT_TOKEN)
    # Test authentication and identity
    auth_test = client.auth_test()
    logger.info(f"Slack client initialized successfully for bot_id: {auth_test.get('bot_id')}")
except SlackApiError as e:
    logger.error(f"Error during Slack client auth_test: {e.response['error']}")
    client = None # Ensure client is None if initialization fails
except Exception as e:
    logger.error(f"Error initializing Slack client: {e}")
    client = None

DEFAULT_CHANNEL_ID = "C08NSPSF1M3"

# Pydantic model for sending messages
class MessagePayload(BaseModel):
    message_text: str

@app.post("/send-message")
async def send_message_endpoint(payload: MessagePayload):
    """
    API endpoint to send a message to a specified Slack channel.
    Defaults to DEFAULT_CHANNEL_ID if channel_id is not provided.
    """
    if not client:
        raise HTTPException(status_code=503, detail="Slack client is not initialized.")

    # Use the provided channel_id or the default one
    channel_to_send = DEFAULT_CHANNEL_ID

    # Optional: Add validation if you want to ensure the default ID is still valid
    if not channel_to_send:
         raise HTTPException(status_code=400, detail="Channel ID is missing and no default is set.") # Should not happen with current logic but good practice

    # Allow sending empty messages if desired, otherwise add validation
    # if not payload.message_text:
    #     raise HTTPException(status_code=400, detail="Message text is empty.")

    try:
        response = client.chat_postMessage(
            channel=channel_to_send, # Use the determined channel ID
            text=payload.message_text
        )
        logger.info(f"Message sent successfully to channel {channel_to_send}. Timestamp: {response['ts']}")
        return {"ok": True, "channel": response['channel'], "ts": response['ts']}
    except SlackApiError as e:
        logger.error(f"Error sending message to channel {channel_to_send}: {e.response['error']}")
        raise HTTPException(status_code=500, detail=f"Slack API error: {e.response['error']}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending message: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@app.get("/messages/{channel_id}")
async def get_messages_endpoint(
    channel_id: str,
    limit: Optional[int] = Query(100, ge=1, le=1000) # Default limit 100, min 1, max 1000
) -> List[Dict[str, Any]]:
    """
    API endpoint to retrieve the latest messages from a specified Slack channel.
    """
    if not client:
        raise HTTPException(status_code=503, detail="Slack client is not initialized.")
    if not channel_id:
         raise HTTPException(status_code=400, detail="Channel ID is missing.")

    try:
        response = client.conversations_history(
            channel=channel_id,
            limit=limit
        )
        messages = response.get('messages', [])
        logger.info(f"Successfully retrieved {len(messages)} messages from channel {channel_id}.")
        # Return only relevant parts or filter messages if needed
        # Example: return [{"user": msg.get("user"), "text": msg.get("text"), "ts": msg.get("ts")} for msg in messages]
        return messages
    except SlackApiError as e:
        logger.error(f"Error retrieving messages from channel {channel_id}: {e.response['error']}")
        # Handle specific errors like 'channel_not_found'
        if e.response['error'] == 'channel_not_found':
            raise HTTPException(status_code=404, detail=f"Channel not found: {channel_id}")
        elif e.response['error'] == 'not_in_channel':
             raise HTTPException(status_code=403, detail=f"Bot is not in channel: {channel_id}")
        else:
            raise HTTPException(status_code=500, detail=f"Slack API error: {e.response['error']}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while retrieving messages: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

mcp = FastApiMCP(
    app,

    name="My SLACK API MCP",
    description="SLACK APP",
    base_url="http://localhost:8008",
)

mcp.mount()
