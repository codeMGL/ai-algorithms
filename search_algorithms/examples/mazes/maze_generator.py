"""Script to generate mazes using a Randomized DFS Algorithm (specifically, the stack implementation)

Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search
"""

import random
from dataclasses import dataclass

random.seed(42)


@dataclass
class Cell:
    x: int
    y: int

    # True indicates there is a wall between those 2 cells
    top: bool = True
    bottom: bool = True
    left: bool = True
    right: bool = True

    visited: bool = False
    current: bool = False

    def __repr__(self):
        return f"({self.x}, {self.y})"


class MazeGenerator:
    def __init__(self, w, h, steps=20):
        self.w = w
        self.h = h

        # Generates a 2D list that contains information about the connection between cells (parent-child relationships)
        # Then, when the maze is completely generated, it will create those Node objects from this list
        self.cells = []
        for i in range(h):
            row = []
            for j in range(w):
                row.append(Cell(x=j, y=i)) # x=j: column, y=i: row
            self.cells.append(row)

        # To eliminate recursion problems on the algorithm
        self.stack = []
        
        # Number of steps to calculate on every 'self.generate_steps()' iteration
        self.steps = steps

    def get_unvisited_neighbours(self, cell) -> list:
        """Returns all the unvisited neighbours a 'Cell' has"""
        x, y = cell.x, cell.y
        unvisited = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                # XOR: Exactly one of i, j is 0 (shared side, no diagonals, no self)
                if (i == 0) != (j == 0):
                    ni, nj = y + i, x + j
                    if 0 <= nj <= self.w - 1 and 0 <= ni <= self.h - 1:
                        if not self.cells[ni][nj].visited: # cells[row][column]
                            unvisited.append(self.cells[ni][nj])

        # print(f"Unvisited neighbours of ({x}, {y}) --> {unvisited}")
        return unvisited

    def remove_wall(self, cell, neighbour) -> None:
        """Removes the common wall between 'cell' and its 'neighbour'"""
        x1, y1 = cell.x, cell.y
        x2, y2 = neighbour.x, neighbour.y

        if x2 == x1 + 1:
            # We remove the right wall
            cell.right = False
        elif y2 == y1 + 1:
            # We remove the top wall
            neighbour.top = False
        elif x1 == x2 + 1:
            # We remove the right wall
            neighbour.right = False
        elif y1 == y2 + 1:
            # We remove the top wall
            cell.top = False

    def run_steps(self, n_steps=1):
        """Calcualtes 'n_steps' steps of the algorithm"""
        neighbour = self.current_cell
        for _ in range(n_steps):
            self.current_cell.current = False
            if self.stack:
                # 1. Pop a cell from the stack and make it a current cell
                self.current_cell = self.stack.pop()
                self.current_cell.current = True
                # 2. If the current cell has any neighbours which have not been visited
                neighbours = self.get_unvisited_neighbours(self.current_cell)
                if neighbours:
                    # 1. Push the current cell to the stack
                    self.stack.append(self.current_cell)
                    # 2. Choose one of the unvisited neighbours
                    neighbour = random.choice(neighbours)
                    # 3. Remove the wall between the current cell and the chosen cell
                    self.remove_wall(self.current_cell, neighbour)
                    # 4. Mark the chosen cell as visited and push it to the stack
                    neighbour.visited = True
                    neighbour.current = True
                    self.current_cell.current = False
                    self.stack.append(neighbour)

    def generate_steps(self, n_steps = 5):
        """Runs the algorithm step by step. To change how many steps it calculates every call, change `n_steps`"""
        # 1. Choose the initial cell, mark it as visited and push it to the stak
        x, y = random.randrange(self.w), random.randrange(self.h)
        self.current_cell = self.cells[x][y]
        self.current_cell.visited = True
        self.current_cell.current = True
        self.stack.append(self.current_cell)
        
        # 2. While the stack is not empty
        self.run_steps(n_steps)
                
    def generate(self):
        """Runs the whole algorithm on one frame"""
        # 1. Choose the initial cell, mark it as visited and push it to the stak
        x, y = random.randrange(self.w), random.randrange(self.h)
        self.current_cell = self.cells[x][y]
        self.current_cell.visited = True
        self.current_cell.current = True
        self.stack.append(self.current_cell)
        
        # 2. While the stack is not empty
        while self.stack:
            self.run_steps()
        
        