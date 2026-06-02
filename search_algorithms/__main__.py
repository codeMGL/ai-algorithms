import pygame as pg
from .bfs import BFS
from utils import Visualizer, SearchNode

W, window_H = 800, 700

# Graph to search A --> H
start = SearchNode("A", root=True, color=(20, 170, 30), W=W)
B = start.create_child("B")
C = start.create_child("C")

D = B.create_child("D")
E = B.create_child("E")

C.add_child(E)

F = D.create_child("F")
G = D.create_child("G")

E.add_child(G)

goal = SearchNode("H", color=(50, 80, 100))
E.add_child(goal)

# # Graph to search A --> J
# start = SearchNode("A", root=True, color=(20, 170, 30))
# B = start.create_child("B")
# C = start.create_child("C")

# D = B.create_child("D")
# E = B.create_child("E")

# F = C.create_child("F")
# G = C.create_child("G")

# H = D.create_child("H")
# I = D.create_child("I")

# end = SearchNode("J", color=(50, 80, 100))
# I.add_child(end)

# -- Running the algorithm --
bfs = BFS(start, goal)
bfs.run()

# -- Running the graph visualizer --
vis = Visualizer(W, window_H, window_title="Breath-First Search (BFS)", root=start)
vis.run()
