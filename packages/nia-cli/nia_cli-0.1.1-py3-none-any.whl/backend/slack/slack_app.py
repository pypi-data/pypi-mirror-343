# /Users/jel/nia-ai-app/backend/slack/slack_app.py

import os
import logging
import asyncio
from typing import Optional, Dict, Any, Callable
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
import json
import httpx
from functools import wraps
import secrets
import time

from slack_bolt import App
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.authorization import AuthorizeResult

# Import your user/project/chat logic
from user_store import get_or_create_user, get_or_create_user_sync, update_user, remove_slack_team_users, add_slack_user_id
from project_store import list_projects, get_project
from chat_store import create_new_chat, add_chat_message
from user_store import get_clerk_id_by_slack_id
from db import db
from .encryption import encrypt_token, decrypt_token

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")

# Basic checks
required_env = [SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET]
if any(v is None for v in required_env):
    missing = [name for (name, val) in {
        "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN,
        "SLACK_SIGNING_SECRET": SLACK_SIGNING_SECRET,
        "SLACK_CLIENT_ID": SLACK_CLIENT_ID,
        "SLACK_CLIENT_SECRET": SLACK_CLIENT_SECRET
    }.items() if not val]
    raise ValueError(f"Missing Slack env vars: {missing}")

# URLs for OAuth
NGROK_URL = os.getenv("NGROK_URL", "https://newt-curious-bison.ngrok-free.app")
PRODUCTION_URL = os.getenv("PRODUCTION_URL", "https://api.trynia.ai")
BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")

# Use production URL if available, otherwise fallback to ngrok for development
API_BASE_URL = PRODUCTION_URL if os.getenv("PRODUCTION_URL") else NGROK_URL

SUCCESS_URL = f"{BASE_URL}/settings/code-providers?success=true&provider=slack"
ERROR_URL = f"{BASE_URL}/settings/code-providers?error=true&provider=slack"

################################################################################
# Slack Authorization
################################################################################
async def authorize(enterprise_id: Optional[str], team_id: Optional[str], user_id: Optional[str]) -> AuthorizeResult:
    """Authorize incoming requests using our MongoDB installation store."""
    logger.info(f"Authorizing request for team_id={team_id}, user_id={user_id}")
    
    try:
        # Find installation in MongoDB
        query = {"team_id": team_id} if team_id else {}
        if enterprise_id:
            query["enterprise_id"] = enterprise_id
            
        installation = db.slack_installations.find_one(query)
        if not installation:
            logger.error(f"No installation found for query: {query}")
            return None
            
        logger.info(f"Found installation for team {team_id}")
        
        # Decrypt the access token
        encrypted_token = installation.get("access_token")
        bot_token = decrypt_token(encrypted_token)
        if not bot_token:
            logger.error(f"Failed to decrypt token for team {team_id}")
            return None
        
        # Return authorization result
        return AuthorizeResult(
            enterprise_id=installation.get("enterprise_id"),
            team_id=installation.get("team_id"),
            bot_token=bot_token,
            bot_user_id=installation.get("bot_user_id"),
            bot_id=None,  # Optional
            user_token=None,  # We don't use user tokens
            user_id=installation.get("slack_user_id")
        )
    except Exception as e:
        logger.error(f"Error in authorize function: {e}")
        return None

# The Slack AsyncApp (only for events, not OAuth)
slack_app = AsyncApp(
    signing_secret=SLACK_SIGNING_SECRET,
    authorize=authorize  # Use our custom authorize function
)

# SlackRequestHandler
slack_handler = AsyncSlackRequestHandler(slack_app)

################################################################################
# Custom OAuth Flow
################################################################################

