"""
Depth-First Search (DFS) algorithm implementation
Author: Marco Gajón López
Date: 02-06-2026

Description:
The algorithm is not complete nor optimal by design.
It is more efficient than BFS for goals deepn in the search tree.
It uses a stack to store the opened nodes (LIFO)
"""
from .search import SearchAlgorithm

class DFS(SearchAlgorithm):
    def __init__(self, start, goal):
        super().__init__(start, goal)

    def run(self):
        """DFS implementation"""
        # Current node is 'start' the first iteration
        
        while self.current_node != self.goal:
            # 1. Expand the current node
            self.expanded.append(self.current_node)

            # 2. Add children (without repeating nodes) to the front of the stack
            for child in self.current_node.children[::-1]:
                if child not in self.opened:
                    # We make their main parent the node that opened it
                    child.parent = self.current_node
                    self.opened.insert(0, child)
                    
            # 3. We select the first node of the queue
            self.current_node = self.opened.pop(0)

        self.path = self._get_path()
