import os
import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.authorization.async_authorize import AsyncAuthorize
from urllib.parse import parse_qs
from slack_bolt.authorization import AuthorizeResult

from models import SlackMention
from slack.slack_app import (
    call_nia_chat_api,
    get_bot_info,
    create_thread_response,
    format_code_block,
    parse_command_text,
    format_error_message,
    format_message_blocks
)
from retriever import LLMRetriever
from chat_store import create_new_chat, add_chat_message
from user_store import get_or_create_user, get_user, update_user
from project_store import list_projects, get_project
from db import db

logger = logging.getLogger(__name__)

# Keep a global map from Slack channel -> Project ID
channel_projects = {}

# Initialize AsyncWebClient
client = AsyncWebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# Get bot info
bot_info = get_bot_info() or {}
BOT_ID = bot_info.get("bot_id")
BOT_USER_ID = bot_info.get("bot_user_id")

# -----------
# Authorization
# -----------
async def authorize(enterprise_id: str, team_id: str, logger: logging.Logger):
    """Simple authorization for single workspace"""
    return AuthorizeResult(
        enterprise_id=enterprise_id,
        team_id=team_id,
        bot_token=os.environ.get("SLACK_BOT_TOKEN"),
        bot_id=BOT_ID,
        bot_user_id=BOT_USER_ID,
    )

# -----------
# Utilities
# -----------
async def get_slack_user_email(user_id: str) -> str:
    """Fetch Slack user's email via Slack API"""
    try:
        result = await client.users_info(user=user_id)
        return result["user"]["profile"]["email"]
    except Exception as e:
        logger.error(f"Failed to fetch Slack user email: {e}")
        return None

def get_web_user_id(slack_user_id: str) -> str:
    """Look up existing web user who is mapped to this Slack user."""
    # Try finding by slack_id
    doc = db.users.find_one({"$or": [
        {"slack_id": slack_user_id},
        {"id": f"slack_{slack_user_id}"},
        {"id": slack_user_id}
    ]})
    
    if doc:
        user_id = doc.get("id")
        logger.info(f"Found user document: {doc}")
        logger.info(f"Using user ID: {user_id}")
        return user_id
    
    return None

def map_slack_to_web_user(slack_user_id: str, slack_email: str) -> str:
    """Map Slack user to web app user"""
    logger.info(f"Mapping Slack user {slack_user_id} with email {slack_email}")
    
    # First try to find user by email (Clerk user)
    logger.info(f"Looking up user by email {slack_email}")
    web_user = db.users.find_one({"email": slack_email})
    if web_user:
        user_id = web_user.get("id")
        logger.info(f"Found existing web user by email: {web_user}")
        if user_id:
            # Update with Slack info
            logger.info(f"Updating user {user_id} with Slack ID {slack_user_id}")
            update_user(user_id, {"slack_id": slack_user_id})
            return user_id
    
    # Try to find by Slack ID
    logger.info(f"Looking up user by Slack ID {slack_user_id}")
    web_user = get_user(slack_user_id)
    if web_user:
        user_id = web_user.get("id")
        logger.info(f"Found existing user by Slack ID: {web_user}")
        if user_id:
            # Update with email if not set
            if not web_user.get("email"):
                update_user(user_id, {"email": slack_email})
            return user_id
    
    # Try to find by email username as Clerk ID
    clerk_id = slack_email.split("@")[0]
    logger.info(f"Looking up user by potential Clerk ID: {clerk_id}")
    web_user = get_user(clerk_id)
    if web_user:
        user_id = web_user.get("id")
        logger.info(f"Found user by Clerk ID: {web_user}")
        if user_id:
            # Update with Slack info
            logger.info(f"Updating user {user_id} with Slack info")
            update_user(user_id, {
                "slack_id": slack_user_id,
                "email": slack_email
            })
            return user_id
    
    # Create new user as last resort
    logger.info(f"Creating new user for Slack user {slack_user_id}")
    user = get_or_create_user(
        clerk_id,  # Use Clerk ID format if possible
        email=slack_email,
        slack_id=slack_user_id
    )
    logger.info(f"Created new user: {user}")
    return user.get("id", clerk_id)  # Fallback to clerk_id if id not in response

def get_project_for_channel(channel_id: str, web_user_id: str):
    """Get project for channel or fallback to first indexed project"""
    if channel_id in channel_projects:
        project = get_project(channel_projects[channel_id], web_user_id)
        if project and project.get("is_indexed"):
            return project

    # Fallback to first indexed project
    projects = list_projects(web_user_id)
    if not projects:
        return None
    indexed = [p for p in projects.values() if p.get("is_indexed")]
    return indexed[0] if indexed else None

