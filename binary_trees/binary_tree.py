"""
Binary Search Tree (BST) Logic
Author: Marco Gajón López
Date: 22-05-2026

Description:
Implementation of a Binary Search Tree with recursive in-order traversal from Scratch,
including visualization, insertion and recursive sorting
"""

from utils import Visualizer, Node

# TO DO
# Duplicate values: Add them always to the right. Or use a counter of repeated IDs on each node
# Investigate AVL Trees or Red-Black Trees

# Screen dimensions
W, H = 800, 700

# Array of number to order
array = [40, 12, 45, 20, 6, 19, 1, 4, 8, 7, 30, 26, 24, 17, 43]


class BinaryTree:
    def __init__(self, array):
        self.root = Node(array[0], W / 2, 12, rad=10)

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

    def _insert_recursive(self, current_node: Node, elt: int) -> None:
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
            current_node.create_child(key, elt, W)

    def sort(self, node: Node = None) -> list:
        """Inorder traversal. Returns sorted list. O(n)"""

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


# BINARY TREE
def main(array):
    binary_tree = BinaryTree(array)

    # Sorting the tree
    sorted_tree = binary_tree.sort()
    print("Sorted tree:\n", sorted_tree)

    binary_tree.root.resize_graph(W, H)

    # Visualizing the tree
    vis = Visualizer(W, H, "Binary tree")

    vis.add_root(binary_tree.root)
    vis.run()


if __name__ == "__main__":
    main(array)
