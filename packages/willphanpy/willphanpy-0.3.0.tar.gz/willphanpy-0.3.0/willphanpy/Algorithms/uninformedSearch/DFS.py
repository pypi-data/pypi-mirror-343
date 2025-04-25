def DFS(adjacency_list, startNode):
    output = []
    visited = {v: False for v in adjacency_list.keys()}
    def DFS_helper(adjacency_list, startNode, visited, output):
        visited[startNode] = True
        # print(startNode)
        output.append(startNode)
        for v in adjacency_list[startNode]:
            if(visited[v]):
                continue
            DFS_helper(adjacency_list, v, visited, output)

    DFS_helper(adjacency_list, startNode, visited, output)

    return output