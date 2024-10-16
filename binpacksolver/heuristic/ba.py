"""
Bat Algorithm (BA) for solving the Bin Packing Problem (BPP), 
using frequency, velocity, and loudness to evolve solutions.
"""

import time
from typing import Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def update_position_and_velocity(
    bat: np.ndarray,
    velocity: np.ndarray,
    best_bat: np.ndarray,
    frequency: float,
    loudness: float,
    r: float,
    min_value: int,
    max_value: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Updates the velocity and position of a bat based on its frequency,
    the global best, and its local random behavior.

    Parameters
    ----------
    bat : np.ndarray
        The current bat (solution).
    velocity : np.ndarray
        The current velocity of the bat.
    best_bat : np.ndarray
        The best bat (global best solution).
    frequency : float
        The frequency at which the bat moves.
    loudness : float
        Loudness value, controlling local search behavior.
    r : float
        Pulse emission rate.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        The new position and velocity of the bat.
    """
    velocity = velocity + (bat - best_bat) * frequency
    new_position = bat + velocity

    if np.random.rand() > r:
        new_position = best_bat + loudness * np.random.uniform(-1, 1, len(bat))

    return np.clip(new_position, min_value, max_value).astype(int), velocity


def bat_algorithm(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    pop_size: int = 30,
    loudness: float = 0.5,
    r: float = 0.5,
    f_min: float = 0,
    f_max: float = 1,
    loudness_factor: float = 0.9,
) -> Tuple[np.ndarray, float]:
    """
    Bat Algorithm (BA) applied to the Bin Packing Problem (BPP).

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
    pop_size : int, optional
        Population size, by default 30.
    loudness : float, optional
        Loudness controlling local search, by default 0.5.
    r : float, optional
        Pulse emission rate, by default 0.5.
    f_min : float, optional
        Minimum frequency, by default 0.
    f_max : float, optional
        Maximum frequency, by default 1.
    loudness_factor : float, optional
        Controlling loudness, by default 0.9.

    Returns
    -------
    Tuple[np.ndarray, float]
        The best solution found and its fitness score.
    """
    min_value = array_base.min()
    max_value = array_base.max()
    num_items = array_base.shape[0]

    # Initialize the population as a matrix with fitness values in the last column
    bat_matrix = generate_initial_matrix_population(array_base, c, pop_size, VALID=True)
    velocities = np.zeros((pop_size, num_items))  # Initialize velocity to zero
    frequencies = np.zeros(pop_size)  # Initialize frequencies

    # Initialize global best solution and fitness
    best_idx = np.argmin(bat_matrix[:, -1])
    best_solution = bat_matrix[best_idx, :-1].copy()
    best_fitness = bat_matrix[best_idx, -1]

    # Control variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        for i in range(pop_size):
            frequencies[i] = f_min + (f_max - f_min) * np.random.rand()

            new_bat, velocities[i] = update_position_and_velocity(
                bat_matrix[i, :-1],
                velocities[i],
                best_solution,
                frequencies[i],
                loudness,
                r,
                min_value,
                max_value,
            )

            bat_matrix[i, :-1] = repair_solution(bat_matrix[i, :-1], new_bat, c)

            fitness_value = fitness(bat_matrix[i, :-1], c)
            bat_matrix[i, -1] = fitness_value

            if fitness_value < best_fitness:
                best_solution = bat_matrix[i, :-1].copy()
                best_fitness = fitness_value

        loudness *= loudness_factor
        r = r * (1 - np.exp(-it))
        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fitness
