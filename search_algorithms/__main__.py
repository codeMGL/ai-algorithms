import pygame as pg
from .bfs import BFS
from utils import Visualizer, Node

W, H = 800, 700

# TO DO
# Move SearchNode to Visualizer and make it PolyTreeNode insted

class SearchNode(Node):
    """Node used for search algorithms. Can handle multiple parents"""
    def __init__(self, id, root=False, color=(80, 80, 80)):
        if root:
            super().__init__(id, x=W / 2, y=40, rad=45, color=color)
        else:
            super().__init__(id, color=color)
        # Can handle multiple parents
        self.parents = []

    def create_child(self, id) -> "SearchNode":
        child = SearchNode(id)

        children_ids = [c.id for c in self.children if c.id]
        if id in children_ids:
            raise ValueError(f"VALUE ERROR: Node {self.id} already has a {id} child")

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
        return child

    def draw(self, screen: pg.surface.Surface) -> None:
        # --- Node ---
        pg.draw.circle(screen, self.color, self.pos, self.rad)
        pg.draw.circle(screen, "white", self.pos, self.rad, width=2)

        Visualizer.draw_text(screen, str(self.id), int(self.rad * 0.8), self.pos)

        # --- Drawing the children ---
        for child in self._get_children(self):
            child.draw(screen)

            # Not drawing (False) if depth is >= 5
            draw_arrow_head = self.depth < 5

            self._draw_arrow(
                screen,
                child,
                draw_arrow_head=draw_arrow_head,
                arrow_size=self.rad * 0.35,
            )

    def __str__(self):
        _txt = f"SearchNode (id={self.id})"
        _txt += f"\nParents: "
        for parent in self.parents:
            if self.parent is not None and parent == self.parent:
                # Main parent
                _txt += f"*{parent.id}*, "
            else:
                _txt += f"{parent.id}, "
        _txt = _txt[:-2] # Extra ', '

        _txt += "\nChildren: "
        for child in self.children:
            _txt += f"{child.id}, "

        return _txt[:-2]


# Graph to search A --> H
start = SearchNode("A", root=True, color=(20, 180, 20))
B = start.create_child("B")
C = start.create_child("C")

D = B.create_child("D")
E = B.create_child("E")

C.add_child(E)

F = D.create_child("F")
G = D.create_child("G")

E.add_child(G)

end = SearchNode("H", color=(20, 20, 180))
E.add_child(end)

print(start)
print(B)
print(C)
print(D)
print(E)
print(F)
print(G)
print(end)

# -- Initializing the algorithm --
bfs = BFS(start, end)

# -- Running the graph visualizer --
vis = Visualizer(W, H, window_title="Breath-First Search", root=start)
vis.run()
