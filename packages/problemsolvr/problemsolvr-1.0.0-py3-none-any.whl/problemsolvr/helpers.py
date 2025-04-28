# problemsolvr/helpers.py

import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(graph, path=None, title="Graph"):
    """
    Visualize a static graph with optional solution path.

    Args:
        graph (dict): Graph represented as adjacency list.
        path (list): List of nodes representing the solution path (optional).
        title (str): Title of the graph plot.
    """
    G = nx.DiGraph()

    # Add edges
    for node, neighbors in graph.items():
        for neighbor_info in neighbors:
            neighbor = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=14)

    if path:
        # Fix path nodes
        clean_path = [p[0] if isinstance(p, tuple) else p for p in path]

        # Highlight the path edges and nodes
        path_edges = list(zip(clean_path, clean_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=clean_path, node_color='lightgreen')

    plt.title(title)
    plt.show()
