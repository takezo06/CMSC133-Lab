"""
Laboratory Exercise: AVL Tree
-----------------------------
Insertion, deletion, and the 4 traversals
(pre-order DFS, in-order DFS, post-order DFS, BFS).

Every operation prints a numbered, step-by-step explanation.
Run:  python avl_tree.py
"""

from collections import deque

# ----------------------------------------------------------------------
# Helpers: step logger, tree renderer, input
# ----------------------------------------------------------------------
_step_no = 0


def reset_steps():
    global _step_no
    _step_no = 0


def step(msg, indent=0):
    """Print a numbered step."""
    global _step_no
    _step_no += 1
    print(f"{'    ' * indent}Step {_step_no:>2}: {msg}")


def note(msg, indent=0):
    """Print a sub-line that is not numbered."""
    print(f"{'    ' * indent}         {msg}")


def render_tree(root, get_left, get_right, label):
    """Return a sideways picture of a binary tree (root on the left,
    right children on top, left children on the bottom)."""
    lines = []

    def walk(n, depth, tag):
        if n is None:
            return
        walk(get_right(n), depth + 1, "┌── ")
        lines.append("    " * depth + tag + label(n))
        walk(get_left(n), depth + 1, "└── ")

    walk(root, 0, "")
    return lines or ["(empty)"]


def print_block(title, lines, indent=1):
    print(f"{'    ' * indent}{title}")
    for ln in lines:
        print(f"{'    ' * indent}  {ln}")


def read_ints(prompt):
    """Read one or more integers separated by spaces/commas."""
    raw = input(prompt).replace(",", " ").split()
    values = []
    for tok in raw:
        try:
            values.append(int(tok))
        except ValueError:
            print(f"  ! '{tok}' is not an integer and was skipped.")
    return values


def pause():
    input("\nPress Enter to continue...")


