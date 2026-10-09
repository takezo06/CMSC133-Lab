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
        print(f"\n--- Inserting {val} ---")
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if node is None:
            print(f"  -> Created new node: ({val})")
            return Node(val)

        if val < node.val:
            print(f"  {val} < {node.val} -> Moving Left")
            node.left = self._insert(node.left, val)
        elif val > node.val:
            print(f"  {val} > {node.val} -> Moving Right")
            node.right = self._insert(node.right, val)
        else:
            print(f"  {val} == {node.val} -> Duplicate value ignored")

        return node

    # --- DELETION ---
    def delete(self, val):
        print(f"\n--- Deleting {val} ---")
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if node is None:
            print(f"  Value {val} not found in the tree.")
            return node

        if val < node.val:
            print(f"  {val} < {node.val} -> Search Left")
            node.left = self._delete(node.left, val)
        elif val > node.val:
            print(f"  {val} > {node.val} -> Search Right")
            node.right = self._delete(node.right, val)
        else:
            print(f"  Found target node ({node.val})")

            # Case 1 & 2: 0 or 1 child
            if node.left is None:
                replacement = node.right.val if node.right else "None"
                print(
                    f"  Node ({node.val}) has no left child -> Replacing with right child ({replacement})"
                )
                return node.right
            elif node.right is None:
                print(
                    f"  Node ({node.val}) has no right child -> Replacing with left child ({node.left.val})"
                )
                return node.left

            # Case 3: 2 children
            print(
                f"  Node ({node.val}) has 2 children -> Searching for in-order successor in right subtree..."
            )
            successor = self._min_value_node(node.right)
            print(f"  In-order successor identified: ({successor.val})")
            node.val = successor.val
            print(
                f"  Replaced target value with ({successor.val}) -> Deleting original successor node..."
            )
            node.right = self._delete(node.right, successor.val)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            print(f"    Navigating left to find successor: ({current.val}) -> ({current.left.val})")
            current = current.left
        return current

    # --- TRAVERSALS ---
    def inorder(self):
        print("\n--- In-Order Traversal (Left -> Root -> Right) ---")
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            print(f"  Visited Node: {node.val}")
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder(self):
        print("\n--- Pre-Order Traversal (Root -> Left -> Right) ---")
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            print(f"  Visited Node: {node.val}")
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        print("\n--- Post-Order Traversal (Left -> Right -> Root) ---")
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            print(f"  Visited Node: {node.val}")
            result.append(node.val)

    def levelorder(self):
        print("\n--- Level-Order Traversal (BFS Iteration) ---")
        result = []
        if not self.root:
            print("  Tree is empty")
            return result

        queue = deque([self.root])
        step = 1

        while queue:
            current = queue.popleft()
            result.append(current.val)

            print(f"  Step {step}: Processed Node ({current.val})")

            if current.left:
                queue.append(current.left)
                print(f"    -> Enqueued Left child: ({current.left.val})")
            if current.right:
                queue.append(current.right)
                print(f"    -> Enqueued Right child: ({current.right.val})")

            queue_vals = [n.val for n in queue]
            print(f"     Current Queue: {queue_vals}")
            step += 1

        return result


# ==========================================
# Example Execution
# ==========================================
if __name__ == "__main__":
    bst = BinarySearchTree()

    # 1. Insertions with trace output
    for val in [50, 30, 70, 20, 40]:
        bst.insert(val)

    # 2. Traversals with trace output
    print("\nResult array:", bst.inorder())
    print("\nResult array:", bst.preorder())
    print("\nResult array:", bst.postorder())
    print("\nResult array:", bst.levelorder())

    # 3. Deletion with trace output
    bst.delete(30)