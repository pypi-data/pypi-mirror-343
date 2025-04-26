import os
import json
from typing import Optional, Dict
import requests
from rich.console import Console
from rich.prompt import Prompt

from nia_cli.config import load_config, save_config, API_BASE_URL

from dotenv import load_dotenv


load_dotenv()

console = Console()

def login(api_key: Optional[str] = None):
    """
    Authenticate with NIA using an API key
    """
    config = load_config()
    
    if not api_key:
        api_key = Prompt.ask("[bold]Enter your NIA API key[/]", password=True)
    
    # Validate the API key against the backend
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "nia-cli/0.1.0",
            "X-Nia-Client": "nia-cli"
        }
        
        
        # Validate against v2 API
        console.print("[bold yellow]Validating API key...[/]")
        
        response = requests.get(
            f"{API_BASE_URL}/v2/repositories", 
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            error_msg = "Invalid API key or server error"
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and "detail" in error_data:
                    error_msg = error_data["detail"]
            except:
                if response.text:
                    error_msg = response.text[:100]
                else:
                    error_msg = f"HTTP {response.status_code}"
            
            raise Exception(f"API key validation failed: {error_msg}")
        
        # Try to show how many repositories we found
        try:
            repos = response.json()
            num_repos = len(repos) if isinstance(repos, list) else 0
        except:
            pass
        
        # Save the API key in the config
        config.api_key = api_key
        config.user_id = "me"  # Use "me" as a special value for user_id
        save_config(config)
        
        console.print(f"[bold green]Successfully authenticated[/]")
        
        return True
    except Exception as e:
        console.print(f"[bold red]Authentication failed: {str(e)}[/]")
        return False

def get_auth_headers() -> Dict[str, str]:
    """
    Return headers with API key for authenticated requests
    """
    config = load_config()
    if not config.api_key:
        raise Exception("Not authenticated. Please run 'nia login' first.")
    
    return {
        "Authorization": f"Bearer {config.api_key}",
        "User-Agent": "nia-cli/0.1.0",
        "X-Nia-Client": "nia-cli"
    }