"""
Binary Search Tree (BST) Implementation in Python
===================================================

RESEARCH NOTES (Binary Tree -> Binary Search Tree):
-----------------------------------------------------
A Binary Tree is a hierarchical data structure where each node has AT MOST
two children, commonly referred to as the "left" child and "right" child.
There is no ordering rule for a generic binary tree - children can hold
any value in any position.

A Binary Search Tree (BST) is a special kind of Binary Tree that enforces
an ORDERING RULE (invariant) on every node:

    1. All values in a node's LEFT subtree must be LESS THAN the node's value.
    2. All values in a node's RIGHT subtree must be GREATER THAN the node's value.
    3. Both the left and right subtrees must themselves also be valid
       Binary Search Trees (the rule applies recursively).
    4. (In this implementation) duplicate values are not inserted twice.

This ordering rule is what makes searching, inserting, and deleting an
average of O(log n) on a balanced tree, because at every node you can
discard half of the remaining tree (go left or go right) instead of
checking every node like you would in a plain unordered binary tree.

Only Python's built-in `queue` "library" (module) is used for the BFS
traversal, plus plain `list` for stacks/collecting results. No external
libraries are used.
"""

from queue import Queue  # Used for Breadth-First Search (level-order) traversal


# ----------------------------------------------------------------------
# NODE CLASS
# ----------------------------------------------------------------------
class Node:
    """A single node in the Binary Search Tree."""

    def __init__(self, value):
        self.value = value      # The data stored in this node
        self.left = None        # Reference to left child (values < self.value)
        self.right = None       # Reference to right child (values > self.value)


