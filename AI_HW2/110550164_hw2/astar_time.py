import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def readFile(end):
    """Read edges.csv, save the adjacency list of the graph, and save time to travel between two nodes.
    
    Read heuristic.csv, use the heuristic function divided by the maximum speed limit from the edges.csv, and set it as the new heuristic function.

    Args:
        end (int): the end node ID

    Returns:
        graph: a dictionary, where the key is the node and value is a list of adjacent nodes.
        times: a dictionary, where the key is a tuple with two adjacent nodes and value is the time to travel between them.
        heuristic: a dictionary, where the key is the node and the value is the corresponding value of the heuristic function of the node.
    """
    graph = {}
    distances = {}
    times = {}
    max_speed_limit = 0.0
    heuristic = {}
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if int(row['start']) not in graph:
                graph[int(row['start'])]=[]
            graph[int(row['start'])].append(int(row['end']))
            distances[(int(row['start']), int(row['end']))] = float(row['distance'])
            times[(int(row['start']), int(row['end']))] = float(row['distance']) / (float(row['speed limit']) * 5 / 18)
            if float(row['speed limit']) > max_speed_limit:
                max_speed_limit = float(row['speed limit'])
    max_speed_limit = max_speed_limit * 5 / 18
    with open(heuristicFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            heuristic[int(row['node'])] = float(row[str(end)]) / max_speed_limit
    return graph, times, heuristic

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

def computeTime(path, times):
    """Compute the total time to travel on the path.

    Args:
        path (list): saves the nodes on the path
        timess (dictionary): save the times to travel between two nodes

    Returns:
        time: int, the total time to travel along the path 
    """
    time = 0
    for i in range(len(path) - 1):
        time += times[(path[i], path[i + 1])]
    return time 

def astar_time(start, end):
    """Use A* search to find the optimal time from start node to end node

    Args:
        start (int): start node ID
        end (int): end node ID

    Returns:
        path: the path from start node to end node
        time: the time to travel on the path
        num_visited: the number of nodes visited by A* search
    """
    graph, times, heuristic = readFile(end)
    open_list = [start] # use a open list to implement A* search
    visited = [start]
    g = {} # use dictionary to store the time to travel from start to all other nodes
    g[start] = 0 
    parent = {} # use dictionary to store the parent of a node
    while len(open_list) > 0:
        current_node = None
        
        for v in open_list: # find a node with the lowest value of f()
            if current_node == None or g[v] + heuristic[v] < g[current_node] + heuristic[current_node]:
                current_node = v;
        
        if current_node == end: # if the current node is the end node
            path = rebuildPath(parent, start, end) # reconstruct the path 
            distance = computeTime(path, times) # calculate the time to travel on the path
            return path, distance, len(visited)
        
        for neighbor in graph.get(current_node, []): # iterate each neighbor node of the current node
            
            if neighbor not in open_list and neighbor not in visited: # if the current node isn't in open list and haven't visited
                open_list.append(neighbor) # add it to open list
                parent[neighbor] = current_node # record the parent of the neighbor node
                g[neighbor] = g[current_node] + times[(current_node, neighbor)] # update the time to travel between start node and this neighbor node
                
            else: # if the current node is in open list or visited
                if g[neighbor] > g[current_node] + times[(current_node, neighbor)]: # check if the time from start node to this neighbor node is larger than from start node to the current node then go to the neighbor node
                    g[neighbor] = g[current_node] + times[(current_node, neighbor)] # if the time is larger, which means go to the current node then go to the neighbor is smaller, update the time from start node to the neighbor node
                    parent[neighbor] = current_node # record the parent of the neighbor node
                    if neighbor in visited: # if the node was in the visited, move it to open list. (because we need to check it again)
                        visited.remove(neighbor)
                        open_list.append(neighbor)
        
        open_list.remove(current_node) # remove the current node from the open list
        visited.append(current_node) # add the current node to visited
    return None, 0, len(visited) # if we cannot find the route from start to end, return None.


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
