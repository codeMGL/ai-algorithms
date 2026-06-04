"""Base class for search algorithms"""


class SearchAlgorithm:
    def __init__(self, start, goal):
        self.cycle = 0
        self.start = start
        self.goal = goal

        self.current_node = start

        # Queue of opened nodes (FIFO)
        self.opened = []

        # List of expanded nodes
        self.expanded = []

        # Found path
        self.path = None

    def run(self) -> None:
        # Implemented on each subclass
        pass

    def _get_path(self):
        # Starting from the goal, we traverse upwards the tree, choosing their main parent
        # to reconstruct the shortest path to the start node found by BFS
        path = [self.goal]
        node = self.goal
        while node.parent:
            path.append(node.parent)
            node = node.parent

        # A deque could be used (plus returning a 'list' object), but this approach is as optimal: O(n)
        path.reverse()
        return path

    def get_shortest_path(self):
        if self.path is None:
            # We calculate the shortest path with BFS
            self.run()

        return self.path
