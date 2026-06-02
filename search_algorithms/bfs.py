"""
Breath-First Search (BFS) algorithm implementation
Author: Marco Gajón López
Date: 28-05-2026

Description:
Complete and optimal, using a queue (FIFO)
"""

class BFS:
    def __init__(self, start, goal):
        self.cycle = 0
        self.start = start
        self.goal = goal

        self.current_node = start

        # Queue of opened nodes (FIFO)
        self.opened = []

        # List of expanded nodes to keep track of the discovered path
        self.expanded = []

        self._shortest_path = None

    def run(self):
        while self.current_node != self.goal:
            # 1. Expand the current node
            children = self.current_node.children
            # Tuple: (Current node, expanded children)
            self.expanded.append((self.current_node, children))

            # 2. Add children (without repeating nodes) to the end of the queue
            for child in children:
                if child not in self.opened:
                    # We make their main parent the node that opened it
                    child.parent = self.current_node
                    self.opened.append(child)

            # 3. We select the first node of the queue
            self.current_node = self.opened.pop(0)

        self._shortest_path = self._get_path()

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
        if self._shortest_path is None:
            # We calculate the shortest path with BFS
            self.run()
            
        return self._shortest_path
    
    def get_ids_path(self):
        path = self.get_shortest_path()
        return [node.id for node in path if node.id]
