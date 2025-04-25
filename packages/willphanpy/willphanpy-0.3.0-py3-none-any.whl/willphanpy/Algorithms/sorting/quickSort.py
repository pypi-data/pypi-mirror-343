from ..Wpya import Wpya

def partition(arr, start, end):
    pivot = arr[end] # set pivot position for the last element
    i = start - 1 # i index
    #For loop O(end - start)
    for j in range(start, end):
        if arr[j] < pivot:
            i += 1
            Wpya.swap(arr, i, j)

    i += 1
    Wpya.swap(arr, end, i) # found a new pivot position

    return i # new pivot position (sorted)
    
def helper(arr, start, end):
    if (end <= start):
        return # base case

    pivotPosition = partition(arr, start, end) # get pivot position -> O(end - start)
    helper(arr, start, pivotPosition - 1)
    helper(arr, pivotPosition + 1, end)

def quickSort(arr: list):
    helper(arr, 0, len(arr) - 1)

    # time complexity
    # T(n) = O(n) + T(n/2) + T(n/2) = O(nlogn)
