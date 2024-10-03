"""_summary_."""

import copy
import random


def opt1_s(p, n):
    """
    Apply a 2-opt swap to the path by swapping two random nodes.

    Args:
        p (list): The path to be modified.
        n (int): The number of nodes in the path.

    Returns:
        list: The modified path with two nodes swapped.
    """
    aux = copy.deepcopy(p)
    left = random.randint(0, n - 1)
    right = random.randint(0, n - 1)

    while left == right:
        left = random.randint(0, n - 1)

    aux[left], aux[right] = aux[right], aux[left]

    return aux
