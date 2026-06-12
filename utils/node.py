import pygame as pg
from utils import Visualizer


class Node:
    """Generic node class used to draw nodes and link children. Can handle multiple parents"""

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

    # --- TREE STRUCTURE ---
    def has_children(self) -> bool:
        return len(self.get_children()) > 0

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

    def create_child(self, id: int | float) -> "Node":

        children_ids = [c.id for c in self.children if c.id]
        if id in children_ids:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {id} child")

        # Creates a child of it's type (accepts polymorphism)
        child = type(self)(id, rad=self.rad)

        return self.add_child(child)

    def add_child(self, child: "Node") -> "Node":
        if self.children.count(child) > 0:
            raise ValueError(
                f"VALUE ERROR: Node {self.id} already has a {child.id} child"
            )

        self.children.append(child)

        child.parents.append(self)

        if child.parent is None:
            child.parent = self

        self.compute_depth()

        return child

    def copy_node(self) -> "Node":
        copied_node = type(self)(self.id, color=self.color, rad=self.rad)
        copied_node.parent = self.parent
        copied_node.children = self.get_children()
        return copied_node

    def remove_node(self) -> None:
        self.parent.children.remove(self)

    # --- DEPTH / LEVEL CALCULATIONS ---
    def compute_depth(self) -> int:
        """Returns depth of the current node"""
        # We get how many generations of parents the node has

        if not self.parent:
            return 0

        # Adding the main parent for binary nodes
        if not self.parents:
            self.parents = [self.parent]

        parent_depths = [parent.depth for parent in self.parents if parent]
        max_depth = max(parent_depths)
        self.depth = 1 + max_depth
        return self.depth

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

    # --- TRAVERSALS ---
    def pre_order_traversal(self, visited=None):
        """Pre-order Traversal (Root-Left-Right). Returns sorted list. O(n)"""
        # Tracks with a 'visited' set the nodes that have already been added
        if visited is None:
            visited = set()  # Prevents mutable default argument bug

        if self in visited:
            return []

        # Adds itself + left array + right array
        arr = []

        arr.append(self)
        visited.add(self)
        for child in self.get_children():
            arr.extend(child.pre_order_traversal(visited))

        return arr

    def post_order_traversal(self, visited=None):
        """Post-order Traversal (Left-Right-Root). Returns sorted list. O(n)"""
        # Tracks with a 'visited' set the nodes that have already been added
        if visited is None:
            visited = set()  # Prevents mutable default argument bug

        if self in visited:
            # Not adding it twice
            return []

        # Adds left array + right array + itself

        arr = []
        for child in self.get_children():
            arr.extend(child.post_order_traversal(visited))

        arr.append(self)
        visited.add(self)

        return arr

    def inorder_traversal(self) -> list:
        """Inorder traversal (Left-Root-Right). Returns sorted list. O(n)"""

        if self.has_children():
            # Adds left array + itself + right array
            arr = []
            children = self.get_children()
            idx = int(len(children) / 2)

            for child in children[:idx]:
                arr.extend(child.inorder_traversal())

            arr.append(self)

            for child in children[idx:]:
                arr.extend(child.inorder_traversal())
            return arr
        else:
            return [self]

    def get_nodes_per_level(self) -> int:
        nodes_list = self.inorder_traversal()
        levels = [0] * len(nodes_list)
        for node in nodes_list:
            idx = node.compute_depth()
            levels[idx] += 1

        return levels

    # --- DRAWING ---
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

            Visualizer.draw_arrow(
                screen,
                scale,
                self,
                child,
                draw_arrow_head=draw_arrow_head,
                arrow_size=rad * 0.45,
            )

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

    def _draw_id(self, screen, pos, rad):
        Visualizer.draw_text(screen, str(self.id), int(rad * 0.8), pos)

    # --- DUNDERS ---
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