# -----------
# Initialize AsyncApp
# -----------
app = AsyncApp(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    authorize=authorize,  # Use our simple authorize function
    process_before_response=True
)

# Create the handler with our app
handler = AsyncSlackRequestHandler(app)

# -----------
# Command Handlers
# -----------
@app.command("/nia-help")
async def handle_help_command(ack, body, logger):
    """Handle help command"""
    try:
        # Acknowledge command receipt immediately
        await ack()
        
        # Get channel ID from the first value if it's a list
        channel_id = body.get("channel_id", [""])[0] if isinstance(body.get("channel_id"), list) else body.get("channel_id", "")
        
        help_text = """
*Nia AI Commands:*
• Just mention @Nia with your question about the codebase
• `/nia-project` - List your projects
• `/nia-project [name]` - Select a project for this channel
• `/nia-help` - Show this help message
• `/nia-status` - Check indexing status

To get started:
1. First, index a repository at https://app.trynia.ai
2. Use `/nia-project` to select which project to use in this channel
3. Ask questions by mentioning @Nia
"""
        # Use the client to send the message
        await client.chat_postMessage(
            channel=channel_id,
            text=help_text,
            blocks=format_message_blocks(help_text)
        )
        
        # Return empty response to acknowledge
        return ""
        
    except Exception as e:
        logger.error(f"Error in help command: {str(e)}")
        if channel_id:
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message(str(e))
            )
        return ""

@app.command("/nia-project")
async def handle_project_command(ack, body, logger):
    """Handle project selection"""
    try:
        await ack()
        
        # Get values from the first item if they're lists
        user_id = body.get("user_id", [""])[0] if isinstance(body.get("user_id"), list) else body.get("user_id", "")
        channel_id = body.get("channel_id", [""])[0] if isinstance(body.get("channel_id"), list) else body.get("channel_id", "")
        text = body.get("text", [""])[0] if isinstance(body.get("text"), list) else body.get("text", "")
        text = text.strip()

        # Get Slack user's email
        try:
            result = await client.users_info(user=user_id)
            slack_email = result["user"]["profile"]["email"]
            logger.info(f"Got Slack user email: {slack_email}")
        except Exception as e:
            logger.error(f"Failed to fetch Slack user email: {e}")
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message("Unable to verify your Slack account. Please make sure your email is visible to apps.")
            )
            return ""

        # Map Slack user to web app user
        web_user_id = map_slack_to_web_user(user_id, slack_email)
        logger.info(f"Mapped Slack user to web user ID: {web_user_id}")
        
        if not web_user_id:
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message(
                    "Could not find your account. Please:\n"
                    "1. Sign in to https://app.trynia.ai with your Slack email\n"
                    "2. Connect your Slack account in settings"
                )
            )
            return ""
        
        # List projects if no argument provided
        if not text:
            projects = list_projects(web_user_id)
            logger.info(f"Found projects for user {web_user_id}: {list(projects.keys()) if projects else 'None'}")
            
            # Filter indexed projects
            indexed_projects = [p for p in projects.values() if p.get("status") == "indexed" or p.get("is_indexed")]
            
            if not indexed_projects:
                await client.chat_postMessage(
                    channel=channel_id,
                    **format_error_message(
                        "No indexed projects found. Please:\n"
                        "1. Sign in to https://app.trynia.ai with your Slack email\n"
                        "2. Add and index repositories there first"
                    )
                )
                return ""
                
            project_list = "*Your Indexed Projects:*\n" + "\n".join([
                f"• *{p['name']}* (id=`{p['id']}`)"
                for p in indexed_projects
            ])
            project_list += "\n\nUse `/nia-project [project name]` to select a project for this channel"
            
            await client.chat_postMessage(
                channel=channel_id,
                text=project_list,
                blocks=format_message_blocks(project_list)
            )
            return ""
        
        # Find project by name or ID
        projects = list_projects(web_user_id)
        project = next(
            (p for p in projects.values() if 
             p["name"].lower() == text.lower() or 
             p["id"].lower() == text.lower()),
            None
        )
        
        if not project:
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message(f"Project '{text}' not found. Use `/nia-project` to list available projects.")
            )
            return ""
            
        if not project.get("is_indexed") and not project.get("status") == "indexed":
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message(f"Project '{project['name']}' is not indexed yet. Please wait for indexing to complete.")
            )
            return ""
        
        # Set project for channel
        channel_projects[channel_id] = project["id"]
        await client.chat_postMessage(
            channel=channel_id,
            text=f"Now using project: *{project['name']}* (id=`{project['id']}`) in this channel",
            blocks=format_message_blocks(f"Now using project: *{project['name']}* (id=`{project['id']}`) in this channel")
        )
        return ""
    except Exception as e:
        logger.error(f"Error in project command: {str(e)}")
        if channel_id:
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message(str(e))
            )
        return ""

