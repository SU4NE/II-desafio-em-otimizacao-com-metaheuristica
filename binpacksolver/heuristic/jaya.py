"""
A word for victory

Implementation of the Jaya optimization algorithm for the bin packing problem.
The algorithm iteratively improves a population of solutions to achieve the 
best possible packing, minimizing the number of bins used.
"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (best_fit_decreasing, bestfit_population,
                                 check_end, fitness,
                                 generate_initial_population,
                                 generate_solution, theoretical_minimum)


def repair_solution(
    solution: np.ndarray, new_solution: np.ndarray, c: int
) -> np.ndarray:
    """
    Repairs a solution by replacing invalid elements in the original solution
    with valid elements from a new solution.

    Parameters
    ----------
    solution : np.ndarray
        The original solution that may contain invalid elements.
    new_solution : np.ndarray
        The new solution from which valid elements will be drawn.

    Returns
    -------
    np.ndarray
        The repaired solution where invalid elements have been replaced with
        valid elements.
    """
    unique_values, counts = np.unique(solution, return_counts=True)
    number_count_dict = dict(zip(unique_values, counts))
    modify = []

    for _, item in enumerate(new_solution):
        if item in number_count_dict and number_count_dict[item]:
            modify.append(item)
            number_count_dict[item] -= 1
            if not number_count_dict[item]:
                number_count_dict.pop(item)

    remaining_values = [
        item for item, count in number_count_dict.items() for _ in range(count)
    ]
    random.shuffle(remaining_values)
    solution = best_fit_decreasing(
        np.array(remaining_values),
        c,
        generate_solution(np.array(modify), c, VALID=True)[0],
    )
    return np.concatenate(solution)


# pylint: disable=R0914
def jaya_optimization(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: float = 7,
) -> Tuple[List[np.ndarray], int]:
    """
    Executes the Jaya optimization algorithm to solve the bin packing problem.

    Jaya is an optimization algorithm that iteratively updates a population of
    solutions by moving each solution closer to the best solution and away from
    the worst solution. The goal is to minimize the number of bins used in packing.

    Parameters
    ----------
    array_base : np.ndarray
        The base array representing the items to be packed.
    c : int
        The capacity of each bin.
    time_max : float, optional
        Maximum allowable time for the algorithm to run, by default 60 seconds.
    max_it : int, optional
        Maximum number of iterations for the algorithm, by default None (unlimited).
    population_size : int, optional
        The size of the population of solutions, by default 30.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness (number of bins used).
    """
    # Set minimum and maximum values
    min_value = array_base.min()
    max_value = array_base.max()

    # Generate initial population
    pop_bins, _ = generate_initial_population(
        array_base, c, population_size, juice=False, VALID=True
    )

    # Flatten the population and combine with fitness values
    fitness_values = np.array([fitness(lst) for lst in pop_bins])
    pop_bins_flat = np.vstack([np.concatenate(lst) for lst in pop_bins]).astype(int)
    pop_matrix = np.hstack((pop_bins_flat, fitness_values[:, np.newaxis])).astype(int)
    best_idx = np.argmin(pop_matrix[:, -1])

    # Initial variables
    best_fit = bestfit_population(pop_bins, c)
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fit, time_max, start, time.time(), max_it, it):
        it += 1

        best_idx = np.argmin(pop_matrix[:, -1])
        worst_idx = np.argmax(pop_matrix[:, -1])
        best_solution = pop_matrix[best_idx, :-1]
        worst_solution = pop_matrix[worst_idx, :-1]
        num_features = pop_matrix.shape[1] - 1
        a_matrix = np.random.rand(pop_matrix.shape[0], num_features)
        b_matrix = np.random.rand(pop_matrix.shape[0], num_features)
        candidate_positions = (
            pop_matrix[:, :-1]
            + a_matrix * (best_solution - np.abs(pop_matrix[:, :-1]))
            - b_matrix * (worst_solution - np.abs(pop_matrix[:, :-1]))
        )
        candidate_positions = np.clip(candidate_positions, min_value, max_value)
        candidate_positions = np.round(candidate_positions).astype(int)

        for i in range(candidate_positions.shape[0]):
            repaired_solution = repair_solution(
                pop_matrix[i, :-1].copy(), candidate_positions[i].copy(), c
            )
            candidate_positions[i] = repaired_solution

        fitness_values = np.apply_along_axis(
            lambda x: fitness(x, c), 1, candidate_positions
        )
        candidate_positions = np.hstack(
            (candidate_positions, fitness_values[:, np.newaxis])
        ).astype(int)
        combined_positions = np.vstack([pop_matrix, candidate_positions]).astype(int)
        combined_positions = combined_positions[combined_positions[:, -1].argsort()]
        pop_matrix = combined_positions[: pop_matrix.shape[0], :]

        best_fit = np.min(pop_matrix[:, -1])

    best_idx = np.argmin(pop_matrix[:, -1])
    return (
        generate_solution(pop_matrix[best_idx, :-1], c, VALID=True)[0],
        pop_matrix[best_idx, -1],
    )


# pylint: enable=R0914
