"""
Laboratory Exercise: AVL Tree and Binary Heap
---------------------------------------------
AVL Tree : insertion, deletion, pre-order / in-order / post-order DFS, BFS
Binary Heap : insertion, root extraction (min-heap or max-heap)

Every operation prints a numbered, step-by-step explanation of how the
final result was reached.
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


def avl_menu(tree):
    while True:
        print("\n" + "=" * 52)
        print("                 AVL TREE MENU")
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
        print(" 0. Back to main menu")
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
            return
        else:
            print("  Invalid choice.")


# ----------------------------------------------------------------------
# BINARY HEAP
# ----------------------------------------------------------------------
class BinaryHeap:
    def __init__(self, kind="min"):
        self.kind = kind          # "min" or "max"
        self.a = []

    def better(self, x, y):
        """True if x should be closer to the root than y."""
        return x < y if self.kind == "min" else x > y

    def show(self, title="Result:"):
        print(f"    {title}")
        print(f"      Array : {self.a}")
        print("      Index : " + str(list(range(len(self.a)))))
        tree = render_tree(0 if self.a else None,
                           lambda i: 2 * i + 1 if 2 * i + 1 < len(self.a) else None,
                           lambda i: 2 * i + 2 if 2 * i + 2 < len(self.a) else None,
                           lambda i: str(self.a[i]))
        print("      Tree  (root at left, right children on top):")
        for ln in tree:
            print("        " + ln)

    def insert(self, key):
        reset_steps()
        print(f"\n=== INSERT {key} into {self.kind.upper()}-HEAP ===")
        self.a.append(key)
        i = len(self.a) - 1
        step(f"Append {key} at the end of the array (index {i}) to keep the tree complete.", 1)
        note(f"Array = {self.a}", 1)
        while i > 0:
            p = (i - 1) // 2
            op = "<" if self.kind == "min" else ">"
            if self.better(self.a[i], self.a[p]):
                step(f"Sift-up: compare {self.a[i]} (idx {i}) with parent {self.a[p]} (idx {p}): "
                     f"{self.a[i]} {op} {self.a[p]} -> violates {self.kind}-heap, SWAP.", 1)
                self.a[i], self.a[p] = self.a[p], self.a[i]
                note(f"Array = {self.a}", 1)
                i = p
            else:
                step(f"Sift-up: compare {self.a[i]} (idx {i}) with parent {self.a[p]} (idx {p}): "
                     f"heap property holds -> STOP.", 1)
                break
        else:
            if i == 0 and len(self.a) > 1:
                step(f"{self.a[0]} reached the root -> STOP.", 1)
        step(f"Insertion of {key} complete.", 1)
        self.show()

    def extract(self):
        reset_steps()
        label = "MINIMUM" if self.kind == "min" else "MAXIMUM"
        print(f"\n=== EXTRACT ROOT ({label}) from {self.kind.upper()}-HEAP ===")
        if not self.a:
            print("  Heap is empty - nothing to extract.")
            return None
        root = self.a[0]
        step(f"Root (index 0) holds {root}; this value will be returned.", 1)
        last = self.a.pop()
        if not self.a:
            step("The root was the only element -> heap is now empty.", 1)
            self.show()
            print(f"\n  Extracted: {root}")
            return root
        self.a[0] = last
        step(f"Remove the last element {last} and move it to the root (index 0).", 1)
        note(f"Array = {self.a}", 1)

        i, n = 0, len(self.a)
        while True:
            l, r, best = 2 * i + 1, 2 * i + 2, i
            kids = []
            if l < n:
                kids.append(f"left={self.a[l]} (idx {l})")
                if self.better(self.a[l], self.a[best]):
                    best = l
            if r < n:
                kids.append(f"right={self.a[r]} (idx {r})")
                if self.better(self.a[r], self.a[best]):
                    best = r
            if not kids:
                step(f"Sift-down: {self.a[i]} (idx {i}) has no children -> STOP.", 1)
                break
            word = "smallest" if self.kind == "min" else "largest"
            step(f"Sift-down: {self.a[i]} (idx {i}) vs children {', '.join(kids)}; "
                 f"{word} of the three is {self.a[best]}.", 1)
            if best == i:
                note("Heap property holds -> STOP.", 1)
                break
            note(f"SWAP {self.a[i]} with {self.a[best]}.", 1)
            self.a[i], self.a[best] = self.a[best], self.a[i]
            note(f"Array = {self.a}", 1)
            i = best
        step(f"Extraction complete.", 1)
        self.show()
        print(f"\n  Extracted: {root}")
        return root


def heap_menu(heap):
    if heap[0] is None:
        while True:
            k = input("Create a (1) Min-heap or (2) Max-heap? ").strip()
            if k in ("1", "2"):
                heap[0] = BinaryHeap("min" if k == "1" else "max")
                break
            print("  Please enter 1 or 2.")
    h = heap[0]

    while True:
        print("\n" + "=" * 52)
        print(f"             BINARY {h.kind.upper()}-HEAP MENU")
        print("=" * 52)
        print(" 1. Insert value(s)")
        print(" 2. Extract root")
        print(" 3. Display current heap")
        print(" 4. Load sample data (35 33 42 10 14 19 27 44 26 31)")
        print(" 5. Clear heap / change heap type")
        print(" 0. Back to main menu")
        choice = input("Choose: ").strip()

        if choice == "1":
            for v in read_ints("Enter integer(s) to insert: "):
                h.insert(v)
            pause()
        elif choice == "2":
            h.extract(); pause()
        elif choice == "3":
            print(); h.show("Current heap:"); pause()
        elif choice == "4":
            h.a = []
            for v in (35, 33, 42, 10, 14, 19, 27, 44, 26, 31):
                h.insert(v)
            pause()
        elif choice == "5":
            heap[0] = None
            print("  Heap cleared.")
            return heap_menu(heap)
        elif choice == "0":
            return
        else:
            print("  Invalid choice.")


# ----------------------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------------------
def main():
    tree = AVLTree()
    heap = [None]  # wrapped in a list so the sub-menu can replace it
    while True:
        print("\n" + "=" * 52)
        print("        AVL TREE & BINARY HEAP - LAB EXERCISE")
        print("=" * 52)
        print(" 1. AVL Tree")
        print(" 2. Binary Heap")
        print(" 0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            avl_menu(tree)
        elif choice == "2":
            heap_menu(heap)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()