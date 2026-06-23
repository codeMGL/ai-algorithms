"""Dijkstra's Algorithm Implementation"""
from .search import SearchAlgorithm

class Dijkstra(SearchAlgorithm):
    def __init__(self, start, goal):
        super().__init__(start, goal)

        # Nodes (with the lowest total cost) that were previously opened
        self._closed = []

    def insert_child(self, child):
        # We search for the index with the same cost
        index = 0
        if len(self.opened) != 0:
            while index < len(self.opened) and self.opened[index].cost < child.cost:
                index += 1

        # EXTRA STEP: Ordering the queue alphabetically or numerically
        if isinstance(child.id, str):
            # We get the ASCII value of the string
            child_val = ord(child.id)
            while index < len(self.opened) and isinstance(self.opened[index].id, str):
                if ord(self.opened[index].id) < child_val:
                    index += 1
                else:
                    break
                
        elif isinstance(child.id, int):
            while index < len(self.opened) and isinstance(self.opened[index].id, int):
                if self.opened[index].id < child.id:
                    index += 1
                else:
                    break

        # And insert it there
        self.opened.insert(index, child)

    def run(self):
        """Dijkstra implementation"""
        # Current node is 'start' the first iteration

        while self.current_node != self.goal:
            # 1. Expand the current node
            self.expanded.append(self.current_node)

            # 2. Add children (without repeating nodes) to the end of the queue
            for child in self.current_node.children:
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
                    # And we add the child on the opened deque, keeping it sorted
                    self.insert_child(child)

            # 4. We select the node with the lowest weight
            if not self.opened:
                # No more nodes to be opened, the goal is unreachable
                self.path = None
                return
            # The lowest is at the beginning of the array
            self.current_node = self.opened.popleft()

        self.path = self._get_path()
