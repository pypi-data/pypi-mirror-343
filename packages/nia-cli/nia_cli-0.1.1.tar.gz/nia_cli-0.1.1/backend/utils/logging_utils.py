import os
import logging
import requests
from typing import List, Dict, Any, Optional

def log_to_keywords_ai(
    provider: str,
    model: str,
    messages: list,
    response: str,
    generation_time: float,
    user_id: str
):
    """
    Send prompt/response logs to Keywords AI for analytics.
    
    Args:
        provider: The LLM provider (e.g., 'anthropic', 'openai')
        model: The specific model used (e.g., 'claude-3-7-sonnet-20250219')
        messages: List of conversation messages
        response: The generated response text
        generation_time: Time taken to generate the response in seconds
        user_id: Unique identifier for the user
    """
    try:
        keywords_api_key = os.getenv("KEYWORDS_AI_API_KEY")
        if not keywords_api_key:
            logging.warning("KEYWORDS_AI_API_KEY not set, skipping logging")
            return
            
        url = "https://api.keywordsai.co/api/request-logs/create/"
        payload = {
            "model": model,
            "prompt_messages": messages,
            "completion_message": {
                "role": "assistant",
                "content": response
            },
            "generation_time": generation_time,
            "customer_params": {
                "customer_identifier": user_id
            }
        }
        headers = {
            "Authorization": f"Bearer {keywords_api_key}",
            "Content-Type": "application/json"
        }
        requests.post(url, headers=headers, json=payload)
        logging.debug(f"Successfully logged to Keywords AI for user {user_id}")
    except Exception as e:
        logging.error(f"Failed to log to Keywords AI: {e}")

def safe_json_dumps(obj: Dict[str, Any]) -> str:
    """
    Safely convert an object to a JSON string, handling any encoding errors.
    
    Args:
        obj: The object to convert to JSON
        
    Returns:
        A JSON string representation of the object
    """
    import json
    try:
        # Let json.dumps handle escaping
        return json.dumps(obj, ensure_ascii=False)
    except Exception as e:
        logging.error(f"JSON encoding error: {str(e)}")
        return json.dumps({"error": "Failed to encode response"})

def setup_logger(
    name: Optional[str] = None, 
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: The name of the logger (defaults to root logger if None)
        level: The logging level (defaults to INFO)
        format_string: Custom format string for log messages
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)
    
    # Create formatter
    if not format_string:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_string)
    
    # Add formatter to handler
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger 