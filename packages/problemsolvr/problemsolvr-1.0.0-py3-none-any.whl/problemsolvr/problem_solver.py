# problemsolvr/problem_solver.py

from .bfs import bfs
from .dfs import dfs
from .a_star import a_star
from .greedy import greedy
from .ucs import ucs
from .helpers import visualize_graph

class ProblemSolver:
    """
    Main interface class for users to solve problems using different algorithms.
    """

    results = {}  # <-- Added a class variable to store results

    @staticmethod
    def solve(graph, start, goal, method="bfs", heuristic=None, visualize=False):
        """
        Solve the problem using the selected algorithm.
        """
        method = method.lower()

        if method == "bfs":
            result = bfs(graph, start, goal)

        elif method == "dfs":
            result = dfs(graph, start, goal)

        elif method == "a_star":
            if heuristic is None:
                raise ValueError("Heuristic function required for A* Search.")
            result = a_star(graph, start, goal, heuristic)

        elif method == "greedy":
            if heuristic is None:
                raise ValueError("Heuristic function required for Greedy Search.")
            result = greedy(graph, start, goal, heuristic)

        elif method == "ucs":
            result = ucs(graph, start, goal)

        else:
            raise ValueError(f"Unknown method '{method}'. Please choose from: 'bfs', 'dfs', 'a_star', 'greedy', 'ucs'.")

        if visualize:
            visualize_graph(graph, result["path"], title=f"{method.upper()} Solution Path")

        # 🔥 Auto-store result inside results dictionary
        ProblemSolver.results[method.upper()] = result

        return result

    @staticmethod
    def show_summary():
        """
        Display a summary of all solved algorithms, paths, steps and time taken.
        """
        if not ProblemSolver.results:
            print("No algorithms have been solved yet!")
            return

        print("\n\n================ FINAL SUMMARY ================\n")
        print(f"{'Algorithm':<25} | {'Path':<20} | {'Steps':<7} | {'Time (sec)':<10}")
        print("-" * 70)

        for algo, res in ProblemSolver.results.items():
            path_str = "->".join(res['path'])
            steps = res['steps']
            time_taken = res['time']
            print(f"{algo:<25} | {path_str:<20} | {steps:<7} | {time_taken:<10}")

        print("\n================================================")
