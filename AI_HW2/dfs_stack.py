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
    graph, distances = readFile()
    visited = [start]
    stack = [start]
    parent = {}
    while stack:
        current_node = stack.pop()
        if current_node == end:
            path = rebuildPath(parent, start, end)
            distance = computeDistance(path, distances)
            return path, distance, len(visited)
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.append(neighbor)
                stack.append(neighbor)
                parent[neighbor] = current_node


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
