"""Base class for search algorithms"""
from collections import deque

class SearchAlgorithm:
    def __init__(self, start, goal):
        self.cycle = 0
        self.start = start
        self.goal = goal

        self.current_node = start

        # Double-queue of opened nodes
        self.opened = deque()

        # List of expanded nodes
        self.expanded = []
        
        # Set of visited nodes
        self.visited = {start}

        # Found path
        self.path = None

    def run(self) -> None:
        # Implemented on each subclass
        pass

    def _get_path(self) -> list:
        # Starting from the goal, we traverse upwards the tree, choosing their main parent
        # to reconstruct the shortest path to the start node found by BFS
        path = [self.goal]
        node = self.goal
        while node.parent:
            path.append(node.parent)
            node = node.parent

        # A deque could be used, but this approach is as optimal: O(n)
        path.reverse()
        return path

    def get_shortest_path(self):
        if self.path is None:
            # We calculate the shortest path with BFS
            self.run()

        return self.path
