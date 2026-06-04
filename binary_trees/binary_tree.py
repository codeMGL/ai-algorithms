"""
Binary Search Tree (BST) Logic
Author: Marco Gajón López
Date: 22-05-2026

Description:
Implementation of a Binary Search Tree with recursive in-order traversal from Scratch,
including visualization, insertion and recursive sorting
"""

import pygame as pg
from utils import BinaryNode

# TO DO
# Investigate AVL Trees or Red-Black Trees

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