async def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """Exchange OAuth code for access token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://slack.com/api/oauth.v2.access",
            data={
                "client_id": SLACK_CLIENT_ID,
                "client_secret": SLACK_CLIENT_SECRET,
                "code": code,
                "redirect_uri": f"{API_BASE_URL}/slack/oauth_redirect"
            }
        )
        
        if not response.is_success:
            logger.error(f"Failed to exchange code: {response.text}")
            raise HTTPException(status_code=400, detail="Failed to exchange code")
            
        data = response.json()
        if not data.get("ok"):
            logger.error(f"Slack API error: {data.get('error')}")
            raise HTTPException(status_code=400, detail=data.get("error"))
            
        return data

def validate_environment() -> None:
    """Validate all required environment variables are set."""
    required_vars = {
        "SLACK_BOT_TOKEN": os.getenv("SLACK_BOT_TOKEN"),
        "SLACK_SIGNING_SECRET": os.getenv("SLACK_SIGNING_SECRET"),
        "SLACK_CLIENT_ID": os.getenv("SLACK_CLIENT_ID"),
        "SLACK_CLIENT_SECRET": os.getenv("SLACK_CLIENT_SECRET"),
        "PRODUCTION_URL": os.getenv("PRODUCTION_URL"),  # Replace NGROK
        "BASE_URL": os.getenv("BASE_URL"),
        "MONGODB_URI": os.getenv("MONGODB_URI")
    }
    
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

def rate_limit(max_requests: int = 5, window_seconds: int = 60) -> Callable:
    """Rate limiting decorator for Slack commands."""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        async def wrapper(ack, body, say, logger, *args, **kwargs):
            user_id = body.get("user_id", "unknown")
            current_time = time.time()
            
            # Clean old entries
            cache[user_id] = [t for t in cache.get(user_id, []) 
                            if current_time - t < window_seconds]
            
            if len(cache.get(user_id, [])) >= max_requests:
                await ack()
                await say("Rate limit exceeded. Please try again later.")
                return
                
            cache.setdefault(user_id, []).append(current_time)
            return await func(ack, body, say, logger, *args, **kwargs)
        return wrapper
    return decorator

async def save_installation(token_response: Dict[str, Any], clerk_user_id: str) -> bool:
    """Save the Slack installation details and link to Clerk user."""
    try:
        # Extract relevant data
        team = token_response.get("team", {})
        team_id = team.get("id")
        
        authed_user = token_response.get("authed_user", {})
        slack_user_id = authed_user.get("id")
        
        if not all([team_id, slack_user_id]):
            logger.error("Missing required fields in token response")
            return False
            
        # Encrypt the access token
        access_token = token_response.get("access_token")
        encrypted_token = encrypt_token(access_token)
        if not encrypted_token:
            logger.error("Failed to encrypt access token")
            return False
        
        # Save to MongoDB
        now = datetime.now(timezone.utc)
        installation = {
            "team_id": team_id,
            "team_name": team.get("name"),
            "slack_user_id": slack_user_id,
            "clerk_user_id": clerk_user_id,
            "access_token": encrypted_token,
            "token_encrypted": True,
            "bot_user_id": token_response.get("bot_user_id"),
            "bot_scopes": token_response.get("scope", "").split(","),
            "enterprise_id": team.get("enterprise_id"),
            "is_enterprise_install": token_response.get("is_enterprise_install", False),
            "installed_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        # Log the installation data (excluding sensitive fields)
        log_data = {k: v for k, v in installation.items() if k not in ["access_token"]}
        logger.info(f"Saving Slack installation: {json.dumps(log_data)}")
        
        # Upsert the installation
        result = db.slack_installations.update_one(
            {"team_id": team_id},
            {"$set": installation},
            upsert=True
        )
        
        # Link Slack user to Clerk user
        success = add_slack_user_id(clerk_user_id, slack_user_id)
        if not success:
            logger.error(f"Failed to link Slack user {slack_user_id} to Clerk user {clerk_user_id}")
            return False
            
      
        
        logger.info(f"Successfully saved Slack installation for team {team_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to save installation: {e}", exc_info=True)
        return False

################################################################################
# FastAPI Routes
################################################################################

async def handle_slack_install(request: Request):
    """Handle the initial OAuth redirect to Slack."""
    clerk_user_id = request.query_params.get("state")
    logger.info(f"[OAuth Install] Starting Slack installation with clerk_id={clerk_user_id}")
    
    if not clerk_user_id:
        logger.error("[OAuth Install] No clerk_user_id provided")
        return RedirectResponse(url=f"{ERROR_URL}&error=no_user_id")
    
    # Generate Slack's OAuth URL
    oauth_url = (
        "https://slack.com/oauth/v2/authorize"
        f"?client_id={SLACK_CLIENT_ID}"
        f"&scope=app_mentions:read,channels:history,channels:read,chat:write,commands,im:history,im:read,im:write,users:read,users:read.email"
        f"&redirect_uri={API_BASE_URL}/slack/oauth_redirect"
        f"&state={clerk_user_id}"
    )
    
    logger.info(f"[OAuth Install] Redirecting to Slack with state={clerk_user_id}")
    return RedirectResponse(url=oauth_url)

async def handle_oauth_redirect(request: Request):
    """Handle the OAuth callback from Slack."""
    request_id = secrets.token_hex(8)
    logger.info(f"[{request_id}] Starting OAuth redirect handling")
    try:
        # Get params
        code = request.query_params.get("code")
        state = request.query_params.get("state")  # This is our clerk_user_id
        error = request.query_params.get("error")
        
        logger.info(f"[{request_id}] Received: code={code}, state={state}, error={error}")
        
        if error:
            logger.error(f"[{request_id}] Slack returned error: {error}")
            return RedirectResponse(url=f"{ERROR_URL}&error={error}&request_id={request_id}")
            
        if not code or not state:
            logger.error(f"[{request_id}] Missing code or state")
            return RedirectResponse(url=f"{ERROR_URL}&error=missing_params&request_id={request_id}")
        
        # Exchange code for token
        token_response = await exchange_code_for_token(code)
        
        # Save installation and link users
        if not await save_installation(token_response, state):
            logger.error(f"[{request_id}] Failed to save installation")
            return RedirectResponse(url=f"{ERROR_URL}&error=installation_failed&request_id={request_id}")
        
        logger.info(f"[{request_id}] Successfully installed")
        return RedirectResponse(url=SUCCESS_URL)
        
    except Exception as e:
        logger.error(f"[{request_id}] Error: {e}")
        # TODO: Add proper error tracking here (e.g., Sentry)
        return RedirectResponse(url=f"{ERROR_URL}&error=server_error&request_id={request_id}")

################################################################################
# The main function that we call from main.py
################################################################################
async def process_slack_events(request: Request):
    """Handle all Slack-related requests."""
    path = request.url.path
    
    if path == "/slack/install":
        return await handle_slack_install(request)
    elif path == "/slack/oauth_redirect":
        return await handle_oauth_redirect(request)
    else:
        # For all other paths (events, commands, etc.), use Slack Bolt
        return await slack_handler.handle(request)

################################################################################
# Slack slash commands
################################################################################

@slack_app.command("/nia")
@rate_limit(max_requests=5, window_seconds=60)
async def slash_command_nia(ack, body, say, logger):
    """
    A single slash command: /nia
    Subcommands:
      /nia list      -> List all projects for the Slack user
      /nia use <id>  -> Set project <id> as current
      /nia chat <question> -> Ask question about current project
    """
    await ack()  # Acknowledge the Slack command immediately

    user_slack_id = body.get("user_id")  # Slack user ID
    text = body.get("text", "").strip()  # Everything typed after /nia

    # Get the Clerk ID for this Slack user
    internal_user_id = get_clerk_id_by_slack_id(user_slack_id)
    if not internal_user_id:
        await say("You need to link your Slack account with Nia first. Please visit the Nia web app and use the Slack integration settings.")
        return

    user_doc = get_or_create_user(internal_user_id)

    # Split the text to see which subcommand
    parts = text.split(maxsplit=1)
    if not parts or parts[0].lower() not in ["list", "use", "chat"]:
        usage_msg = (
            "Usage:\n"
            "`/nia list` - list your available indexed projects\n"
            "`/nia use <project_id>` - choose which project to chat with\n"
            "`/nia chat <question>` - ask a question about your current project"
        )
        await say(usage_msg)
        return

    subcmd = parts[0].lower()

    if subcmd == "list":
        # Show all projects that are "indexed"
        projects = list_projects(internal_user_id)
        indexed_projects = [p for p in projects.values() if p.get("status") == "indexed"]

        if not indexed_projects:
            await say("You have no indexed projects. Please index one first!")
            return

        # Build a simple text list:
        lines = ["Your *indexed* projects:"]
        for proj in indexed_projects:
            lines.append(f"- *{proj['name']}* (id={proj['id']})")
        await say("\n".join(lines))

    elif subcmd == "use":
        if len(parts) < 2:
            await say("Please specify a project id. Example: `/nia use 815e9e67-e59c-4f94-990e-62ea74a6637e`")
            return
        project_id = parts[1].strip()
        # Check if that project belongs to this user & is indexed
        doc = get_project(project_id, internal_user_id)
        if not doc:
            await say(f"No project found with id={project_id} or you don't own it.")
            return
        if doc.get("status") != "indexed":
            await say("That project is not fully indexed. Please wait until it's indexed.")
            return

        # Mark in user doc
        update_user(internal_user_id, {"slack_selected_project": project_id})
        await say(f"Got it! Using project `{doc['name']}` (id={project_id}) for future questions.")

    elif subcmd == "chat":
        if len(parts) < 2:
            await say("Please provide a question after `/nia chat`")
            return
        question = parts[1].strip()

        # Retrieve the user's currently selected project
        selected_project_id = user_doc.get("slack_selected_project")
        if not selected_project_id:
            await say("No project selected. Please run `/nia list` and `/nia use <id>` first.")
            return

        # Confirm the project still exists
        proj_doc = get_project(selected_project_id, internal_user_id)
        if not proj_doc or proj_doc.get("status") != "indexed":
            await say("Your selected project is invalid or not indexed. Try `/nia list` again.")
            return

        # Create or reuse a Slack chat_id. We'll do one chat per Slack user. 
        chat_id = f"slack-user-{user_slack_id}"
        
        # Add user message
        try:
            add_chat_message(selected_project_id, chat_id, "user", question, internal_user_id, images=None)
        except Exception as e:
            logger.warning(f"Failed to save user message: {e}")

        # Call your /chat endpoint
        try:
            logger.info(f"Processing chat request: {question}")
            answer = await call_nia_chat_api(
                user_id=internal_user_id,
                project_id=selected_project_id,
                chat_id=chat_id,
                user_prompt=question
            )
            
            # Format the response for Slack
            if answer and len(answer) > 0:
                # Add the chat message to history
                try:
                    add_chat_message(selected_project_id, chat_id, "assistant", answer, internal_user_id, images=None)
                except Exception as e:
                    logger.warning(f"Failed to save assistant message: {e}")
                
                # Format nicely for Slack
                await say(answer)
            else:
                await say("Sorry, I couldn't generate a response. Please try again.")
                
        except Exception as e:
            logger.error(f"Failed to get chat answer: {e}", exc_info=True)
            await say(f"Sorry, I encountered an error: {str(e)}\nPlease try again or check with support.")

################################################################################
# Slack mention event
################################################################################
@slack_app.event("app_mention")
async def handle_app_mention(body, say, logger):
    """
    If a user mentions @nia in a channel or DM, we respond.
    We only respond if they've set a project, otherwise we instruct them.
    """
    event = body.get("event", {})
    user_text = event.get("text", "")
    user_slack_id = event.get("user", "")
    channel_id = event.get("channel", "")
    bot_id = event.get("authorizations", [{}])[0].get("user_id", "")

    logger.info(f"[Slack] Mention by user {user_slack_id} text: {user_text}")

    # Get the Clerk ID for this Slack user
    internal_user_id = get_clerk_id_by_slack_id(user_slack_id)
    if not internal_user_id:
        await say("You need to link your Slack account with Nia first. Please visit the Nia web app and use the Slack integration settings.")
        return

    user_doc = get_or_create_user(internal_user_id)
    selected_project_id = user_doc.get("slack_selected_project")

    if not selected_project_id:
        msg = (
            f"You haven't selected a project yet! "
            f"Use `/nia list` to see your projects, then `/nia use <id>` to select one."
        )
        await say(msg)
        return

    # Check project
    proj_doc = get_project(selected_project_id, internal_user_id)
    if not proj_doc or proj_doc.get("status") != "indexed":
        await say("Your currently selected project is not indexed or doesn't exist. Try `/nia list` again.")
        return

    # Strip out the mention text properly
    # e.g. user_text might be "<@U032N3> hello" or "<@U032N3|nia> hello"
    question = user_text
    if bot_id:
        question = question.replace(f"<@{bot_id}>", "").strip()
        question = question.replace(f"<@{bot_id}|nia>", "").strip()

    # If the user typed literally nothing
    if not question or len(question) < 2:
        await say("Please ask a question, for example: `@nia how does the DB code work?`")
        return

    # We define chat_id by channel
    chat_id = f"slack-channel-{channel_id}"
    add_chat_message(selected_project_id, chat_id, "user", question, internal_user_id, sources=None, images=None)

    try:
        answer = await call_nia_chat_api(
            user_id=internal_user_id,
            project_id=selected_project_id,
            chat_id=chat_id,
            user_prompt=question
        )
        await say(answer)
    except SlackApiError as e:
        logger.error(f"Slack API error: {e}")
        await say("Slack error occurred. Check logs.")
    except Exception as e:
        logger.error(f"Failed to process mention: {e}", exc_info=True)
        await say(f"Error: {e}")

################################################################################
# Helper: Use your existing /projects/{project_id}/chat endpoint to get LLM answer
################################################################################
def format_slack_message(message: str, question: str = None) -> str:
    """Format a message for Slack, handling code blocks and other formatting gracefully."""
    try:
        formatted_message = []
        
        # Add the original question if provided
        if question:
            formatted_message.append(f"*Question:*\n{question}\n")

        # Split message into sources and content if sources are present
        if message.startswith("Sources:"):
            parts = message.split("\n\n", 1)
            sources = parts[0]
            content = parts[1] if len(parts) > 1 else ""
            
            # Format sources as a bulleted list
            formatted_sources = sources.replace("- ", "• ")
            formatted_message.append(formatted_sources)
            
            # Handle code blocks in content
            if "```" in content:
                # Split by code blocks
                segments = content.split("```")
                formatted_segments = []
                
                for i, segment in enumerate(segments):
                    if i % 2 == 0:  # Not a code block
                        formatted_segments.append(segment.strip())
                    else:  # Code block
                        # Remove language identifier if present
                        if "\n" in segment:
                            code = segment.split("\n", 1)[1]
                        else:
                            code = segment
                        formatted_segments.append(f"```{code.strip()}```")
                
                formatted_content = "\n".join(formatted_segments)
            else:
                formatted_content = content
            
            formatted_message.append(formatted_content)
        else:
            # Handle code blocks in regular messages
            if "```" in message:
                # Split by code blocks
                segments = message.split("```")
                formatted_segments = []
                
                for i, segment in enumerate(segments):
                    if i % 2 == 0:  # Not a code block
                        formatted_segments.append(segment.strip())
                    else:  # Code block
                        # Remove language identifier if present
                        if "\n" in segment:
                            code = segment.split("\n", 1)[1]
                        else:
                            code = segment
                        formatted_segments.append(f"```{code.strip()}```")
                
                formatted_message.append("\n".join(formatted_segments))
            else:
                formatted_message.append(message)
        
        return "\n\n".join(formatted_message)
    except Exception as e:
        logger.error(f"Error formatting Slack message: {e}")
        return message  # Return original message if formatting fails

async def call_nia_chat_api(user_id: str, project_id: str, chat_id: str, user_prompt: str) -> str:
    """
    Calls your existing "chat" endpoint to get a model response.
    Handles streaming response and combines it into a single message.
    """
    chat_url = f"{API_BASE_URL}/projects/{project_id}/chat"

    payload = {
        "user_id": user_id,
        "prompt": user_prompt,
        "chat_id": chat_id,
        "messages": [],
        "max_tokens": 2048,
        "temperature": 0.2,
        "stream": True  # Keep stream true to get chunks
    }

    async with httpx.AsyncClient() as client:
        try:
            logger.debug(f"Calling chat API with payload: {payload}")
            async with client.stream('POST', chat_url, json=payload, timeout=120) as response:
                response.raise_for_status()
                
                full_response = []
                sources = None
                
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    
                    try:
                        data = json.loads(line[6:])  # Skip "data: " prefix
                        
                        # Handle sources
                        if "sources" in data:
                            sources = data["sources"]
                            continue
                            
                        # Handle content chunks
                        if "content" in data:
                            content = data["content"]
                            if content == "[DONE]":
                                break
                            full_response.append(content)
                    except json.JSONDecodeError:
                        continue

                # Combine all chunks into one message
                complete_response = "".join(full_response)
                
                # If we have sources, add them at the top
                if sources:
                    source_text = "Sources:\n" + "\n".join([f"- {s}" for s in sources])
                    complete_response = f"{source_text}\n\n{complete_response}"
                
                # Format the response for Slack, including the original question
                formatted_response = format_slack_message(complete_response or "No response generated", user_prompt)
                return formatted_response

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling chat API: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Chat API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error calling chat API: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

