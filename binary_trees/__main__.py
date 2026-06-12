from .binary_tree import BinaryTree
from utils import Visualizer

# Screen dimensions
window_W, window_H = 800, 700

# Array of number to order
array = [50, 25, 13, 28, 3, 2, 1, 75, 67, 65, 68, 22, 26, 27, 24]
# array = [40, 12, 45, 20, 6, 19, 1, 4, 8, 7, 30, 26, 24, 17, 43]


# --- BINARY TREE ---
binary_tree = BinaryTree(array)

# Sorting the tree
sorted_tree = binary_tree.sort()
print("Sorted tree:\n", sorted_tree)

# Visualizing the tree
vis = Visualizer(window_W, window_H, "Binary tree", root=binary_tree.root)
vis.run()
