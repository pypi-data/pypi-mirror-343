from .Queue.Queue import Queue

class Node:
    def __init__(self, data):
        self.data = data 
        self.left: Node = None
        self.right: Node = None
        self.visited = False
        self.height = 0
        self.depth = 0
        self.BF = 0

class Tree:
    def __init__(self):
        self.__root = None
        self.__depth = -1
        self.__height = -1

    def insert(self, data):
        """
        - Method to insert a node to the tree using recursive approach. This also provides tree rotation after insertion to make the tree become AVL tree
        - After insertion for each node, current node depth is computed, current node height is computed, current node balance factor (BF) is computed
        - Finally, the current node is considered to be rotated or not based on its BF
        - After insertion for the entire tree, tree height and tree depth are recomputed
        """
        def _insert_helper(current: Node, data, depth):
            if current is None:
                return Node(data)
            
            if data < current.data:
                current.left = _insert_helper(current.left, data, depth + 1)

            if data > current.data:
                current.right = _insert_helper(current.right, data, depth + 1)

            # Balance the tree if needed
            return self.__balance(current)

        self.__root = _insert_helper(self.__root, data, 0)
        self.__height = self.__getHeight(self.__root)
        self.__depth = self.__height

    def __balance(self, current):
        """
        Method to balance a tree node
        """
        if current.BF > 1 and self.__getBalance(current.left) >= 0:
            return self.__rightRotation(current)
        
        if current.BF > 1 and self.__getBalance(current.left) < 0:
            current.left = self.__leftRotation(current.left)
            return self.__rightRotation(current)
        
        if current.BF < -1 and self.__getBalance(current.right) <= 0:
            return self.__leftRotation(current)
        
        if current.BF < -1 and self.__getBalance(current.right) > 0:
            current.right = self.__rightRotation(current.right)
            return self.__leftRotation(current)
        
        current.height = self.__getHeight(current)
        current.depth = self.__getDepth(current)
        current.BF = self.__getBalance(current)

        return current
    
    def delete(self, data):
        """
        - Method to delete a node using recursive approach. This also provides tree rotation after insertion to make the tree become AVL tree
        - Case 1: the deleted node is a leaf node -> just delete it
        - Case 2: the deleted node has either left subtree or right subtree -> connect the only subtree of the deleted node to the parent of the deleted node
        - Case 3: the deleted node has both left subtree and right subtree -> either find the max node in the left subtree or min node in the right subtree (Node T), then copy node T value to the deleted node, then recursively delete node T
        - After deletion of a current node, it would be imbalanced, hence it needs to be balanced, then its depth, height, BF are recomputed
        - After deletion for the entire tree, tree height and tree depth are recomputed
        """

        def _delete_helper(current: Node, data):
            if current is None:
                print("Node does not exist")
                return
            
            if data < current.data:
                current.left = _delete_helper(current.left, data)

            if data > current.data:
                current.right = _delete_helper(current.right, data)

            if data == current.data:
                # case 1
                if current.left is None and current.right is None:
                    return None

                # case 2
                # only left subtree exists
                if current.left is not None and current.right is None:
                    return current.left

                # only right subtree exists
                if current.left is None and current.right is not None:
                    return current.right
                
                # case 3
                # find the max node in the left subtree (or min node in the right subtree)
                temp = current.left
                while(temp.right != None):
                    temp = temp.right # property of BST
                
                current.data = temp.data # copy value to the current node
                temp.data = data
                # Then delete the temp node recursively
                current.left = _delete_helper(current.left, data)

            # Balance the tree if needed
            return self.__balance(current)

        self.__root = _delete_helper(self.__root, data)
        self.__height = self.__getHeight(self.__root)
        self.__depth = self.__height

    def __leftRotation(self, node: Node):
        """
        Left Rotation \\
        node \\
        -right: X \\
        --left: T1 \\
        --right: T2
        """

        x = node.right
        T1 = x.left
        x.left = node
        node.right = T1

        x.height = self.__getHeight(x)
        x.BF = self.__getBalance(x)
        x.depth = self.__getDepth(x)

        node.height = self.__getHeight(node)
        node.BF = self.__getBalance(node)
        node.depth = self.__getDepth(node)
        return x

    def __rightRotation(self, node: Node):
        """
        Right Rotation \\
        node \\
        -left: X \\
        --left: T1 \\
        --right: T2
        """
        x = node.left
        T2 = x.right
        x.right = node
        node.left = T2

        x.height = self.__getHeight(x)
        x.BF = self.__getBalance(x)
        x.depth = self.__getDepth(x)

        node.height = self.__getHeight(node)
        node.BF = self.__getBalance(node)
        node.depth = self.__getDepth(node)

        return x

    def __getBalance(self, node: Node) -> int:
        """
        Method to get balance factor of a node
        """
        if node is None:
            return -99
        
        if node.left is None and node.right is not None:
            return -1 - node.right.height
        
        if node.left is not None and node.right is None:
            return node.left.height + 1
        
        return self.__getHeight(node.left) - self.__getHeight(node.right)


    def __getHeight(self, node: Node) -> int:
        """
        Get height of a node
        """
        if node is None:
            return -1

        return 1 + max(self.__getHeight(node.left), self.__getHeight(node.right))

    def __getDepth(self, node: None) -> int:
        """
        Method to get depth of a node
        """
        pass
            
    def insert_iter(self, data):
        """
        Method to insert a node to the tree using iterative approach
        """
        if(self.__root is None):
            self.__root = Node(data)
        else:
            current = self.__root
            parent = None
            while(current is not None):
                if(data < current.data):
                    parent = current
                    current = current.left
                elif(data > current.data):
                    parent = current
                    current = current.right
                else:
                    return False #duplicated data insert

            if(data < parent.data):
                parent.left = Node(data)
                return True # inserted successfully
            elif(data > parent.data):
                parent.right = Node(data)
                return True # inserted successfully
        return False
    
    def getRoot(self):
        """
        Get root of the tree
        """
        return self.__root
    
    def visualize_tree(self):
        """
        Method to visualize the tree
        """
        def visualize_tree_helper(current, depth):
            if current is not None:
                print(f"{current.data}")
            
            if current.left is not None:
                print(f"{' ' * (depth+1)}-- L :", end=" ")
                visualize_tree_helper(current.left, depth + 1)

            if current.right is not None:
                print(f"{' ' * (depth+1)}-- R :", end=" ")
                visualize_tree_helper(current.right, depth + 1)

        if self.__root is None:
            print("The tree is empty")
            return
        
        print("Root: ", end = " ")       
        visualize_tree_helper(self.__root, 0)

    def getTreeHeight(self):
        """
        Method to get tree height
        """
        return self.__height

    def getTreeDepth(self):
        """
        Method to get tree depth
        """
        return self.__depth


    def inorder(self):
        """
        Method to provide inorder traversal
        """
        def inorder_helper(current):
            if(current is not None):
                inorder_helper(current.left)
                print(current.data, end = ", ")
                inorder_helper(current.right)
        inorder_helper(self.__root)
        print("\n")

    def preorder(self):
        """
        Method to provide preorder traversal
        """
        def preorder_helper(current):
            if(current is not None):
                print(current.data, end = ", ")
                preorder_helper(current.left)
                preorder_helper(current.right)

        preorder_helper(self.__root)
        print("\n")

    def postorder(self):
        """
        Method to provide postorder traversal
        """
        def postorder_helper(current):
            if(current is not None):
                postorder_helper(current.left)
                postorder_helper(current.right)
                print(current.data, end = ", ")

        postorder_helper(self.__root)
        print("\n")

    def BFS(self):
        """
        Breadth First Search
        """
        queue = Queue()
        queue.enqueue(self.__root)

        while(not queue.isEmpty()):
            current = queue.dequeue();
            print(current.data, end = ", ")

            if(current.left is not None):
                queue.enqueue(current.left)
            if(current.right is not None):
                queue.enqueue(current.right)

        print("\n")

    def DFS(self):
        """
        Depth First Search. This search is similar to preorder search
        """
        if(self.__root is None):
            print("The tree is empty")
            return

        def DFS_helper(node):
            node.visited = True
            print(node.data, end = ", ")
            if(node.left is not None):
                if(not node.left.visited):
                    DFS_helper(node.left)
            if(node.right is not None):
                if(not node.right.visited):
                    DFS_helper(node.right)
        DFS_helper(self.__root)
        print("\n")

