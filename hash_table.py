"""
Hash table — O(1) average-case lookup by student_id.

Python's built-in dict IS a hash table (open-addressing with
pseudo-random probing), so we wrap it here to expose a named
interface that matches the project's data-structure design.
"""
from typing import Optional, Any


class HashTable:
    def __init__(self):
        self._data: dict = {}

    def insert(self, key: Any, value: Any) -> None:
        """Insert or overwrite the value for key."""
        self._data[key] = value

    def lookup(self, key: Any) -> Optional[Any]:
        """Return the value for key, or None if not present."""
        return self._data.get(key)

    def delete(self, key: Any) -> bool:
        """Remove key. Returns True if it existed, False otherwise."""
        if key in self._data:
            del self._data[key]
            return True
        return False

    def contains(self, key: Any) -> bool:
        return key in self._data

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)