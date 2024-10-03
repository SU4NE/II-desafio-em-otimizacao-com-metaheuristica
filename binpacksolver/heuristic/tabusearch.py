"""_summary_"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (TabuStructure, check_end, fitness,
                                 generate_solution, merge_np,
                                 theoretical_minimum)


def __container_concatenate(
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


def __container_change(
    a: int, b: int, containers: List[int], solution: List[np.ndarray], c: int
) -> np.ndarray:

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


def __container_insert(
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

    solution = __container_concatenate(a, b, containers, solution)
    solution = __container_change(a, b, containers, solution, c)

    return solution, best_fit


def __operations(
    best_fit: int,
    solution: List[np.ndarray],
    tabu: TabuStructure,
    containers: List[int],
    c: int,
) -> Tuple[List[np.ndarray], int]:
    """_summary_

    Parameters
    ----------
    best_fit : int
        _description_
    solution : np.ndarray
        _description_
    tabu : TabuStructure
        _description_
    containers : List[int]
        _description_

    Returns
    -------
    Tuple[np.ndarray, int]
        _description_
    """
    a = random.randint(0, best_fit - 2)
    b = random.randint(a, best_fit - 1)

    while a == b or tabu.find((a, b)):
        a = random.randint(0, best_fit - 2)
        b = random.randint(a, best_fit - 1)

    tabu.insert((a, b))
    new_solution, new_fit = __container_insert(
        (a, b), containers, solution, best_fit, c
    )

    return new_solution, new_fit


# pylint: disable=R0913
def tabu_search(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    alpha: int = 4,
):
    """_summary_

    Parameters
    ----------
    array_base : np.ndarray
        _description_
    c : int
        _description_
    time_max : float, optional
        _description_, by default 60
    max_it : int, optional
        _description_, by default None
    tabu : int, optional
        _description_, by default 4

    Returns
    -------
    _type_
        _description_
    """
    solution: np.ndarray = array_base.copy()
    solution, containers = generate_solution(solution, c)

    th_min: int = theoretical_minimum(array_base, c)
    best_fit: int = fitness(solution)
    tabu = TabuStructure(best_fit // max(alpha, best_fit - 1))
    it: int = 0
    time_start: float = time.time()

    while check_end(th_min, best_fit, time_max, time_start, time.time(), max_it, it):
        solution, best_fit = __operations(best_fit, solution, tabu, containers, c)
        solution.reverse()
        it += 1

    return solution, best_fit
