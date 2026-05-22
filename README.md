# ai-algorithms
AI from Scratch: Building foundational AI algorithms in Python

## Visualizer
Drawing the graphs using the [Reingold-Tilford algorithm](https://towardsdatascience.com/reingold-tilford-algorithm-explained-with-walkthrough-be5810e8ed93/) and the [Pygame](https://www.pygame.org/docs/) library

## 2. Binary Trees
Implementation of a Binary Search Tree (BST) with recursive in-order traversal from Scratch,
including visualization, insertion and recursive sorting

- To run the script: ``python -m binary_trees``
- To run some tests: ``python -m pytest tests/binary_trees`` or ``pytest tests/binary_trees/test_binary_tree.py``

## Possible future structure

```
ai-algorithms/
├── README.md
├── search_algorithms/
│   ├── __init__.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── dijkstra.py
│   ├── astar.py
│   └── examples/
│       └── maze_solver.py
├── binary_trees/
│   ├── __init__.py
│   ├── binary_tree.py
│   ├── bst.py
│   └── examples/
│       └── word_search.py
├── decision_trees/
│   ├── __init__.py
│   ├── id3.py
│   ├── one_r.py
│   └── examples/
│       └── classifier.py
├── production_systems/
│   ├── __init__.py
│   ├── inference_engine.py
│   ├── facts/
│   │   └── animals.pl
│   └── examples/
│       └── animal_classifier.py
├── uncertainty/
│   ├── __init__.py
│   ├── bayesian_network.py
│   ├── markov_chain.py
│   ├── hmm.py
│   ├── mdp.py
│   └── examples/
│       ├── weather_prediction.ipynb
│       └── grid_world.ipynb
├── utils/
│   ├── __init__.py
│   └── visualizer.py
└── tests/
    ├── __init__.py
    ├── search_algorithms/
    │   ├── __init__.py
    │   └── test_bfs.py
    ├── binary_trees/
    │   ├── __init__.py
    │   └── test_binary_tree.py
    ├── decision_trees/
    │   ├── __init__.py
    │   └── test_id3.py
    ├── production_systems/
    │   ├── __init__.py
    │   └── test_inference_engine.py
    └── uncertainty/
        ├── __init__.py
        └── test_bayesian_network.py
```