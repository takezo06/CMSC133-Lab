from collections import deque


class Node:
    """Represents a single node in a Binary Search Tree."""

    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation."""

    def __init__(self):
        self.root = None

    # --- INSERTION ---
    def insert(self, val):
        """Public method to insert a value into the BST."""
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        # Base case: Found an empty spot, place the new node here
        if node is None:
            return Node(val)

        # Enforce BST Rule: Lesser values left, greater values right
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)

        # Duplicate values are ignored to maintain set property
        return node

    # --- DELETION ---
    def delete(self, val):
        """Public method to delete a value from the BST."""
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if node is None:
            return node

        # Navigate tree to find the node
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Node found. Handle the 3 deletion scenarios:

            # Case 1 & 2: Node with 0 or 1 child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 3: Node with 2 children
            # Find the in-order successor (smallest value in the right subtree)
            successor = self._min_value_node(node.right)
            # Copy successor's value to current node
            node.val = successor.val
            # Recursively delete the successor
            node.right = self._delete(node.right, successor.val)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # --- TRAVERSALS ---
    def inorder(self):
        """In-order Traversal: Left -> Root -> Right

        Yields elements in sorted ascending order.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder(self):
        """Pre-order Traversal: Root -> Left -> Right

        Useful for cloning or serializing the tree structure.
        """
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """Post-order Traversal: Left -> Right -> Root

        Useful for deleting or freeing nodes bottom-up.
        """
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.val)

    def levelorder(self):
        """Level-order Traversal (BFS): Top -> Bottom, Left -> Right

        Visits nodes level-by-level using a FIFO queue.
        """
        result = []
        if not self.root:
            return result

        queue = deque([self.root])
        while queue:
            current = queue.popleft()
            result.append(current.val)

            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return result