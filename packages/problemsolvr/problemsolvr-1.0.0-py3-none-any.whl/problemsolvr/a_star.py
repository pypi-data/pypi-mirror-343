# problemsolvr/a_star.py

import heapq
import time

def a_star(graph, start, goal, heuristic):
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (0, [start]))
    g_score = {start: 0}
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

        steps += 1

        neighbors = graph.get(node, [])
        for neighbor_info in neighbors:
            neighbor, cost = (neighbor_info if isinstance(neighbor_info, tuple) else (neighbor_info, 1))
            tentative_g_score = g_score[node] + cost

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(open_set, (f_score, new_path))

    end_time = time.time()
    return {
        "path": [],
        "steps": steps,
        "time": round(end_time - start_time, 5)
    }
