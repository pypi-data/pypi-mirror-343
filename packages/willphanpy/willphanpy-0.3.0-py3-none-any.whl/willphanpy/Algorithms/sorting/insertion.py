# Insertion sort

# 5 2 3 1 8 9
#   j

# 2 5 3 1 8 9
#     j

# 2 3 5 1 8 9
#   j  

from ..Wpya import Wpya

def insertion(arr: list):
    for i in range(1, len(arr)):
        k = i

        while(k > 0):
            if(arr[k] < arr[k - 1]):
                Wpya.swap(arr, k, k-1)
                k -= 1
                continue
            
            break
