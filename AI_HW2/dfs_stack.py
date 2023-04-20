import csv
edgeFile = 'edges.csv'

def readFile():
    """ Read edges.csv, save the adjacency list of the graph, and save distances between two nodes.

    Returns:
        graph: a dictionary, where key is the node and value is a list of adjacent nodes.
        distances: a dictionary, where key is a tuple with two adjacent nodes and value is the distance between them.
    """
    graph = {}
    distances = {}  
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if int(row['start']) not in graph:
                graph[int(row['start'])]=[]
            graph[int(row['start'])].append(int(row['end']))
            distances[(int(row['start']), int(row['end']))] = float(row['distance'])
    return graph, distances

def rebuildPath(parent, start, end):
    """Rebuild the path from start node to end node with the saved parent relationship.

    Args:
        parent (dictionary): saves parents of the node
        start (int): start node ID
        end (int): end node ID

    Returns:
        path: a list with the start node to end node.
    """
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

def computeDistance(path, distances):
    """Compute the total distance of the path.

    Args:
        path (list): saves the nodes on the path
        distances (dictionary): save the distances between two nodes

    Returns:
        distance: int, the total distance along the path 
    """
    distance = 0
    for i in range(len(path) - 1):
        distance += distances[(path[i], path[i + 1])]
    return distance

def dfs(start, end):
    """Use stack to implement dfs

    Args:
        start (int): start node ID
        end (int): end node ID

    Returns:
        path: the path from start node to end node
        dist: the total distance on the path
        num_visited: the number of nodes visited by dfs
    """
    graph, distances = readFile()
    stack = [start] # put the start node into stack
    visited = [start] # put the start node into visited
    parent = {} # use dictionary to store the parent of a node
    while stack:
        current_node = stack.pop() # let the current node be the top node of the stack
        visited.append(current_node) # put current node into visited
        if current_node == end: # if the current node is the end node
            path = rebuildPath(parent, start, end) # reconstruct the path 
            distance = computeDistance(path, distances) # calculate the distance of the path
            return path, distance, len(visited)
        for neighbor in graph.get(current_node, []): # iterate each neighbor node of the current node
            if neighbor not in visited: # if we haven't visited the neighbor node
                stack.append(neighbor) # put neighbor into stack
                parent[neighbor] = current_node # record the parent of the neighbor node
    return None, 0, len(visited) # if we cannot find the route from start to end, return None.


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
