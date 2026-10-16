import json
from typing import Any


def load_json(filepath: str) -> Any:
    """Load JSON data from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, filepath: str, indent: int = 2) -> None:
    """Save data as JSON to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def validate_json(data: Any) -> bool:
    """Basic validation: check if data is a dict or list."""
    return isinstance(data, (dict, list))
