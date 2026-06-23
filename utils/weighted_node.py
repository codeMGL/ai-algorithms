import pygame as pg
from utils import Node, Visualizer


class WeightedNode(Node):
    """Node used for search algorithms with weights"""

    def __init__(self, id, x=None, y=None, color=(50, 80, 100), rad=30):
        super().__init__(id, color=color, rad=rad)

        if x is not None and y is not None:
            self.pos.x, self.pos.y = x, y

        # The node gets to know the shortest path, in order to draw the green arrows
        self.path = None

        # Dictionary (child, weight) to assign weights to every child
        self._init_weights()

    def _init_weights(self):
        self.weights = {}
        for child in self.get_children():
            self.weights[child] = 1

    @property
    def weight(self):
        """Returns the weight of the edge between its main parent and itself"""
        if self.parent:
            return self.parent.weights[self]
        else:
            return 0
        
    @property
    def cost(self):
        """Returns the total weight (cost) of the path, from the root to itself"""
        weight = 0

        node = self
        while node.parent:
            weight += node.weight
            node = node.parent

        return round(weight, 2)


    def draw_optimized(self, screen: pg.surface.Surface, scale: float) -> None:
        """Same as 'draw', but reduces drawing elements to optimize the graph"""
        # We multiply all the elements by the scale
        pos, rad = self._scaled_pos_rad(scale)

        # --- Node ---
        pg.draw.circle(screen, self.color, pos, rad)

        # --- Drawing the children and a line connecting them ---
        for child in self.get_children():
            child_pos, _ = child._scaled_pos_rad(scale)

            color = "white"
            if self.path is not None:
                if self in self.path and child in self.path:
                    color = "green"
                    # Only drawing lines if they are part of the shortest path
                    pg.draw.line(screen, color, pos, child_pos)

            child.draw_optimized(screen, scale)

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

            child_pos, child_rad = child._scaled_pos_rad(scale)

            # The arrow ends at the parent circle
            diff = child_pos - pos
            diff.scale_to_length(diff.length() - child_rad)
            end_vec = pos + diff
            # and starts at the start of the child's circle
            diff.scale_to_length(rad)
            start_vec = pos + diff

            if self.path is None:
                Visualizer.draw_arrow(
                    screen,
                    start_vec,
                    end_vec,
                    thickness=1,
                    draw_arrow_head=True,
                    arrow_size=rad * 0.45,
                )
            elif self in self.path and child in self.path:
                # If the child is part of the path, we draw a green arrow
                Visualizer.draw_arrow(
                    screen,
                    start_vec,
                    end_vec,
                    thickness=3,
                    color="green",
                    draw_arrow_head=True,
                    arrow_size=rad * 0.65,
                )

    def create_child(self, id, weight=1):
        child = super().create_child(id)
        self.weights[child] = weight

        return child

    def add_child(self, child, weight=1):
        super().add_child(child)
        self.weights[child] = weight

        return child

    def print_weights(self):
        nodes = self.pre_order_traversal()
        print("\nPrinting all nodes:")
        for node in nodes:
            if node.parents:
                weights_txt = ""
                for parent in node.parents:
                    weights_txt += f"{parent.id} --> {node.id} ({node.weight}), "
                weights_txt = weights_txt[:-2]
            else:
                weights_txt = "None (Root)"

            if node.parent:
                print(
                    " ",
                    node,
                    f"\tWeights: {weights_txt: <30}",
                    f"Cost: {node.cost}",
                )
            else:
                print(
                    " ",
                    node,
                    f"\tWeights: {weights_txt: <30}",
                    f"Cost: {node.cost}",
                )

    def __repr__(self):
        return f"{self.id}({self.cost})"

    def __str__(self):
        return f"{self.id}({self.cost})"

        # return str(self.id)

        # _txt = f"SearchNode ({self.id})"
        # _txt += f"\n Parents: "
        # for parent in self.parents:
        #     if self.parent is not None and parent == self.parent:
        #         # Main parent
        #         _txt += f"*{parent.id}*, "
        #     else:
        #         _txt += f"{parent.id}, "
        # _txt = _txt[:-2]  # Deleting extra ', '

        # _txt += "\n Children: "
        # for child in self.children:
        #     _txt += f"{child.id}, "

        # return _txt[:-2]
