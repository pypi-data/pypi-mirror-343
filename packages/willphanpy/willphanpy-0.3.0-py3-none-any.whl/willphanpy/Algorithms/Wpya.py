import sympy as sym
import pandas
from collections import deque

class Wpya:
    def __init__(self):
        pass
    
    #calculate factorial of a non-negative number a (a!)
    @staticmethod
    def factorial(a):
        fac=1
        for i in range(1, a+1):
            fac=fac*i
        return fac

    #calculate a combinatorics of (n,k)
    @staticmethod
    def combinatorics(n, k):
        return Wpya.factorial(n)//(Wpya.factorial(k)*Wpya.factorial(n-k))

    #calculate an arrangement of (n,k)
    @staticmethod
    def arrangement(n,k):
        return Wpya.factorial(n)//Wpya.factorial(n-k)

    #calculate a permutation of (k)
    @staticmethod
    def permutation(k):
        return Wpya.factorial(k)

    #find a root of an equation using bisection method
    @staticmethod
    def bisection(f, a, b, loop):
        xn=(a+b)/2
        for n in range(loop):
            print(xn)
            if f(xn)==0:
                break
            if f(xn)*f(a)>0:
                a=xn
                xnew=(a+b)/2
            elif f(xn)*f(a)<0:
                b=xn
                xnew=(a+b)/2
            xn=xnew

    #find a root of an equation using iterative method
    @staticmethod
    def iterative(g, q, x0, tol, loop):
        xn=x0
        for n in range(loop):
            xnew=g(xn)
            if (q*abs(xnew-xn)/(1-q))<tol:
                break
            print(xnew)
            xn=xnew

    #find a root of an equation using Newton method
    @staticmethod
    def newton(f ,fd, x0, tol, loop):
        xn=x0
        for n in range(loop):
            xnew=xn-f(xn)/fd(xn)
            if abs(xnew - xn)<tol:
                break
            print(xnew)
            xn=xnew

    @staticmethod
    def seriessin():
        x = sym.symbols('x')
        b = 0
        for i in range(100):
            a = (-1)**i*(x**(2*i+1)/Wpya.factorial(2*i+1))
            b += a
        return b

    @staticmethod
    def seriescos():
        x = sym.symbols('x')
        b = 0
        for i in range(100):
            a = (-1)**i*(x**(2*i)/Wpya.factorial(2*i))
            b += a
        return b

    @staticmethod
    def read_excel(file: str):
        # Reading the Excel file
        data = pandas.read_excel(file)

        # Display the first few rows
        return data.to_numpy()
    

    # Algorithm that converts infix expression to postfix expression
    @staticmethod
    def infixToPostfix(infix: str) -> str:
        r"""
        This method is used to convert infix expression to postfix expression
        """
        power1 = ['+', '-']
        power2 = ['*', '/']
        parenthesis = ['(', ')']
        operator = power1 + power2
        postfix = ''

        stack = [] # stack

        for i in range(len(infix)):
            e = infix[i]
            if(e not in operator + parenthesis):
                postfix = postfix + e
                continue

            if(e in operator):
                if(len(stack) == 0):
                    stack.append(e)
                    continue

                if(stack[-1] in power2):
                    postfix = postfix + stack.pop()
                    stack.append(e)

                else:
                    stack.append(e)

                continue

            if(e in parenthesis):
                if(e == '('):
                    stack.append(e)
                
                else:
                    while(stack[-1] != '('):
                        postfix = postfix + stack.pop()

                    stack.pop() # remove the openning parenthesis
                    
        while(True):
            if(len(stack) == 0):
                break
            postfix = postfix + stack.pop()
        return postfix

    # Algorithm that converts postfix expression back to infix expression
    @staticmethod
    def evaluatePostfix(postfix: str) -> int:
        r"""
        This method is used to evaluate postfix expression
        """
        stack = []
        power1 = ['+', '-']
        power2 = ['*', '/']
        operator = power1 + power2

        for i in range(len(postfix)):
            e = postfix[i]

            if(e not in operator):
                stack.append(e)
                continue

            pop_2 = stack.pop()
            pop_1 = stack.pop()

            match(e):
                case '+':
                    stack.append(int(pop_1) + int(pop_2))
                case '-':
                    stack.append(int(pop_1) - int(pop_2))
                case '*':
                    stack.append(int(pop_1) * int(pop_2))
                case '/':
                    stack.append(int(pop_1) / int(pop_2))

        return stack.pop()


    @staticmethod
    def sort(arr: list, algorithm: str = "heap"):
        r"""
        This sorting function implements multiple sorting algorithms
        Quick sort : O(nlogn) -> algorithm = 'quick'
        Merge sort : O(nlogn) -> algorithm = 'merge'
        Heap sort : O(nlogn) -> algorithm = 'heap'
        Radix sort : O(kn) -> algorithm = 'radix'
        Insertion sort : O(n2) -> algorithm = 'insertion'
        Selection sort : O(n2) -> algorithm = 'selection'

        @param arr: The list to be sorted.
        @param algorithm: The sorting algorithm to be used. Default is heap sort
        @return: None. The input list is sorted in place.
        """
        match(algorithm):
            case 'quick':
                from .sorting.quickSort import quickSort as qs
                qs(arr)
            case 'merge':
                from .sorting.merge import mergeSort as ms
                ms(arr)
            case 'insertion':
                from .sorting.insertion import insertion as ise
                ise(arr)
            case 'selection':
                from .sorting.selection import selection as ss
                ss(arr)
            case 'heap':
                from .sorting.heap import heap as hs
                hs(arr)
            case 'radix':
                from .sorting.radix import radix as rs
                rs(arr)

    @staticmethod
    def maxSlidingWindow(arr: list[int], k: int) -> list[int]:
        r"""
        This methos is to find maximum value of a k window (window size of k) sliding across the arr list
        """
        n = len(arr)
        result = []
        d = deque()
        i = 0 # Sliding window
        j = 0 # Slding window element

        while(i <= n - k):
            while(j <= i + k - 1):
                if(not d):
                    d.append(j)
                else:
                    while(d and arr[d[-1]] < arr[j]):
                        d.pop()

                    d.append(j)

                j += 1
            
            result.append(arr[d[0]])
            i += 1
            if(d[0] < i):
                d.popleft()
        
        return result

    @staticmethod
    def two_pointers(set, target):
        r"""
        The problem is given a sorted set of numbers and a target. Find two numbers in the set that add up to the target
        @param set : a SORTED list of number
        @param target : a target number
        @return a list of the first number and the second number that add up to the target if found
        @ return False if not found
        """
        p1 = 0 # set pointer 1 to the beginning of the set
        p2 = len(set) - 1 # set pointer 2 to the end of the set

        while(p1 < p2):
            sum = set[p1] + set[p2]
            if(sum == target):
                return [set[p1], set[p2]]
            elif(sum < target):
                p1 += 1
            else:
                p2 -= 1

        return False

    @staticmethod
    # swap function
    def swap(arr, i, j):
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp

    @staticmethod
    def DFS(adjacency_list: dict[str, list[str]], startNode: str) -> list:
        r"""
        Define a Depth First Search function. This will search as deep as possible on the left side of the graph
        """
        from .uninformedSearch.DFS import DFS
        return DFS(adjacency_list, startNode)
    
    @staticmethod
    def BFS(adjacency_list: dict[str, list[str]], startNode: str) -> list:
        r"""
        Define a Breadth First Search function. This will search down the graph level by level
        """
        from .uninformedSearch.BFS import BFS
        return BFS(adjacency_list, startNode)
                