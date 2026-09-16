# AZUHATA, INTO, PAPICA
# LAB-ACT3
# sorting implementations


# sorting_algorithms.py

def bubble_sort(arr):
    """
    Sorts an array using the Bubble Sort algorithm.
    Outputs every check and swap step to the console.
    """
    n = len(arr)
    print(f"Initial array: {arr}\n")
    
    for i in range(n):
        swapped = False
        print(f"--- Pass {i + 1} ---")
        
        # The last 'i' elements are already sorted, so we don't need to check them again.
        for j in range(0, n - i - 1):
            print(f"Checking if {arr[j]} > {arr[j+1]}...")
            
            if arr[j] > arr[j + 1]:
                # Swap the elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(f"  -> SWAP! Array is now: {arr}")
            else:
                print("  -> No swap needed.")
                
        # Optimization: If no swaps happened in a full pass, the array is already sorted.
        if not swapped:
            print(f"\nNo swaps occurred during Pass {i + 1}. Array is fully sorted!")
            break
            
    print(f"\nFinal sorted array: {arr}")
    return arr

# Showcase
if __name__ == "__main__":
    print("=== BUBBLE SORT SHOWCASE ===")
    test_array = [5, 2, 9, 1, 5]
    bubble_sort(test_array)
