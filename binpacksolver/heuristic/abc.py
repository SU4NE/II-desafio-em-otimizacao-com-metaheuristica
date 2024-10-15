"""
Module for implementing the Artificial Bee Colony (ABC) algorithm for optimization problems.
"""

import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, local_search,generate_solution, fitness, repair_solution,
                                 theoretical_minimum, tournament_roulette, generate_initial_matrix_population)

def __employed_bees(bees_matrix: np.ndarray, c: int, min_value: int, max_value: int) -> np.ndarray:
    """
    Updates the solutions of the employed bees using local search.

    Parameters
    ----------
    bees_matrix : np.ndarray
        Matrix containing the bees' solutions.
    c : int
        Maximum container capacity.

    Returns
    -------
    np.ndarray
        Updated solution matrix.
    """
    for i in range(bees_matrix.shape[0]):
        new_solution = local_search(bees_matrix[i, :-2].copy(), c, min_value, max_value)
        new_fit = fitness(new_solution, c)
        
        if new_fit < bees_matrix[i, -2]:
            bees_matrix[i, :-2] = new_solution
            bees_matrix[i, -2] = new_fit
            bees_matrix[i, -1] = 0
        else:
            bees_matrix[i, -1] += 1
    
    return bees_matrix


def __onlooker_bees(bees_matrix: np.ndarray, c: int, gama: float, onlooker: int, min_value: int, max_value: int, tournament_size: int = 3) -> np.ndarray:
    """
    Updates the solutions of the onlooker bees based on roulette wheel selection.

    Parameters
    ----------
    bees_matrix : np.ndarray
        Matrix containing the bees' solutions.
    c : int
        Maximum container capacity.
    gama : float
        Adjustment parameter for roulette selection.
    onlooker : int
        Number of onlooker bees.

    Returns
    -------
    np.ndarray
        Updated solution matrix.
    """
    fitness_values = 1 / (bees_matrix[:, -1] + 1e-6)
    probabilities = fitness_values ** gama / np.sum(fitness_values ** gama)

    for _ in range(onlooker):
        selected_idx = tournament_roulette(bees_matrix[:, :-1], tournament_size)
        selected_idx = np.random.choice(range(bees_matrix.shape[0]), p=probabilities)
        new_solution = local_search(bees_matrix[selected_idx, :-2].copy(), c, min_value, max_value)
        new_fit = fitness(new_solution, c)

        if new_fit < bees_matrix[selected_idx, -2]:
            bees_matrix[selected_idx, :-2] = new_solution
            bees_matrix[selected_idx, -2] = new_fit
            bees_matrix[selected_idx, -1] = 0
        else:
            bees_matrix[selected_idx, -1] += 1
    
    return bees_matrix


def __scout_bees(bees_matrix: np.ndarray, c: int, scout_limit: int = 10) -> np.ndarray:
    """
    Resets the bees that exceed the limit of failed attempts.

    Parameters
    ----------
    bees_matrix : np.ndarray
        Matrix containing the bees' solutions.
    c : int
        Maximum container capacity.
    scout_limit : int, optional
        Limit of failed attempts before resetting, default is 10.

    Returns
    -------
    np.ndarray
        Updated solution matrix.
    """
    for i in range(bees_matrix.shape[0]):
        if bees_matrix[i, -1] > scout_limit:
            shuffled_solution = bees_matrix[i, :-2].copy()
            np.random.shuffle(shuffled_solution)
            new_solution = repair_solution(bees_matrix[i, :-2], shuffled_solution[:len(shuffled_solution[:-2]) // 2], c)
            new_fit = fitness(new_solution, c)
            bees_matrix[i, :-2] = new_solution
            bees_matrix[i, -2] = new_fit
            bees_matrix[i, -1] = 0

    return bees_matrix

# pylint: disable=R0913 R0914
def artificial_bee_colony(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    employed: int = 7,
    onlooker: int = 3,
    scout: int = 5,
    gama: float = 1.8,
    tournament_size: int = 3,
) -> Tuple[List[np.ndarray], int]:
    """
    Solves the BPP using the artificial bee colony algorithm.

    Parameters
    ----------
    array_base : np.ndarray
        Initial item array.
    c : int
        Maximum container capacity.
    time_max : float, optional
        Max time allowed for execution, by default 60.
    max_it : int, optional
        Max iterations, by default None.
    employed : int, optional
        Number of employed bees, by default 7.
    onlooker : int, optional
        Number of onlooker bees, by default 10.
    scout : int, optional
        Scout limit before resetting a bee, by default 10.
    gama : float, optional
        Parameter for roulette selection, by default 1.8.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        Best solution found and its fitness value.
    """
    min_value = array_base.min()
    max_value = array_base.max()
    
    bees_matrix = generate_initial_matrix_population(array_base.copy(), c, employed, VALID=True)
    bees_matrix = np.hstack((bees_matrix, np.zeros((bees_matrix.shape[0], 1), dtype=int)))
    
    # Identify the best solution in the initial population
    best_idx = np.argmin(bees_matrix[:, -2])
    best_fit = bees_matrix[best_idx, -2]
    best_solution = bees_matrix[best_idx, :-2]
    
    # Initial variables
    onlooker = min(onlooker, employed)
    th_min = theoretical_minimum(array_base, c)
    it = 0
    time_start = time.time()

    while check_end(th_min, best_fit, time_max, time_start, time.time(), max_it, it):
        bees_matrix = __employed_bees(bees_matrix, c, min_value, max_value)
        bees_matrix = __onlooker_bees(bees_matrix, c, gama, onlooker, min_value, max_value, tournament_size)
        bees_matrix = __scout_bees(bees_matrix,c, scout)

        # Find the best solution
        best_idx = np.argmin(bees_matrix[:, -2])
        best_fit = bees_matrix[best_idx, -2]
        best_solution = bees_matrix[best_idx, :-2]
        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fit


# pylint: enable=R0913 R0914
