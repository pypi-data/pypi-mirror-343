# problemsolvr/ucs.py

import heapq
import time

def ucs(graph, start, goal):
    """
    Uniform Cost Search algorithm to find the minimum cost path.

    Args:
        graph (dict): Graph represented as adjacency list.
                      If weighted, edges should be (neighbor, cost) tuples.

        start (any): Starting node.
        goal (any): Goal node.

    Returns:
        dict: {
            "path": List of nodes representing the path from start to goal,
            "steps": Number of nodes expanded,
            "time": Time taken in seconds
        }
    """
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (0, [start]))  # (cumulative cost, path)
    steps = 0
    visited = {}

    while open_set:
        cost_so_far, path = heapq.heappop(open_set)
        node = path[-1]

        if node == goal:
            end_time = time.time()
            return {
                "path": path,
                "steps": steps,
                "time": round(end_time - start_time, 5)
            }

        if node not in visited or cost_so_far < visited[node]:
            visited[node] = cost_so_far
            steps += 1

            for neighbor_info in graph.get(node, []):
                if isinstance(neighbor_info, tuple):
                    neighbor, edge_cost = neighbor_info
                else:
                    neighbor = neighbor_info
                    edge_cost = 1  # Default cost if no weight given

                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(open_set, (cost_so_far + edge_cost, new_path))

    end_time = time.time()
    return {
        "path": [],
        "steps": steps,
        "time": round(end_time - start_time, 5)
    }
