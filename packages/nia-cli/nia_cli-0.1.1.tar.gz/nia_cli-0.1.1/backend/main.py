# main.py
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi import APIRouter

# Import middleware
from middleware import RateLimitMiddleware, RequestLoggingMiddleware, SecurityHeadersMiddleware

# Import routers
from routes.health import router as health_router
from routes.slack import router as slack_router
from routes.projects import router as projects_router
from routes.projects import api_router as projects_api_router
from routes.github import router as github_routers
from routes.users import router as users_router, api_router as users_api_router, usage_router as users_usage_router
from routes.api_keys import router as api_keys_router
from routes.v2_api import router as v2_api_router
from routes.files import router as files_router
from routes.community import router as community_router
from routes.billing import router as billing_router
from routes.files import api_router as files_api_router
from routes.openai_compat import router as openai_compat_router
from routes.nuanced_status import router as nuanced_status_router
from routes import projects
from routes.data_sources import router as data_sources_router

# Load environment variables using an absolute path
dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check required environment variables
required_env_vars = [
    "OPENAI_API_KEY", 
    "PINECONE_API_KEY", 
    "PINECONE_ENV", 
    "ANTHROPIC_API_KEY", 
    "KEYWORDS_AI_API_KEY", 
    "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY",
    "ADMIN_USER_ID"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Initialize FastAPI app
app = FastAPI(title="Nia AI API", version="1.0.0")

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Configure CORS
origins = [
    "https://app.trynia.ai",  # Production
    "https://api.trynia.ai",  # API domain
    "http://localhost:3000",   # Local development
    "*"  # Allow all origins for API users
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "X-GitHub-Token"
    ],
    expose_headers=[
        "Content-Length",
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
        "X-Monthly-Limit",
        "X-Monthly-Remaining",
        "X-Monthly-Reset",
        "X-Billing-Rate"
    ],
    max_age=600,
)

# Include all routers
app.include_router(health_router)
app.include_router(slack_router)
app.include_router(projects_router)
app.include_router(projects_api_router)
for router in github_routers:
    app.include_router(router)
app.include_router(users_router)
app.include_router(users_api_router)
app.include_router(users_usage_router)
app.include_router(api_keys_router)
app.include_router(v2_api_router)
app.include_router(files_router)
app.include_router(files_api_router)
app.include_router(community_router)
app.include_router(billing_router)
app.include_router(nuanced_status_router)
app.include_router(projects.router)
app.include_router(data_sources_router)


# Mount the OpenAI compat router at both the root (for production) and at /v1 (for compatibility)
# This ensures both api.trynia.ai and api.trynia.ai/v1 work as override URLs
app.include_router(openai_compat_router)

# Also mount a duplicate router with /v1 prefix for backward compatibility
v1_prefixed_router = APIRouter(prefix="/v1")
for route in openai_compat_router.routes:
    v1_prefixed_router.routes.append(route)
app.include_router(v1_prefixed_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Nia AI API"}

# Run the app with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        timeout_keep_alive=120,  # Increase keep-alive timeout to 120 seconds
        limit_concurrency=20,    # Limit concurrent connections
    )