# ----------------------------------------------------------------------
# AVL TREE
# ----------------------------------------------------------------------
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self._changed = False  # set True when insert/delete really modifies the tree

    # ---- basic utilities --------------------------------------------
    @staticmethod
    def height(n):
        return n.height if n else 0

    def balance(self, n):
        return self.height(n.left) - self.height(n.right) if n else 0

    def update(self, n):
        n.height = 1 + max(self.height(n.left), self.height(n.right))

    @staticmethod
    def label(n):
        return f"{n.key}"

    def label_full(self, n):
        return f"{n.key} [h={n.height}, bf={self.balance(n)}]"

    def subtree_lines(self, n):
        return render_tree(n, lambda x: x.left, lambda x: x.right, self.label_full)

    def show(self, title="Current AVL tree (root at left, right children on top):"):
        print_block(title, self.subtree_lines(self.root), indent=1)

    # ---- rotations --------------------------------------------------
    def rotate_right(self, y):
        x = y.left
        step(f"Right rotation on {y.key}: {x.key} (its left child) becomes the new subtree root.", 1)
        y.left = x.right
        x.right = y
        self.update(y)
        self.update(x)
        return x

    def rotate_left(self, x):
        y = x.right
        step(f"Left rotation on {x.key}: {y.key} (its right child) becomes the new subtree root.", 1)
        x.right = y.left
        y.left = x
        self.update(x)
        self.update(y)
        return y

    def rebalance(self, n):
        """Update height, report balance factor, rotate if needed."""
        self.update(n)
        bf = self.balance(n)
        step(f"Back at {n.key}: height = {n.height}, balance factor = "
             f"{self.height(n.left)} - {self.height(n.right)} = {bf}", 1)

        if -1 <= bf <= 1:
            note("Balanced (|bf| <= 1). No rotation needed.", 1)
            return n

        before = self.subtree_lines(n)
        if bf > 1:
            if self.balance(n.left) >= 0:
                step(f"Unbalanced at {n.key}: LEFT-LEFT case -> single RIGHT rotation.", 1)
                n = self.rotate_right(n)
            else:
                step(f"Unbalanced at {n.key}: LEFT-RIGHT case -> LEFT rotation on "
                     f"{n.left.key}, then RIGHT rotation on {n.key}.", 1)
                n.left = self.rotate_left(n.left)
                n = self.rotate_right(n)
        else:
            if self.balance(n.right) <= 0:
                step(f"Unbalanced at {n.key}: RIGHT-RIGHT case -> single LEFT rotation.", 1)
                n = self.rotate_left(n)
            else:
                step(f"Unbalanced at {n.key}: RIGHT-LEFT case -> RIGHT rotation on "
                     f"{n.right.key}, then LEFT rotation on {n.key}.", 1)
                n.right = self.rotate_right(n.right)
                n = self.rotate_left(n)

        print_block("Subtree BEFORE rotation:", before, indent=2)
        print_block("Subtree AFTER rotation:", self.subtree_lines(n), indent=2)
        return n

    # ---- insertion --------------------------------------------------
    def insert(self, key):
        reset_steps()
        print(f"\n=== INSERT {key} ===")
        self._changed = False
        self.root = self._insert(self.root, key)
        if self._changed:
            step(f"Insertion of {key} complete.", 1)
        else:
            step(f"{key} already exists - duplicates are not allowed, tree unchanged.", 1)
        self.show("Result:")

    def _insert(self, n, key):
        if n is None:
            step(f"Reached an empty spot -> place {key} here as a new leaf.", 1)
            self._changed = True
            return AVLNode(key)
        if key < n.key:
            step(f"Compare {key} < {n.key}: go LEFT.", 1)
            n.left = self._insert(n.left, key)
        elif key > n.key:
            step(f"Compare {key} > {n.key}: go RIGHT.", 1)
            n.right = self._insert(n.right, key)
        else:
            return n
        if not self._changed:
            return n
        return self.rebalance(n)

    # ---- deletion ---------------------------------------------------
    def delete(self, key):
        reset_steps()
        print(f"\n=== DELETE {key} ===")
        self._changed = False
        self.root = self._delete(self.root, key)
        if self._changed:
            step(f"Deletion of {key} complete.", 1)
        else:
            step(f"{key} was not found - tree unchanged.", 1)
        self.show("Result:")

    def _delete(self, n, key):
        if n is None:
            step(f"Reached an empty spot: {key} is not in the tree.", 1)
            return None
        if key < n.key:
            step(f"Compare {key} < {n.key}: go LEFT.", 1)
            n.left = self._delete(n.left, key)
        elif key > n.key:
            step(f"Compare {key} > {n.key}: go RIGHT.", 1)
            n.right = self._delete(n.right, key)
        else:
            self._changed = True
            if n.left is None and n.right is None:
                step(f"Found {key}: it is a LEAF -> simply remove it.", 1)
                return None
            if n.left is None:
                step(f"Found {key}: only a RIGHT child ({n.right.key}) -> replace {key} with it.", 1)
                return n.right
            if n.right is None:
                step(f"Found {key}: only a LEFT child ({n.left.key}) -> replace {key} with it.", 1)
                return n.left
            succ = n.right
            while succ.left:
                succ = succ.left
            step(f"Found {key}: TWO children. In-order successor (smallest in right "
                 f"subtree) is {succ.key}.", 1)
            step(f"Copy {succ.key} into the node, then delete {succ.key} from the right subtree.", 1)
            n.key = succ.key
            n.right = self._delete(n.right, succ.key)
        if not self._changed:
            return n
        return self.rebalance(n)

    # ---- traversals (iterative, to show the stack / queue) ----------
    @staticmethod
    def _fmt(container):
        return "[" + ", ".join(str(x.key) for x in container) + "]"

    def preorder(self):
        reset_steps()
        print("\n=== PRE-ORDER DFS (Root -> Left -> Right) ===")
        if not self.root:
            print("  Tree is empty.")
            return
        result, stack = [], [self.root]
        step(f"Push root {self.root.key}. Stack = {self._fmt(stack)}")
        while stack:
            n = stack.pop()
            result.append(n.key)
            step(f"Pop {n.key} and VISIT it. Visited = {result}")
            if n.right:
                stack.append(n.right)
                note(f"Push right child {n.right.key} (so it is processed after the left).")
            if n.left:
                stack.append(n.left)
                note(f"Push left child {n.left.key} (processed next).")
            note(f"Stack = {self._fmt(stack)}")
        print(f"\n  Pre-order result: {' '.join(map(str, result))}")

    def inorder(self):
        reset_steps()
        print("\n=== IN-ORDER DFS (Left -> Root -> Right) ===")
        if not self.root:
            print("  Tree is empty.")
            return
        result, stack, cur = [], [], self.root
        while cur or stack:
            while cur:
                stack.append(cur)
                step(f"Push {cur.key} and move to its left child. Stack = {self._fmt(stack)}")
                cur = cur.left
            note("Left child is empty -> backtrack.")
            cur = stack.pop()
            result.append(cur.key)
            step(f"Pop {cur.key} and VISIT it. Visited = {result}")
            cur = cur.right
            if cur:
                note(f"Move to right child {cur.key}.")
        print(f"\n  In-order result: {' '.join(map(str, result))}  (sorted order)")

    def postorder(self):
        reset_steps()
        print("\n=== POST-ORDER DFS (Left -> Right -> Root) ===")
        if not self.root:
            print("  Tree is empty.")
            return
        result, stack, cur, last = [], [], self.root, None
        while cur or stack:
            if cur:
                stack.append(cur)
                step(f"Push {cur.key} and move to its left child. Stack = {self._fmt(stack)}")
                cur = cur.left
            else:
                top = stack[-1]
                if top.right and last is not top.right:
                    step(f"Peek {top.key}: right subtree not done yet -> move to right child {top.right.key}.")
                    cur = top.right
                else:
                    stack.pop()
                    result.append(top.key)
                    last = top
                    step(f"Peek {top.key}: both subtrees done -> pop and VISIT it. "
                         f"Visited = {result}")
                    note(f"Stack = {self._fmt(stack)}")
        print(f"\n  Post-order result: {' '.join(map(str, result))}")

    def bfs(self):
        reset_steps()
        print("\n=== BFS / LEVEL-ORDER (level by level, left to right) ===")
        if not self.root:
            print("  Tree is empty.")
            return
        result, q = [], deque([self.root])
        step(f"Enqueue root {self.root.key}. Queue = {self._fmt(q)}")
        while q:
            n = q.popleft()
            result.append(n.key)
            step(f"Dequeue {n.key} and VISIT it. Visited = {result}")
            for child, side in ((n.left, "left"), (n.right, "right")):
                if child:
                    q.append(child)
                    note(f"Enqueue {side} child {child.key}.")
            note(f"Queue = {self._fmt(q)}")
        print(f"\n  BFS result: {' '.join(map(str, result))}")


