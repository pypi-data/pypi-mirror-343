import requests
import json
import time
import os
from typing import Dict, Any, Optional, Generator
from rich.console import Console

from nia_cli.config import API_BASE_URL
from nia_cli.auth import get_auth_headers

console = Console()

# Default timeout values (in seconds)
DEFAULT_TIMEOUT = 600
DEFAULT_STREAM_TIMEOUT = 600
class ApiError(Exception):
    """API error"""
    pass

def api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    retries: int = 3,
    retry_delay: float = 1.0,
    timeout: Optional[int] = None
) -> Any:
    """
    Make an authenticated API request with retries
    
    Args:
        method: HTTP method to use
        endpoint: API endpoint
        data: Request data
        params: Query parameters
        headers: Additional headers
        retries: Number of retries
        retry_delay: Delay between retries
        timeout: Request timeout in seconds (overrides default)
    """
    url = f"{API_BASE_URL}{endpoint}"
    auth_headers = get_auth_headers()
    all_headers = {**auth_headers, **(headers or {})}
    
    # Use provided timeout or fall back to default
    request_timeout = timeout or DEFAULT_TIMEOUT
    
    for attempt in range(retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=all_headers,
                timeout=request_timeout
            )
            
            response.raise_for_status()
            
            # Try to get JSON response
            try:
                response_data = response.json()
                
                # For v2 API, check if we have a success field
                if isinstance(response_data, dict) and "success" in response_data:
                    if not response_data["success"]:
                        # This is an error response
                        error_detail = response_data.get("error", {}).get("message", "Unknown error")
                        raise ApiError(f"API error: {error_detail}")
                
                return response_data
            except json.JSONDecodeError:
                # Return raw text if not JSON
                return response.text
                
        except requests.RequestException as e:
            if attempt == retries - 1:
                # This is the last attempt
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        # Try to parse as JSON
                        error_data = e.response.json()
                        # Handle API error format
                        if isinstance(error_data, dict):
                            if "error" in error_data:
                                error_message = error_data["error"].get("message", str(e))
                            elif "detail" in error_data:
                                error_message = error_data.get("detail", str(e))
                            else:
                                error_message = str(error_data)
                    except:
                        # If not JSON, get text content
                        try:
                            error_message = e.response.text
                        except:
                            error_message = str(e)
                else:
                    error_message = str(e)
                
                raise ApiError(f"API error: {error_message}")
            
            # Wait before retrying
            time.sleep(retry_delay * (attempt + 1))

def stream_api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None
) -> Generator[str, None, None]:
    """
    Make a streaming API request
    
    Args:
        method: HTTP method to use
        endpoint: API endpoint
        data: Request data
        params: Query parameters
        headers: Additional headers
        timeout: Request timeout in seconds (overrides default)
    """
    url = f"{API_BASE_URL}{endpoint}"
    auth_headers = get_auth_headers()
    all_headers = {**auth_headers, **(headers or {})}
    
    # Use provided timeout or fall back to default
    stream_timeout = timeout or DEFAULT_STREAM_TIMEOUT
    
    with requests.request(
        method=method,
        url=url,
        json=data,
        params=params,
        headers=all_headers,
        stream=True,
        timeout=stream_timeout
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                yield line.decode('utf-8')