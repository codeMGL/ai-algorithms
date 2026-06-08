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

        # Root node, links the rest of the tree
        self.root = root

        self.W = W
        self.H = H

        # Automatically resizes the graph
        self.resize_graph()

    def reingold_tilford(self, x_off=10, y_off=20):
        """Reingold-Tilford algorithm to order the graph"""
        # x: Initial x coordinate based on the node's position
        # mod: Amount of shift for the descendants to make the children centered
        # shift: Amount of shift for the descendants (and the node itself) to
        # not overlap with the subtrees on the left

        # First Pass
        # Post-order Traversal (Left-Right-Root) of the tree to compute the x, mod, and shift attributes
        self._first_pass()

        # Second Pass
        # Pre-order Traversal (Root-Left-Right) of the tree, to compute final x and y values
        self._second_pass(x_off=x_off, y_off=y_off)

        # Third Pass
        # Pre-order Traversal of the tree, adjusting x values for any negative cases, if any

    def _first_pass(self):
        # Computing 'x' attributes
        print("First Pass")
        nodes = self._post_order_traversal(self.root)

        for child in self.root.get_children():
            # Computes 'x' and 'mod' values for every child
            self._compute_first_pass(child)

        # Can be collapsed on the same loop REFACTOR (Check for bugs)
        print("Second phase of first pass (Post-order traversal)")
        print(nodes)
        # For every node traversed, we will check for overlaps with the subtrees of all the left siblings with its subtree
        for node in nodes:
            # Computes 'shift' values for every node
            self._compute_shift(node)

        print("x values")
        for node in nodes:
            print(node, node.x, end="; ")
        print("\nmod values")
        for node in nodes:
            print(node, node.mod, end="; ")
        print("\nshift values")
        for node in nodes:
            print(node, node.shift, end="; ")
        print()

    def _compute_first_pass(self, node) -> int:
        # Leftmost node: 'x' is the midpoint between its children
        sum = 0
        # If it's the leftmost child and has children
        is_leftmost_child = node.parent.get_children()[0] == node
        if is_leftmost_child and node.has_children():
            for child in node.get_children():
                x = self._compute_first_pass(child)
                sum += x
                # print("  ", child, x)
            node.x = sum / node.children_count
            # print(node, node.x, "leftmost node and has children: midpoint between children")
        elif is_leftmost_child:
            node.x = 0
            # print(node, node.x, "leftmost child, has no children")
        elif node.has_children():
            for child in node.get_children():
                self._compute_first_pass(child)
                # print(node, "computes x for child", child)

            self._compute_mod(node)
        else:
            # Sibling distance to the rightmost one
            # print(node, node.x, "the rest. NO CHANGES YET")
            pass

        # Computing 'x' for it's siblings
        i = 1
        sibling_distance = 1
        for sibling in node.get_right_siblings():
            sibling.x = node.x + sibling_distance * i
            # print(sibling, sibling.x, f"right sibling of {node}")
            i += 1

        return node.x

    def _compute_mod(self, node):
        print(node)
        sum = 0
        for child in node.get_children():
            sum += child.x
        midpoint = sum / node.children_count

        node.mod = node.x - midpoint

    def _get_left_contour(self, node):
        contour = [node]

        left_child = node
        while left_child.has_children():
            # Just adding children that have left_child as their main parent
            children = [c for c in left_child.get_children() if c.parent == left_child]
            if not children:
                break

            left_child = children[0]
            contour.append(left_child)

        return contour

    def _get_right_contour(self, node):
        contour = [node]

        right_child = node
        while right_child.has_children():
            # Just adding children that have left_child as their main parent
            children = [
                c for c in right_child.get_children() if c.parent == right_child
            ]
            if not children:
                break

            right_child = children[-1]
            contour.append(right_child)

        return contour

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

    def _compute_shift(self, node):
        # Calculating the "profile" of a subtree from a left/right POV
        # If the root has children [A, B, C, D], all the calculations would be:
        # right(A) vs left(B)
        # right(B) vs left(C), right(A) vs left(C)
        # right(C) vs left(D), right(B) vs left(D), right(A) vs left(D)

        children = node.get_children()
        for i in range(len(children) - 1):
            shift = 0
            child = children[i + 1]
            left_contour = self._get_left_contour(child)
            for j in range(0, i + 1):
                right_contour = self._get_right_contour(children[j])
                # Calculating if there's an overlap
                subtree_dist = 2

                # zip() automatically stops when the shortest list is finished
                for left_node, right_node in zip(left_contour, right_contour):
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

                    # We calculate the right shift needed and update the 'shift' if it's higher
                    shift_needed = max(0, right_x - left_x + subtree_dist)
                    shift = max(shift, shift_needed)
            """
`children` — es la lista de hijos del nodo que estás procesando, que es exactamente lo que necesitas iterar
para redistribuir el shift entre todos ellos.
`siblings` sería correcto si estuvieras dentro del contexto de `child`, pero aquí estás en el contexto de `node`,
así que `children`.
            """
            # We shift it's siblings
            # siblings = child.get_siblings()
            # for n in range(i + 1):
            #     # left_shift(n) += total_shift * (n / child_index)
            #     siblings[n].shift += shift * (n / (i + 1))

            # # The child gets all the shift: total_sift * (n / child_index), where n == child_index
            # child.shift += shift
            for n in range(len(children)):
                # left_shift(n) += total_shift * (n / child_index)
                children[n].shift += shift * (n / (i + 1))

    def _second_pass(self, x_off, y_off):
        """Computes the real x,y coordinates of every node"""
        nodes = self._pre_order_traversal(self.root)
        print("Second pass (Pre-order traversal):")
        print(nodes)

        # We need to get the max 'x' to map the values
        x_values = []
        for node in nodes:
            # 'mod' shifts just its descendants
            mod = self._get_mod(node)
            # while 'shift' shifts the current node as well
            shift = self._get_shift(node)
            node.pos.x = node.x + mod + shift
            print(node, node.pos.x)
            x_values.append(node.pos.x)

        # First, we separate the nodes on the same depth so their circles don't overlap
        print("NO overlaps")
        min_gap = float("inf")
        for i in range(self.root.get_max_depth()):
            nodes_at_depth = self._get_nodes_depth(i)
            nodes_at_depth.sort(key=lambda node: node.pos.x)
            print(i, nodes_at_depth, [node.pos.x for node in nodes_at_depth if node])
            for j in range(len(nodes_at_depth) - 1):
                dist = nodes_at_depth[j + 1].pos.x - nodes_at_depth[j].pos.x
                if dist < min_gap:
                    print(
                        f"New min_gap: {dist} between {nodes_at_depth[j]} and {nodes_at_depth[j+1]} at depth {i}"
                    )
                min_gap = min(min_gap, dist)

        scale_x = (self.root.rad * 2) / min_gap
        print("scl_x", min_gap, scale_x)

        # Adding some offset at both ends to make the graph look better
        off = x_off + self.root.rad
        W = self.W - off * 2

        x_values = [x * scale_x for x in x_values]
        range_x = max(x_values) - min(x_values)
        mult_factor = W / (range_x * 1)
        print("---")
        for node in nodes:
            scale = max(scale_x, mult_factor)
            node.pos.x = off + node.pos.x * scale_x * mult_factor
            print(node, node.pos.x)

        # The root must be in the middle of its children
        sum = 0
        for child in self.root.get_children():
            sum += child.pos.x
        self.root.pos.x = sum / self.root.children_count

    def _get_nodes_depth(self, depth) -> list:
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

    def resize_graph(self) -> None:
        # Applying the algorithm to recalculate the 'x' position
        self.reingold_tilford()
        # Recalculating the 'y' position

        # We calculate the vertical height of the graph based on the depth
        max_depth = self.root.get_max_depth()

        off = 20  # small offset
        H = self.H - off

        # -- Dividing the screen --
        max_diameter = min((H / max_depth) * 0.7, 30 * 2)
        # Vertical separation between parent-children levels
        level_separation = (H / max_depth) - max_diameter

        self.root.rad = max_diameter / 2
        self.root.pos.y = off / 2 + self.root.rad

        self._reposition_subtree(self.root, level_separation)

    def _reposition_subtree(self, node, level_separation):
        """Updates the position of every children and their offspring"""
        # -- Horizontal position --
        """
        if node.parent:
            parent = node.parent

            # If this node is an only-child, it is positioned directly under its parent
            if parent.children_count == 1:
                node.pos.x = parent.pos.x
            else:

                # We calculate the number of nodes on each level
                nodes_per_level = self.root.get_nodes_per_level()
                # print("children_level", nodes_per_level)

                level = node.calculate_level()
                if parent.children_count == 0:
                    raise ValueError("Has no sense!!")
                    node.pos.x = parent.pos.x
                else:
                    # REFACTOR: Difference between re-ordering BinaryNodes and other Nodes
                    # Maybe create a [temp] list such as [left_child|None, right_child|Node]
                    if isinstance(node.children, dict):
                        # BinaryNode
                        x_off = self.W / (2 ** (level + 1))
                        if node.key == "left":
                            node.pos.x = parent.pos.x - x_off
                        else:
                            node.pos.x = parent.pos.x + x_off
                    else:
                        # SearchNode or generic Node
                        # REFACTOR? Use Reingold-Tilford algorithm
                        num = parent.children_count
                        # sep_between_children = W / (num ** (level + 1))
                        depth = node.compute_depth()
                        num = nodes_per_level[depth]
                        # print("nodes at level", depth, ": ", num)
                        sep_between_children = self.W / (num * 2)  # W / num
                        sep_between_children = self.W / 2 ** (num + 1)
                        # Leftest child position, relative to the number of nodes on that level
                        # 2 children per level: -0.5 * sep | 3 children per level: -1 * sep
                        x_off = (num - 1) * sep_between_children
                        index = parent.children.index(node)
                        x = index * sep_between_children * 2
                        node.pos.x = parent.pos.x - x_off + x
        """
        # -- Vertical position --
        for child in node.get_children():
            child.rad = node.rad * 0.98
            child.pos.y = (node.rad * 2 + level_separation) * child._depth
            self._reposition_subtree(child, level_separation)

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
