# Radix sort
# We are going to use queue data structure for this sorting algorithm
# We are going to extract digit at one's ten's 100's 1000's places depending on how large the max value in the list is
# Because we have 10 digits from 0 to 9, so we are going to use 10 queues being contained in a dictionary indexed from 0 to 9

from ...DataStructure.Wpyd import Wpyd as d

def extractDigit(number, place):
    return (number // place) % 10 # O(1)

# method to find to max number of digits (k) in in the list -> O(n)
def maxNumberOfDigits(arr):
    maxValue = max(arr) # find max value in the list -> O(n)

    # O(logn)
    count = 0
    while maxValue > 0:
        maxValue //= 10
        count += 1

    return count

def radix(arr):
    maxDigits = maxNumberOfDigits(arr) # O(n)
    queueList = {i: d.Queue() for i in range(10)}
    n = len(arr)

    place = 0 # start with one's place of a number
    while(True):
        for i in range(n):
            digit = extractDigit(arr[i], 10 ** place) # O(1)
            queueList[digit].enqueue(arr[i]) # O(1)
        
        # for loop -> O(n)

        k = 0 # keeps track of what element is being inserted back to the list
        for j in range(10):
            currentQueue = queueList[j]
            while(not currentQueue.isEmpty()):
                arr[k] = currentQueue.dequeue()
                k += 1

        # for loop -> O(1)

        if place == maxDigits:
            break

        place += 1
    
    # while loop -> run k times O(n) -> O(kn) where k is the max number of digits

        