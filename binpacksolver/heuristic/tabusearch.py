"""
Module for implementing the Tabu Search algorithm for optimization problems.
"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (TabuStructure, check_end, container_insert,
                                 fitness, generate_solution,
                                 theoretical_minimum)


def __operations(
    best_fit: int,
    solution: List[np.ndarray],
    tabu: TabuStructure,
    containers: List[int],
    c: int,
) -> Tuple[List[np.ndarray], int]:
    """
    Performs operations for the Tabu Search algorithm.

    Parameters
    ----------
    best_fit : int
        The best fitness value found so far.
    solution : np.ndarray
        The current solution represented as an array.
    tabu : TabuStructure
        The structure used to manage taboo moves.
    containers : List[int]
        List of container capacities.
    c : int
        A parameter representing a constraint or capacity.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The new solution and its fitness value.
    """
    a = random.randint(0, best_fit - 2)
    b = random.randint(a, best_fit - 1)

    while a == b or tabu.find((a, b)):
        a = random.randint(0, best_fit - 2)
        b = random.randint(a, best_fit - 1)

    tabu.insert((a, b))
    new_solution, new_fit, containers = container_insert(
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
) -> Tuple[List[np.ndarray], int]:
    """
    Executes the Tabu Search algorithm for bin packing.

    Parameters
    ----------
    array_base : np.ndarray
        The base array representing items to pack.
    c : int
        The capacity of the bins or containers.
    time_max : float, optional
        Maximum allowable time for the search, by default 60.
    max_it : int, optional
        Maximum number of iterations allowed, by default None.
    alpha : int, optional
        Parameter affecting tabu structure size, by default 4.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness value.
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
        it += 1

    return solution, best_fit


# pylint: enable=R0913
