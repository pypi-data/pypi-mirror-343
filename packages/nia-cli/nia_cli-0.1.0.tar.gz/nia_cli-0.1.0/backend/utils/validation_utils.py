import os
import re
from typing import Tuple, Optional, List, Dict, Any
from urllib.parse import urlparse
from uuid import UUID

def validate_github_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Securely validates and normalizes GitHub repository URLs.
    Returns (is_valid, normalized_url, error_message).
    
    Implements strict validation:
    - Only allows github.com domain
    - Proper URL parsing and normalization
    - Validates URL structure and components
    - Prevents SSRF through URL parsing tricks
    
    Args:
        url: The GitHub URL to validate
        
    Returns:
        Tuple of (is_valid, normalized_url, error_message)
    """
    try:
        # Normalize URL
        url = url.strip()
        
        # Parse URL
        parsed = urlparse(url)
        
        # Validate scheme
        if parsed.scheme not in ('https',):
            return False, None, "Only HTTPS URLs are allowed"
            
        # Validate and normalize hostname
        hostname = parsed.hostname.lower() if parsed.hostname else ''
        if hostname not in ('github.com', 'www.github.com'):
            return False, None, "Only github.com domain is allowed"
            
        # Remove www if present
        if hostname.startswith('www.'):
            hostname = hostname[4:]
            
        # Validate path format (should be /owner/repo)
        path_parts = [p for p in parsed.path.split('/') if p]
        if len(path_parts) != 2:
            return False, None, "Invalid repository path format"
            
        # Validate owner and repo names with updated pattern
        owner, repo = path_parts
        valid_chars = lambda s: all(c.isalnum() or c in '-_.' for c in s)
        if not all(part.strip() and valid_chars(part) for part in (owner, repo)):
            return False, None, "Invalid owner or repository name"
            
        # Remove .git extension if present
        if repo.endswith('.git'):
            repo = repo[:-4]
            
        # Construct normalized URL
        normalized = f"https://github.com/{owner}/{repo}"
        
        return True, normalized, None
        
    except Exception as e:
        return False, None, f"URL validation error: {str(e)}"

def validate_safe_path(base_dir: str, user_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Securely validates and normalizes file paths to prevent directory traversal.
    Returns (is_valid, normalized_path, error_message).
    
    Security measures:
    - Prevents directory traversal attacks
    - Ensures paths stay within base directory
    - Validates path components
    - Normalizes path separators
    
    Args:
        base_dir: The base directory that should contain the path
        user_path: The user-provided path to validate
        
    Returns:
        Tuple of (is_valid, normalized_path, error_message)
    """
    try:
        # Convert paths to absolute and normalize
        base_dir = os.path.abspath(base_dir)
        full_path = os.path.abspath(os.path.join(base_dir, user_path))
        
        # Check if the full path starts with base_dir
        if not full_path.startswith(base_dir):
            return False, None, "Path would escape base directory"
            
        # Validate path components
        path_parts = full_path.split(os.sep)
        for part in path_parts:
            # Skip empty parts
            if not part:
                continue
                
            # Allow standard path components
            if part in ('.', '..'):
                return False, None, "Invalid path component"
                
            # Check for dangerous characters
            if any(c in part for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']):
                return False, None, "Invalid path component"
                
            # Special handling for my_local_repo_ prefix
            if part.startswith('my_local_repo_'):
                try:
                    # Extract and validate UUID
                    potential_uuid = part.replace('my_local_repo_', '')
                    UUID(potential_uuid)
                except ValueError:
                    return False, None, "Invalid project ID format"
        
        return True, full_path, None
        
    except Exception as e:
        return False, None, f"Path validation error: {str(e)}"

def validate_file_path(file_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validates a file path for security concerns.
    
    Checks for directory traversal attempts and other security issues.
    
    Args:
        file_path: The file path to validate
        
    Returns:
        Tuple of (is_valid, normalized_path, error_message)
    """
    try:
        # Check for empty path
        if not file_path or not file_path.strip():
            return False, None, "File path is required"
            
        # Check for directory traversal attempts
        if '..' in file_path:
            return False, None, "Invalid file path: directory traversal not allowed"
            
        # Remove leading/trailing slashes and normalize path
        normalized_path = file_path.strip('/')
        
        # Check for other dangerous patterns
        dangerous_patterns = ['~/', './', '../', '//', '\\\\']
        if any(pattern in normalized_path for pattern in dangerous_patterns):
            return False, None, "Invalid file path: potentially unsafe path pattern"
            
        return True, normalized_path, None
        
    except Exception as e:
        return False, None, f"Path validation error: {str(e)}"

def validate_api_request(
    api_key: Optional[str] = None,
    required_params: Optional[Dict[str, Any]] = None
) -> Tuple[bool, Optional[str]]:
    """
    Validates an API request by checking the API key and required parameters.
    
    Args:
        api_key: The API key to validate
        required_params: Dictionary of required parameters and their values
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check API key if provided
    if api_key is not None and not api_key:
        return False, "Missing API key"
        
    # Check required parameters if provided
    if required_params:
        for param_name, param_value in required_params.items():
            if param_value is None:
                return False, f"Missing required parameter: {param_name}"
                
    return True, None 