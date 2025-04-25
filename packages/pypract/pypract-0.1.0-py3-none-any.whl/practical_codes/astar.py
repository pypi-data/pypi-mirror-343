import heapq

def a_star_search(graph, start, goal, heuristics):
    open_list = [] 
    heapq.heappush(open_list, (0 + heuristics[start], start, [start], 0))
    
    visited = set()

    while open_list:
        f_cost, current, path, g_cost = heapq.heappop(open_list)

        if current in visited:
            continue
        
        visited.add(current)

        if current == goal:
            print("Path found:", ' -> '.join(path))
            print("Total cost:", g_cost)
            return

        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                new_g = g_cost + cost
                new_f = new_g + heuristics[neighbor]
                heapq.heappush(open_list, (new_f, neighbor, path + [neighbor], new_g))

    print("No path found.")

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 3)],
    'D': [('G', 1)],
    'E': [('G', 2)],
    'F': [('G', 5)],
    'G': []
}

heuristics = {
    'A': 7,
    'B': 6,
    'C': 5,
    'D': 4,
    'E': 3,
    'F': 2,
    'G': 0
}

a_star_search(graph, 'A', 'G', heuristics)