@app.command("/nia-status")
async def handle_status_command(ack, body, logger):
    """Handle status command"""
    try:
        await ack()
        
        # Get values from the first item if they're lists
        user_id = body.get("user_id", [""])[0] if isinstance(body.get("user_id"), list) else body.get("user_id", "")
        channel_id = body.get("channel_id", [""])[0] if isinstance(body.get("channel_id"), list) else body.get("channel_id", "")
        
        # Get Slack user's email
        try:
            result = await client.users_info(user=user_id)
            slack_email = result["user"]["profile"]["email"]
        except Exception as e:
            logger.error(f"Failed to fetch Slack user email: {e}")
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message("Unable to verify your Slack account. Please make sure your email is visible to apps.")
            )
            return ""
            
        # Map Slack user to web app user
        web_user_id = map_slack_to_web_user(user_id, slack_email)
        
        # Get current project for channel
        project = get_project_for_channel(channel_id, web_user_id)
        
        status = "*System Status:* ✅ Operational\n\n"
        if project:
            status += f"*Current Project:* {project['name']}\n"
            status += f"*Status:* {'✅ Indexed' if project.get('is_indexed') else '⏳ Indexing'}\n"
        else:
            status += "*No project selected for this channel*\nUse `/nia-project` to select a project"
        
        await client.chat_postMessage(
            channel=channel_id,
            text=status,
            blocks=format_message_blocks(status)
        )
        return ""
    except Exception as e:
        logger.error(f"Error in status command: {str(e)}")
        if channel_id:
            await client.chat_postMessage(
                channel=channel_id,
                **format_error_message(str(e))
            )
        return ""

# -----------
# Event Handlers
# -----------
@app.event("app_mention")
async def handle_mention(event, logger):
    """Handle app mentions in channels"""
    try:
        # Extract necessary information
        user_id = event.get("user")
        channel_id = event.get("channel")
        thread_ts = event.get("thread_ts", event.get("ts"))
        text = event.get("text", "").strip()

        logger.info(f"Received mention from user {user_id} in channel {channel_id}")

        # Get Slack user's email
        try:
            slack_email = await get_slack_user_email(user_id)
            if not slack_email:
                raise ValueError("Could not fetch Slack user email")
        except Exception as e:
            logger.error(f"Failed to fetch Slack user email: {e}")
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                **format_error_message("Unable to verify your Slack account. Please make sure your email is visible to apps.")
            )
            return

        # Map Slack user to web app user
        web_user_id = map_slack_to_web_user(user_id, slack_email)
        if not web_user_id:
            logger.error(f"Could not map Slack user {user_id} to web user")
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                **format_error_message(
                    "Could not find your account. Please:\n"
                    "1. Sign in to https://app.trynia.ai with your Slack email\n"
                    "2. Connect your Slack account in settings"
                )
            )
            return

        # Get project for this channel
        project = get_project_for_channel(channel_id, web_user_id)
        if not project:
            logger.error(f"No project found for channel {channel_id}")
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                **format_error_message(
                    "No project selected for this channel. Please:\n"
                    "1. Use `/nia-project` to list your projects\n"
                    "2. Select a project with `/nia-project [name]`"
                )
            )
            return

        # Create new chat or get existing
        chat = create_new_chat(web_user_id, project["id"])
        
        # Process the mention and get response
        try:
            response = await call_nia_chat_api(
                user_id=web_user_id,
                project_id=project["id"],
                chat_id=chat["id"],
                user_prompt=text
            )
            
            # Send response in thread
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                text=response
            )
            
        except Exception as e:
            logger.error(f"Error processing mention: {e}")
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                **format_error_message(f"Error processing your request: {str(e)}")
            )

    except Exception as e:
        logger.error(f"Error in mention handler: {e}")
        try:
            await client.chat_postMessage(
                channel=channel_id,
                thread_ts=thread_ts,
                **format_error_message("An unexpected error occurred. Please try again later.")
            )
        except:
            logger.error("Failed to send error message to Slack")
