"""Using Pygame to visualize graphs with nodes
Other visualization options: Arcane, Matplotlib, Pyglet, Ursina...

This file includes some classes to make coding custom graphs
(binary trees, Bayesian networks, etc) easier and faster"""

# TO DO
# Resize graph horizontally as well
# Add params to control options (node color, arrow head, etc)

import pygame as pg


class Node:
    def __init__(self, id, x, y, color=(80, 80, 80), rad=40, depth=None):
        self.id = id

        self.pos = pg.Vector2(x, y)
        self.color = color
        self.rad = int(rad)

        self.children = {"left": None, "right": None}
        self.parent = None

        self.depth = depth if depth is not None else self.calculate_depth()

    def has_children(self) -> bool:
        return self.children["left"] is not None or self.children["right"] is not None

    def remove_node(self) -> None:
        # We find if it's the right or left child of its parent
        # and then we delete it
        left_child = self.parent.children["left"]
        if left_child is not None and left_child == self:
            self.parent.children["left"] = None

        right_child = self.parent.children["right"]
        if right_child is not None and right_child == self:
            self.parent.children["right"] = None

    def create_child(self, key: str, id: int | float, W: int) -> None:
        # x_off of the children relative to the parent
        # First gen get's a W / 4 offset. Second W / 8
        # As the first gen has a depth of one --> 4 = 2 ** (depth=1 + 1)
        self.calculate_depth()
        x_off = W / (2 ** (self.depth + 2))

        x = self.pos.x - x_off
        if key == "right":
            x = self.pos.x + x_off

        node = Node(id, x, self.pos.y + self.rad * 3.5, self.color, rad=self.rad * 0.9)

        if self.children[key]:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {key} child")

        self.children[key] = node
        node.parent = self

    def add_child(self, child: "Node", key: str) -> None:
        if self.children[key]:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {key} child")
        self.children[key] = child

    def calculate_depth(self) -> int:
        """Returns depth of the current node"""
        # We get how many generations of parents the node has
        self.depth = 0

        node = self
        while node.parent:
            node = node.parent
            self.depth += 1

        return self.depth

    def draw(self, screen: pg.surface.Surface, draw_id: bool = True) -> None:
        # First, we calculate it's depth to know the y coordinate and
        # the angle the children have (less spread the more deep they are)
        if self.depth is None:
            self.calculate_depth()

        # --- Node ---
        pg.draw.circle(screen, self.color, self.pos, self.rad)
        pg.draw.circle(screen, "white", self.pos, self.rad, width=2)

        # --- Text ---
        font = pg.font.SysFont("Arial", int(self.rad * 0.6))
        text = font.render(str(self.id), True, "white")
        rect = text.get_rect(center=self.pos)
        screen.blit(text, rect)

        # --- Drawing the children ---
        if len(self.children) > 0:
            for child in self.children.values():
                if child:
                    child.draw(screen, draw_id)

                    # Not drawing (False) if depth is > 5
                    draw_arrow_head = self.depth < 5

                    self._draw_arrow(
                        screen,
                        child,
                        draw_arrow_head=draw_arrow_head,
                        arrow_size=self.rad * 0.35,
                    )

    def _draw_arrow(self, screen, child, draw_arrow_head=True, arrow_size=15):
        # We draw a line between the bottom of the parent
        # and the top of the child
        # Then, we add a triangle to make the head of the arrow
        parent_vec = pg.Vector2(self.pos.x, self.pos.y + self.rad)
        child_vec = pg.Vector2(child.pos.x, child.pos.y - child.rad * 1.0)

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

    def resize_graph(self, W: int, H: int) -> None:
        if self.parent is not None:
            raise ValueError("Resizing should be done on the root of the tree")

        # We calculate the vertical height of the graph based on the depth
        max_depth = self._get_max_depth() + 0.5

        off = 20  # small offset
        H -= off

        # -- Dividing the screen --
        max_diameter = min((H / max_depth) * 0.7, 30 * 2)
        # Vertical separation between parent-children levels
        level_separation = (H / max_depth) * 0.3

        self.rad = max_diameter / 2
        self.pos.y = off / 2 + self.rad

        self._resize_children(level_separation)
        print("Graph resized!")

    def _get_max_depth(self) -> int:
        """Calculates the maximum depth of the graph given one node"""

        # If it's a leaf, returns its depth
        if not self.has_children():
            return self.calculate_depth()

        # Checks if the node has any children and calculates their depth
        left, right = 0, 0
        if self.children["right"]:
            right = self.children["right"]._get_max_depth()
        if self.children["left"]:
            left = self.children["left"]._get_max_depth()

        return max(right, left)

    def _resize_children(self, level_separation):
        """Resizes every children and their offspring"""
        if self.children["right"]:
            self.children["right"].rad = self.rad
            self.children["right"].pos.y = self.pos.y + self.rad * 2 + level_separation
            self.children["right"]._resize_children(level_separation)

        if self.children["left"]:
            self.children["left"].rad = self.rad
            self.children["left"].pos.y = self.pos.y + self.rad * 2 + level_separation
            self.children["left"]._resize_children(level_separation)

    def copy_node(self) -> "Node":
        copied_node = Node(
            self.id, self.pos.x, self.pos.y, self.color, self.rad, self.depth
        )
        copied_node.parent = self.parent
        copied_node.children = self.children
        return copied_node

    def __str__(self):
        return str(self.id)

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id


class Visualizer:

    def __init__(self, W=800, H=600, window_title=""):
        pg.init()
        pg.display.set_caption(window_title)
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.running = True

        # List containing root nodes
        self.nodes = []

    def add_root(self, root) -> None:
        self.nodes.append(root)

    def add_nodes(self, nodes) -> None:
        for node in nodes:
            self.nodes.append(node)

    def run(self) -> None:
        while self.running:
            keys = pg.key.get_pressed()

            # Check if the user wants to quit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            if keys[pg.K_q]:
                self.running = False

            # --- Drawing code ---
            self.screen.fill("black")

            for node in self.nodes:
                if node:
                    node.draw(self.screen)

            # --- Updating screen ---
            pg.display.flip()
            self.clock.tick(60)  # 60 FPS

        # If not running
        pg.quit()
