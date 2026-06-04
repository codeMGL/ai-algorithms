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
        """DFS implementation"""
        # Current node is 'start' the first iteration
        
        while self.current_node != self.goal:
            # 1. Expand the current node
            self.expanded.append(self.current_node)

            # 2. Add children (without repeating nodes) to the end of the queue
            for child in self.current_node.children:
                if child not in self.opened:
                    # We make their main parent the node that opened it
                    child.parent = self.current_node
                    self.opened.append(child)

            # 3. We check if the goal is already on the opened list as
            # it's guaranteed that if we go there we'll find the optimal path
            if self.goal in self.opened:
                self.goal.parent = self.current_node
                break
                
            # 4. We select the first node of the queue
            self.current_node = self.opened.pop(0)
            

        self.path = self._get_path()
