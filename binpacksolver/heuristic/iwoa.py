import time
import numpy as np
import random
from typing import Tuple
from binpacksolver.utils import (
    check_end,
    fitness,
    generate_initial_matrix_population,
    repair_solution,
    theoretical_minimum,
    generate_solution,
)

# Update the position of whales (improved with chaos or hybrid operators)
def update_whale_position(whale: np.ndarray, leader: np.ndarray, b: float, l: float, a: float, A: float, C: float) -> np.ndarray:
    """
    Updates the position of a whale based on linear or spiral motion, depending on a probabilistic condition.

    Parameters
    ----------
    whale : np.ndarray
        The current whale solution.
    leader : np.ndarray
        The leader solution (best current solution).
    b : float
        Spiral constant.
    l : float
        Random value for spiral movement.
    a : float
        Adaptive parameter to control the A factor.
    A : float
        Adjustment factor for whale position update.
    C : float
        Another adjustment factor for whale position update.

    Returns
    -------
    np.ndarray
        The updated position of the whale.
    """
    if random.random() < 0.5:
        D = abs(C * leader - whale)
        whale = leader - A * D
    else:
        distance_to_leader = abs(leader - whale)
        whale = distance_to_leader * np.exp(b * l) * np.cos(2 * np.pi * l) + leader
    return whale


def improved_whale_optimization_algorithm(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7,
    spiral_constant: float = 1,
) -> Tuple[np.ndarray, float]:
    """
    Improved Whale Optimization Algorithm (IWOA) applied to the Bin Packing Problem (BPP).

    Parameters
    ----------
    array_base : np.ndarray
        Base array of items for the problem.
    c : int
        Capacity of each bin.
    time_max : float, optional
        Maximum optimization time, by default 60 seconds.
    max_it : int, optional
        Maximum number of iterations, by default None (unlimited).
    population_size : int, optional
        Population size of whales, by default 7.

    Returns
    -------
    Tuple[np.ndarray, float]
        The best solution found and its fitness score.
    """
    # Initialize the population as a matrix, where the last column stores fitness values
    population_matrix = generate_initial_matrix_population(array_base, c, population_size, VALID=True)

    # Initialize personal best positions (personal bests) and global best (global best)
    personal_best_positions = population_matrix[:, :-1].copy()
    personal_best_scores = population_matrix[:, -1].copy()

    global_best_idx = np.argmin(personal_best_scores)
    global_best_position = personal_best_positions[global_best_idx].copy()
    global_best_score = personal_best_scores[global_best_idx]

    # Control variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, global_best_score, time_max, start, time.time(), max_it, it):
        a = 2 - it * (2 / (max_it if max_it else max((time_max * 1e8) // population_size, 100)))
        A = 2 * a * random.random() - a
        C = 2 * random.random()
        spiral_constant = 1
        l = (2 * random.random()) - 1

        for i in range(population_size):
            new_position = update_whale_position(
                population_matrix[i, :-1], global_best_position, spiral_constant, l, a, A, C
            )

            population_matrix[i, :-1] = repair_solution(
                population_matrix[i, :-1].copy(), np.abs(new_position).astype(int), c
            )

            current_fitness = fitness(population_matrix[i, :-1], c)
            population_matrix[i, -1] = current_fitness

            if current_fitness < personal_best_scores[i]:
                personal_best_scores[i] = current_fitness
                personal_best_positions[i] = population_matrix[i, :-1].copy()

        best_particle_idx = np.argmin(personal_best_scores)
        if personal_best_scores[best_particle_idx] < global_best_score:
            global_best_score = personal_best_scores[best_particle_idx]
            global_best_position = personal_best_positions[best_particle_idx].copy()

        it += 1

    return generate_solution(global_best_position, c, VALID=True)[0], global_best_score
