import networkx as nx
import pytest
import random

from search_algorithms import BFS, DFS
from utils import SearchNode, Visualizer

random.seed(42)

window_W, window_H = 1200, 700
test_values = [1, 10, 100, 1000, 10_000, 100_000]


def random_tree_generator(n):
    start = SearchNode("0", root=True)

    G= nx.Graph()

    # i: Number of nodes on the tree
    i = 1
    if n == 1:
        G.add_edge(start.id, start.id)
        return start, start, G

    while i < n:
        node = start
        # There's a 70% chance to choose the children
        while random.random() < 0.7 + 0.08 * node.children_count:
            if node.children_count != 0:
                node = random.choice(node.children)
            else:
                # No more children
                break

        # Number of children
        for _ in range(random.randrange(1, 5)):
            # Adding a SearchNode object
            new_node = node.create_child(str(i))
            # Adding an edge to the NetworkX Graph
            G.add_edge(new_node.id, node.id)
            i += 1

    goal = new_node
    goal.color = (50, 80, 100)
    return start, goal, G


@pytest.mark.parametrize("n", test_values)
def test_bfs(n):
    start, goal, G = random_tree_generator(n)
    bfs = BFS(start, goal)
    bfs.run()

    # vis = Visualizer(window_W, window_H, root=start)
    # vis.run()

    path = nx.shortest_path(G, start.id, goal.id)

    bfs_path = [node.id for node in bfs.path if node.id]
    print(n, bfs_path)

    assert bfs_path == path


@pytest.mark.parametrize("n", test_values)
def test_dfs(n):
    start, goal, G = random_tree_generator(n)
    dfs = DFS(start, goal)
    dfs.run()

    path = nx.shortest_path(G, start.id, goal.id)

    dfs_path = [node.id for node in dfs.path if node.id]
    print(n, dfs_path)

    assert dfs_path == path
