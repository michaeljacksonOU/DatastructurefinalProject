import json
from student_service import StudentService


def load_students(filepath: str) -> list[dict]:
    """Load raw student records from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_students(filepath: str, students: list[dict]) -> None:
    """
    Write the current student list back to the JSON file.
    We save sorted by student_id so the file stays tidy and
    diffs are readable across sessions.
    """
    sorted_students = sorted(students, key=lambda s: s["student_id"])
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sorted_students, f, indent=2, ensure_ascii=False)


def build_service(students: list[dict]) -> StudentService:
    """
    Populate a StudentService with the given records.
    Inserts into all three data structures (linked list, hash table, BST).
    """
    service = StudentService()
    for s in students:
        service.add(s)
    return service