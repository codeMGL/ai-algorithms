"""Reingold-Tildford Algorithm Implementation"""
class ReingoldTilford:
    """Calculates the coordinates x,y of a tree using the R-T algorithm"""

    def __init__(self, root, W, H, x_off, y_off):
        self.root = root
        self.W, self.H = W, H
        self.x_off, self.y_off = x_off, y_off
        self._scale = 1

    def run(self):
        """Reingold-Tilford algorithm to order the graph"""
        # We will calculate the following values:
        #  - x: Initial x coordinate based on the node's position
        #  - mod: Amount of shift for the descendants to make the children centered
        #  - shift: Amount of shift for the descendants (and the node itself) to
        #    not overlap with the subtrees on the left
        if not self.root.has_children():
            return

        # First Pass
        # Post-order Traversal (Left-Right-Root) of the tree to compute the x, mod, and shift attributes
        self._first_pass(self.root.rad * 2, self.root.rad * 2)

        # Second Pass
        # Pre-order Traversal (Root-Left-Right) of the tree, to compute final x and y values
        self._second_pass()

        # Third Pass
        # Adjusting x values for any negative cases, if any
        # --> Not needed, negative cases are handled on the second pass
        return self._scale

    # ---  FIRST PASS ---

    def _first_pass(self, sibling_dist, subtree_dist):
        """Calculates the 'x', 'mod' and 'shift' attributes"""
        nodes = self.root.post_order_traversal()

        # --- Part 1 ---
        # Computes 'x' and 'mod' values for every child
        for node in nodes:
            self._compute_first_pass(node, sibling_dist)

        # Can be collapsed on the same loop REFACTOR (Check for bugs)

        # --- Part 2 ---
        # For every node traversed, we will check for overlaps with the subtrees of all the left siblings with its subtree

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
                # Leftmost node and has children: centered with respect to its children
                children = node.get_children()
                node.x = (children[0].x + children[-1].x) / 2
            else:
                node.x = 0

        elif node.has_children():
            # Not the leftmost, but has children: It needs to center itself with respect to its children
            children = node.get_children()
            midpoint = (children[0].x + children[-1].x) / 2
            node.mod = node.x - midpoint

        # Computing 'x' for it's siblings
        i = 1
        for sibling in node.get_right_siblings():
            sibling.x = node.x + sibling_dist * i
            i += 1

        return node.x

    def _compute_shift(self, node, subtree_dist):
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

    # --- SECOND PASS ---

    def _second_pass(self):
        """Computes the real x,y coordinates of every node"""
        nodes = self.root.pre_order_traversal()
        max_depth = self.root.get_max_depth()

        node_radius = self._calc_x_coords(nodes, max_depth)
        self._calc_y_coords(nodes, max_depth, node_radius)

    def _calc_x_coords(self, nodes, max_depth):
        # -- Calculating the 'x' coordinates after the algorithm --
        for node in nodes:
            # 'mod' shifts just its descendants
            # while 'shift' shifts the current node as well
            mod = self._get_mod(node)
            shift = self._get_shift(node)
            node.pos.x = node.x + mod + shift

        # -- Calculating the minumum distance between nodes --
        # This way, we can see what's the maximum radius they can have while they don't overlap
        min_dist = float("inf")
        for depth in range(1, max_depth + 1):
            nodes_at_depth = self._get_nodes_at_depth(depth)
            nodes_at_depth.sort(key=lambda node: node.pos.x)

            for j in range(len(nodes_at_depth) - 1):
                dist = nodes_at_depth[j + 1].pos.x - nodes_at_depth[j].pos.x
                min_dist = min(min_dist, dist)

        # Makes the node occupy all the space (plus some separation)
        # In case there's just a node on each level
        if min_dist == float("inf"):
            min_dist = self.root.rad * 2

        # min_dist / 3 gives a radius as spacing | min_dist / 4 gives double the radius as spacing
        node_radius = min_dist / 3

        # Adding some offset at both ends to make the graph look better
        x_off = self.x_off + node_radius
        W = self.W - x_off * 2

        x_values = [node.pos.x for node in nodes]
        min_x, max_x = min(x_values), max(x_values)
        # Formula: range_x = (max + rad) - (min - rad) = max - min + rad + rad
        range_x = max_x - min_x + node_radius * 2

        # Scaling so the graph fits the screen (used in 'scaled_to_fit' mode)
        self._scale = W / range_x

        # And we apply the offset to every node
        for node in nodes:
            node.x_off = self.x_off
            node.y_off = self.y_off
        # The root must be in the middle of its children
        children = self.root.get_children()
        self.root.pos.x = (children[0].pos.x + children[-1].pos.x) / 2

        return node_radius

    def _calc_y_coords(self, nodes, max_depth, node_radius):
        y_off = self.y_off + node_radius
        H = self.H - y_off * 2

        # Each level must have at least space --> 'level_separation = node_radius * 2 + line_length'
        # The line should be as long as the diameter --> 'line_length >= rad * 2'
        # level_separation = rad * 2 + line_length
        # ==> level_separation >= rad * 4
        # ==> rad <= level_separation / 4
        level_separation = H / max_depth
        max_rad_by_separation = level_separation / 4

        # We choose the better option, so they don't intersect
        node_radius = min(max_rad_by_separation, node_radius)

        line_length = level_separation - node_radius * 2


        # Adjusting the rad for each level so nodes don't overlap
        for node in nodes:
            if node.parent:
                # 'node.rad' cannot be bigger than the parent
                node.rad = min(node.parent.rad, node_radius)
            else:
                # Root node
                node.rad = node_radius

        self._reposition_subtree(self.root, line_length, level_separation)

    # --- TRAVERSAL AND CONTOUR HELPERS ---

    def _reposition_subtree(self, node, line_length, level_separation):
        """Updates the 'y' position of every children and their offspring"""

        for child in node.get_children():
            child.pos.y = (child.rad * 2 + line_length) * child.depth
            self._reposition_subtree(child, line_length, level_separation)

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

    # --- OTHER HELPERS ---

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

    def _get_nodes_at_depth(self, depth) -> list:
        """Returns all the nodes at an specified depth"""
        nodes = self.root.pre_order_traversal()
        return [node for node in nodes if node.compute_depth() == depth]