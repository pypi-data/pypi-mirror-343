"""
OpenAI-compatible API endpoints for Cursor integration.

This module implements API endpoints that are compatible with OpenAI's API format,
allowing Cursor AI to use Nia's capabilities as a drop-in replacement for OpenAI models.
"""
import logging
import time
import uuid
import json
import asyncio
from typing import Dict, List, Any, Optional, Generator, AsyncGenerator, Tuple
from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from api_store import validate_api_key, increment_api_usage, simple_validate_api_key, get_user_api_keys
from project_store import get_project, list_projects
from chat_store import add_chat_message, create_new_chat
from utils.retriever_utils import fallback_pinecone_retrieval
from utils import format_context, safe_json_dumps
from llm import llm_generate

# Import NuancedService if available
try:
    from services.nuanced_service import NuancedService
    nuanced_available = True
except ImportError:
    nuanced_available = False

# Create logger
logger = logging.getLogger(__name__)

# Create router - Remove the prefix to allow direct API domain usage 
router = APIRouter(tags=["openai-compat"])

class Message(BaseModel):
    role: str
    content: str
    name: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    user: Optional[str] = None
    
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletion(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage

class ChunkDelta(BaseModel):
    content: Optional[str] = None

class ChunkChoice(BaseModel):
    index: int
    delta: ChunkDelta
    finish_reason: Optional[str] = None

class ChatCompletionChunk(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChunkChoice]

def get_api_key_from_header(request: Request) -> Dict[str, Any]:
    """Extract and validate API key from Authorization header."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing API key")
    
    key = auth.replace("Bearer ", "")
    api_key_doc = validate_api_key(key)
    if not api_key_doc:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key_doc

async def get_project_for_api_key(api_key_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Get the project associated with the API key or the most recent one."""
    user_id = api_key_doc.get("user_id")
    
    # Check if this is a Cursor API key with a specific project_id
    metadata = api_key_doc.get("metadata", {})
    if metadata and metadata.get("type") == "cursor_integration":
        # Store the fact that this is a Cursor request in the api_key_doc
        # This will be used later to determine whether to include sources
        api_key_doc["is_cursor_request"] = True
        
        project_id = metadata.get("project_id")
        if project_id:  # Only proceed if project_id is not None
            project = get_project(project_id, user_id)
            if project and project.get("status") == "indexed":
                return project
    
    # If this is a request from the MCP client, try to find the right project for this API key
    if api_key_doc.get("is_mcp_request", False) and api_key_doc.get("key"):
        key = api_key_doc.get("key")
        # Get all API keys for this user and check for a match with project_id
        all_keys = get_user_api_keys(user_id)
        for key_data in all_keys:
            if key_data.get("key") == key and key_data.get("metadata", {}).get("project_id"):
                project_id = key_data.get("metadata", {}).get("project_id")
                project = get_project(project_id, user_id)
                if project and project.get("status") == "indexed":
                    # Mark this as a Cursor request for source handling consistency
                    api_key_doc["is_cursor_request"] = True
                    logger.info(f"MCP client using API key matched to project: {project_id}")
                    return project
    
    # Fallback to most recent project
    return await get_most_recent_project(user_id)

async def get_most_recent_project(user_id: str) -> Dict[str, Any]:
    """Get the most recent project for a user."""
    projects = list_projects(user_id)
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found for this user")
    
    # Find indexed projects
    indexed_projects = {k: v for k, v in projects.items() if v.get("status") == "indexed"}
    if not indexed_projects:
        raise HTTPException(status_code=404, detail="No indexed projects found for this user")
    
    # Sort by last_updated
    sorted_projects = sorted(
        indexed_projects.values(), 
        key=lambda x: x.get("last_updated", 0), 
        reverse=True
    )
    
    return sorted_projects[0]

async def get_context_for_prompt(user_id: str, project_id: str, messages: List[Message]) -> Tuple[str, List[str]]:
    """Retrieve context for the prompt from the repository."""
    # Extract the user message - typically the last one in the messages list
    user_messages = [m.content for m in messages if m.role == "user"]
    if not user_messages:
        return "", []
    
    query = user_messages[-1]  # Use the last user message as query
    
    # Retrieve context using the query with fallback_pinecone_retrieval
    project_config = [{
        "project_id": project_id,
        "user_id": user_id,
        "index_name": "nia-app",
        "is_community": False
    }]
    
    try:
        # Check if this is a query that would benefit from GraphRAG
        should_use_graph_rag = is_graph_appropriate_query(query)
        
        # Set use_nuanced=True to enable Nuanced enhancement if available
        # and use_graph_rag=True if the query is appropriate for GraphRAG
        _, contexts, sources = await fallback_pinecone_retrieval(
            prompt=query,
            project_configs=project_config,
            use_nuanced=nuanced_available and not should_use_graph_rag,  # Enable Nuanced enhancement if available and not using GraphRAG
            use_graph_rag=should_use_graph_rag,  # Enable GraphRAG when appropriate
            user_id=user_id  # Add user_id for data isolation
        )
        
        # Add Nuanced/GraphRAG status to logs
        if should_use_graph_rag:
            logger.info(f"Using GraphRAG-enhanced context for query: {query[:50]}...")
        elif nuanced_available:
            logger.info(f"Using Nuanced-enhanced context for query: {query[:50]}...")
        
        # Format the context
        formatted_context = format_context(sources, contexts)
        return formatted_context, sources
    except Exception as e:
        logging.error(f"Error retrieving context: {e}")
        return "", []

def is_graph_appropriate_query(query: str) -> bool:
    """Determine if a query is appropriate for GraphRAG instead of traditional RAG.
    
    Args:
        query: The user query string
        
    Returns:
        True if GraphRAG is appropriate for this query
    """
    # Pattern matching for structural/relationship questions
    import re
    
    # Check if the query is about code structure, architecture, relationships
    structure_patterns = [
        r'(code|system|software)\s+(structure|architecture|design|organization)',
        r'(how|what)\s+(does|is)\s+the\s+(structure|architecture)',
        r'(show|explain|describe)\s+(me)?\s+.*\s+(structure|architecture|design)',
        r'overview\s+of\s+.*\s+(code|system|architecture)',
        r'components?\s+of\s+.*\s+(system|codebase)',
        r'(relationship|relate|connection)\s+between',
        r'(how|what).*components.*interact',
        r'(visualize|visualise|graph)\s+.*\s+codebase',
        r'(function|method|class).*calls?',
        r'(dependency|dependencies|depends)',
        r'(who|what).*calls',
        r'call\s+(graph|hierarchy|tree|structure)',
        r'(execution|call|dependency)\s+(flow|path|trace)',
        r'(high|top)(\s|-)level\s+(view|overview)',
        r'functions?\s+group',
        r'module\s+organization',
    ]
    
    # Check for matches
    for pattern in structure_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            logger.info(f"Query matches GraphRAG pattern: {pattern}")
            return True
    
    # Check for community/global level analysis terms
    community_patterns = [
        r'(group|cluster|communit(y|ies))\s+of\s+(function|class|method)',
        r'related\s+(function|class|method)',
        r'(closely|tightly)\s+coupled',
        r'(module|component|subsystem)',
        r'(functional|logical)\s+(group|unit)',
        r'(breakdown|break\s+down|decompose)',
    ]
    
    for pattern in community_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            logger.info(f"Query matches GraphRAG community pattern: {pattern}")
            return True
    
    return False

async def stream_chat_completion(
    completion_id: str,
    model: str,
    messages: List[Message],
    context: str,
    sources: List[str],
    timestamp: int,
    api_key_doc: Dict[str, Any] = None
) -> AsyncGenerator[str, None]:
    """Stream chat completion as server-sent events."""
    # First, yield the start of the stream
    start_chunk = ChatCompletionChunk(
        id=completion_id,
        object="chat.completion.chunk",
        created=timestamp,
        model=model,
        choices=[
            ChunkChoice(
                index=0,
                delta=ChunkDelta(content=""),
                finish_reason=None
            )
        ]
    )
    yield f"data: {start_chunk.json()}\n\n"
    
    # Start generating the response
    prompt = prepare_prompt(messages, context)
    
    # llm_generate returns a coroutine that needs to be awaited first
    # Add retry mechanism for first connection
    max_retries = 3
    retry_count = 0
    last_error = None
    
    while retry_count < max_retries:
        try:
            generator = await llm_generate(prompt, stream=True)
            break
        except Exception as e:
            retry_count += 1
            last_error = e
            logging.warning(f"Attempt {retry_count}/{max_retries} failed: {str(e)}")
            if retry_count < max_retries:
                await asyncio.sleep(1)  # Wait before retrying
            else:
                logging.error(f"Failed to connect after {max_retries} attempts: {str(last_error)}")
                # Send error message as a chunk
                error_chunk = ChatCompletionChunk(
                    id=completion_id,
                    object="chat.completion.chunk",
                    created=timestamp,
                    model=model,
                    choices=[
                        ChunkChoice(
                            index=0,
                            delta=ChunkDelta(content="Sorry, there was an error connecting to the AI service. Please try again."),
                            finish_reason="error"
                        )
                    ]
                )
                yield f"data: {error_chunk.json()}\n\n"
                yield "data: [DONE]\n\n"
                return
    
    # Set up a keepalive mechanism to prevent timeouts
    last_chunk_time = time.time()
    
    full_content = ""
    async for chunk in generator:
        # Reset the last chunk time
        last_chunk_time = time.time()
        
        # Save current chunk
        full_content += chunk
        
        # Format each chunk as OpenAI would
        response_chunk = ChatCompletionChunk(
            id=completion_id,
            object="chat.completion.chunk",
            created=timestamp,
            model=model,
            choices=[
                ChunkChoice(
                    index=0,
                    delta=ChunkDelta(content=chunk),
                    finish_reason=None
                )
            ]
        )
        
        yield f"data: {response_chunk.json()}\n\n"
        
        # Add a small delay to prevent overwhelming the client
        await asyncio.sleep(0.01)
    
    # After the main content is done, add sources as a separate chunk if sources exist
    # But only if this is not a Cursor request
    is_cursor_request = False
    # Check if this is a Cursor request based on api_key_doc that should be available
    # in the outer function scope
    try:
        is_cursor_request = api_key_doc.get("is_cursor_request", False)
    except NameError:
        # If api_key_doc is not available, assume it's not a Cursor request
        pass
    
    if sources and not is_cursor_request:
        sources_text = "\n\n**Sources:**\n" + "\n".join([f"- `{source}`" for source in sources])
        sources_chunk = ChatCompletionChunk(
            id=completion_id,
            object="chat.completion.chunk",
            created=timestamp,
            model=model,
            choices=[
                ChunkChoice(
                    index=0,
                    delta=ChunkDelta(content=sources_text),
                    finish_reason=None
                )
            ]
        )
        yield f"data: {sources_chunk.json()}\n\n"
    
    # End the stream
    end_chunk = ChatCompletionChunk(
        id=completion_id,
        object="chat.completion.chunk",
        created=timestamp,
        model=model,
        choices=[
            ChunkChoice(
                index=0,
                delta=ChunkDelta(content=None),
                finish_reason="stop"
            )
        ]
    )
    yield f"data: {end_chunk.json()}\n\n"
    yield "data: [DONE]\n\n"

def prepare_prompt(messages: List[Message], context: str) -> str:
    """Prepare the prompt for the LLM with context."""
    prompt_parts = []
    
    # Add system message if present
    system_messages = [m for m in messages if m.role == "system"]
    if system_messages:
        prompt_parts.append(f"System: {system_messages[0].content}")
    
    # Add context section
    if context:
        prompt_parts.append(f"Context from repositories:\n{context}")
    
    # Add conversation history
    for msg in messages:
        if msg.role == "system":
            continue  # Already handled
        role_name = "User" if msg.role == "user" else "Assistant"
        prompt_parts.append(f"{role_name}: {msg.content}")
    
    return "\n\n".join(prompt_parts)

async def generate_non_streaming_response(
    completion_id: str,
    model: str,
    messages: List[Message],
    context: str,
    sources: List[str],
    timestamp: int,
    api_key_doc: Dict[str, Any] = None
) -> ChatCompletion:
    """Generate non-streaming response in OpenAI format."""
    prompt = prepare_prompt(messages, context)
    
    # For non-streaming, we just get the full response at once
    full_content = await llm_generate(prompt, stream=False)
    
    # Check if this is a Cursor request
    is_cursor_request = api_key_doc.get("is_cursor_request", False)
    
    # Add sources to the response if they exist and this is not a Cursor request
    if sources and not is_cursor_request:
        sources_text = "\n\n**Sources:**\n" + "\n".join([f"- `{source}`" for source in sources])
        full_content_with_sources = full_content + sources_text
    else:
        full_content_with_sources = full_content
    
    # Create OpenAI-compatible response
    return ChatCompletion(
        id=completion_id,
        object="chat.completion",
        created=timestamp,
        model=model,
        choices=[
            Choice(
                index=0,
                message=Message(
                    role="assistant",
                    content=full_content_with_sources
                ),
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=len(prompt) // 4,  # Rough approximation
            completion_tokens=len(full_content_with_sources) // 4,  # Rough approximation
            total_tokens=(len(prompt) + len(full_content_with_sources)) // 4  # Rough approximation
        )
    )

@router.post("/chat/completions")
async def chat_completions(
    request: Request,
    chat_request: ChatCompletionRequest,
    background_tasks: BackgroundTasks
):
    """OpenAI-compatible chat completions endpoint."""
    # Extract and validate API key
    api_key_doc = get_api_key_from_header(request)
    user_id = api_key_doc.get("user_id")
    
    # Check for MCP client based on User-Agent or other headers
    user_agent = request.headers.get("User-Agent", "")
    if "nia-mcp" in user_agent or request.headers.get("X-Nia-MCP-Client"):
        # Flag this as an MCP client request
        api_key_doc["is_mcp_request"] = True
        logger.info(f"Detected MCP client request with API key: {api_key_doc.get('key', '')[:8]}...")
    
    # Check if this is just a verification request (Cursor does this with minimal content)
    is_verification_request = (
        len(chat_request.messages) == 1 and
        chat_request.messages[0].role == "user" and
        len(chat_request.messages[0].content.strip()) < 50 and
        "verify" in chat_request.messages[0].content.lower()
    )
    
    # If this appears to be just a verification request, respond quickly with minimal processing
    if is_verification_request:
        logger.info("Detected API key verification request, responding quickly")
        completion_id = f"nia-{int(time.time())}"
        timestamp = int(time.time())
        
        return ChatCompletion(
            id=completion_id,
            object="chat.completion",
            created=timestamp,
            model=chat_request.model,
            choices=[
                Choice(
                    index=0,
                    message=Message(
                        role="assistant",
                        content="API key verified successfully. You can now use Nia AI with Cursor."
                    ),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=10,
                completion_tokens=15,
                total_tokens=25
            )
        )
    
    # Get the project for this API key
    project = await get_project_for_api_key(api_key_doc)
    project_id = project.get("id")
    
    # Get context for the user's prompt
    context, sources = await get_context_for_prompt(user_id, project_id, chat_request.messages)
    
    # Generate a completion ID and timestamp
    completion_id = f"nia-{int(time.time())}"
    timestamp = int(time.time())
    
    # Create a new chat if needed for tracking
    chat_id = f"cursor-{completion_id}"
    create_new_chat(user_id, project_id, "Cursor Chat")
    
    # Track last user message for history
    user_messages = [m for m in chat_request.messages if m.role == "user"]
    if user_messages:
        last_user_message = user_messages[-1].content
        background_tasks.add_task(
            add_chat_message, 
            project_id=project_id, 
            chat_id=chat_id, 
            role="user", 
            content=last_user_message, 
            user_id=user_id
        )
    
    # For Cursor integration with Pro subscription, we don't want to track API usage
    if not api_key_doc.get("is_cursor_request", False):
        # Only track API usage for non-Cursor requests
        background_tasks.add_task(
            increment_api_usage,
            key=api_key_doc.get("key"),  # Use "key" instead of "api_key_id"
            tokens=0,  # We'll update this later
            requests=1  # Count as one request
        )
    
    # Handle streaming vs non-streaming
    if chat_request.stream:
        # For streaming, we return a StreamingResponse
        return StreamingResponse(
            stream_chat_completion(
                completion_id,
                chat_request.model,
                chat_request.messages,
                context,
                sources,
                timestamp,
                api_key_doc  # Pass the api_key_doc to check if it's a Cursor request
            ),
            media_type="text/event-stream"
        )
    else:
        # For non-streaming, generate the full response
        response = await generate_non_streaming_response(
            completion_id,
            chat_request.model,
            chat_request.messages,
            context,
            sources,
            timestamp,
            api_key_doc  # Pass the api_key_doc to check if it's a Cursor request
        )
        
        # Track assistant response for history
        assistant_content = response.choices[0].message.content
        background_tasks.add_task(
            add_chat_message,
            project_id=project_id,
            chat_id=chat_id,
            role="assistant",
            content=assistant_content,
            user_id=user_id
        )
        
        return response

# Models endpoint
@router.get("/models")
async def list_models():
    """Return a list of available models (used for API key verification by Cursor)."""
    # Optimize this endpoint for fast response - it's used for API key verification
    # Don't perform any heavy operations here
    
    return {
        "object": "list",
        "data": [
            {"id": "gpt-4.1-2025-04-14", "object": "model"},
        ]
    }

@router.get("/validate")
async def validate_api_key_endpoint(authorization: Optional[str] = Header(None)):
    """
    Dedicated endpoint for API key validation that's extremely lightweight.
    This helps tools like Cursor validate API keys faster on first connection.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    api_key = authorization.replace("Bearer ", "")
    is_valid = simple_validate_api_key(api_key)
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {"status": "valid", "message": "API key is valid"}
