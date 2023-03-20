import csv
import os
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
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
    visited = [start]
    stack = [start]
    parent = {}
    distance = 0
    while stack:
        node = stack[-1]
        if node == end:
            path = [end]
            while path[-1] != start:
                # print(path[-1])
                # os.system("pause")
                # print(parent[path[-1]])
                path.append(parent[path[-1]])
            path.reverse()
            for i in range(len(path) - 1):
                distance += distances[(path[i], path[i + 1])]
                # print(path[i], path[i+1], distances[(path[i], path[i + 1])], distance)
            return path, distance, len(visited)
        if node not in visited:
            visited.append(node)
        remove_from_stack = True
        for next_node in graph.get(node, []):
            if next_node not in visited:
                stack.append(next_node)
                parent[next_node] = node
                remove_from_stack = False
                break
        if remove_from_stack:
            stack.pop()
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
