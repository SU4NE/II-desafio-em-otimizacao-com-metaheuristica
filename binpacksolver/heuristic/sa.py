"""
Module for implementing the Tabu Search algorithm for optimization problems.
"""

import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness, generate_solution, theoretical_minimum, evaluate_solution)


def __perturb_solution(best_fit: int, solution: List[np.ndarray], containers: List[int], c: int):
    """_summary_

    Parameters
    ----------
    best_fit : int
        _description_
    solution : np.ndarray
        _description_
    containers : List[int]
        _description_
    c : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    if best_fit < 2:
        return solution 
    
    new_solution = solution.copy()
    new_containers = containers.copy()
    
    source_bin_idx = np.random.randint(best_fit)
    item_to_move = np.random.randint(0, fitness(new_solution[source_bin_idx]))
    item = new_solution[item_to_move]
    new_solution[source_bin_idx] = np.delete(new_solution[source_bin_idx], item_to_move)
    new_containers[source_bin_idx] -= item
    
    if new_containers[source_bin_idx] == c:
        del new_solution[source_bin_idx]
        del new_containers[source_bin_idx]
        
    destination_bin_idx = np.random.randint(fitness(new_solution) + 1)
    if destination_bin_idx == len(new_solution):
        new_solution.append(np.array([item], dtype=int))
        new_containers.append(c - item)
    else:
        new_solution[destination_bin_idx] = np.append(new_solution[destination_bin_idx], item)
        new_containers[destination_bin_idx] -= item

    return new_solution, new_containers


def __accept_solution(new_fitness: int, best_fit: int, temperature: float):
        return True if new_fitness < best_fit \
            else np.random.random() < np.exp((best_fit - new_fitness) / temperature)

def __operations(best_fit: int, solution: List[np.ndarray], containers: List[int], c: int, temperature: float):
    """_summary_

    Parameters
    ----------
    best_fit : int
        _description_
    solution : List[np.ndarray]
        _description_
    containers : List[int]
        _description_
    c : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    new_solution, new_containers = __perturb_solution(best_fit, solution, containers, c)
    new_fitness = fitness(new_solution)
    if evaluate_solution(new_containers) and __accept_solution(new_fitness, best_fit, temperature):
        solution = new_solution
        containers = new_containers
        best_fit = new_fitness
        

# pylint: disable=R0913
def simulated_annealing_bpp(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    min_temperature: float = 0.01,
    alpha: float = 0.9,
    iterations_per_temperature: int = 100,
    initial_temperature: float = 0.01
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
    temperature: float = initial_temperature
    time_start: float = time.time()

    while check_end(th_min, best_fit, time_max, time_start, time.time(), temperature, min_temperature):
        __operations(best_fit, solution, containers, c)
        it = it + it * alpha 

    return solution, best_fit


# pylint: enable=R0913
