"""_summary_"""

import numpy as np


def generate_solution(N: int, C: int, **kwargs) -> np.ndarray:
    """
    Generates a solution consisting of random integers.

    Parameters
    ----------
    N : int
        The number of random integers to generate.
    C : int
        The upper bound (exclusive) for the random integers.

    Returns
    -------
    np.ndarray
        A NumPy array containing C random integers in the range [0, N).
    """
    return np.random.randint(C, 1, N)


def fitness(solution: np.ndarray, C: int) -> int:
    """
    Counts how many times the cumulative sum exceeds C.

    Parameters
    ----------
    solution : np.ndarray
        Array of values to evaluate the cumulative sum.
    C : int
        Threshold value. Each time the cumulative sum exceeds C, it counts.

    Returns
    -------
    int
        The total number of times the cumulative sum exceeded C.
    """
    sum = 0
    response = 0

    for value in solution:
        sum += value
        if sum > C:
            response += 1
            sum = value

    if sum > 0:
        response += 1

    return response
