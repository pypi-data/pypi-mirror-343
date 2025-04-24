#!/usr/bin/env python3
"""
Configuration management for Mintlify Changelog.

Handles loading, saving, and validating user configuration settings.
"""
import os
import json
import keyring
from pathlib import Path
from typing import Dict, Any, Optional

# Constants
APP_NAME = "mintlify-changelog"
CONFIG_DIR = Path(os.path.expanduser("~/.config/mintlify"))
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "api": {
        "base_url": "https://mintlify-take-home.com",
        "endpoint": "/api/message",
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 4096,
        "temperature": 0.5,
        "timeout": 60
    },
    "defaults": {
        "count": 20, 
        "output_format": "markdown",
        "show_emoji": True,
        "min_group_size": 3,  # Group similar commits when ≥ this number
        "theme": "default"
    },
    "templates": {
        "default": {
            "categories": [
                {"name": "New Features", "emoji": "✨", "patterns": ["add", "new", "feat", "implement", "introduce"]},
                {"name": "Changes & Improvements", "emoji": "🔄", "patterns": ["change", "update", "improve", "enhance", "refactor", "perf"]},
                {"name": "Bug Fixes", "emoji": "🐛", "patterns": ["fix", "bug", "issue", "resolve", "patch"]},
                {"name": "Documentation", "emoji": "📚", "patterns": ["doc", "readme", "changelog", "comment"]},
                {"name": "Development", "emoji": "🧰", "patterns": ["test", "dev", "build", "ci", "chore", "deps", "bump"]},
                {"name": "Security", "emoji": "🔒", "patterns": ["security", "auth", "secure", "vulnerability", "cve"]}
            ]
        },
        "conventional": {
            "categories": [
                {"name": "Features", "emoji": "✨", "patterns": ["feat"]},
                {"name": "Bug Fixes", "emoji": "🐛", "patterns": ["fix"]},
                {"name": "Documentation", "emoji": "📚", "patterns": ["docs"]},
                {"name": "Styles", "emoji": "💎", "patterns": ["style"]},
                {"name": "Refactoring", "emoji": "♻️", "patterns": ["refactor"]},
                {"name": "Performance", "emoji": "⚡", "patterns": ["perf"]},
                {"name": "Tests", "emoji": "🧪", "patterns": ["test"]},
                {"name": "Build", "emoji": "🔧", "patterns": ["build"]},
                {"name": "CI", "emoji": "🤖", "patterns": ["ci"]},
                {"name": "Chore", "emoji": "🔨", "patterns": ["chore"]},
                {"name": "Revert", "emoji": "⏪", "patterns": ["revert"]}
            ]
        },
        "minimal": {
            "categories": [
                {"name": "Added", "emoji": "+", "patterns": ["add", "new", "feat", "implement"]},
                {"name": "Changed", "emoji": "~", "patterns": ["change", "update", "improve", "refactor"]},
                {"name": "Fixed", "emoji": "*", "patterns": ["fix", "bug", "issue", "resolve"]},
                {"name": "Other", "emoji": "•", "patterns": []}
            ]
        }
    }
}


def ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load configuration from file, or create default if not exists."""
    ensure_config_dir()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            # Merge with defaults in case config file is missing keys
            return _merge_config(DEFAULT_CONFIG, config)
    except Exception as e:
        print(f"Warning: Could not load config file: {e}. Using defaults.")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save config file: {e}")


def _merge_config(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge user config with default config."""
    result = default.copy()
    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_config(result[key], value)
        else:
            result[key] = value
    return result


def get_api_key() -> Optional[str]:
    """Get API key from keyring or environment variable."""
    # Try keyring first
    try:
        key = keyring.get_password(APP_NAME, "api_key")
        if key:
            return key
    except Exception:
        pass
    
    # Try environment variable
    return os.getenv("MINTLIFY_API_KEY")


def set_api_key(api_key: str) -> None:
    """Store API key in keyring."""
    try:
        keyring.set_password(APP_NAME, "api_key", api_key)
    except Exception as e:
        print(f"Warning: Could not store API key in keyring: {e}")
        print("Your API key will not be saved. Set MINTLIFY_API_KEY environment variable instead.")


def get_template(name: str = "default") -> Dict[str, Any]:
    """Get a specific template by name."""
    config = load_config()
    templates = config.get("templates", {})
    return templates.get(name, templates.get("default", DEFAULT_CONFIG["templates"]["default"]))


def get_default_count() -> int:
    """Get default commit count from config."""
    config = load_config()
    return config.get("defaults", {}).get("count", DEFAULT_CONFIG["defaults"]["count"])


def get_api_config() -> Dict[str, Any]:
    """Get API configuration."""
    config = load_config()
    return config.get("api", DEFAULT_CONFIG["api"])


def update_config_value(key_path: str, value: Any) -> None:
    """Update a specific config value by dot-notation path.
    
    Example: update_config_value("api.temperature", 0.7)
    """
    config = load_config()
    parts = key_path.split('.')
    
    # Navigate to the correct part of the config
    current = config
    for i, part in enumerate(parts[:-1]):
        if part not in current:
            current[part] = {}
        current = current[part]
    
    # Set the value
    current[parts[-1]] = value
    save_config(config)
