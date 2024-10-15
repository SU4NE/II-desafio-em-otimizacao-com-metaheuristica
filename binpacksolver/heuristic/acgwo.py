"""
Module for implementing the Chaotic Grey Wolf Optimization (CGWO) algorithm
for the Bin Packing Problem (BPP). The algorithm optimizes the packing of items
into bins by simulating the social hunting behavior of grey wolves with chaotic
factors to enhance exploration and exploitation.
"""

import random
import time

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def chaotic_map(t: int, max_value: int) -> np.ndarray:
    """
    Generates a chaotic value based on the current iteration and max value.

    Parameters
    ----------
    t : int
        Current iteration number.
    max_value : int
        Maximum number of iterations.

    Returns
    -------
    np.ndarray
        Chaotic value for the current iteration.
    """
    return np.sin(np.pi * t / max_value)


# pylint: disable=R0913, R0914
def update_position(
    position: np.ndarray,
    alpha: np.ndarray,
    beta: np.ndarray,
    delta: np.ndarray,
    acf: float,
    chaotic_factor: float,
    min_value: int,
    max_value: int,
    wolf_adjustment: float = 0.5,
) -> np.ndarray:
    """
    Updates the position of the wolf based on the positions of the best wolves.

    Parameters
    ----------
    position : np.ndarray
        Current position of the wolf (solution).
    alpha : np.ndarray
        Position of the best wolf (alpha).
    beta : np.ndarray
        Position of the second-best wolf (beta).
    delta : np.ndarray
        Position of the third-best wolf (delta).
    acf : float
        Adaptive coefficient for controlling step size.
    chaotic_factor : float
        Factor generated from the chaotic map to introduce randomness.
    min_value : int
        Minimum allowed value for the solution.
    max_value : int
        Maximum allowed value for the solution.
    wolf_adjustment : float, optional
        Adjustment factor for chaotic influence, by default 0.5.

    Returns
    -------
    np.ndarray
        Updated position of the wolf.
    """
    new_position = np.copy(position)
    for i, pos in enumerate(position):
        r1 = random.random()
        r2 = random.random()
        adaptive_coeff = 2 * acf * r1 - acf
        chaotic_coeff = 2 * r2

        dist_alpha = abs(chaotic_coeff * alpha[i] - pos)
        dist_beta = abs(chaotic_coeff * beta[i] - pos)
        dist_delta = abs(chaotic_coeff * delta[i] - pos)

        x1 = alpha[i] - adaptive_coeff * dist_alpha
        x2 = beta[i] - adaptive_coeff * dist_beta
        x3 = delta[i] - adaptive_coeff * dist_delta

        new_position[i] = (x1 + x2 + x3) / 3
        new_position[i] += chaotic_factor * (random.random() - wolf_adjustment)

    return np.clip(new_position, min_value, max_value)


def caotic_grey_wolf_optimization(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7,
    wolf_adjustment: float = 0.5,
) -> np.ndarray:
    """
    Executes the Chaotic Grey Wolf Optimization (CGWO) algorithm for the BPP.

    Parameters
    ----------
    array_base : np.ndarray
        Array representing the base items to be packed.
    c : int
        Capacity of the bins.
    time_max : float, optional
        Maximum allowed runtime in seconds, by default 60.
    max_it : int, optional
        Maximum number of iterations, by default None.
    population_size : int, optional
        Number of wolves (solutions) in the population, by default 7..
    wolf_adjustment : float, optional
        Adjustment factor for chaotic influence, by default 0.5. The value is
        automatically clipped between 0 and 1.

    Returns
    -------
    np.ndarray
        The best solution found by the algorithm and its fitness value.
    """
    min_value = array_base.min()
    max_value = array_base.max()

    # Generate initial population
    wolf_adjustment = max(min(wolf_adjustment, 1), 0)
    wolves_matrix = generate_initial_matrix_population(
        array_base, c, population_size, VALID=True
    )

    # Identify the best solution in the initial population
    best_idx = np.argmin(wolves_matrix[:, -1])
    best_fit = wolves_matrix[best_idx, -1]
    best_alpha = wolves_matrix[best_idx, :-1]

    # Initial variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fit, time_max, start, time.time(), max_it, it):

        sorted_indices = np.argsort(wolves_matrix[:, -1])
        alpha = wolves_matrix[sorted_indices[0], :-1]
        beta = wolves_matrix[sorted_indices[1], :-1]
        delta = wolves_matrix[sorted_indices[2], :-1]

        a = 2 - 2 * (it / max_it) if max_it else 1
        chaotic_factor = chaotic_map(
            it, max_it or max((time_max * 1e8) // population_size, 100)
        )

        for i in range(1, population_size):
            new_wolf = update_position(
                wolves_matrix[i, :-1],
                alpha,
                beta,
                delta,
                a,
                chaotic_factor,
                min_value,
                max_value,
                wolf_adjustment,
            )
            wolves_matrix[i, :-1] = repair_solution(
                wolves_matrix[i, :-1].copy(), new_wolf, c
            )
            wolves_matrix[i, -1] = fitness(wolves_matrix[i, :-1], c)

        best_idx = np.argmin(wolves_matrix[:, -1])
        if wolves_matrix[best_idx, -1] < best_fit:
            best_fit = wolves_matrix[best_idx, -1]
            best_alpha = wolves_matrix[best_idx, :-1]

    return generate_solution(best_alpha, c, VALID=True)[0], best_fit


# pylint: enable=R0913, R0914
