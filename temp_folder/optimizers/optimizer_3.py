"""_summary_."""

import copy
import random


def opt3_s(p, n):
    """
    Apply a 3-opt swap to the path by swapping two segments of the path.

    Args:
        p (list): The path to be modified.
        n (int): The number of nodes in the path.

    Returns:
        list: The modified path with two segments swapped.
    """
    aux = copy.deepcopy(p)
    left = random.randint(0, n - 1)
    right = random.randint(0, n - 1)

    while left == right:
        left = random.randint(0, n - 1)

    if left > right:
        left, right = right, left

    if left + right > n:
        return aux

    start_idx = random.randint(0, n - left - right)

    (
        aux[start_idx : start_idx + left],
        aux[start_idx + left : start_idx + left + right],
    ) = (
        aux[start_idx + left : start_idx + left + right],
        aux[start_idx : start_idx + left],
    )

    return aux
