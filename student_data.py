import json


def load_students(filepath: str) -> list[dict]:
    """Load student records from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)