from fastapi import APIRouter, Request, Body, HTTPException
from datetime import datetime, timezone
import logging
from slack.slack_app import process_slack_events
from user_store import get_clerk_id_by_slack_id, add_slack_user_id, get_user
from db import db

router = APIRouter(prefix="/slack", tags=["slack"])

@router.post("/events")
async def slack_events(request: Request):
    """Handle Slack events and event subscriptions."""
    return await process_slack_events(request)

@router.post("/commands/nia")
async def slack_commands(request: Request):
    """Handle Slack slash commands."""
    return await process_slack_events(request)

@router.get("/install")
async def slack_install(request: Request):
    """Handle the initial Slack install request."""
    return await process_slack_events(request)

@router.get("/oauth_redirect")
async def slack_oauth_redirect(request: Request):
    """Handle the OAuth callback from Slack."""
    return await process_slack_events(request)

@router.post("/user/link")
async def link_slack_user(
    clerk_user_id: str = Body(...),
    slack_user_id: str = Body(...),
):
    """Link a Slack user ID to a Clerk user account."""
    try:
        # First check if this Slack ID is already linked to another user
        existing_clerk_id = get_clerk_id_by_slack_id(slack_user_id)
        if existing_clerk_id and existing_clerk_id != clerk_user_id:
            raise HTTPException(
                status_code=400,
                detail="This Slack account is already linked to a different user"
            )

        # Add the Slack user ID to the user's slack_user_ids array
        success = add_slack_user_id(clerk_user_id, slack_user_id)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to link Slack account"
            )

        return {"success": True, "user": get_user(clerk_user_id)}
    except Exception as e:
        logging.error(f"Error linking Slack user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/unlink")
async def unlink_slack_user(
    clerk_user_id: str = Body(...),
    slack_user_id: str = Body(...),
):
    """Unlink a Slack user ID from a Clerk user account."""
    try:
        # Get the user document
        user_doc = get_user(clerk_user_id)
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")

        # Remove the Slack user ID from the user's slack_user_ids array
        result = db.users.update_one(
            {"id": clerk_user_id},
            {
                "$pull": {"slack_user_ids": slack_user_id},
                "$set": {"updated_at": datetime.now(timezone.utc)}
            }
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="Slack user ID not found or already unlinked"
            )

        return {"success": True, "user": get_user(clerk_user_id)}
    except Exception as e:
        logging.error(f"Error unlinking Slack user: {e}")
        raise HTTPException(status_code=500, detail=str(e))
