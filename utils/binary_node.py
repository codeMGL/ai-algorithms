# Clean BinaryNode vs. Node code
# Duplicate values: Add them always to the right. Or use a counter of repeated IDs on each node
import pygame as pg
from .node import Node

class BinaryNode(Node):
    def __init__(self, id, x=0, y=0, color=(80, 80, 80), rad=40, depth=None):
        super().__init__(id, x=x, y=y, color=color, rad=rad, depth=depth)

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

    def create_child(self, key: str, id: int | float, W: int) -> None:
        # x_off of the children relative to the parent
        # First gen get's a W / 4 offset. Second W / 8
        # As the first gen has a depth of one --> 4 = 2 ** (depth=1 + 1)
        level = self.calculate_level()
        x_off = W / (2 ** (level + 2))

        x = self.pos.x - x_off
        if key == "right":
            x = self.pos.x + x_off

        node = BinaryNode(
            id, x, self.pos.y + self.rad * 3.5, self.color, rad=self.rad * 0.9
        )

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

    def draw(self, screen: pg.surface.Surface) -> None:
        return super().draw(screen)

    def _draw_children(self, screen):
        for child in self.get_children():
            if child is None:
                continue
            child.draw(screen)

            # Not drawing (False) if depth is >= 5
            draw_arrow_head = self.depth < 5

            self._draw_arrow(
                screen,
                child,
                draw_arrow_head=draw_arrow_head,
                arrow_size=self.rad * 0.35,
            )

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
