from fastapi import APIRouter
import os
from datetime import datetime, timezone
import logging
import db  

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    """Comprehensive health check endpoint for all critical services."""
    health = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.0.0",
        "services": {}
    }
    

    try:
        db.client.admin.command('ping')
        health["services"]["mongodb"] = "healthy"
    except Exception as e:
        health["services"]["mongodb"] = {"status": "unhealthy", "error": str(e)}
        health["status"] = "degraded"
    
   
    try:
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_env = os.getenv("PINECONE_ENV")
        if pinecone_api_key and pinecone_env:
            health["services"]["pinecone"] = "healthy"
        else:
            raise ValueError("Pinecone configuration missing")
    except Exception as e:
        health["services"]["pinecone"] = {"status": "unhealthy", "error": str(e)}
        health["status"] = "degraded"
    
    
    api_services = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
    }
    
    for service, env_key in api_services.items():
        if os.getenv(env_key):
            health["services"][service] = "healthy"
        else:
            health["services"][service] = {"status": "unhealthy", "error": "API key missing"}
            health["status"] = "degraded"
    
    
    return health