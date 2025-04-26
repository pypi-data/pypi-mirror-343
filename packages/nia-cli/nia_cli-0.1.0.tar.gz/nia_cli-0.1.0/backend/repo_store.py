import os
import json
from typing import Dict, Optional, Any

def get_user_store_file(user_id: str) -> str:
    return f"/tmp/nozomio_repo_store_{user_id}.json"

def load_store(user_id: str) -> Dict[str, Any]:
    store_file = get_user_store_file(user_id)
    if os.path.exists(store_file):
        with open(store_file, "r") as f:
            return json.load(f)
    return {"repos": {}}

def save_store(store: Dict[str, Any], user_id: str):
    store_file = get_user_store_file(user_id)
    with open(store_file, "w") as f:
        json.dump(store, f, indent=2)

def add_repo_to_store(repo_id: str, repo_url: str, user_id: str):
    store = load_store(user_id)
    store["repos"][repo_id] = {
        "repoUrl": repo_url,
    }
    save_store(store, user_id)

def list_repos(user_id: str) -> Dict[str, Dict[str, str]]:
    store = load_store(user_id)
    return store["repos"]

def get_repo(repo_id: str, user_id: str) -> Optional[Dict[str, str]]:
    store = load_store(user_id)
    return store["repos"].get(repo_id)
