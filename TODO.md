## utils/visualizer.py

### TODO
- [ ] Let the user dynamically change the Y scale as well
- [ ] Let the graph have several trees (`self.roots = []`)
- [ ] Separate the `_draw_arrow` logic of the `Node` classes
- [ ] Make "small" graphs be centered at the middle of the canvas, not to the left
- [ ] Collapse the 2 loops on `_first_pass`, if possible
- [ ] Add params to control options (node color, arrow head, etc)

### Known bugs
- [ ] R-T: child not centered under parent (`_compute_first_pass`) (solved after _second_pass improve?)

