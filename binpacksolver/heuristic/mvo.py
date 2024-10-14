"""
Implementation of the Multi-Verse Optimizer (MVO) algorithm for the bin packing problem.
This algorithm simulates the interaction of universes in terms of fitness, 
moving objects between them using White Hole, Black Hole, and Wormhole mechanisms. 
The goal is to iteratively improve a population of solutions (universes) 
to achieve the best packing solution, minimizing the number of bins used.
"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def roulette_wheel_selection(inflation_rates: np.ndarray) -> int:
    """
    Performs roulette wheel selection based on the normalized inflation rates.

    Parameters
    ----------
    inflation_rates : np.ndarray
        The normalized inflation rates (fitness values).

    Returns
    -------
    int
        The index selected by roulette wheel.
    """
    accumulation = np.cumsum(inflation_rates)
    p = random.random() * accumulation[-1]
    chosen_index = np.where(accumulation >= p)[0][0]
    return chosen_index


# pylint: disable=R0913, R0914
def update_universe(
    universe: np.ndarray,
    population: np.ndarray,
    normalized_fitness: np.ndarray,
    best_universe: np.ndarray,
    wep: float,
    tdr: float,
    min_value: int,
    max_value: int,
    c: int,
) -> np.ndarray:
    """
    Updates the current universe using the White Hole, Black Hole, and Wormhole mechanisms.

    Parameters
    ----------
    universe : np.ndarray
        The current universe/solution being updated.
    population : np.ndarray
        The entire population of universes.
    normalized_fitness : np.ndarray
        The normalized fitness values (inflation rates).
    best_universe : np.ndarray
        The best universe/solution found so far.
    wep : float
        Wormhole Existence Probability.
    tdr : float
        Traveling Distance Rate.
    min_value : int
        Minimum value for an item.
    max_value : int
        Maximum value for an item.
    c : int
        The capacity of each bin.

    Returns
    -------
    np.ndarray
        The updated universe.
    """
    new_universe = np.copy(universe)
    num_items = len(universe)
    white_hole_idx = roulette_wheel_selection(normalized_fitness)

    for j in range(num_items):
        r1 = random.random()
        if r1 < normalized_fitness[white_hole_idx]:
            new_universe[j] = population[white_hole_idx, j]
        r2 = random.random()
        if r2 < wep:
            r3 = random.random()
            if r3 < 0.5:
                rand_val = random.random()
                new_universe[j] = best_universe[j] + tdr * (
                    (max_value - min_value) * rand_val + min_value
                )
            else:
                rand_val = random.random()
                new_universe[j] = best_universe[j] - tdr * (
                    (max_value - min_value) * rand_val + min_value
                )

    new_universe = np.clip(new_universe, min_value, max_value)
    new_universe = np.round(new_universe).astype(int)

    return repair_solution(universe, new_universe, c)


def multi_verse_optimizer(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7,
    wep_max=1.0,
    wep_min=0.2,
) -> Tuple[List[np.ndarray], int]:
    """
    Executes the Multi-Verse Optimizer algorithm for the bin packing problem.

    The MVO algorithm iteratively improves a population of solutions (universes)
    by moving each universe closer to the best universe using the White Hole/Black Hole
    and Wormhole mechanisms, minimizing the number of bins used in packing.

    Parameters
    ----------
    array_base : np.ndarray
        The base array representing the items to be packed.
    c : int
        The capacity of each bin.
    time_max : float, optional
        Maximum allowable time for the algorithm to run, by default 60 seconds.
    max_it : int, optional
        Maximum number of iterations for the algorithm, by default None.
    population_size : int, optional
        The size of the population of solutions, by default 7.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness (number of bins used).

    Notes
    -----
    If the search is limited only by iterations (`max_it`) or if `max_it` is set too small,
    the quality of the solution may deteriorate because the algorithm may not have enough time
    to fully explore the neighborhood and improve the solution. It is recommended to
    to provide a reasonable iteration limit, especially for longer time limits.
    """
    min_value = array_base.min()
    max_value = array_base.max()

    uni_matrix = generate_initial_matrix_population(
        array_base, c, population_size, VALID=True
    )

    # Initial variables
    best_idx = np.argmin(uni_matrix[:, -1])
    best_universe = np.copy(uni_matrix[best_idx, :-1])
    best_fitness = uni_matrix[best_idx, -1]
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    max_iterations = max_it if max_it is not None else 10000

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        it += 1
        wep = wep_min + it * ((wep_max - wep_min) / max_iterations)
        tdr = 1 - (it ** (1 / 6) / max_iterations ** (1 / 6))
        fitness_inv = 1 / (uni_matrix[:, -1] + 1e-10)
        norm_fitness = fitness_inv / np.sum(fitness_inv)

        for i in range(population_size):
            if i == best_idx:
                continue
            uni_matrix[i, :-1] = update_universe(
                uni_matrix[i, :-1],
                uni_matrix[:, :-1],
                norm_fitness,
                best_universe,
                wep,
                tdr,
                min_value,
                max_value,
                c,
            )

        fitness_values = np.apply_along_axis(
            lambda x: fitness(x, c), 1, uni_matrix[:, :-1]
        )
        uni_matrix[:, -1] = fitness_values

        current_best_idx = np.argmin(uni_matrix[:, -1])
        if uni_matrix[current_best_idx, -1] < best_fitness:
            best_fitness = uni_matrix[current_best_idx, -1]
            best_universe = np.copy(uni_matrix[current_best_idx, :-1])
            best_idx = current_best_idx

    return generate_solution(best_universe, c, VALID=True)[0], best_fitness


# pylint: enable=R0913, R0914
