"""_summary_"""
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, local_search,
                                 repair_solution, theoretical_minimum)


def assimilate(
    colony: np.ndarray, imperialist: np.ndarray, assimilation_coefficient: float
) -> np.ndarray:
    """
    Moves the colony towards the imperialist.

    Parameters
    ----------
    colony : np.ndarray
        The current colony solution.
    imperialist : np.ndarray
        The imperialist solution.
    assimilation_coefficient : float
        The coefficient controlling the assimilation rate.

    Returns
    -------
    np.ndarray
        The assimilated colony.
    """
    new_position = colony + assimilation_coefficient * np.random.uniform(0, 1) * (
        imperialist - colony
    )
    new_position = np.clip(new_position, 0, np.max(imperialist))
    return new_position


def revolution(colony: np.ndarray, revolution_rate: float, c: int) -> np.ndarray:
    """
    Applies revolution to a colony with a certain probability.

    Parameters
    ----------
    colony : np.ndarray
        The current colony solution.
    revolution_rate : float
        The probability of applying revolution.
    c : int
        Minimum allowable value for any dimension.

    Returns
    -------
    np.ndarray
        The potentially modified colony.
    """
    if np.random.rand() < revolution_rate:
        new_colony = np.random.choice(colony.copy(), size=len(colony), replace=True)
        new_colony = np.random.permutation(new_colony)
        colony = repair_solution(colony, new_colony, c)
    return colony


def compete(empires: List[np.ndarray], empire_fitness: np.ndarray) -> List[np.ndarray]:
    """
    Handles competition between empires by transferring colonies from the weakest
    to the strongest empire.

    Parameters
    ----------
    empires_matrix : np.ndarray
        The matrix representing all empires and their colonies.
    empire_fitness : np.ndarray
        Array of fitness values for each empire.

    Returns
    -------
    List[np.ndarray]
        Updated empires matrix after competition.
    """
    weakest_empire_idx = np.argmax(empire_fitness)
    strongest_empire_idx = np.argmin(empire_fitness)

    if len(empires[weakest_empire_idx]) > 1:
        col_idx = np.random.randint(empires[weakest_empire_idx].shape[0])
        empires[strongest_empire_idx] = np.vstack(
            [empires[strongest_empire_idx], empires[weakest_empire_idx][col_idx, :]]
        )
        empires[weakest_empire_idx] = np.delete(
            empires[weakest_empire_idx], col_idx, axis=0
        )

    return empires


def imperialist_competitive_algorithm(
    solution: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    num_empires: int = 3,
    num_colonies: int = 5,
    assimilation_coefficient: float = 0.7,
    revolution_rate: float = 0.9,
) -> Tuple[np.ndarray, int]:
    """
    Imperialist Competitive Algorithm (ICA) applied to the Bin Packing Problem (BPP).

    Parameters
    ----------
    solution : np.ndarray
        Array of item sizes.
    c : int
        Maximum capacity of each bin.
    time_max : float, optional
        Maximum allowable time for the algorithm to run, by default 60 seconds.
    num_empires : int, optional
        Number of empires, by default 5.
    num_colonies : int, optional
        Number of colonies per empire, by default 20.
    max_it : int, optional
        Maximum number of iterations, by default None.
    assimilation_coefficient : float, optional
        Assimilation coefficient, by default 0.1.
    revolution_rate : float, optional
        Revolution rate, by default 0.1.

    Returns
    -------
    Tuple[np.ndarray, int]
        The best solution found and its fitness value.
    """
    min_value = solution.min()
    max_value = solution.max()

    # Initialize empires (a list of matrices where each matrix represents an empire with colonies)
    empires = [
        generate_initial_matrix_population(solution, c, num_colonies, VALID=True)
        for _ in range(num_empires)
    ]

    # Track the best solution globally
    imperialists = [empire[np.argmin(empire[:, -1])] for empire in empires]
    empire_fitness = np.array([fitness(imperialist, c) for imperialist in imperialists])
    best_idx = np.argmin(empire_fitness)
    best_fitness = empire_fitness[best_idx]
    best_solution = imperialists[best_idx][:-1].copy()

    # Initialize variables for loop
    th_min = theoretical_minimum(solution, c)
    it = 0
    time_start = time.time()

    while check_end(
        th_min, best_fitness, time_max, time_start, time.time(), max_it, it
    ):
        # Assimilation Phase: Move colonies towards imperialist
        for i in range(num_empires):
            # Get the imperialist solution (without fitness)
            imperialist = imperialists[i][:-1]
            for j in range(empires[i].shape[0]):
                colony = empires[i][j, :-1]
                if np.array_equal(colony, imperialist):
                    continue

                # Assimilate
                assimilated_colony = assimilate(
                    colony.copy(), imperialist, assimilation_coefficient
                )
                assimilated_colony = np.round(assimilated_colony).astype(int)
                assimilated_colony = repair_solution(colony, assimilated_colony, c)

                # Revolution
                assimilated_colony = revolution(assimilated_colony, revolution_rate, c)
                assimilated_colony = local_search(
                    assimilated_colony, c, min_value, max_value
                )

                # Update the colony in the matrix and calculate its fitness
                empires[i][j, :-1] = assimilated_colony
                empires[i][j, -1] = fitness(assimilated_colony, c)

        imperialists = [empire[np.argmin(empire[:, -1])] for empire in empires]
        empire_fitness = np.array(
            [fitness(imperialist, c) for imperialist in imperialists]
        )
        empires = compete(empires, empire_fitness)
        best_idx = np.argmin(empire_fitness)
        current_best_fitness = empire_fitness[best_idx]
        current_best_solution = imperialists[best_idx][:-1].copy()

        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_solution.copy()

        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fitness
