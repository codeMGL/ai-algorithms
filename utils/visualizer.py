"""Using Pygame to visualize graphs with nodes
Other visualization options: Arcane, Matplotlib, Pyglet, Ursina...

This file includes some classes to make coding custom graphs
(binary trees, Bayesian networks, etc) easier and faster"""

import pygame as pg
from .reingold_tilford import ReingoldTilford


class Visualizer:
    """Handles the code to draw trees on the screen, based on a root"""

    def __init__(self, W=800, H=600, window_title="", x_off=15, y_off=20, root=None, fit_canvas=True, auto_scale=True, optimize_drawing=False):
        pg.init()
        pg.display.set_caption(window_title)
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.running = True

        # Root node, links the rest of the tree
        self.root = root

        # --- Drawing and scaling parameters ---
        self.W = W
        self.H = H
        self.x_off, self.y_off = x_off, y_off

        # Whether to scale the graph to fit on the screen or not
        self._scaled_to_fit = fit_canvas
        # SCALES: Added together w hen self.scale_to_fit is True
        # Automatically calculated via R-T algorithm
        self._scale = 1
        # Can be edited by the user (mouse wheel)
        self._zoom = 1

        if auto_scale:
            rt = ReingoldTilford(self.root, self.W, self.H, self.x_off, self.y_off)
            self._scale = rt.run()

        # If True, makes the WeightedNodes be drawn more optimized
        self.optimize_drawing = optimize_drawing

    def run(self) -> None:
        """Listens to events and calls the draw method if there are changed on the graph"""

        # -- Draws the background, the text and the graph for the first time --
        self.draw()
        while self.running:
            keys = pg.key.get_pressed()

            # Check for key events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self._scaled_to_fit = not self._scaled_to_fit

                if event.type == pg.MOUSEWHEEL:
                    self._zoom += event.precise_y * 0.1
                    self.draw()

            # Pressing 'Q' also quits the program
            if keys[pg.K_q]:
                self.running = False

            # Translating the graph (and re-drawing it each time)
            step = 15
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self._move_graph(-step, 0)

            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self._move_graph(step, 0)

            if keys[pg.K_UP] or keys[pg.K_w]:
                self._move_graph(0, step)

            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self._move_graph(0, -step)

            # Reseting position
            if keys[pg.K_r]:
                self._zoom = 1
                self._move_graph(0, 0, reset=True)  

            self.clock.tick(60)  # 60 FPS

        # If not running
        pg.quit()

    def draw(self):
        # -- Drawing the background --
        self.screen.fill("black")

        # -- Drawing the graph and the text --
        if self._scaled_to_fit:
            scale = self._scale * self._zoom
            if self.optimize_drawing:
                self.root.draw_optimized(self.screen, scale)
            else:
                self.root.draw(self.screen, scale)
            Visualizer.draw_text(
                self.screen, f"Scaled to fit. Scale: {round(scale, 2)}", 18, (90, 20)
            )
        else:
            if self.optimize_drawing:
                self.root.draw_optimized(self.screen, self._zoom)
            else:
                self.root.draw(self.screen, self._zoom)
            Visualizer.draw_text(
                self.screen,
                f"Infinite canvas. Scale: {round(self._zoom, 2)}",
                18,
                (90, 20),
            )

        # -- Updating the screen --
        pg.display.flip()

    def _move_graph(self, x, y, reset=False):
        """Moves the graph some amount (x, y) and re-draws it"""
        if reset:
            # Resets the entire graph position, no moves it
            self.x_off, self.y_off = x, y
        else:
            self.x_off += x
            self.y_off += y

        nodes = self.root.pre_order_traversal()
        for node in nodes:
            node.x_off = self.x_off
            node.y_off = self.y_off

        self.draw()

    @staticmethod
    def draw_text(
        screen: pg.surface.Surface, text: str, font_size: int, pos: pg.Vector2
    ):
        """Custom function to draw text"""
        font = pg.font.SysFont("Arial", font_size)
        text = font.render(text, True, "white")
        rect = text.get_rect(center=pos)
        screen.blit(text, rect)

    @staticmethod
    def draw_arrow(screen, start_vec, end_vec, thickness=1, draw_arrow_head=True, arrow_size=15, color="white"):
        if thickness != 1:
            # Creating an artificial thick anti-aliased line
            for i in range(thickness):
                # We enlarge the line on all directions
                off = i - thickness // 2
                pg.draw.aaline(
                    screen,
                    color,
                    (start_vec[0] + off / 2, start_vec[1] + off / 2),
                    (end_vec[0] + off, end_vec[1] + off / 2),
                )
        else:
            # Drawing and Anti-Aliased line
            pg.draw.aaline(screen, color, start_vec, end_vec)

        # --- Head ---
        if draw_arrow_head:
            # Triangle abc, with 'b' being the top of the head
            difference_vector = start_vec - end_vec
            difference_vector.scale_to_length(arrow_size)

            a = difference_vector.copy().rotate(30)
            a += end_vec

            c = difference_vector.copy().rotate(-30)
            c += end_vec

            b = end_vec.copy()

            pg.draw.polygon(screen, color, [a, b, c])
