"""_summary_"""

import random
import time
from typing import Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, local_search,
                                 repair_solution, theoretical_minimum)


def crossover(parent1: np.ndarray, parent2: np.ndarray, c: int) -> np.ndarray:
    """
    Performs crossover between two parents to generate a child solution.

    Parameters
    ----------
    parent1 : np.ndarray
        The first parent solution.
    parent2 : np.ndarray
        The second parent solution.
    c : int
        Maximum container capacity.

    Returns
    -------
    np.ndarray
        The generated child solution.
    """
    cross_point = random.randint(1, len(parent1) - 2)
    child = np.concatenate([parent1[:cross_point], parent2[cross_point:]])
    return repair_solution(parent1, child, c)


def mutate(solution: np.ndarray, c: int, min_value: int, max_value: int) -> np.ndarray:
    """
    Mutates the solution by changing one dimension.

    Parameters
    ----------
    solution : np.ndarray
        The solution to mutate.
    c : int
        Maximum container capacity.
    min_value : int
        Minimum allowable value for mutation.
    max_value : int
        Maximum allowable value for mutation.

    Returns
    -------
    np.ndarray
        The mutated solution.
    """
    mutation_point = random.randint(0, len(solution) - 1)
    new_solution = solution.copy()
    new_solution[mutation_point] = random.randint(min_value, max_value)
    return repair_solution(solution, new_solution, c)


def memetic_algorithm(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 8,
) -> Tuple[np.ndarray, int]:
    """
    Memetic algorithm with elitism for solving the bin packing problem.

    Parameters
    ----------
    array_base : np.ndarray
        The initial array of items.
    c : int
        Maximum container capacity.
    time_max : float, optional
        Maximum time allowed for execution, by default 60.
    max_it : int, optional
        Maximum number of iterations, by default None.
    population_size : int, optional
        Size of the population, by default 8.

    Returns
    -------
    Tuple[np.ndarray, int]
        The best solution found and its fitness value.
    """
    if population_size % 2:
        population_size += 1

    min_value = array_base.min()
    max_value = array_base.max()

    # Generate initial population
    memetic_matrix = generate_initial_matrix_population(
        array_base.copy(), c, population_size, VALID=True
    )

    # Identify the best solution in the initial population
    best_idx = np.argmin(memetic_matrix[:, -1])
    best_fit = memetic_matrix[best_idx, -1]
    best_solution = memetic_matrix[best_idx, :-1]

    # Initial variables
    th_min = theoretical_minimum(array_base, c)
    it = 0
    time_start = time.time()

    while check_end(th_min, best_fit, time_max, time_start, time.time(), max_it, it):
        fitness_values = memetic_matrix[:, -1]
        sorted_indices = np.argsort(fitness_values)

        current_best_idx = sorted_indices[0]
        current_best_solution = memetic_matrix[current_best_idx, :-1]
        current_best_fitness = fitness_values[current_best_idx]

        new_population = []

        for i in range(0, population_size - 1, 2):
            parent1 = memetic_matrix[sorted_indices[i], :-1]
            parent2 = memetic_matrix[sorted_indices[i + 1], :-1]

            child1 = crossover(parent1=parent1, parent2=parent2, c=c)
            child2 = crossover(parent1=parent2, parent2=parent1, c=c)

            child1 = mutate(child1, c, min_value, max_value)
            child2 = mutate(child2, c, min_value, max_value)

            child1 = local_search(child1, c, min_value, max_value)
            child2 = local_search(child2, c, min_value, max_value)

            new_population.append(np.concatenate([child1, [fitness(child1, c)]]))
            new_population.append(np.concatenate([child2, [fitness(child2, c)]]))

        new_population.append(np.concatenate([best_solution, [best_fit]]))

        memetic_matrix = np.array(new_population)

        current_best_idx = np.argmin(memetic_matrix[:, -1])
        current_best_fitness = memetic_matrix[current_best_idx, -1]
        current_best_solution = memetic_matrix[current_best_idx, :-1]

        if current_best_fitness < best_fit:
            best_fit = current_best_fitness
            best_solution = current_best_solution

        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fit
