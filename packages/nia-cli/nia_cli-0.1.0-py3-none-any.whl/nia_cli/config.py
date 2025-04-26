import os
import json
from typing import Optional
from pydantic import BaseModel


# Get API URL from environment or use default
API_BASE_URL = os.environ.get("NIA_API_URL", "http://localhost:8000")

class Config(BaseModel):
    """Configuration for NIA CLI"""
    api_key: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    default_project: Optional[str] = None
    default_model: str = "claude-3-7-sonnet-latest"

def get_config_path() -> str:
    """Get the path to the config file"""
    config_dir = os.path.expanduser("~/.nia")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

def load_config() -> Config:
    """Load configuration from the config file"""
    config_path = get_config_path()
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return Config.model_validate(json.load(f))
        except:
            # Return default config if loading fails
            return Config()
    else:
        # Create default config if it doesn't exist
        config = Config()
        save_config(config)
        return config

def save_config(config: Config) -> None:
    """Save configuration to the config file"""
    config_path = get_config_path()
    
    with open(config_path, "w") as f:
        json.dump(config.model_dump(), f, indent=2)