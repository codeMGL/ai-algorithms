import pygame as pg
from utils import Node
from utils import Visualizer


class WeightedNode(Node):
    """Node used for search algorithms with weights"""

    def __init__(self, id, root=False, color=(50, 80, 100), rad=30):
        super().__init__(id, color=color, rad=rad)

    def __str__(self):
        return str(self.id)
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
