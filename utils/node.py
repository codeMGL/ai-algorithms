import pygame as pg
from utils import Visualizer

class Node:
    """Generic node class used to draw nodes and store children (using lists)"""

    def __init__(self, id, x=0, y=0, color=(80, 80, 80), rad=40, depth=None):
        self.id = id

        self.pos = pg.Vector2(x, y)

        # Reingold-Tilford algorithm params
        self.x = 0
        self.mod = 0
        self.shift = 0

        self.color = color
        self.rad = int(rad)

        self.children = []
        self.parent = None

        self.depth = depth if depth is not None else self.calculate_depth()

    def has_children(self) -> bool:
        return len(self.children) > 0

    @property
    def children_count(self) -> int:
        return len(self.children)

    def remove_node(self) -> None:
        self.parent.children.remove(self)

    def create_child(self, key: str, id: int | float, W: int) -> None:
        # x_off of the children relative to the parent
        # First gen get's a W / 4 offset. Second W / 8
        # As the first gen has a depth of one --> 4 = 2 ** (depth=1 + 1)
        level = self.calculate_level()
        x_off = W / (2 ** (level + 2))

        x = self.pos.x - x_off
        if key == "right":
            x = self.pos.x + x_off

        node = Node(id, x, self.pos.y + self.rad * 3.5, self.color, rad=self.rad * 0.9)

        if self.children[key]:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {key} child")

        self.children[key] = node
        node.parent = self

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

    def calculate_depth(self) -> int:
        """Returns depth of the current node"""
        # We get how many generations of parents the node has
        self.depth = 0

        node = self
        while node.parent:
            node = node.parent
            self.depth += 1

        return self.depth

    def calculate_level(self) -> int:
        """Returns the node's level: number of depths in which a node has 2 children
        level=depth if the subtrees are complete"""
        node = self
        # Starts at 0, unless parent has 2 children
        level = 0  # 1 if node.children_count == 2 else 0

        while node.parent:
            node = node.parent
            # Checking if the parent has 2 children
            if node.children_count == 2:
                level += 1

        return level

    def draw(self, screen: pg.surface.Surface) -> None:
        # --- Node ---
        pg.draw.circle(screen, self.color, self.pos, self.rad)
        pg.draw.circle(screen, "white", self.pos, self.rad, width=2)

        # If this node is an only-child, it is positioned directly under its parent
        parent = self.parent
        only_child = parent and parent.children_count == 1
        # --- Text ---
        if only_child:
            # We add a "L" or "R" tag
            tag = "R"
            if parent.children["right"] is None:
                tag = "L"

            font_size = int(self.rad * 0.45)
            text_pos = pg.Vector2(
                self.pos.x + self.rad * 0.5, self.pos.y + self.rad * 0.35
            )

            Visualizer.draw_text(screen, str(self.id), int(self.rad * 0.65), self.pos)
            Visualizer.draw_text(screen, tag, font_size, text_pos)
        else:
            # Just drawing its id
            Visualizer.draw_text(screen, str(self.id), int(self.rad * 0.8), self.pos)

        # --- Drawing the children ---
        for child in self._get_children(self):
            child.draw(screen)

            # Not drawing (False) if depth is >= 5
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

    def _get_max_depth(self) -> int:
        """Calculates the maximum depth of the graph given one node"""

        # If it's a leaf, returns its depth
        if not self.has_children():
            return self.calculate_depth()

        # Checks if the node has any children and calculates their depth
        max_depth = 0
        for children in self._get_children(self):
            d = children._get_max_depth()
            if d > max_depth:
                max_depth = d

        return max_depth

    def copy_node(self) -> "Node":
        copied_node = Node(
            self.id, self.pos.x, self.pos.y, self.color, self.rad, self.depth
        )
        copied_node.parent = self.parent
        copied_node.children = self.children
        return copied_node

    def _get_children(self, node):
        if isinstance(node.children, dict):
            return [c for c in node.children.values() if c is not None]
        return [c for c in node.children if c is not None]

    def __str__(self):
        return str(self.id)

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id
