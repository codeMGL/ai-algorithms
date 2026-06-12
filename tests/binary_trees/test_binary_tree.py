""" Testing if the BST works properly against 'sorted()' Python function"""
# python -m pytest tests/binary_trees

import pytest
import random

from binary_trees import BinaryTree

random.seed(42)

def create_random_array(n):
    return [random.randint(-100, 100) for _ in range(n)]

@pytest.mark.parametrize("n", [1, 10, 100, 1000, 5_000, 10_000, 100_000, 1_000_000])
def test_sort(n):
    array = create_random_array(n)
    
    binary_tree = BinaryTree(array)
    
    result = binary_tree.sort()
    
    assert result == sorted(set(array))
