import random
import numpy as np
import time
from typing import Tuple
from binpacksolver.utils import (
    check_end,
    fitness,
    generate_initial_matrix_population,
    repair_solution,
    theoretical_minimum,
    generate_solution,
)

def clan_update(elephant: np.ndarray, leader: np.ndarray, alpha: float) -> np.ndarray:
    """
    Updates the elephant's position based on the clan leader's position.
    
    Parameters
    ----------
    elephant : np.ndarray
        The current solution of the elephant.
    leader : np.ndarray
        The solution of the clan leader.
    alpha : float
        The factor controlling how much the elephant moves towards the leader.
    
    Returns
    -------
    np.ndarray
        The updated position of the elephant.
    """
    return elephant + alpha * (leader - elephant)


def isolation(elephant: np.ndarray) -> np.ndarray:
    """
    Applies mutation (isolation) to the elephant by randomly.
    
    Parameters
    ----------
    elephant : np.ndarray
        The current solution of the elephant.
    Returns
    -------
    np.ndarray
        The mutated elephant solution.
    """
    isolated_elephant = np.copy(elephant)
    return np.random.permutation(isolated_elephant)[:len(isolated_elephant)]

def elephant_herding_optimization(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 3,
    alpha: float = 0.5
) -> Tuple[np.ndarray, float]:
    """
    Elephant Herding Optimization (EHO) algorithm applied to the Bin Packing Problem (BPP).
    
    Parameters
    ----------
    array_base : np.ndarray
        Base array of items for the BPP.
    c : int
        Capacity of each bin.
    time_max : float, optional
        Maximum time allowed for optimization, by default 60 seconds.
    max_it : int, optional
        Maximum number of iterations, by default None (unlimited).
    population_size : int, optional
        Population size, by default 7.
    alpha : float, optional
        Control factor for the clan update, by default 0.5.
    
    Returns
    -------
    Tuple[np.ndarray, float]
        The best solution found and its fitness score.
    """
    num_bins = array_base.shape[0]
    elephant_matrix = generate_initial_matrix_population(array_base, c, population_size, VALID=True)

    # Initialize the best solution and its fitness
    best_idx = np.argmin(elephant_matrix[:, -1])
    best_solution = elephant_matrix[best_idx, :-1].copy()
    best_fitness = elephant_matrix[best_idx, -1]

    # Control variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        for clan_idx in range(elephant_matrix.shape[0]):
            leader = elephant_matrix[clan_idx, :-1].copy()

            for i in range(elephant_matrix.shape[0]):
                if random.random() < 0.5:
                    new_elephant = clan_update(elephant_matrix[i, :-1], leader, alpha)
                    new_elephant = np.clip(new_elephant, 0, num_bins - 1).astype(int)
                    elephant_matrix[i, :-1] = repair_solution(elephant_matrix[i, :-1], new_elephant, c)

            if fitness(elephant_matrix[clan_idx, :-1], c) > best_fitness:
                new_elephant = isolation(elephant_matrix[clan_idx, :-1])
                elephant_matrix[clan_idx, :-1] = repair_solution(elephant_matrix[clan_idx, :-1], new_elephant, c)

        for i in range(elephant_matrix.shape[0]):
            elephant_matrix[i, -1] = fitness(elephant_matrix[i, :-1], c)

        best_idx = np.argmin(elephant_matrix[:, -1])
        if elephant_matrix[best_idx, -1] < best_fitness:
            best_fitness = elephant_matrix[best_idx, -1]
            best_solution = elephant_matrix[best_idx, :-1].copy()

        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fitness
