import pygame as pg
from utils import Visualizer


class MazeVisualizer:

    def __init__(self, maze, W=750, H=750, window_title="", step_delay=0):
        """Class that draws a maze using Pygame

        Args:
            maze (Maze)
            W (int, optional): Pygame window width. Defaults to 750.
            H (int, optional): Pygame window height. Defaults to 750.
            window_title (str, optional): Text to display as the title of the Pygame window. Defaults to "".
            step_delay (int, optional): Milliseconds to wait to run each frame. Defaults to 1000.
        """

        self.maze = maze

        pg.init()
        pg.display.set_caption(window_title)
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.running = True
        self.refresh_every = step_delay

        self.W = W
        self.H = H
        self.off = 10
        self.line_width = 2

        # REFACTOR: Change `self.screen` dimensions based on the maze dimensions
        max_dimension = max(self.W, self.H)
        max_maze_dimension = max(self.maze.w, self.maze.h)
        self.cell_width = (
            max_dimension - self.off * 2 - self.line_width
        ) / max_maze_dimension

        # We run once the code to draw the initial frame
        self.maze.generate_steps()  # To just generate the first frame
        # self.maze.generate() # To generate all the maze at once
        self.draw()

    def run(self):
        time_elapsed = 0
        while self.running:
            keys = pg.key.get_pressed()

            # Check for key events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # Pressing 'Q' also quits the program
            if keys[pg.K_q]:
                self.running = False

            dt = self.clock.tick(60)  # Max: 60 FPS
            time_elapsed += dt

            if time_elapsed > self.refresh_every:
                self.maze.run_steps(n_steps=self.maze.steps)
                self.draw()
                time_elapsed = 0

        # If not running
        pg.quit()

    def draw(self):
        # -- Drawing the background --
        self.screen.fill("black")

        w = self.cell_width
        self.line_width = min(self.line_width, w / 2)

        # -- Drawing the cells (blue and green squares) --
        for i in range(self.maze.h):
            for j in range(self.maze.w):
                # x=j: column, y=i: row
                vec = pg.Vector2(self.off + j * w, self.off + i * w)
                cell = self.maze.cells[i][j]

                x = vec.x + self.line_width / 2
                y = vec.y + self.line_width / 2
                rect = pg.Rect(x, y, w, w)
                if cell.current:
                    pg.draw.rect(self.screen, "green", rect)
                elif cell.visited:
                    pg.draw.rect(self.screen, "blue", rect)

        # -- Drawing all the walls --
        for i in range(self.maze.w + 1):
            # Drawing all vertical walls as slim rectangles
            thick_line = pg.Rect(
                self.off + i * w,
                self.off,
                self.line_width,
                self.maze.h * w + self.line_width,
            )
            pg.draw.rect(self.screen, "white", thick_line)
        for j in range(self.maze.h + 1):
            # Drawing all horizontal walls as slim rectangles
            thick_line = pg.Rect(
                self.off, self.off + j * w, self.maze.w * w, self.line_width
            )
            pg.draw.rect(self.screen, "white", thick_line)

        # -- Drawing the cells (blue and green squares) --
        for i in range(self.maze.h):
            for j in range(self.maze.w):
                vec = pg.Vector2(
                    self.off + j * w, self.off + i * w
                )  # x=j: column, y=i: row
                cell = self.maze.cells[i][j]

                # Drawing a blue line where there is no wall (to hide the white line)
                if not cell.top:
                    thick_line = pg.Rect(
                        vec.x + self.line_width,
                        vec.y,
                        w - self.line_width,
                        self.line_width,
                    )
                    pg.draw.rect(self.screen, "blue", thick_line)

                if not cell.right:
                    start = vec + pg.Vector2(w, 0)
                    thick_line = pg.Rect(
                        start.x,
                        start.y + self.line_width,
                        self.line_width,
                        w - self.line_width,
                    )
                    pg.draw.rect(self.screen, "blue", thick_line)

        # -- Updating screen --
        pg.display.flip()
