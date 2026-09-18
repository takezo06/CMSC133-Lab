# AZUHATA, INTO, PAPICA, SOMERA
# LAB-ACT3
# sorting implementations


# sorting_algorithms.py

def get_user_numbers():
    """Prompts for and validates exactly 5 distinct integers of any size."""
    while True:
        try:
            raw_input = input("\nEnter 5 distinct integers separated by spaces: ").strip()
            tokens = raw_input.split()
            
            if len(tokens) != 5:
                print("Error: You must enter exactly 5 numbers.")
                continue
                
            # Convert all entries to integers (handles positive and negative multi-digit numbers)
            numbers = [int(t) for t in tokens]
            
            if len(set(numbers)) != 5:
                print("Error: Numbers must be distinct (no duplicates).")
                continue
                
            return numbers
        except ValueError:
            print("Error: All inputs must be valid integers.")

# ==================== SORTING ALGORITHMS ====================

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    step = 1
    print(f"\n--- BUBBLE SORT START: {arr} ---")
    
    for i in range(n):
        swapped = False
        print(f"\n--- Pass {i + 1} ---")
        for j in range(0, n - i - 1):
            val1, val2 = arr[j], arr[j + 1]
            if val1 > val2:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(f"Step {step}: Compare index {j} ({val1}) & index {j+1} ({val2}) -> SWAP  | Array: {arr}")
            else:
                print(f"Step {step}: Compare index {j} ({val1}) & index {j+1} ({val2}) -> NO SWAP | Array: {arr}")
            step += 1
            
        if not swapped:
            print("No swaps in this pass. Array is fully sorted early!")
            break

    print(f"\nFINAL SORTED RESULT: {arr}")


def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)
    step = 1
    print(f"\n--- SELECTION SORT START: {arr} ---")
    
    for i in range(n):
        min_idx = i
        print(f"\n--- Pass {i + 1}: Finding minimum for index {i} ---")
        
        for j in range(i + 1, n):
            print(f"Step {step}: Compare current min ({arr[min_idx]} at index {min_idx}) with ({arr[j]} at index {j})")
            if arr[j] < arr[min_idx]:
                min_idx = j
                print(f"  -> New minimum found: {arr[min_idx]} at index {min_idx}")
            step += 1
            
        if min_idx != i:
            print(f"ACTION: Swapping index {i} ({arr[i]}) with index {min_idx} ({arr[min_idx]})")
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        else:
            print(f"ACTION: Element {arr[i]} is already in correct position. No swap.")
            
        print(f"Current Array State: {arr}")

    print(f"\nFINAL SORTED RESULT: {arr}")


def insertion_sort(arr):
    arr = arr.copy()
    n = len(arr)
    step = 1
    print(f"\n--- INSERTION SORT START: {arr} ---")
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        print(f"\n--- Pass {i}: Inserting element key = {key} (index {i}) ---")
        
        while j >= 0 and arr[j] > key:
            print(f"Step {step}: {arr[j]} at index {j} > key ({key}) -> Shift {arr[j]} right to index {j+1}")
            arr[j + 1] = arr[j]
            j -= 1
            step += 1
            print(f"  Array State: {arr}")
            
        arr[j + 1] = key
        print(f"Placed key ({key}) at index {j + 1}")
        print(f"Current Array State: {arr}")

    print(f"\nFINAL SORTED RESULT: {arr}")


def merge_sort_wrapper(arr):
    print(f"\n--- MERGE SORT START: {arr} ---")
    
    def merge_sort(sub_arr, depth=0):
        indent = "  " * depth
        if len(sub_arr) <= 1:
            return sub_arr

        mid = len(sub_arr) // 2
        left = sub_arr[:mid]
        right = sub_arr[mid:]

        print(f"{indent}DIVIDE: {sub_arr} -> Left: {left}, Right: {right}")

        sorted_left = merge_sort(left, depth + 1)
        sorted_right = merge_sort(right, depth + 1)

        print(f"{indent}MERGE: Combining {sorted_left} and {sorted_right}")
        
        merged = []
        i = j = 0
        step = 1

        while i < len(sorted_left) and j < len(sorted_right):
            print(f"{indent}  Step {step}: Compare Left[{i}] ({sorted_left[i]}) vs Right[{j}] ({sorted_right[j]})")
            if sorted_left[i] <= sorted_right[j]:
                print(f"{indent}    -> Take {sorted_left[i]} from Left")
                merged.append(sorted_left[i])
                i += 1
            else:
                print(f"{indent}    -> Take {sorted_right[j]} from Right")
                merged.append(sorted_right[j])
                j += 1
            step += 1

        while i < len(sorted_left):
            print(f"{indent}  Append remaining Left[{i}] ({sorted_left[i]})")
            merged.append(sorted_left[i])
            i += 1

        while j < len(sorted_right):
            print(f"{indent}  Append remaining Right[{j}] ({sorted_right[j]})")
            merged.append(sorted_right[j])
            j += 1

        print(f"{indent}Merged Output: {merged}")
        return merged

    final_result = merge_sort(arr)
    print(f"\nFINAL SORTED RESULT: {final_result}")

# ==================== MAIN MENU ====================

def main():
    while True:
        print("\n" + "="*35)
        print("    SORTING ALGORITHM VISUALIZER")
        print("="*35)
        print("1. Bubble Sort")
        print("2. Selection Sort")
        print("3. Insertion Sort")
        print("4. Merge Sort")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            numbers = get_user_numbers()
            bubble_sort(numbers)
        elif choice == '2':
            numbers = get_user_numbers()
            selection_sort(numbers)
        elif choice == '3':
            numbers = get_user_numbers()
            insertion_sort(numbers)
        elif choice == '4':
            numbers = get_user_numbers()
            merge_sort_wrapper(numbers)
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main()