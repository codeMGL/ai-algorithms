"""Using Pygame to visualize graphs with nodes
Other visualization options: Arcane, Matplotlib, Pyglet, Ursina...

This file includes some classes to make coding custom graphs
(binary trees, Bayesian networks, etc) easier and faster"""

# TO DO
# REFACTOR: Difference between re-ordering BinaryNodes and other Nodes
# - Maybe create a [temp] list such as [left_child|None, right_child|Node]


# Resize graph horizontally as well --> Reingold-Tilford algorithm to order the graph
# Add params to control options (node color, arrow head, etc)

import pygame as pg

class Visualizer:
    """Handles the code to draw trees on the screen, based on a root"""

    def __init__(self, W=800, H=600, window_title="", root=None):
        pg.init()
        pg.display.set_caption(window_title)
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.running = True

        # List containing root nodes
        self.root = root

        # Automatically resizes the graph
        self.resize_graph(W, H)

    def reingold_tilford(self):
        """Reingold-Tilford algorithm to order the graph"""
        ###################################################
        # WIP

        # First Pass
        # Post-order Traversal (Left-Right-Root) of the tree to compute the x, mod, and shift attributes
        self._first_pass()
        # Second Pass
        # Pre-order Traversal (Root-Left-Right) of the tree, computing final x and y values
        self._second_pass()
        # Third Pass
        # Pre-order Traversal of the tree, adjusting x values for any negative cases, if any

    def _first_pass(self):
        # Computing 'x' attributes
        print("First Pass")
        id_array = self._post_order_traversal(self.root)
        print(id_array)
        x_position = []
        dict = {"id": 0, "x": 0, "mod": 0, "shift": 0}
        for i in range(len(id_array)):
            d = dict.copy()
            d["id"] = id_array[i]
            x_position.append(d.copy())
        # print(x_position)
        # Leftest node is 0
        self.root.x = 0
        self._compute_x(self.root)

    def _compute_x(self, node):
        if node.has_children():
            # Left node is already 0
            if node.children["right"]:
                node.children["right"].x = 1
                # If 'node' has both children
                if node.children["left"]:
                    node.x = 0.5

    def _second_pass(self):
        pass

    def _post_order_traversal(self, node):
        """Post-order Traversal (Left-Right-Root). Returns sorted list. O(n)"""
        if node.has_children():
            # Adds left array + itself + right array
            sorted_arr = []

            if node.children["left"]:
                sorted_arr.extend(self._post_order_traversal(node.children["left"]))

            if node.children["right"]:
                sorted_arr.extend(self._post_order_traversal(node.children["right"]))

            sorted_arr.append(node.id)

            return sorted_arr
        else:
            return [node.id]

    def resize_graph(self, W: int, H: int) -> None:
        # We calculate the vertical height of the graph based on the depth
        max_depth = self.root._get_max_depth() + 0.5

        off = 20  # small offset
        H -= off

        # -- Dividing the screen --
        max_diameter = min((H / max_depth) * 0.7, 30 * 2)
        # Vertical separation between parent-children levels
        level_separation = (H / max_depth) * 0.3

        self.root.rad = max_diameter / 2
        self.root.pos.y = off / 2 + self.root.rad

        self._reposition_subtree(self.root, level_separation, W)
        print("Graph resized!")

    def _reposition_subtree(self, node, level_separation, W):
        """Updates the position of every children and their offspring"""
        # -- Horizontal position --
        # If this node is an only-child, it is positioned directly under its parent
        parent = node.parent
        if parent:
            if parent.children_count == 1:
                node.pos.x = parent.pos.x
            else:
                level = node.calculate_level()
                if parent.children_count == 0:
                    node.pos.x = parent.pos.x
                else:
                    # REFACTOR: Difference between re-ordering BinaryNodes and other Nodes
                    # Maybe create a [temp] list such as [left_child|None, right_child|Node]
                    if isinstance(node.children, dict):
                        # BinaryNode
                        x_off = W / (2 ** (level + 1))
                        if node.key == "left":
                            node.pos.x = parent.pos.x - x_off
                        else:
                            node.pos.x = parent.pos.x + x_off
                    else:
                        # SearchNode or generic Node
                        # REFACTOR? Use Reingold-Tilford algorithm
                        num = parent.children_count
                        sep_between_children = W / (num ** (level + 1))
                        # Leftest child position
                        # 2 children: -0.5 * sep | 3 children: -1 * sep
                        x_off = (num - 1) * sep_between_children
                        index = parent.children.index(node)
                        x = index * sep_between_children * 2
                        node.pos.x = parent.pos.x - x_off + x

        # -- Vertical position --
        for child in self._get_children(node):
            child.rad = node.rad * 0.97
            child.pos.y = node.pos.y + node.rad * 2 + level_separation
            self._reposition_subtree(child, level_separation, W)

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

            self.root.draw(self.screen)

            # --- Updating screen ---
            pg.display.flip()
            self.clock.tick(60)  # 60 FPS

        # If not running
        pg.quit()

    def _get_children(self, node):
        if isinstance(node.children, dict):
            return [c for c in node.children.values() if c is not None]
        return [c for c in node.children if c is not None]
    
    @staticmethod
    def draw_text(screen: pg.surface.Surface, text: str, font_size: int, pos: pg.Vector2):
        """Custom function to draw text"""
        font = pg.font.SysFont("Arial", font_size)
        text = font.render(text, True, "white")
        rect = text.get_rect(center=pos)
        screen.blit(text, rect)
