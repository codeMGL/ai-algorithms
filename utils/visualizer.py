"""Using Pygame to visualize graphs with nodes
Other visualization options: Arcane, Matplotlib, Pyglet, Ursina...

This file includes some classes to make coding custom graphs
(binary trees, Bayesian networks, etc) easier and faster"""

import pygame as pg
from .reingold_tilford import ReingoldTilford


class Visualizer:
    """Handles the code to draw trees on the screen, based on a root"""

    def __init__(self, W=800, H=600, window_title="", root=None, fit_canvas=True):
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
        self.x_off, self.y_off = 15, 20

        # Whether to scale the graph to fit on the screen or not
        self._scaled_to_fit = fit_canvas
        # SCALES: Added together when self.scale_to_fit is True
        # Automatically calculated via R-T algorithm
        rt = ReingoldTilford(self.root, self.W, self.H, self.x_off, self.y_off)
        self._scale = rt.run()
        # Can be edited by the user (mouse wheel)
        self._zoom = 1

    def run(self) -> None:
        while self.running:
            keys = pg.key.get_pressed()

            # Check if the user wants to quit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self._scaled_to_fit = not self._scaled_to_fit

                if event.type == pg.MOUSEWHEEL:
                    self._zoom += event.precise_y * 0.1

            if keys[pg.K_q]:
                self.running = False

            # Translating the graph
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
                self._move_graph(10, 10, reset=True)

            self.draw()

        # If not running
        pg.quit()

    def draw(self):
        # --- Drawing code ---
        self.screen.fill("black")

        # Writing if the graph is scaled or not & applying scale
        if self._scaled_to_fit:
            scale = self._scale * self._zoom
            self.root.draw(self.screen, scale)
            Visualizer.draw_text(
                self.screen, f"Scaled to fit. Scale: {round(scale, 2)}", 18, (90, 20)
            )
        else:
            self.root.draw(self.screen, self._zoom)
            Visualizer.draw_text(
                self.screen,
                f"Infinite canvas. Scale: {round(self._zoom, 2)}",
                18,
                (90, 20),
            )

        # --- Updating screen ---
        pg.display.flip()
        self.clock.tick(60)  # 60 FPS

    def _move_graph(self, x, y, reset=False):
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
    def draw_arrow(
        screen, scale, parent, child, draw_arrow_head=True, arrow_size=15
    ):
        # We scale first
        parent_pos, parent_rad = parent._scaled_pos_rad(scale)
        child_pos, child_rad = child._scaled_pos_rad(scale)

        # We draw a line between the bottom of the parent
        # and the top of the child
        # Then, we add a triangle to make the head of the arrow
        parent_vec = pg.Vector2(parent_pos.x, parent_pos.y + parent_rad)
        child_vec = pg.Vector2(child_pos.x, child_pos.y - child_rad)

        if child.parent == parent and draw_arrow_head:
            # Main parent, line is thicker (creating a thick anti-aliased line)
            thickness = 3
            for i in range(thickness):
                # We enlarge the line on all directions
                off = i - thickness // 2
                pg.draw.aaline(
                    screen,
                    "white",
                    (parent_vec[0] + off / 2, parent_vec[1] + off / 2),
                    (child_vec[0] + off, child_vec[1] + off / 2),
                )

        else:
            # Not the main parent, line is 1 pixel thick
            pg.draw.aaline(screen, "white", parent_vec, child_vec)

        # --- Head ---
        if draw_arrow_head:
            # Triangle abc, with 'b' being the top of the head
            difference_vector = parent_vec - child_vec
            difference_vector.scale_to_length(arrow_size)

            a = difference_vector.copy().rotate(30)
            a += child_vec

            c = difference_vector.copy().rotate(-30)
            c += child_vec

            b = child_vec.copy()

            pg.draw.polygon(screen, "white", [a, b, c])
