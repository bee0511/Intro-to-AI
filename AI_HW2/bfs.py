import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    graph = {}
    distances = {}
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            if int(row['start']) not in graph:
                graph[int(row['start'])]=[]
            graph[int(row['start'])].append(int(row['end']))
            distances[(int(row['start']), int(row['end']))] = float(row['distance'])
            
    # print(graph)
    queue = []
    visited = []
    parent = {}
    queue.append(start)
    visited.append(start)
    distance = 0
    while queue:
        node = queue.pop(0)
        if node == end:
            path = [end]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            for i in range(len(path) - 1):
                distance += distances[(path[i], path[i + 1])]
                # print(path[i], path[i+1], distances[(path[i], path[i + 1])], distance)
            return path, distance, len(visited)
        for adjacent in graph.get(node, []):
            # print(v)
            # print(distance)
            if adjacent not in visited:
                visited.append(adjacent)
                queue.append(adjacent)
                parent[adjacent] = node
    # End your code (Part 1)

if __name__ == '__main__':
    
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')