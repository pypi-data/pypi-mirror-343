from ...DataStructure.Wpyd import Wpyd as d

# This requires a queue data structure

# Define Breadth First Search
def BFS(adjacency_list, startNode):
    output = []
    queue = d.Queue()
    queue.enqueue(startNode)
    visited = {v: False for v in adjacency_list.keys()}
    inList = {v: False for v in adjacency_list.keys()}
    while(not queue.isEmpty()):
        removed = queue.dequeue()
        visited[removed] = True
        # print(removed)
        output.append(removed)
        for v in adjacency_list[removed]:
            if(visited[v]):
                continue
            if(inList[v]):
                continue
            queue.enqueue(v)
            inList[v] = True

    return output
