from typing import List, Tuple

import numpy as np

from .utils import merge_np


def container_concatenate(
    a: int, b: int, containers: List[int], solution: np.ndarray
) -> np.ndarray:
    """
    concatenates elements from line b into line a, respecting the capacity of container a.

    Parameters
    ----------
    a : int
        Index of line a in the solution.
    b : int
        Index of line b in the solution.
    containers : List[int]
        List of remaining capacities in each container.
    solution : np.ndarray
        The 2D array representing the solution.

    Returns
    -------
    np.ndarray
        The updated solution array after the concatenation.
    """
    a_line: np.ndarray = solution[a]
    b_line: np.ndarray = solution[b]

    cumsum_b_line: np.ndarray = np.cumsum(b_line)
    it = min(len(b_line) - 1, np.searchsorted(cumsum_b_line, containers[a]))

    if it > 0:
        containers[a] -= cumsum_b_line[it - 1]
        containers[b] += cumsum_b_line[it - 1]

        solution[b] = b_line[it:]
        solution[a] = merge_np(a_line, b_line[:it])

    return solution


def container_change(
    a: int, b: int, containers: List[int], solution: List[np.ndarray], c: int
) -> np.ndarray:
    """_summary_

    Parameters
    ----------
    a : int
        _description_
    b : int
        _description_
    containers : List[int]
        _description_
    solution : List[np.ndarray]
        _description_
    c : int
        _description_

    Returns
    -------
    np.ndarray
        _description_
    """
    a_line = solution[a].copy()
    cumsum_b = np.cumsum(solution[b])
    update_a: List[np.ndarray] = []

    for x in a_line:
        idx = np.searchsorted(cumsum_b, x)

        if idx > 1 and cumsum_b[-1] - cumsum_b[idx - 1] + x <= c:
            range_b: np.ndarray = solution[b][:idx]
            update_a.append(range_b)
            index_to_remove = np.where(solution[a] == x)[0]
            solution[a] = np.delete(solution[a], index_to_remove[0])

            solution[b] = solution[b][idx:]
            if len(solution[b]):
                solution[b] = merge_np(solution[b], np.array([x], dtype=int))
            else:
                solution[b] = np.append(solution[b], x)

            cumsum_b = np.cumsum(solution[b])

    for subrange in update_a:
        solution[a] = merge_np(solution[a], subrange)

    containers[a] = c - solution[a].sum()
    containers[b] = c - solution[b].sum()

    return solution


def container_insert(
    indexs: Tuple[int, int],
    containers: List[int],
    solution: List[np.ndarray],
    best_fit: int,
    c: int,
) -> Tuple[List[np.ndarray], int]:
    """_summary_

    Parameters
    ----------
    indexs : Tuple[int, int]
        _description_
    containers : List[int]
        _description_
    solution : np.ndarray
        _description_
    best_fit : int
        _description_

    Returns
    -------
    Tuple[np.ndarray, int]
        _description_
    """
    a, b = indexs
    if containers[a] >= c - containers[b]:
        containers[a] -= c - containers[b]
        solution[a] = merge_np(solution[a], solution[b])
        del solution[b]
        del containers[b]
        return solution, best_fit - 1

    solution = container_concatenate(a, b, containers, solution)
    solution = container_change(a, b, containers, solution, c)

    return solution, best_fit
