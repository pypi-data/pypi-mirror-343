# Divide and conquer algorithm

# 0 1 2 3 4 5 6
# 0 4 5 3 9 2 1

# (0 1 2 3) (4 5 6)
# [0 4 5 3] [9 2 1]

# (0 1) (2 3) (4 5) (6)
# [0 4] [5 3] [9 2] [1]

# (0) (1) (2) (3) (4) (5) (6)
# [0] [4] [5] [3] [9] [2] [1]

# Merge process
# [1 2 4] [3 6 7]
# (i)     (j)
#  i   <   j

from ..Wpya import Wpya

def merge(arr, arr_left, arr_right):
    i, j, k = 0, 0, 0

    while(i < len(arr_left) and j < len(arr_right)):
        if(arr_left[i] < arr_right[j]):
            arr[k] = arr_left[i]
            i += 1
        else:
            arr[k] = arr_right[j]
            j += 1
        k += 1

    while(i < len(arr_left)):
        arr[k] = arr_left[i]
        i += 1
        k += 1

    while(j < len(arr_right)):
        arr[k] = arr_right[j]
        j += 1
        k += 1


def mergeSort(arr: list):
    if(len(arr) == 1):
        return

    start = 0
    end = len(arr) - 1

    mid = (end - start) // 2 # Get midpoint of the list

    arr_left = arr[start:(mid+1)]
    arr_right = arr[(mid+1):(end+1)]

    mergeSort(arr_left)
    mergeSort(arr_right)

    merge(arr, arr_left, arr_right)
    
