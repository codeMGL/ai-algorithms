import networkx as nx
import pytest
import random

from search_algorithms import BFS
from utils import SearchNode, Visualizer

random.seed(42)

W, H = 1200, 700

def random_tree_generator(n):
    start = SearchNode("0", root=True, W=W)

    G= nx.Graph()

    # i: Number of nodes on the tree
    i = 1
    if n == 1:
        G.add_edge(start.id, start.id)
        return start, start, G
    
    
    while i < n:
        node = start
        # There's a 50% chance to choose the children
        while random.random() < 0.7 + 0.08 * node.children_count:
            if node.children_count != 0:
                node = random.choice(node.children)
            else:
                # No more children
                break

        # Number of parents
        for _ in range(random.randrange(1, 5)):
            # Adding a SearchNode object
            new_node = node.create_child(str(i))
            # Adding an edge to the NetworkX Graph
            G.add_edge(new_node.id, node.id)
            i += 1
            
    goal = new_node
    goal.color = (50, 80, 100)
    return start, goal, G


@pytest.mark.parametrize("n", [1, 10, 100, 1000, 5_000, 10_000, 20_000])
def test_sort(n):
    start, goal, G = random_tree_generator(n)
    bfs = BFS(start, goal)
    bfs.run()
    
    # vis = Visualizer(W, H, root=start)
    # vis.run()

    path = nx.shortest_path(G, start.id, goal.id)
    
    print(n, bfs.get_ids_path())
    # print(path)
    
    assert bfs.get_ids_path() == path
