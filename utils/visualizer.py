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

    def __init__(self, W=800, H=600, window_title="", root=None, fit_canvas=True):
        pg.init()
        pg.display.set_caption(window_title)
        self.screen = pg.display.set_mode((W, H))
        self.clock = pg.time.Clock()
        self.running = True

        # Root node, links the rest of the tree
        self.root = root

        # --- Drawing parameters ---
        self.W = W
        self.H = H

        # Whether to scale the graph to fit on the screen or not
        self._scaled_to_fit = fit_canvas
        # SCALES: Added together when self.scale_to_fit is True
        # Automatically calculated via R-T algorithm
        self._scale = 1
        # Can be edited by the user (mouse wheel)
        self._zoom = 1

        self.x_off, self.y_off = 10, 10

        # Automatically resizes the graph using the R-T algorithm
        self.reingold_tilford()

    def reingold_tilford(self, sibling_dist=1, subtree_dist=1):
        """Reingold-Tilford algorithm to order the graph"""
        # x: Initial x coordinate based on the node's position
        # mod: Amount of shift for the descendants to make the children centered
        # shift: Amount of shift for the descendants (and the node itself) to
        # not overlap with the subtrees on the left
        if not self.root.has_children():
            return

        # First Pass
        # Post-order Traversal (Left-Right-Root) of the tree to compute the x, mod, and shift attributes
        # self._first_pass(sibling_dist, subtree_dist)
        self._first_pass(self.root.rad * 2, self.root.rad * 2)

        # Second Pass
        # Pre-order Traversal (Root-Left-Right) of the tree, to compute final x and y values
        self._second_pass()

        # Third Pass
        # Pre-order Traversal of the tree, adjusting x values for any negative cases, if any
        # --> Not needed, negative cases are handled on the second pass

    def _first_pass(self, sibling_dist, subtree_dist):
        """Calculates the 'x', 'mod' and 'shift' attributes"""
        nodes = self._post_order_traversal(self.root)
        print("First Pass")
        print(nodes)

        # --- Part 1 ---
        # Computes 'x' and 'mod' values for every child
        for node in nodes:
            self._compute_first_pass(node, sibling_dist)

        # Can be collapsed on the same loop REFACTOR (Check for bugs)
        print("Second phase of first pass (Post-order traversal)")
        print(nodes)

        # --- Part 2 ---
        # For every node traversed, we will check for overlaps with the subtrees of all the left siblings with its subtree
        print("\n[Compute shift]")

        for node in nodes:
            # Computes 'shift' values for every node
            self._compute_shift(node, subtree_dist=subtree_dist)

    def _compute_first_pass(self, node, sibling_dist) -> int:
        # Leftmost node & has children: 'x' is the midpoint between its children
        if not node.parent:
            # Root, we omit it
            return 0

        if node.parent.get_children()[0] == node:  # If it's the leftmost child

            if node.has_children():
                # Yellow node, centered with respect to its children
                children = node.get_children()
                node.x = (children[0].x + children[-1].x) / 2
            else:
                node.x = 0

        elif node.has_children():
            # Red node: It needs to center itself with respect to its children
            children = node.get_children()
            midpoint = (children[0].x + children[-1].x) / 2
            node.mod = node.x - midpoint

        # Computing 'x' for it's siblings
        i = 1
        for sibling in node.get_right_siblings():
            sibling.x = node.x + sibling_dist * i
            # print(f"{sibling} (x={sibling.x}) right sibling of {node}")
            i += 1

        return node.x

    def _get_contour(self, node, contour_type):
        """Returns the left/right contour of a subtree"""
        contour = []
        self._traverse_contour(node, 0, contour_type, contour)
        return contour

    def _traverse_contour(self, node, depth, contour_type, contour):
        # We add it if it's the first node of that depth/level
        if depth == len(contour):
            contour.append(node)

        children = node.get_children()
        # Reversed if contour_type is "RIGHT" (we visit from right to left)
        if contour_type == "RIGHT":
            children.reverse()

        for child in children:
            self._traverse_contour(child, depth + 1, contour_type, contour)

    def _get_mod(self, node):
        """Returns the accumulated mod of all the parents of a node"""
        mod = 0
        while node.parent:
            mod += node.parent.mod
            node = node.parent
        return mod

    def _get_shift(self, node):
        """Returns the accumulated shift of all the parents and the node"""
        shift = node.shift
        while node.parent:
            shift += node.parent.shift
            node = node.parent
        return shift

    def _compute_shift(self, node, subtree_dist=1):
        # Calculating the "profile" of a subtree from a left/right POV
        # If the root has children [A, B, C, D], all the calculations would be:
        # right(A) vs left(B)
        # right(B) vs left(C), right(A) vs left(C)
        # right(C) vs left(D), right(B) vs left(D), right(A) vs left(D)

        children = node.get_children()

        for i in range(len(children) - 1):
            total_shift = 0
            child = children[i + 1]
            left_contour = self._get_contour(child, "LEFT")
            for j in range(0, i + 1):
                right_contour = self._get_contour(children[j], "RIGHT")
                # Calculating if there's an overlap

                # zip() automatically stops when the shortest list is finished
                # right_node is a node of the left contour and viceversa
                for right_node, left_node in zip(left_contour, right_contour):
                    left_x = (
                        left_node.x
                        + self._get_mod(left_node)
                        + self._get_shift(left_node)
                    )
                    right_x = (
                        right_node.x
                        + self._get_mod(right_node)
                        + self._get_shift(right_node)
                    )

                    # We calculate the right shift needed and update 'total_shift' if it's higher
                    # Formula: (left_x + shift) - (right_x + shift * j/(i+1)) >= subtree_dist
                    # shift * (1 - j/(i+1)) >= right_x + subtree_dist - left_x
                    # shift >= (right_x + subtree_dist - left_x) / (1 - j/(i+1))

                    # shift_needed = max(0, right_x - left_x + subtree_dist)
                    formula = (left_x - right_x + subtree_dist) / (1 - j / (i + 1))
                    shift_needed = max(0, formula)
                    total_shift = max(total_shift, shift_needed)

            # Distributing the shift to every child (sibling of 'child')
            for n in range(len(children)):
                # Formula: left_shift(n) += total_shift * (n / child_index)
                children[n].shift += total_shift * (n / (i + 1))

    def _second_pass(self):
        """Computes the real x,y coordinates of every node"""
        # Using self.root.rad * 2
        # DIVIDE FUNCTION IN PARTS
        # SET COMMENTS AND DELETE UNNECESSARY ONES
        # CLEAN CODE AND CODE ORDER (max_depth, ._depth, for nodes in nodes x2, x_off)

        # Vertical height of the graph based on the depth
        max_depth = self.root.get_max_depth()
        print("total depth", max_depth)

        # --- CALCULATING 'x' COORDINATES ---
        nodes = self._pre_order_traversal(self.root)

        # -- Calculating the 'x' coordinates after the algorithm --
        for node in nodes:
            # 'mod' shifts just its descendants
            # while 'shift' shifts the current node as well
            mod = self._get_mod(node)
            shift = self._get_shift(node)
            node.pos.x = node.x + mod + shift

        # x_off added later
        # # Adding some offset at both ends to make the graph look better
        # x_off = self.x_off + self.root.rad
        # W = self.W - x_off * 2

        # -- Updating the x coordinates --
        for node in nodes:
            # node.pos.x = x_off + (node.pos.x - min_x) * fit_screen
            # node.pos.x = 0 + (node.pos.x - min_x) * node.rad * 2
            pass

        # -- Calculating the minumum distance between nodes, so they don't overlap --
        min_dist = float("inf")
        for depth in range(1, max_depth + 1):
            nodes_at_depth = self._get_nodes_at_depth(depth)
            nodes_at_depth.sort(key=lambda node: node.pos.x)

            for j in range(len(nodes_at_depth) - 1):
                dist = nodes_at_depth[j + 1].pos.x - nodes_at_depth[j].pos.x
                min_dist = min(min_dist, dist)

        # Makes the node occupy all the space (plus some separation)
        global_rad = min_dist / 3

        print("Separation between nodes:", min_dist)
        print("Nodes radius (global_rad):", global_rad)

        # Adding some offset at both ends to make the graph look better
        x_off = self.x_off + global_rad
        W = self.W - x_off * 2

        x_values = [node.pos.x for node in nodes]
        min_x = min(x_values)
        # Formula: range_x = (max + rad) - (min - rad) = max - min + rad + rad
        range_x = (
            max(x_values) - min_x + global_rad * 2
        )  # We need to account for nodes radius as well
        fit_screen = W / range_x  ### Transform to scale and comment meaning explanation
        print("new fit_screen", fit_screen)
        self._scale = fit_screen  ################################################### SCALE ###############

        for node in nodes:
            node.x_off = self.x_off
            node.y_off = self.y_off

        # The root must be in the middle of its children
        children = self.root.get_children()
        self.root.pos.x = (children[0].pos.x + children[-1].pos.x) / 2

        # --- CALCULATING 'y' COORDINATES ---
        y_off = self.y_off + global_rad
        H = self.H - y_off * 2

        # CHECH COMMENTS ############################
        # Dividing the screen 'H' (each level must be at least 'global_rad * 2 + level_separation' long)
        # Vertical size of a level
        # Formula (Param.): line_length >= rad * 2      # Aesthetically pleasing line
        # Formula:          level_separation = rad * 2 + line_length
        # level_separation >= rad * 2 + rad * 2
        # level_separation >= rad * 4
        level_separation = H / max_depth

        rad = level_separation / 4
        print("Node rad (global_rad):", global_rad, "rad (by level separation)", rad)

        global_rad = min(rad, global_rad)
        print("final rad", global_rad)

        # Adjusting the rad for each level so nodes don't overlap
        for node in nodes:
            # 'node.rad' cannot be bigger than the parent
            if node.parent:
                node.rad = min(node.parent.rad, global_rad)
                pass
            else:
                # Root node
                node.rad = global_rad
                pass

        # Already takes into account y_off as an attribute
        self.root.pos.y = 0

        # 'H' now starts from the root node, so we remove it's 'y' position
        # H -= global_rad * 2  # self.y_off
        level_separation = H / max_depth
        line_length = level_separation - global_rad * 2
        line_length = H / max_depth - global_rad * 2
        print("level_separation", level_separation, "line_length", line_length)

        y = (global_rad * 2 + line_length) * max_depth  # - global_rad * 2
        # H = global_rad * 2 * max_depth + line_length * max_depth
        # (H - global_rad * 2 * max_depth) / max_depth = line_length
        #  H / max_depth - global_rad * 2 = line_length

        print("H", H, "H (with line_length)", y)

        self._reposition_subtree(self.root, line_length, level_separation)

    # Bien con not scaled (excepto que los nodos se quedan en el borde izdo)
    def _second_pass0(self):
        """Computes the real x,y coordinates of every node"""
        # sibling_dist, subtree_dist
        # DIVIDE FUNCTION IN PARTS
        # SET COMMENTS AND DELETE UNNECESSARY ONES
        # CLEAN CODE AND CODE ORDER (max_depth, ._depth, for nodes in nodes x2, x_off)

        # Vertical height of the graph based on the depth
        max_depth = self.root.get_max_depth()
        print("total depth", max_depth)

        # --- CALCULATING 'x' COORDINATES ---
        nodes = self._pre_order_traversal(self.root)

        # -- Calculating the 'x' coordinates after the algorithm --
        for node in nodes:
            # 'mod' shifts just its descendants
            # while 'shift' shifts the current node as well
            mod = self._get_mod(node)
            shift = self._get_shift(node)
            node.pos.x = node.x + mod + shift

        # x_off added later
        # # Adding some offset at both ends to make the graph look better
        # x_off = self.x_off + self.root.rad
        # W = self.W - x_off * 2

        # Multiplying factor to draw the nodes throughout all the span of the screen
        x_values = [node.pos.x for node in nodes]
        min_x = min(x_values)

        # -- Updating the x coordinates --
        for node in nodes:
            node.pos.x = 0 + (node.pos.x - min_x) * node.rad * 2

        # -- Calculating the minumum distance between nodes, so they don't overlap --
        min_dist = float("inf")
        for depth in range(1, max_depth + 1):
            nodes_at_depth = self._get_nodes_at_depth(depth)
            nodes_at_depth.sort(key=lambda node: node.pos.x)

            for j in range(len(nodes_at_depth) - 1):
                dist = nodes_at_depth[j + 1].pos.x - nodes_at_depth[j].pos.x
                min_dist = min(min_dist, dist)

        # Makes the node occupy all the space (plus some separation)
        global_rad = min_dist / 3

        print("Separation between nodes:", min_dist)
        print("Nodes radius (global_rad):", global_rad)

        # Adjusting the rad for each level so nodes don't overlap
        self.root.rad = global_rad
        for node in nodes:
            # 'node.rad' cannot be bigger than the parent
            if node.parent:
                node.rad = min(node.parent.rad, global_rad)
            else:
                node.rad = global_rad

        # Adding some offset at both ends to make the graph look better
        x_off = self.x_off + global_rad
        W = self.W - x_off * 2

        x_values = [node.pos.x for node in nodes]
        min_x = min(x_values)
        range_x = (
            max(x_values) - min_x + global_rad * 2
        )  # We need to account for nodes radius as well
        fit_screen = W / range_x  ### Transform to scale and comment meaning explanation
        print("new fit_screen", fit_screen)
        self._scale = fit_screen  ################################################### SCALE ###############

        for node in nodes:
            # node.pos.x = off + (node.pos.x - min_x) * fit_screen
            # node.pos.x = off + (node.pos.x - min_x) * node.rad * 2
            node.x_off = self.x_off
            node.y_off = self.y_off

        # The root must be in the middle of its children
        children = self.root.get_children()
        self.root.pos.x = (children[0].pos.x + children[-1].pos.x) / 2

        # --- CALCULATING 'y' COORDINATES ---
        y_off = self.y_off + global_rad
        H = self.H - y_off * 2

        # CHECH COMMENTS ############################
        # Dividing the screen 'H' (each level must be at least 'global_rad * 2 + level_separation' long)
        # Vertical size of a level
        # Formula (Param.): line_length >= rad * 2      # Aesthetically pleasing line
        # Formula:          level_separation = rad * 2 + line_length
        # level_separation >= rad * 2 + rad * 2
        # level_separation >= rad * 4
        # rad = level_separation / 4

        # Already takes into account y_off as an attribute
        self.root.pos.y = 0

        # 'H' now starts from the root node, so we remove it's 'y' position
        # H -= global_rad * 2  # self.y_off
        level_separation = H / max_depth
        line_length = level_separation - global_rad * 2
        line_length = H / max_depth - global_rad * 2

        y = (global_rad * 2 + line_length) * max_depth  # - global_rad * 2
        # H = global_rad * 2 * max_depth + line_length * max_depth
        # (H - global_rad * 2 * max_depth) / max_depth = line_length
        #  H / max_depth - global_rad * 2 = line_length

        print("H", H, "H (with line_length)", y)

        self._reposition_subtree(self.root, line_length, level_separation)

    def _reposition_subtree(self, node, line_length, level_separation):
        """Updates the 'y' position of every children and their offspring"""

        for child in node.get_children():
            child.pos.y = (child.rad * 2 + line_length) * child.depth
            self._reposition_subtree(child, line_length, level_separation)

    def _get_nodes_at_depth(self, depth) -> list:
        """Returns all the nodes at an specified depth"""
        nodes = self._pre_order_traversal(self.root)
        return [node for node in nodes if node.compute_depth() == depth]

    def _post_order_traversal(self, node, visited=None):
        """Post-order Traversal (Left-Right-Root). Returns sorted list. O(n)"""
        # Tracks with a 'visited' set the nodes that have already been added
        if visited is None:
            visited = set()  # Prevents mutable default argument bug

        if node in visited:
            # Not adding it twice
            return []

        # Adds left array + right array + itself

        arr = []
        for child in node.get_children():
            arr.extend(self._post_order_traversal(child, visited))

        arr.append(node)
        visited.add(node)

        return arr

    def _pre_order_traversal(self, node, visited=None):
        """Pre-order Traversal (Root-Left-Right). Returns sorted list. O(n)"""
        # Tracks with a 'visited' set the nodes that have already been added
        if visited is None:
            visited = set()  # Prevents mutable default argument bug

        if node in visited:
            return []

        # Adds itself + left array + right array
        arr = []

        arr.append(node)
        visited.add(node)
        for child in node.get_children():
            arr.extend(self._pre_order_traversal(child, visited))

        return arr

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
            Visualizer.draw_text(self.screen, f"Scaled to fit. Scale: {round(scale, 2)}", 18, (90, 20))
        else:
            self.root.draw(self.screen, self._zoom)
            Visualizer.draw_text(self.screen, f"Infinite canvas. Scale: {round(self._zoom, 2)}", 18, (90, 20))

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

        nodes = self._pre_order_traversal(self.root)
        for node in nodes:
            node.x_off = self.x_off
            node.y_off = self.y_off

    def get_children(self, node):
        print("=" * 20, "Shoudln't be used! Refactor", node.id, node)
        if isinstance(node.children, dict):
            return [c for c in node.children.values() if c is not None]
        return [c for c in node.children if c is not None]

    @staticmethod
    def draw_text(
        screen: pg.surface.Surface, text: str, font_size: int, pos: pg.Vector2
    ):
        """Custom function to draw text"""
        font = pg.font.SysFont("Arial", font_size)
        text = font.render(text, True, "white")
        rect = text.get_rect(center=pos)
        screen.blit(text, rect)
