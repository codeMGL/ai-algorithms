import argparse
from .bfs import BFS
from .dfs import DFS
from utils import Visualizer, SearchNode

window_W, window_H = 800, 700


def create_graph(arg):
    start_color = (20, 170, 30)
    goal_color = (23, 104, 72)
    match arg:
        case "graph1":
            # A --> J
            start = SearchNode("A", root=True, color=start_color)
            B = start.create_child("B")
            C = start.create_child("C")

            D = B.create_child("D")
            E = B.create_child("E")

            F = C.create_child("F")
            G = C.create_child("G")

            H = D.create_child("H")
            I = D.create_child("I")

            goal = SearchNode("J", color=goal_color)
            I.add_child(goal)
        case "graph2":
            # A --> H
            start = SearchNode("A", root=True, color=start_color)
            B = start.create_child("B")
            C = start.create_child("C")

            D = B.create_child("D")
            E = B.create_child("E")

            C.add_child(E)

            F = D.create_child("F")
            G = D.create_child("G")

            goal = SearchNode("H", color=goal_color)
            E.add_child(goal)
            G.add_child(goal)

        case "graph3":
            # A --> I
            start = SearchNode("A", root=True, color=start_color)
            B = start.create_child("B")
            C = start.create_child("C")

            D = B.create_child("D")
            E = B.create_child("E")

            C.add_child(E)

            F = D.create_child("F")
            G = F.create_child("G")

            E.add_child(G)
            E.create_child("H")

            goal = SearchNode("I", color=goal_color)
            G.add_child(goal)

        case "graph4":
            # A --> Z
            start = SearchNode("A", root=True, color=start_color)
            print(start.color)
            B = start.create_child("B")
            C = start.create_child("C")
            D = start.create_child("D")
            E = start.create_child("E")

            F = B.create_child("F")
            G = B.create_child("G")
            H = B.create_child("H")

            I = C.create_child("I")
            J = C.create_child("J")
            K = E.create_child("K")

            L = K.create_child("L")
            M = K.create_child("M")
            J.add_child(M)
            N = L.create_child("N")
            O = N.create_child("O")

            goal = SearchNode("Z", color=goal_color)
            O.add_child(goal)

        case "test_graph":
            # r -> p
            start = SearchNode("r", root=True, color=(20, 170, 30))

            g = start.create_child("g")
            h = start.create_child("h")
            n = start.create_child("n")
            q = start.create_child("q")

            a = g.create_child("a")
            b = g.create_child("b")
            e = g.create_child("e")
            f = g.create_child("f")

            c = e.create_child("c")
            d = e.create_child("d")

            k = n.create_child("k")
            l = n.create_child("l")
            m = n.create_child("m")

            i = k.create_child("i")
            j = k.create_child("j")

            o = q.create_child("o")
            goal = SearchNode("p", color=goal_color)
            q.add_child(goal)
        case _:
            raise ValueError("Graph not defined. Please choose a valid argument")

    return start, goal


# -- Running the chosen algorithm --
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph",
        choices=(
            "graph1",
            "graph2",
            "graph3",
            "graph4",
            "test_graph",
            "8-puzzle",
            "top-spin",
        ),
        help="Graph to run the algorithm in",
    )
    parser.add_argument(
        "algorithm",
        choices=("bfs", "dfs", "all"),
        help="Search algorithm to run",
    )
    args = parser.parse_args()

    start, goal = create_graph(args.graph)

    match args.algorithm:
        case "bfs":
            bfs = BFS(start, goal)
            bfs.run()
            print("PATH (bfs):", bfs.path)
            print("Expanded nodes:", bfs.expanded)
        case "dfs":
            dfs = DFS(start, goal)
            dfs.run()
            print("PATH (dfs):", dfs.path)
            print("Expanded nodes:", dfs.expanded)
        case "all":
            bfs = BFS(start, goal)
            bfs.run()
            print("BFS:")
            print("Path:", bfs.path)
            print("Expanded nodes:", bfs.expanded)

            dfs = DFS(start, goal)
            dfs.run()
            print("\nDFS:")
            print("Path:", dfs.path)
            print("Expanded nodes:", dfs.expanded)
        case _:
            raise ValueError("Incorrect argument")

    # -- Running the graph visualizer --
    vis = Visualizer(window_W, window_H, window_title="Search Algorithms", root=start)
    vis.run()


if __name__ == "__main__":
    main()
