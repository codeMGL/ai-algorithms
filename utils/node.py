import pygame as pg
from utils import Visualizer


class Node:
    """Generic node class used to draw nodes and store children (using lists)"""

    def __init__(self, id, color=(50, 80, 100), rad=30):
        self.id = id

        self.pos = pg.Vector2(0, 0)
        self.x_off, self.y_off = 0, 0

        # Reingold-Tilford algorithm params
        self.x = 0
        self.mod = 0
        self.shift = 0

        self.color = color
        self.rad = int(rad)

        self.children = []
        self.parent = None

        self.parents = []  # NOT used on Binary Nodes

        self.depth = self.compute_depth()

    def has_children(self) -> bool:
        return len(self.children) > 0

    @property
    def children_count(self) -> int:
        return len(self.get_children())

    def get_children(self):
        if isinstance(self.children, dict):
            return [c for c in self.children.values() if c is not None]
        return [c for c in self.children if c is not None]

    def get_siblings(self):
        """Returns its siblings. Not counting itself as sibling"""
        offspring = self.parent.get_children()
        siblings = [node for node in offspring if node is not self]
        return siblings

    def get_right_siblings(self):
        """Returns its siblings at the right. Not counting itself as sibling"""
        offspring = self.parent.get_children()
        idx = offspring.index(self)

        # Right-est child
        if idx == len(offspring) - 1:
            return []

        siblings = offspring[idx + 1 :]

        return siblings

    def create_child(self, key: str, id: int | float, W: int) -> None:
        # x_off of the children relative to the parent
        # First gen get's a W / 4 offset. Second W / 8
        # As the first gen has a depth of one --> 4 = 2 ** (depth=1 + 1)
        level = self.calculate_level()
        x_off = W / (2 ** (level + 2))

        x = self.pos.x - x_off
        if key == "right":
            x = self.pos.x + x_off

        node = Node(id, x, self.pos.y + self.rad * 3.5, self.color, rad=self.rad)

        if self.children[key]:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {key} child")

        self.children[key] = node
        node.parent = self

        self.compute_depth()

    def add_child(self, child: "Node") -> None:
        if self.children.count(child) > 0:
            raise ValueError(
                f"VALUE ERROR: Node {self.id} already has a {child.id} child"
            )
        self.children.append(child)
        if child.parent is None:
            child.parent = self
        else:
            print("Handle exception")

        self.compute_depth()

    def compute_depth(self) -> int:
        """Returns depth of the current node"""
        # We get how many generations of parents the node has
        # depth = 0

        if not self.parent:
            return 0

        # Adding the main parent for binary nodes
        if not self.parents:
            self.parents = [self.parent]

        parent_depths = [parent.depth for parent in self.parents if parent]
        max_depth = max(parent_depths)
        self.depth = 1 + max_depth
        return 1 + max_depth

    def get_max_depth(self) -> int:
        """Calculates the maximum depth of the graph given one node"""

        # If it's a leaf, returns its depth
        if not self.has_children():
            return self.compute_depth()

        # Checks if the node has any children and calculates their depth
        max_depth = 0
        for children in self.get_children():
            d = children.get_max_depth()
            if d > max_depth:
                max_depth = d

        return max_depth

    def calculate_level(self) -> int:
        """Returns the node's level: number of depths in which a node has 2 children
        level=depth if the subtrees are complete (on Binary Trees)"""
        node = self
        # Starts at 0, unless parent has 2 children
        level = 0  # 1 if node.children_count == 2 else 0

        while node.parent:
            node = node.parent
            # Checking if the parent has 2 children
            if node.children_count == 2:
                level += 1

        return level

    def get_nodes_per_level(self) -> int:
        nodes_list = self.inorder_traversal(self)
        levels = [0] * len(nodes_list)
        for node in nodes_list:
            idx = node.compute_depth()
            levels[idx] += 1

        return levels

    def inorder_traversal(self, node) -> list:
        """Inorder traversal (Left-Root-Right). Returns sorted list. O(n)"""

        if node.has_children():
            # Adds left array + itself + right array
            arr = []
            children = node.get_children()
            idx = int(len(children) / 2)

            for child in children[:idx]:
                arr.extend(self.inorder_traversal(child))

            arr.append(node)

            for child in children[idx:]:
                arr.extend(self.inorder_traversal(child))
            return arr
        else:
            return [node]

    def _scaled_pos_rad(self, scale) -> tuple:
        rad = self.rad * min(scale, 1.5)
        # Constraining to get nice radius
        rad = min(rad, 30)

        # We position the root at the top, regardless of the scale
        x = rad + self.x_off + (self.pos.x) * scale
        if not self.parents:
            y = self.y_off + rad + self.pos.y
        else:
            y = self.y_off + self.rad + self.pos.y

        # Constraining the values
        x = min(max(x, -(2**20)), 2**20)
        y = min(max(y, -(2**20)), 2**20)
        pos = pg.math.Vector2(x, y)

        return pos, rad

    def draw(self, screen: pg.surface.Surface, scale: float) -> None:
        # We multiply all the elements by the scale
        pos, rad = self._scaled_pos_rad(scale)

        # --- Node ---
        pg.draw.circle(screen, self.color, pos, rad)
        pg.draw.circle(screen, "white", pos, rad, width=2)

        self._draw_id(screen, pos, rad)

        # --- Drawing the children ---
        for child in self.get_children():
            child.draw(screen, scale)

            # Not drawing (False) if depth is >= 5
            draw_arrow_head = self.depth < 5

            self._draw_arrow(
                screen,
                scale,
                child,
                pos,
                rad,
                draw_arrow_head=draw_arrow_head,
                arrow_size=rad * 0.45,
            )

    def _draw_arrow(
        self, screen, scale, child, pos, rad, draw_arrow_head=True, arrow_size=15
    ):
        # We scale first
        child_pos, child_rad = child._scaled_pos_rad(scale)

        # if not self.parents:
        #     print(self.id, child.id)
        #     y = child.y_off + rad + child.pos.y
        # else:
        #     y = child.y_off + child.rad + child.pos.y
        # child_pos = pg.math.Vector2((child.x_off + child.pos.x) * scale + rad, y)

        # We draw a line between the bottom of the parent
        # and the top of the child
        # Then, we add a triangle to make the head of the arrow
        parent_vec = pg.Vector2(pos.x, pos.y + rad)
        child_vec = pg.Vector2(child_pos.x, child_pos.y - child_rad)

        if child.parent == self and draw_arrow_head:
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

    def copy_node(self) -> "Node":
        copied_node = Node(
            self.id, self.pos.x, self.pos.y, self.color, self.rad, self.depth
        )
        copied_node.parent = self.parent
        copied_node.children = self.children
        return copied_node

    def remove_node(self) -> None:
        self.parent.children.remove(self)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
