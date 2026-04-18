"""
StudentService — the single source of truth for all mutations.

The GUI should NEVER touch the linked list / hash table / BST directly.
It goes through this service, which guarantees all three structures
stay in sync after every add / remove operation.

  Hash Table  →  O(1) lookup by student_id  (also stores node refs
                 for O(1) linked-list removal)
  Linked List →  primary store, iteration for filtering
  BST         →  sorted display via inorder traversal
"""
from typing import Optional
from linked_list import LinkedList, Node
from hash_table import HashTable
from bst import BST


class StudentService:
    def __init__(self):
        self._list = LinkedList()
        self._hash = HashTable()   # student_id → Node (linked list reference)
        self._bst = BST()

    # ── Mutations ────────────────────────────────────────────────────────
    def add(self, student: dict) -> bool:
        """Insert into all three structures. Returns False if ID already exists."""
        sid = student["student_id"]
        if sid in self._hash:
            return False
        node = self._list.append(student)
        self._hash.insert(sid, node)
        self._bst.insert(sid, student)
        return True

    def remove(self, student_id: int) -> bool:
        """Remove from all three structures. Returns False if ID not found."""
        node = self._hash.lookup(student_id)
        if node is None:
            return False
        self._list.remove_node(node)
        self._hash.delete(student_id)
        self._bst.delete(student_id)
        return True

    def modify(self, student_id: int, updates: dict) -> bool:
        node = self._hash.lookup(student_id)
        if node is None:
            return False
        # Mutate in place — linked list node, BST node, and hash table entry
        # all reference this same dict, so one update covers all three.
        for key, value in updates.items():
            if key == "student_id":
                continue  # never mutate the key
            node.student[key] = value
        return True

    # ── Queries ──────────────────────────────────────────────────────────
    def find(self, student_id: int) -> Optional[dict]:
        """O(1) lookup by ID via hash table."""
        node = self._hash.lookup(student_id)
        return node.student if node is not None else None

    def exists(self, student_id: int) -> bool:
        return student_id in self._hash

    def filter(self, major: str = "", last_name: str = "") -> list[dict]:
        """
        Return students matching the given substrings (case-insensitive).
        Iterates the BST inorder so results come back sorted by student_id.
        Empty strings mean "no filter" on that field.
        """
        major_q = major.strip().lower()
        last_q = last_name.strip().lower()
        result = []
        for s in self._bst.inorder():
            if major_q and major_q not in s.get("major", "").lower():
                continue
            if last_q and last_q not in s.get("last_name", "").lower():
                continue
            result.append(s)
        return result

    def get_all(self) -> list[dict]:
        """Insertion order (from the linked list)."""
        return self._list.to_list()

    def get_sorted(self) -> list[dict]:
        """Sorted by student_id (BST inorder)."""
        return self._bst.inorder()

    def __len__(self) -> int:
        return len(self._list)