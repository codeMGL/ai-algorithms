import pygame as pg
from utils import Node
from utils import Visualizer

class SearchNode(Node):
    """Node used for search algorithms. Can handle multiple parents"""

    def __init__(self, id, root=False, color=(80, 80, 80), W = 800):
        if root:
            super().__init__(id, x=W / 2, y=40, rad=45, color=color)
        else:
            super().__init__(id, color=color)

    def create_child(self, id) -> "SearchNode":
        children_ids = [c.id for c in self.children if c.id]
        if id in children_ids:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {id} child")

        child = SearchNode(id)
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

    def draw(self, screen: pg.surface.Surface) -> None:
        # --- Node ---
        pg.draw.circle(screen, self.color, self.pos, self.rad)
        pg.draw.circle(screen, "white", self.pos, self.rad, width=2)

        Visualizer.draw_text(screen, str(self.id), int(self.rad * 0.8), self.pos)

        # --- Drawing the children ---
        for child in self.get_children():
            child.draw(screen)

            # Not drawing (False) if depth is >= 5
            draw_arrow_head = self._depth < 5

            self._draw_arrow(
                screen,
                child,
                draw_arrow_head=draw_arrow_head,
                arrow_size=self.rad * 0.35,
            )


    def compute_depth(self):
        return super().compute_depth()

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
