import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".pseudo_runner_config.json"

def save_config(api_key, model):
    """
    Saves the API key and selected model to the configuration file.
    """
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"api_key": api_key, "model": model}, f)

def load_config():
    """
    Loads the saved configuration if it exists.
    """
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None