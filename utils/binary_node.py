# Clean BinaryNode vs. Node code
# Duplicate values: Add them always to the right. Or use a counter of repeated IDs on each node
import pygame as pg
from .node import Node
from .visualizer import Visualizer


class BinaryNode(Node):

    def __init__(self, id, color=(50, 80, 100), rad=20):
        super().__init__(id, color=color, rad=rad)

        # We overwrite the method to use dictionaries
        self.children = {"left": None, "right": None}

    def has_children(self) -> bool:
        return self.children["left"] is not None or self.children["right"] is not None

    @property
    def children_count(self) -> int:
        children = list(self.children.values())
        return len([c for c in children if c is not None])

    @property
    def key(self) -> int | float:
        """Key: Whether it's a left or right child"""
        for key in self.parent.children.keys():
            if self.parent.children[key].id == self.id:
                return key

    def create_child(self, key: str, id: int | float) -> None:
        # x_off of the children relative to the parent
        node = BinaryNode(id, self.color, rad=self.rad * 0.9)

        if self.children[key]:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {key} child")

        self.children[key] = node
        node.parent = self
        node.compute_depth()

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

    def draw(self, screen: pg.surface.Surface, scale: float) -> None:
        # We multiply all the elements by the scale
        pos, rad = self._scaled_pos_rad(scale)

        # --- Node ---
        pg.draw.circle(screen, self.color, pos, rad)
        pg.draw.circle(screen, "white", pos, rad, width=2)

        self._draw_id(screen, pos, rad)

        # Drawing the children
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
                arrow_size=self.rad * 0.35,
            )

    def _draw_id(self, screen, pos, rad):
        # If this node is an only-child, it is positioned directly under its parent
        parent = self.parent
        only_child = parent and parent.children_count == 1
        # --- Text ---
        if only_child:
            # We add a "L" or "R" tag
            tag = "R"
            if parent.children["right"] is None:
                tag = "L"

            font_size = int(rad * 0.45)
            text_pos = pg.Vector2(pos.x + rad * 0.5, pos.y + rad * 0.35)

            Visualizer.draw_text(screen, str(self.id), int(rad * 0.65), pos)
            Visualizer.draw_text(screen, tag, font_size, text_pos)
        else:
            # Just drawing its id
            Visualizer.draw_text(screen, str(self.id), int(rad * 0.8), pos)

    def copy_node(self) -> "BinaryNode":
        copied_node = BinaryNode(
            self.id, self.pos.x, self.pos.y, self.color, self.rad, self.depth
        )
        copied_node.parent = self.parent
        copied_node.children = self.children
        return copied_node

    def remove_node(self) -> None:
        self.parent.children[self.key] = None

    def __repr__(self):
        return super().__repr__()