# ----------------------------------------------------------------------
# BINARY SEARCH TREE CLASS
# ----------------------------------------------------------------------
class BinarySearchTree:
    """
    Binary Search Tree supporting insertion, deletion, and 4 traversal
    strategies: BFS (level-order), Pre-order, In-order, and Post-order.
    """

    def __init__(self):
        self.root = None   # The tree starts empty

    # --------------------------------------------------------------
    # INSERTION
    # --------------------------------------------------------------
    def insert(self, value):
        """
        Public method to insert a value into the BST.
        Maintains the BST property: left < node < right.
        """
        if self.root is None:
            # Tree is empty -> new node becomes the root
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current_node, value):
        """
        Helper method that walks down the tree to find the correct
        empty spot for the new value, following BST ordering rules.
        """
        if value < current_node.value:
            # Value belongs in the left subtree
            if current_node.left is None:
                current_node.left = Node(value)
            else:
                self._insert_recursive(current_node.left, value)

        elif value > current_node.value:
            # Value belongs in the right subtree
            if current_node.right is None:
                current_node.right = Node(value)
            else:
                self._insert_recursive(current_node.right, value)

        else:
            # value == current_node.value -> duplicate, ignore it
            print(f"Value {value} already exists in the tree. Skipping insert.")

    # --------------------------------------------------------------
    # DELETION
    # --------------------------------------------------------------
    def delete(self, value):
        """
        Public method to delete a value from the BST while preserving
        the BST property. There are 3 cases to handle for the node
        being deleted:
            1. Leaf node (no children)          -> simply remove it.
            2. Node with one child               -> replace node with its child.
            3. Node with two children            -> replace node's value with
                                                     its in-order successor
                                                     (smallest value in the
                                                     right subtree), then
                                                     delete that successor
                                                     node from the right subtree.
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, current_node, value):
        # Base case: value not found (reached an empty branch)
        if current_node is None:
            print(f"Value {value} not found in the tree.")
            return current_node

        # Traverse left or right to find the node to delete
        if value < current_node.value:
            current_node.left = self._delete_recursive(current_node.left, value)
        elif value > current_node.value:
            current_node.right = self._delete_recursive(current_node.right, value)
        else:
            # Found the node to delete (current_node.value == value)

            # Case 1: Node has no left child
            # (covers both "no children" and "only right child" cases)
            if current_node.left is None:
                return current_node.right

            # Case 2: Node has no right child (only left child)
            elif current_node.right is None:
                return current_node.left

            # Case 3: Node has two children
            else:
                # Find the in-order successor (smallest value in right subtree)
                successor = self._find_min_node(current_node.right)
                # Copy successor's value into the current node
                current_node.value = successor.value
                # Delete the successor from the right subtree
                # (it has at most one right child, so this recursive call
                # will hit Case 1 or Case 2 above, not Case 3 again)
                current_node.right = self._delete_recursive(current_node.right, successor.value)

        return current_node

    def _find_min_node(self, current_node):
        """Walks left as far as possible to find the smallest value in a subtree."""
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    # --------------------------------------------------------------
    # TRAVERSAL 1: BREADTH-FIRST SEARCH (Level-Order)
    # --------------------------------------------------------------
    def bfs(self):
        """
        Visits nodes level by level, left to right, using a Queue
        (FIFO) to keep track of which nodes to visit next.
        Returns a list of values in BFS order.
        """
        result = []
        if self.root is None:
            return result

        node_queue = Queue()
        node_queue.put(self.root)

        while not node_queue.empty():
            current_node = node_queue.get()   # Dequeue the front node
            result.append(current_node.value)

            if current_node.left is not None:
                node_queue.put(current_node.left)
            if current_node.right is not None:
                node_queue.put(current_node.right)

        return result

    # --------------------------------------------------------------
    # TRAVERSAL 2: PRE-ORDER (Root -> Left -> Right)
    # --------------------------------------------------------------
    def pre_order(self):
        """Returns a list of values using recursive Pre-order traversal."""
        result = []
        self._pre_order_recursive(self.root, result)
        return result

    def _pre_order_recursive(self, current_node, result):
        if current_node is not None:
            result.append(current_node.value)               # Visit ROOT first
            self._pre_order_recursive(current_node.left, result)   # Then LEFT
            self._pre_order_recursive(current_node.right, result)  # Then RIGHT

    # --------------------------------------------------------------
    # TRAVERSAL 3: IN-ORDER (Left -> Root -> Right)
    # --------------------------------------------------------------
    def in_order(self):
        """
        Returns a list of values using recursive In-order traversal.
        NOTE: For a valid BST, in-order traversal always produces
        values in SORTED (ascending) order - a great way to verify
        the BST property holds.
        """
        result = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, current_node, result):
        if current_node is not None:
            self._in_order_recursive(current_node.left, result)    # Visit LEFT first
            result.append(current_node.value)                # Then ROOT
            self._in_order_recursive(current_node.right, result)   # Then RIGHT

    # --------------------------------------------------------------
    # TRAVERSAL 4: POST-ORDER (Left -> Right -> Root)
    # --------------------------------------------------------------
    def post_order(self):
        """Returns a list of values using recursive Post-order traversal."""
        result = []
        self._post_order_recursive(self.root, result)
        return result

    def _post_order_recursive(self, current_node, result):
        if current_node is not None:
            self._post_order_recursive(current_node.left, result)   # Visit LEFT first
            self._post_order_recursive(current_node.right, result)  # Then RIGHT
            result.append(current_node.value)                 # Then ROOT last


# ----------------------------------------------------------------------
# MENU-DRIVEN PROGRAM
# ----------------------------------------------------------------------
def print_menu():
    """Displays the list of available operations to the user."""
    print("\n===== Binary Search Tree Menu =====")
    print("1. Insert a value")
    print("2. Delete a value")
    print("3. BFS Traversal (Level-Order)")
    print("4. Pre-Order Traversal")
    print("5. In-Order Traversal")
    print("6. Post-Order Traversal")
    print("7. Exit")
    print("====================================")


def get_integer_input(prompt):
    """
    Repeatedly asks the user for input until a valid integer is entered.
    Keeps the menu loop from crashing on bad input (e.g., letters).
    """
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")


if __name__ == "__main__":
    bst = BinarySearchTree()

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            count = get_integer_input("How many values do you want to insert? ")
            if count <= 0:
                print("Number of values must be greater than 0.")
            else:
                for i in range(count):
                    value = get_integer_input(f"Enter value {i + 1} of {count}: ")
                    bst.insert(value)
                    print(f"{value} inserted into the tree.")

        elif choice == "2":
            value = get_integer_input("Enter the value to delete: ")
            bst.delete(value)

        elif choice == "3":
            print("BFS (Level-Order):", bst.bfs())

        elif choice == "4":
            print("Pre-Order:", bst.pre_order())

        elif choice == "5":
            print("In-Order (sorted):", bst.in_order())

        elif choice == "6":
            print("Post-Order:", bst.post_order())

        elif choice == "7":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")