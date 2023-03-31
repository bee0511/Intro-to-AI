import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
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
            
    open_list = set([start])
    visited = set([])
    # g contains current distances from start_node to all other nodes
    # the default value (if it's not found in the map) is +infinity
    g = {}
    g[start] = 0
    # parents contains an adjacency map of all nodes
    parents = {}
    parents[start] = start
    time = 0
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
                time += times[(path[i], path[i + 1])]
            return path, time, len(visited)
        # for all neighbors of the current node do
        for neighbor in graph.get(current, []):
            # if the current node isn't in both open_list and closed_list
            # add it to open_list and note n as it's parent
            if neighbor not in open_list and neighbor not in visited:
                open_list.add(neighbor)
                parents[neighbor] = current
                g[neighbor] = g[current] + times[(current, neighbor)]
            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update parent data and g data
            # and if the node was in the closed_list, move it to open_list
            else:
                if g[neighbor] > g[current] + times[(current, neighbor)]:
                    g[neighbor] = g[current] + times[(current, neighbor)]
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
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
