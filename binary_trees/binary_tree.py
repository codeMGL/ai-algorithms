"""
Binary Search Tree (BST) Logic
Author: Marco Gajón López
Date: 22-05-2026

Description:
Implementation of a Binary Search Tree with recursive in-order traversal from Scratch,
including visualization, insertion and recursive sorting
"""

import pygame as pg
from utils import Node

# TO DO
# Clean BinaryNode vs. Node code
# Duplicate values: Add them always to the right. Or use a counter of repeated IDs on each node
# Investigate AVL Trees or Red-Black Trees


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

    def remove_node(self) -> None:
        self.parent.children[self.key] = None
        # We find if it's the right or left child of its parent
        # and then we delete it
        # left_child = self.parent.children["left"]
        # if left_child is not None and left_child == self:
        #     self.parent.children["left"] = None

        # right_child = self.parent.children["right"]
        # if right_child is not None and right_child == self:
        #     self.parent.children["right"] = None

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
        for child in self._get_children(self):
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

class BinaryTree:
    def __init__(self, array: list, W: int):
        self.root = BinaryNode(array[0], W / 2, 25, rad=20)

        self.W = W

        self.create_tree(array[1:])

    def create_tree(self, array: list) -> None:
        """Creates the tree from the array

        Args:
            array (list): List of values to create the tree
        """
        for elt in array:
            # Comparing current node value with the children
            current_node = self.root
            self._insert_recursive(current_node, elt)

    def _insert_recursive(self, current_node: BinaryNode, elt: int) -> None:
        """Calculates where should the value 'elt' be located on the tree

        Args:
            root (Node)
            current_node (Node)
            elt (int): Value to sort
        """

        if elt < current_node.id:
            key = "left"
        elif elt > current_node.id:
            key = "right"
        else:
            # Duplicate! We don't add it
            return

        child = current_node.children[key]

        if child is not None:
            return self._insert_recursive(child, elt)
        else:
            # We create it
            current_node.create_child(key, elt, self.W)

    def sort(self, node: BinaryNode = None) -> list:
        """Inorder traversal (Left-Root-Right). Returns sorted list. O(n)"""

        if node is None:
            node = self.root

        if node.has_children():
            # Adds left array + itself + right array
            sorted_arr = []

            if node.children["left"]:
                sorted_arr.extend(self.sort(node.children["left"]))

            sorted_arr.append(node.id)

            if node.children["right"]:
                sorted_arr.extend(self.sort(node.children["right"]))

            return sorted_arr
        else:
            return [node.id]
