from abc import ABC, abstractmethod
from typing import Any


class DataStore(ABC):
    """Abstract base class for dictionary-like data access."""

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def all(self) -> dict:
        pass



import os
import json
import uuid
try:
    import yaml
except ImportError:
    yaml = None

class DictDataStore(DataStore):
    """
    DataStore implementation supporting both JSON and YAML files.
    Uses file extension to select loader/saver.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.yaml', '.yml']:
            if yaml is None:
                raise ImportError('pyyaml is required for YAML support')
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)
        elif ext == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            raise ValueError('Unsupported file type: ' + ext)

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()

    def delete(self, key: str) -> None:
        if key in self.data:
            del self.data[key]
            self._save()

    def all(self) -> dict:
        return self.data

    def _save(self) -> None:
        ext = os.path.splitext(self.filepath)[1].lower()
        if ext in ['.yaml', '.yml']:
            if yaml is None:
                raise ImportError('pyyaml is required for YAML support')
            with open(self.filepath, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.data, f, default_flow_style=False, allow_unicode=True)
        elif ext == '.json':
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError('Unsupported file type: ' + ext)

# Example usage:
# store = DictDataStore('path/to/data.json')
# store = DictDataStore('path/to/data.yaml')
# value = store.get('some_key')
# store.set('some_key', new_value)
# store.delete('some_key')
# all_data = store.all()

# Later, you can add a SqliteDataStore class with the same interface.
