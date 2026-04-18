"""
Binary Search Tree — keyed on student_id, used for sorted display
via inorder traversal.

Note: this is an unbalanced BST. If IDs are inserted in sorted order
(as they are in mock_data.json: 1, 2, 3, ...), the tree degenerates
into a right-leaning chain and search becomes O(n). Inorder traversal
still produces correctly sorted output — it's only search/insert
performance that suffers. Upgrading to an AVL or Red-Black tree would
fix this if the dataset grows large.
"""
from typing import Optional


class BSTNode:
    __slots__ = ("key", "student", "left", "right")

    def __init__(self, key: int, student: dict):
        self.key: int = key
        self.student: dict = student
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


class BST:
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size: int = 0

    # ── Insert ───────────────────────────────────────────────────────────
    def insert(self, key: int, student: dict) -> None:
        self.root, inserted = self._insert(self.root, key, student)
        if inserted:
            self._size += 1

    def _insert(self, node: Optional[BSTNode], key: int, student: dict):
        if node is None:
            return BSTNode(key, student), True
        if key < node.key:
            node.left, inserted = self._insert(node.left, key, student)
        elif key > node.key:
            node.right, inserted = self._insert(node.right, key, student)
        else:
            # Same key — overwrite the student record, no size change
            node.student = student
            inserted = False
        return node, inserted

    # ── Search ───────────────────────────────────────────────────────────
    def search(self, key: int) -> Optional[dict]:
        node = self.root
        while node is not None:
            if key == node.key:
                return node.student
            node = node.left if key < node.key else node.right
        return None

    # ── Delete ───────────────────────────────────────────────────────────
    def delete(self, key: int) -> bool:
        """Returns True if a node was removed, False if key wasn't found."""
        if self.search(key) is None:
            return False
        self.root = self._delete(self.root, key)
        self._size -= 1
        return True

    def _delete(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Found the node to delete
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Two children: replace with inorder successor (leftmost of right subtree)
            succ = node.right
            while succ.left is not None:
                succ = succ.left
            node.key, node.student = succ.key, succ.student
            node.right = self._delete(node.right, succ.key)
        return node

    # ── Traversal ────────────────────────────────────────────────────────
    def inorder(self) -> list[dict]:
        """Returns all students sorted by student_id."""
        result: list[dict] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[BSTNode], result: list) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.student)
        self._inorder(node.right, result)

    def __len__(self) -> int:
        return self._size