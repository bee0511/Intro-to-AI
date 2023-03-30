import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
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
    visited = {}
    distance = 0
    queue = PriorityQueue()
    queue.put((0, [start]))
    visited[start] = 1
    while not queue.empty():
        pair = queue.get()
        current = pair[1][-1]
        if current == end:
            path = pair[1]
            for i in range(len(path) - 1):
                distance += distances[(path[i], path[i + 1])]
            return path, distance, len(visited)
        for neighbor in graph.get(current, []):
            if visited.get(neighbor) == 1:
                # print(neighbor, "is visited")
                continue
            new_path = list(pair[1])
            new_path.append(neighbor)
            visited[neighbor] = 1
            queue.put((pair[0] + distances[(current, neighbor)], new_path))
    return path, distance, len(visited)
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
