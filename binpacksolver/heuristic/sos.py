"""_summary_"""

import random
import time
from typing import Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def mutualism(org1: np.ndarray, org2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Executes the mutualism phase between two organisms.

    Parameters
    ----------
    org1 : np.ndarray
        The first organism.
    org2 : np.ndarray
        The second organism.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        The new positions of the two organisms after the mutualism phase.
    """
    mutual_vector = (org1 + org2) / 2
    org1_new = org1 + random.random() * (mutual_vector - org1)
    org2_new = org2 + random.random() * (mutual_vector - org2)
    return org1_new, org2_new


def commensalism(org: np.ndarray, other_org: np.ndarray) -> np.ndarray:
    """
    Executes the commensalism phase where an organism interacts with another organism.

    Parameters
    ----------
    org : np.ndarray
        The current organism.
    other_org : np.ndarray
        Another organism from the organisms_matrix.

    Returns
    -------
    np.ndarray
        The new position of the organism after the commensalism phase.
    """
    return org + (random.random() * (other_org - org))


def parasitism(
    org: np.ndarray, organisms_matrix: np.ndarray, bin_capacity: int
) -> np.ndarray:
    """
    Executes the parasitism phase where an organism generates a parasite.

    Parameters
    ----------
    org : np.ndarray
        The current organism.
    organisms_matrix : np.ndarray
        The organisms_matrix matrix.
    bin_capacity : int
        The bin capacity constraint.

    Returns
    -------
    np.ndarray
        The new position of the organism after the parasitism phase.
    """
    parasite = np.copy(org)
    random_index = random.randint(0, len(organisms_matrix) - 1)
    parasite[random_index] = random.randint(0, bin_capacity - 1)
    return parasite


def symbiotic_organisms_search(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7,
) -> Tuple[np.ndarray, float]:
    """
    Symbiotic Organisms Search (SOS) algorithm applied to the Bin Packing Problem (BPP).

    Parameters
    ----------
    array_base : np.ndarray
        Base array of items for the problem.
    c : int
        Bin capacity.
    population_size : int, optional
        Size of the organisms_matrix, by default 30.
    max_iterations : int, optional
        Maximum number of iterations, by default 100.

    Returns
    -------
    Tuple[np.ndarray, float]
        The best solution found and its fitness score.
    """
    # Generate initial organisms_matrix as a matrix where the last column holds fitness values
    organisms_matrix = generate_initial_matrix_population(
        array_base, c, population_size, VALID=True
    )

    # Find the initial best solution
    best_idx = np.argmin(organisms_matrix[:, -1])
    best_fit = organisms_matrix[best_idx, -1]
    best_solution = organisms_matrix[best_idx, :-1]

    # Initial variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fit, time_max, start, time.time(), max_it, it):
        for i in range(population_size):
            org1 = organisms_matrix[i, :-1]
            org2 = organisms_matrix[random.randint(0, population_size - 1), :-1]
            org1_new, org2_new = mutualism(org1, org2)

            organisms_matrix[i, :-1] = repair_solution(
                org1.copy(), np.abs(org1_new).astype(int), c
            )
            organisms_matrix[i, -1] = fitness(organisms_matrix[i, :-1], c)

            other_idx = random.randint(0, population_size - 1)
            organisms_matrix[other_idx, :-1] = repair_solution(
                org2.copy(), np.abs(org2_new).astype(int), c
            )
            organisms_matrix[other_idx, -1] = fitness(
                organisms_matrix[other_idx, :-1], c
            )

            other_org = organisms_matrix[random.randint(0, population_size - 1), :-1]
            org_new = commensalism(organisms_matrix[i, :-1], other_org)
            repaired_org = repair_solution(
                organisms_matrix[i, :-1].copy(), np.abs(org_new).astype(int), c
            )
            current_fitness = fitness(repaired_org, c)

            if current_fitness < organisms_matrix[i, -1]:
                organisms_matrix[i, :-1] = repaired_org
                organisms_matrix[i, -1] = current_fitness

            parasite = parasitism(organisms_matrix[i, :-1], organisms_matrix[:, :-1], c)
            repaired_parasite = repair_solution(organisms_matrix[i, :-1], parasite, c)
            parasite_fitness = fitness(repaired_parasite, c)

            if parasite_fitness < organisms_matrix[i, -1]:
                organisms_matrix[i, :-1] = repaired_parasite
                organisms_matrix[i, -1] = parasite_fitness

        best_idx = np.argmin(organisms_matrix[:, -1])
        if organisms_matrix[best_idx, -1] < best_fit:
            best_fit = organisms_matrix[best_idx, -1]
            best_solution = organisms_matrix[best_idx, :-1].copy()

    return generate_solution(best_solution, c, VALID=True)[0], best_fit
