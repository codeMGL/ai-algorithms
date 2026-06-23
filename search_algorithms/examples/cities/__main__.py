"""Script to find the best path between a set of cities, using Dijkstra's Algorithm and weighted edges"""

import random
import math
from utils import Visualizer, WeightedNode
from search_algorithms.examples.cities import Dijkstra

window_W, window_H = 1000, 700
node_radius = 10

# random.seed(42)


def create_map(num_cities, max_neighbours=3):
    start = WeightedNode(
        0, x=node_radius, y=window_H / 2, rad=node_radius, color=(20, 170, 30)
    )

    nodes = [start]

    for n in range(num_cities):
        if n < num_cities - 1:
            x = random.randint(node_radius * 2, window_W - node_radius * 2)
            y = random.randint(node_radius * 2, window_H - node_radius * 2)

            node = WeightedNode(n + 1, x=x, y=y, rad=node_radius)
        else:
            node = WeightedNode(
                n + 1,
                x=window_W - node_radius * 3,
                y=window_H / 2,
                rad=node_radius,
                color=(23, 104, 72),
            )
            # We delete the start node, we don't want both connected
            nodes = nodes[1:]

        num_neighbours = min(max_neighbours, len(nodes) - 1)
        posible_nodes = nodes.copy()

        for _ in range(num_neighbours):
            idx = random.choice(range(len(posible_nodes)))
            parent = posible_nodes.pop(idx)
            
            # We calculate the cost to its parent (Euclidian distance by some multiplier)
            dist = parent.pos.distance_to(node.pos) / 100
            cost = dist * random.uniform(0.75, 1.25)

            parent.add_child(node, weight=round(cost, 2))

        # We add the new node
        nodes.append(node)

    return start, node

n = 30
start, goal = create_map(n, max_neighbours=math.ceil(math.log10(n)))
dij = Dijkstra(start, goal)
dij.run()

if dij.path is not None:
    print("Path:", dij.path)

    # We draw the lines of the path thicker
    for node in dij.path:
        node.path = dij.path
else:
    print("There's no path between the start and goal nodes")

optimize_drawing = n > 100
vis = Visualizer(
    W=window_W,
    H=window_H,
    root=start,
    x_off=0,
    y_off=0,
    window_title="Path finder between cities (Dijkstra's Algorithm)",
    auto_scale=False,
    optimize_drawing=optimize_drawing,
)
vis.run()
