"""_summary_."""
import copy
import random

def opt2_s(p, n):
    """
    Apply a 3-opt swap to the path by reversing a segment of the path.

    Args:
        p (list): The path to be modified.
        n (int): The number of nodes in the path.

    Returns:
        list: The modified path with a segment reversed.
    """
    aux = copy.deepcopy(p)
    left = random.randint(0, n - 1)
    right = random.randint(0, n - 1)

    while left == right:
        left = random.randint(0, n - 1)

    if left > right:
        left, right = right, left

    while left > right:
        aux[left], aux[right] = aux[right], aux[left]
        left += 1
        right -= 1

    return aux