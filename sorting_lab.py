"""
Sorting Algorithms Visualization Lab

Complete the TODO sections.

Do not use list.sort() or sorted() to perform the sorting.
"""

import random
import time
import platform
import subprocess
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Settings
# ------------------------------------------------------------

DEFAULT_LIST_SIZE = 20
MIN_VALUE = 1
MAX_VALUE = 100
ANIMATION_DELAY = 0.10
SOUND_ENABLED = True
LOW_FREQUENCY = 200
HIGH_FREQUENCY = 1200


# ------------------------------------------------------------
# Sound Functions
# ------------------------------------------------------------

def value_to_frequency(value):
    """
    Convert a list value into a frequency.

    Map values from MIN_VALUE through MAX_VALUE
    into frequencies from LOW_FREQUENCY through HIGH_FREQUENCY.
    Smaller values produce lower pitches; larger values produce higher pitches.
    """
    if MAX_VALUE == MIN_VALUE:
        return LOW_FREQUENCY
    
    # Linear interpolation formula to map value to frequency
    freq = LOW_FREQUENCY + (value - MIN_VALUE) * (HIGH_FREQUENCY - LOW_FREQUENCY) / (MAX_VALUE - MIN_VALUE)
    return int(freq)


def play_value_sound(value):
    """
    Play a short sound whose pitch depends on value.
    Handles Windows, macOS, and Linux sound execution safely.
    """
    if not SOUND_ENABLED:
        return

    freq = value_to_frequency(value)
    duration_ms = 50  # 50 milliseconds

    try:
        os_name = platform.system()
        if os_name == "Windows":
            import winsound
            winsound.Beep(freq, duration_ms)

        elif os_name == "Darwin":  # macOS
            subprocess.run(
                ["osascript", "-e", "beep 1"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        elif os_name == "Linux":
            subprocess.run(
                ["speaker-test", "-t", "sine", "-f", str(freq), "-l", "1"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=duration_ms / 1000.0
            )
    except Exception:
        # Guarantee sound execution issues will not crash the visualization loop
        pass


# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def generate_list(size=DEFAULT_LIST_SIZE):
    """
    Return a list containing 'size' random integers between MIN_VALUE and MAX_VALUE.
    """
    return [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(size)]


def draw_list(values, title="Sorting"):
    """
    Draw the current list as a bar graph.
    """
    plt.clf()

    plt.bar(range(len(values)), values)

    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Value")

    plt.pause(ANIMATION_DELAY)


# ------------------------------------------------------------
# Sorting Algorithms
# ------------------------------------------------------------

def selection_sort(values):
    """
    Sort values using Selection Sort.
    """
    n = len(values)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if values[j] < values[min_idx]:
                min_idx = j

        if min_idx != i:
            values[i], values[min_idx] = values[min_idx], values[i]
            play_value_sound(values[i])
            draw_list(values, "Selection Sort")


def bubble_sort(values):
    """
    Sort values using Bubble Sort.
    """
    n = len(values)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
                swapped = True
                play_value_sound(values[j + 1])
                draw_list(values, "Bubble Sort")
        if not swapped:
            break


def insertion_sort(values):
    """
    Sort values using Insertion Sort.
    """
    for i in range(1, len(values)):
        key = values[i]
        j = i - 1
        play_value_sound(key)
        
        while j >= 0 and values[j] > key:
            values[j + 1] = values[j]
            j -= 1
            draw_list(values, "Insertion Sort")
            
        values[j + 1] = key
        draw_list(values, "Insertion Sort")


def merge(values, start, mid, end):
    """
    Merge two sorted sublists values[start..mid] and values[mid+1..end]
    directly in place on the original list.
    """
    left = values[start:mid + 1]
    right = values[mid + 1:end + 1]

    i = 0  # Pointer for left sublist
    j = 0  # Pointer for right sublist
    k = start  # Pointer for values array

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            values[k] = left[i]
            i += 1
        else:
            values[k] = right[j]
            j += 1

        play_value_sound(values[k])
        draw_list(values, "Merge Sort")
        k += 1

    while i < len(left):
        values[k] = left[i]
        play_value_sound(values[k])
        draw_list(values, "Merge Sort")
        i += 1
        k += 1

    while j < len(right):
        values[k] = right[j]
        play_value_sound(values[k])
        draw_list(values, "Merge Sort")
        j += 1
        k += 1


def merge_sort_helper(values, start, end):
    """
    Recursively split and merge sub-arrays using boundaries start and end.
    """
    if start < end:
        mid = (start + end) // 2
        merge_sort_helper(values, start, mid)
        merge_sort_helper(values, mid + 1, end)
        merge(values, start, mid, end)


def merge_sort(values):
    """
    Sort values using Merge Sort.
    """
    merge_sort_helper(values, 0, len(values) - 1)
    return values


def partition(values, low, high):
    pivot = values[high]
    i = low - 1

    for j in range(low, high):
        if values[j] <= pivot:
            i += 1
            values[i], values[j] = values[j], values[i]
            play_value_sound(values[i])
            draw_list(values, "Quick Sort")

    values[i + 1], values[high] = values[high], values[i + 1]
    play_value_sound(values[i + 1])
    draw_list(values, "Quick Sort")
    return i + 1


def quick_sort_helper(values, low, high):
    if low < high:
        pi = partition(values, low, high)
        quick_sort_helper(values, low, pi - 1)
        quick_sort_helper(values, pi + 1, high)


def quick_sort(values):
    """
    Sort values using Quick Sort.
    """
    quick_sort_helper(values, 0, len(values) - 1)
    return values


# ------------------------------------------------------------
# Algorithm Explanations / Pseudocode
# ------------------------------------------------------------

def print_selection_info():
    print("\n--- Selection Sort ---")
    print("Explanation:")
    print("Selection Sort divides the list into a sorted section and an unsorted section.")
    print("It repeatedly scans the unsorted portion to find the smallest remaining element")
    print("and swaps it to the end of the sorted section.")
    print("\nPseudocode:")
    print("FOR i = 0 TO length - 1:")
    print("    min_index = i")
    print("    FOR j = i + 1 TO length - 1:")
    print("        IF list[j] < list[min_index]:")
    print("            min_index = j")
    print("    SWAP list[i] AND list[min_index]\n")


def print_bubble_info():
    print("\n--- Bubble Sort ---")
    print("Explanation:")
    print("Bubble Sort steps through the list repeatedly, compares adjacent elements, and")
    print("swaps them if they are in the wrong order. Larger values 'bubble' up to the end.")
    print("\nPseudocode:")
    print("FOR i = 0 TO length - 1:")
    print("    FOR j = 0 TO length - i - 2:")
    print("        IF list[j] > list[j + 1]:")
    print("            SWAP list[j] AND list[j + 1]\n")


def print_insertion_info():
    print("\n--- Insertion Sort ---")
    print("Explanation:")
    print("Insertion Sort builds the final sorted array one item at a time. It picks each")
    print("element and inserts it into its correct relative position in the sorted subset.")
    print("\nPseudocode:")
    print("FOR i = 1 TO length - 1:")
    print("    key = list[i]")
    print("    j = i - 1")
    print("    WHILE j >= 0 AND list[j] > key:")
    print("        list[j + 1] = list[j]")
    print("        j = j - 1")
    print("    list[j + 1] = key\n")


def print_merge_info():
    print("\n--- Merge Sort ---")
    print("Explanation:")
    print("Merge Sort is a Divide and Conquer algorithm. It recursively splits the list")
    print("into two halves until sublists reach size 1, then merges those sorted halves.")
    print("\nPseudocode:")
    print("FUNCTION MergeSort(list, start, end):")
    print("    IF start < end:")
    print("        mid = (start + end) / 2")
    print("        MergeSort(list, start, mid)")
    print("        MergeSort(list, mid + 1, end)")
    print("        Merge(list, start, mid, end)\n")


def print_quick_info():
    print("\n--- Quick Sort ---")
    print("Explanation:")
    print("Quick Sort chooses a 'pivot' element, partitions the array so smaller elements move")
    print("left of the pivot and larger elements move right, then recursively sorts the sub-arrays.")
    print("\nPseudocode:")
    print("FUNCTION QuickSort(list, low, high):")
    print("    IF low < high:")
    print("        pivot_index = Partition(list, low, high)")
    print("        QuickSort(list, low, pivot_index - 1)")
    print("        QuickSort(list, pivot_index + 1, high)\n")


def print_info_menu():
    print()
    print("ALGORITHM INFORMATION")
    print()
    print("1. Selection Sort")
    print("2. Bubble Sort")
    print("3. Insertion Sort")
    print("4. Merge Sort")
    print("5. Quick Sort")
    print("6. Return to Main Menu")
    print()


def algorithm_info_menu():
    """
    Display explanations and pseudocode for the sorting algorithms.
    """
    while True:
        print_info_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            print_selection_info()
        elif choice == "2":
            print_bubble_info()
        elif choice == "3":
            print_insertion_info()
        elif choice == "4":
            print_merge_info()
        elif choice == "5":
            print_quick_info()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a number from 1 through 6.")


# ------------------------------------------------------------
# Menu
# ------------------------------------------------------------

def print_menu():
    print()
    print("SORTING VISUALIZER")
    print()
    print("1. Generate New Random List")
    print("2. Selection Sort")
    print("3. Bubble Sort")
    print("4. Insertion Sort")
    print("5. Merge Sort")
    print("6. Quick Sort")
    print("7. Algorithm Information / Pseudocode")
    print("8. Exit")
    print()


def main():

    # Interactive plotting allows the graph to update repeatedly.
    plt.ion()

    values = generate_list()

    while True:

        print()
        print("Current List:")
        print(values)

        print_menu()

        choice = input("Choice: ").strip()

        if choice == "1":
            values = generate_list()
            draw_list(values, "New Random List")

        elif choice == "2":
            working_list = values.copy()
            draw_list(working_list, "Selection Sort")
            selection_sort(working_list)
            print("Sorted List:")
            print(working_list)

        elif choice == "3":
            working_list = values.copy()
            draw_list(working_list, "Bubble Sort")
            bubble_sort(working_list)
            print("Sorted List:")
            print(working_list)

        elif choice == "4":
            working_list = values.copy()
            draw_list(working_list, "Insertion Sort")
            insertion_sort(working_list)
            print("Sorted List:")
            print(working_list)

        elif choice == "5":
            working_list = values.copy()
            draw_list(working_list, "Merge Sort")

            result = merge_sort(working_list)

            if result is not None:
                working_list = result

            print("Sorted List:")
            print(working_list)

        elif choice == "6":
            working_list = values.copy()
            draw_list(working_list, "Quick Sort")

            result = quick_sort(working_list)

            if result is not None:
                working_list = result

            print("Sorted List:")
            print(working_list)

        elif choice == "7":
            algorithm_info_menu()

        elif choice == "8":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 through 8.")

    plt.ioff()
    plt.close()


if __name__ == "__main__":
    main()
