from .maze_generator import MazeGenerator
from .maze_visualizer import MazeVisualizer

maze_size = 20
maze = MazeGenerator(maze_size, maze_size, steps=1)
vis = MazeVisualizer(maze, window_title="Maze", step_delay=0)
vis.run()
