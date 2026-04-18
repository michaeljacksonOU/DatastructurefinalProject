"""
Doubly linked list — primary storage for student records.
"""
from typing import Optional, Iterator


class Node:
    __slots__ = ("student", "prev", "next")

    def __init__(self, student: dict):
        self.student: dict = student
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class LinkedList:
    """Doubly linked list of student records."""

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def append(self, student: dict) -> Node:
        """Insert at the tail. Returns the new node so callers can track it."""
        node = Node(student)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def remove_node(self, node: Node) -> None:
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = node.next = None
        self._size -= 1

    def __iter__(self) -> Iterator[dict]:
        curr = self.head
        while curr is not None:
            yield curr.student
            curr = curr.next

    def __len__(self) -> int:
        return self._size

    def to_list(self) -> list[dict]:
        return list(iter(self))