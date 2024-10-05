"""_summary_"""

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
    new_solution, new_fit = container_insert((a, b), containers, solution, best_fit, c)

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
        it += 1

    return solution, best_fit


# pylint: enable=R0913
