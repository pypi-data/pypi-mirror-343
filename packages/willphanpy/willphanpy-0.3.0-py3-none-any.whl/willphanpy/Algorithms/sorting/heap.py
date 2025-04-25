# heap sort
# O(nlogn)

from ..Wpya import Wpya

# O(log)
def heapify(arr, i, n):
    l = 2*i + 1 # left child of node i
    r = 2*i + 2 # right child of node i

    # at this point, we have three values to compare to find the maximum value
    if l < n and arr[l] > arr[i]:
        k = l
    else:
        k = i

    if r < n and arr[k] < arr[r]:
        k = r
    
    if k != i:
        Wpya.swap(arr, i, k)
        heapify(arr, k, n)

def buildMaxHeap(arr):
    n = len(arr)
    lastNonLeaf = (n - 1) // 2 # get index of the last non-leaf
    for i in range(lastNonLeaf, -1, -1):
        heapify(arr, i, n)

    # for loop O(nlogn)

def heap(arr):
    buildMaxHeap(arr) # O(nlogn)

    for i in range(len(arr) - 1, -1, -1):
        Wpya.swap(arr, 0, i) # the first element is the largest element after building max heap
        heapify(arr, 0, i) # O(logn)

    # for loop O(nlogn)