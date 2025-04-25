# Selection sort
# find the minimum element and put it in the first position of the list

# 4 5 1 2 6
# i   k
# 1 5 4 2 6
#   i   k
# 1 2 4 5 6
#     i

from ..Wpya import Wpya

def selection(arr: list):
    for i in range(len(arr)):
        minValue = arr[i] # set the i element to be the minimum element
        k = i # set the index of min element

        for j in range(i, len(arr)):
            if(arr[j] < minValue):
                minValue = arr[j]
                k = j

        Wpya.swap(arr, k, i)

        