def main():
    tree = AVLTree()
    while True:
        print("\n" + "=" * 52)
        print("            AVL TREE - LAB EXERCISE")
        print("=" * 52)
        print(" 1. Insert node(s)")
        print(" 2. Delete node(s)")
        print(" 3. Pre-order traversal  (DFS)")
        print(" 4. In-order traversal   (DFS)")
        print(" 5. Post-order traversal (DFS)")
        print(" 6. Breadth-first traversal (BFS)")
        print(" 7. Display current tree")
        print(" 8. Load sample data (10 20 30 40 50 25)")
        print(" 9. Clear tree")
        print(" 0. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            for v in read_ints("Enter integer(s) to insert: "):
                tree.insert(v)
            pause()
        elif choice == "2":
            for v in read_ints("Enter integer(s) to delete: "):
                tree.delete(v)
            pause()
        elif choice == "3":
            tree.preorder(); pause()
        elif choice == "4":
            tree.inorder(); pause()
        elif choice == "5":
            tree.postorder(); pause()
        elif choice == "6":
            tree.bfs(); pause()
        elif choice == "7":
            print()
            tree.show()
            pause()
        elif choice == "8":
            tree.__init__()
            for v in (10, 20, 30, 40, 50, 25):
                tree.insert(v)
            pause()
        elif choice == "9":
            tree.__init__()
            print("  Tree cleared.")
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("  Invalid choice.")




if __name__ == "__main__":
    main()