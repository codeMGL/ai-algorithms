import pygame as pg
from utils import Node
from utils import Visualizer


class SearchNode(Node):
    """Node used for search algorithms. Can handle multiple parents"""

    def __init__(self, id, root=False, color=(50, 80, 100), rad=30):
        if root:
            super().__init__(id, rad=rad, color=color)
        else:
            super().__init__(id, color=color, rad=rad)

    def create_child(self, id) -> "SearchNode":
        children_ids = [c.id for c in self.children if c.id]
        if id in children_ids:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {id} child")

        child = SearchNode(id, rad=self.rad)
        self._depth = self.compute_depth()

        return self.add_child(child)

    def add_child(self, child: "Node") -> None:
        if self.children.count(child) > 0:
            raise ValueError(
                f"VALUE ERROR: Node {self.id} already has a {child.id} child"
            )
        self.children.append(child)
        child.parents.append(self)

        # We add the first parent as the main parent
        if child.parent is None:
            child.parent = self

        self._depth = self.compute_depth()
        return child

    def draw(self, screen: pg.surface.Surface, scale: float) -> None:
        return super().draw(screen, scale)

    def _draw_id(self, screen, pos, rad):
        Visualizer.draw_text(screen, str(self.id), int(rad * 0.8), pos)

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

    def __repr__(self):
        return super().__repr__()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return super().__hash__()
