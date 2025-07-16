import heapq
def read_adjacency_list(filename):
    graph = {}
    lookup = {}
    with open(filename, 'r') as file:
        for line in file:
            items = line.strip().split()
            name = items[0]
            h_val = int(items[1])
            key = (name, h_val)

            graph[key] = []
            for i in range(2, len(items), 2):
                if i + 1 >= len(items):
                    break
                next_node = items[i]
                weight = int(items[i + 1])
                graph[key].append((next_node, weight))

            lookup[name] = key
    return graph, lookup


def a_star_search(adj_list, node_to_key, start, end):
    if start not in node_to_key or end not in node_to_key:
        return None, None

    start_key = node_to_key[start]
    g_scores = {node: float('inf') for node in node_to_key}
    g_scores[start] = 0

    initial_h = start_key[1]
    queue = [(0 + initial_h, start, [start], 0)]

    while queue:
        current_f, current_node, path, current_g = heapq.heappop(queue)

        if current_node == end:
            return path, current_g

        if current_g > g_scores[current_node]:
            continue

        current_key = node_to_key[current_node]
        for neighbor, distance in adj_list[current_key]:
            tentative_g = current_g + distance
            if tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                neighbor_key = node_to_key[neighbor]
                f_score = tentative_g + neighbor_key[1]
                heapq.heappush(queue, (f_score, neighbor, path + [neighbor], tentative_g))

    return None, None

adj_list, node_to_key = read_adjacency_list("Input file.txt")

start = input("Start node: ").strip()
destination = input("Destination: ").strip()

path, distance = a_star_search(adj_list, node_to_key, start, destination)

if path:
    print(f"Path: {' -> '.join(path)}")
    print(f"Total distance: {distance} km")
else:
    print("NO PATH FOUND")