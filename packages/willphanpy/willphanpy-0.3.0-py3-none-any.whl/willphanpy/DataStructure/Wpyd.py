class Wpyd:
    @staticmethod
    def Queue():
        """
        Return an instance of a queue data structure
        """
        from .Queue.Queue import Queue
        return Queue()
    @staticmethod
    def Deque():
        """
        Return an instance of a double ended queue data structure
        """
        from .Queue.Deque import Deque
        return Deque()
    @staticmethod
    def Tree():
        """
        Return an instance of a tree data structure
        """
        from .Tree import Tree
        return Tree()

    @staticmethod
    def randomInt(fromNumber: int, toNumber: int, shuffle = False) -> list:
        import random
        arr = list(range(fromNumber, toNumber + 1))
        if shuffle:
            random.shuffle(arr)
            return arr

        return arr
