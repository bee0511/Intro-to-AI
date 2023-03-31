import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    graph = {}
    distances = {}
    heuristic = {}
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if int(row['start']) not in graph:
                graph[int(row['start'])]=[]
            graph[int(row['start'])].append(int(row['end']))
            distances[(int(row['start']), int(row['end']))] = float(row['distance'])
    with open(heuristicFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            heuristic[int(row['node'])] = float(row[str(end)])
            
    open_list = set([start])
    visited = set([])
    # g contains current distances from start_node to all other nodes
    # the default value (if it's not found in the map) is +infinity
    g = {}
    g[start] = 0
    # parents contains an adjacency map of all nodes
    parents = {}
    parents[start] = start
    distance = 0
    while len(open_list) > 0:
        current = None
        # find a node with the lowest value of f() - evaluation function
        for v in open_list:
            if current == None or g[v] + heuristic[v] < g[current] + heuristic[current]:
                current = v;
        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node
        if current == end:
            path = []
            while parents[current] != current:
                path.append(current)
                current = parents[current]
            path.append(start)
            path.reverse()
            for i in range(len(path) - 1):
                distance += distances[(path[i], path[i + 1])]
            return path, distance, len(visited)
        # for all neighbors of the current node do
        for neighbor in graph.get(current, []):
            # if the current node isn't in both open_list and closed_list
            # add it to open_list and note n as it's parent
            if neighbor not in open_list and neighbor not in visited:
                open_list.add(neighbor)
                parents[neighbor] = current
                g[neighbor] = g[current] + distances[(current, neighbor)]
            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update parent data and g data
            # and if the node was in the closed_list, move it to open_list
            else:
                if g[neighbor] > g[current] + distances[(current, neighbor)]:
                    g[neighbor] = g[current] + distances[(current, neighbor)]
                    parents[neighbor] = current
                    if neighbor in visited:
                        visited.remove(neighbor)
                        open_list.add(neighbor)
        # remove n from the open_list, and add it to closed_list
        # because all of his neighbors were inspected
        open_list.remove(current)
        visited.add(current)
    return None
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
