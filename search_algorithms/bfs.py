"""
Breath-First Search (BFS) algorithm implementation
Author: Marco Gajón López
Date: 28-05-2026

Description:
It is complete and optimal
It uses a queue to store the opened nodes (FIFO)
"""
from .search import SearchAlgorithm

class BFS(SearchAlgorithm):
    def __init__(self, start, goal):
        super().__init__(start, goal)

    def run(self):
        """BFS implementation"""
        # Current node is 'start' the first iteration

        while self.current_node != self.goal:
            # 1. Expand the current node
            self.expanded.append(self.current_node)

            # 2. Add children (without repeating nodes) to the end of the queue
            for child in reversed(self.current_node.children):
                # 3. We check if the goal is already on the opened list as
                # it's guaranteed that if we go there we'll find the optimal path
                if child == self.goal:
                    self.goal.parent = self.current_node
                    self.path = self._get_path()
                    return

                if child not in self.visited:
                    self.visited.add(child)

                    # We make their main parent the node that opened it
                    child.parent = self.current_node
                    self.opened.append(child)

            # 4. We select the first node of the queue
            if not self.opened:
                # No more nodes to be opened, the goal is unreachable
                self.path = None
                return
            self.current_node = self.opened.popleft()

        self.path = self._get_path()
