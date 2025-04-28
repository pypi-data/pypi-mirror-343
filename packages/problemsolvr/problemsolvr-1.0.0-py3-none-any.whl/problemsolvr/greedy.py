# problemsolvr/greedy.py

import heapq
import time

def greedy(graph, start, goal, heuristic):
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (heuristic(start), [start]))
    visited = set()
    steps = 0

    while open_set:
        _, path = heapq.heappop(open_set)
        node = path[-1]

        if node == goal:
            end_time = time.time()
            return {
                "path": path,
                "steps": steps,
                "time": round(end_time - start_time, 5)
            }

        if node not in visited:
            visited.add(node)
            steps += 1

            neighbors = graph.get(node, [])
            for neighbor_info in neighbors:
                neighbor = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(open_set, (heuristic(neighbor), new_path))

    end_time = time.time()
    return {
        "path": [],
        "steps": steps,
        "time": round(end_time - start_time, 5)
    }
