import random
import time
import numpy as np
from typing import Tuple
from binpacksolver.utils import (
    check_end,
    fitness,
    generate_initial_matrix_population,
    repair_solution,
    theoretical_minimum,
    generate_solution,
)

def update_dragonfly_position(dragonfly: np.ndarray, neighbors: np.ndarray, food: np.ndarray, enemy: np.ndarray, r: float) -> np.ndarray:
    """
    Updates the position of a dragonfly based on neighbors, food (best solution), and enemy (worst solution).
    
    Parameters
    ----------
    dragonfly : np.ndarray
        The current solution of the dragonfly.
    neighbors : np.ndarray
        The neighbors of the dragonfly (influencing forces).
    food : np.ndarray
        The best solution found so far.
    enemy : np.ndarray
        The worst solution found so far.
    r : float
        A random factor for updating the position.
    
    Returns
    -------
    np.ndarray
        The updated position of the dragonfly.
    """
    new_position = np.copy(dragonfly)
    alignment = np.mean(neighbors - dragonfly, axis=0)
    for i in range(len(dragonfly)):
        new_position[i] += r * (food[i] - enemy[i]) + r * alignment[i]
    return new_position.astype(int)


def dragonfly_algorithm(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7
) -> Tuple[np.ndarray, float]:
    """
    Dragonfly Algorithm (DA) applied to the Bin Packing Problem (BPP).
    
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
        Population size of dragonflies, by default 7.
    
    Returns
    -------
    Tuple[np.ndarray, float]
        The best solution found and its fitness score.
    """
    min_value = array_base.min()
    max_value = array_base.max()

    population_matrix = generate_initial_matrix_population(array_base, c, population_size, VALID=True)

    # Initialize the best solution and its fitness
    best_idx = np.argmin(population_matrix[:, -1])
    best_solution = population_matrix[best_idx, :-1].copy()
    best_fitness = population_matrix[best_idx, -1]

    # Control variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        fitness_values = population_matrix[:, -1]
        current_best_idx = np.argmin(fitness_values)

        if fitness_values[current_best_idx] < best_fitness:
            best_fitness = fitness_values[current_best_idx]
            best_solution = population_matrix[current_best_idx, :-1].copy()

        food = best_solution
        enemy = population_matrix[np.argmax(fitness_values), :-1]

        for i in range(population_size):
            neighbors = population_matrix[:, :-1]
            r = np.random.random()
            new_position = update_dragonfly_position(
                population_matrix[i, :-1], neighbors, food, enemy, r
            )
            
            new_position = np.clip(new_position, min_value, max_value).astype(int)
            population_matrix[i, :-1] = repair_solution(population_matrix[i, :-1], new_position, c)
            population_matrix[i, -1] = fitness(population_matrix[i, :-1], c)

        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fitness
