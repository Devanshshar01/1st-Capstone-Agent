import json
import os
from typing import Dict, Any

def load_user_profile(file_path: str) -> Dict[str, Any]:
    """
    Loads user profile from a JSON file.
    """
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_user_profile(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Saves user profile to a JSON file.
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False
