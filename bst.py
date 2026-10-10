"""
BST implementation adapted for storing Contact objects,
keyed by contact name.
"""

class Contact:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Contact({self.name}, {self.phone}, {self.email})"


class Node:
    def __init__(self, contact: Contact):
        self.contact = contact
        self.left = None
        self.right = None


class ContactBST:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, contact: Contact):
        key = contact.name.lower()
        if self.root is None:
            self.root = Node(contact)
            self._size += 1
            return True

        current = self.root
        while True:
            curr_key = current.contact.name.lower()
            if key == curr_key:
                # Update contact if name already exists
                current.contact = contact
                return False
            elif key < curr_key:
                if current.left is None:
                    current.left = Node(contact)
                    self._size += 1
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(contact)
                    self._size += 1
                    return True
                current = current.right

    def search(self, name: str):
        key = name.lower()
        current = self.root
        while current is not None:
            curr_key = current.contact.name.lower()
            if key == curr_key:
                return current.contact
            current = current.left if key < curr_key else current.right
        return None

    def delete(self, name: str):
        key = name.lower()
        if self.search(name) is not None:
            self.root = self._delete(self.root, key)
            self._size -= 1
            return True
        return False

    def _delete(self, node, key):
        if node is None:
            return None

        node_key = node.contact.name.lower()
        if key < node_key:
            node.left = self._delete(node.left, key)
        elif key > node_key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Two-child case: find in-order successor
            successor = node.right
            while successor.left is not None:
                successor = successor.left

            node.contact = successor.contact
            node.right = self._delete(node.right, successor.contact.name.lower())

        return node

    def inorder(self):
        result = []

        def walk(node):
            if node is not None:
                walk(node.left)
                result.append(node.contact)
                walk(node.right)

        walk(self.root)
        return result