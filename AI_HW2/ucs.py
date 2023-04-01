import csv
from queue import PriorityQueue
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

def ucs(start, end):
    """Use priority queue to implement ucs

    Args:
        start (int): start node ID
        end (int): end node ID

    Returns:
        path: the path from start node to end node
        dist: the total distance on the path
        num_visited: the number of nodes visited by ucs
    """
    graph, distances = readFile()
    visited = [start] # put the start node into visited
    queue = PriorityQueue()
    queue.put((0, [start])) # the first element is the distance of the path, the second element is the path
    while queue:
        pair = queue.get() # get the path whose distance is the smallest in the priority queue
        current_node = pair[1][-1] # get the last node from the path to be the current node
        
        if current_node == end: # if the current node is the end node
            path = pair[1] # get the path from start node to end node
            distance = computeDistance(path, distances) # calculate the distance of the path
            return path, distance, len(visited)
        
        for neighbor in graph.get(current_node, []): # iterate each neighbor node of the current node
            if neighbor not in visited: # if we haven't visited the neighbor node
                new_path = list(pair[1])
                new_path.append(neighbor) # put the neighbor node into the path
                visited.append(neighbor) # put neighbor into visited
                queue.put((pair[0] + distances[(current_node, neighbor)], new_path)) # update the total distance of the path
    return None, 0, len(visited) # if we cannot find the route from start to end, return None.


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
