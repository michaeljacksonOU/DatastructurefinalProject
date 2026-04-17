import json


def load_students(filepath: str) -> list[dict]:
    """Load student records from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def build_hash_table(students: list[dict]) -> dict:
    """Build a hash table keyed by student_id for O(1) lookups."""
    return {s["student_id"]: s for s in students}