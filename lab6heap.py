"""
Laboratory Exercise: Binary Heap
--------------------------------
Insertion, root extraction, and deletion (min-heap or max-heap).

Every operation prints a numbered, step-by-step explanation.
Run:  python binary_heap.py
"""

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

    def delete(self, key):
        reset_steps()
        print(f"\n=== DELETE {key} from {self.kind.upper()}-HEAP ===")
        if not self.a:
            print("  Heap is empty - nothing to delete.")
            return False
        if key not in self.a:
            print(f"  {key} was not found in the heap.")
            return False

        i = self.a.index(key)
        step(f"Search the array for {key}: found at index {i}.", 1)
        last = self.a.pop()

        if i == len(self.a):
            step(f"{key} is the last element -> simply remove it; no reordering needed.", 1)
            note(f"Array = {self.a}", 1)
        else:
            step(f"Remove the last element {last} and place it at index {i}, replacing {key}.", 1)
            self.a[i] = last
            note(f"Array = {self.a}", 1)

            p = (i - 1) // 2
            if i > 0 and self.better(self.a[i], self.a[p]):
                step(f"{last} is better than its parent {self.a[p]} (idx {p}) -> sift UP.", 1)
                op = "<" if self.kind == "min" else ">"
                while i > 0:
                    p = (i - 1) // 2
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
                    step(f"{self.a[0]} reached the root -> STOP.", 1)
            else:
                step(f"{last} is not better than its parent -> sift DOWN.", 1)
                n = len(self.a)
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

        step(f"Deletion of {key} complete.", 1)
        self.show()
        return True


def choose_type():
    while True:
        k = input("Create a (1) Min-heap or (2) Max-heap? ").strip()
        if k in ("1", "2"):
            return BinaryHeap("min" if k == "1" else "max")
        print("  Please enter 1 or 2.")


def main():
    h = choose_type()
    while True:
        print("\n" + "=" * 52)
        print(f"             BINARY {h.kind.upper()}-HEAP MENU")
        print("=" * 52)
        print(" 1. Insert value(s)")
        print(" 2. Extract root")
        print(" 3. Display current heap")
        print(" 4. Load sample data (35 33 42 10 14 19 27 44 26 31)")
        print(" 5. Clear heap / change heap type")
        print(" 6. Delete a value")
        print(" 0. Exit")
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
            h = choose_type()
        elif choice == "6":
            for v in read_ints("Enter integer(s) to delete: "):
                h.delete(v)
            pause()
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()