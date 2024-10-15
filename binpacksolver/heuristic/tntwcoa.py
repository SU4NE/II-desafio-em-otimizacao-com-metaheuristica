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

def nonlinear_inertia_weight(it: int, max_it: int, w_max: float = 0.9, w_min: float = 0.4) -> float:
    """
    Computes the nonlinear inertia weight, used to control the balance
    between global and local search.

    Parameters
    ----------
    it : int
        Current iteration number.
    max_it : int
        Maximum number of iterations.
    w_max : float, optional
        Maximum inertia weight, by default 0.9.
    w_min : float, optional
        Minimum inertia weight, by default 0.4.

    Returns
    -------
    float
        The computed inertia weight for the current iteration.
    """
    return w_max - ((w_max - w_min) * (it / max_it) ** 2)

def adaptive_t_distribution(n: int, dim: int, scale: float = 1.0) -> np.ndarray:
    """
    Generates random numbers using the T-distribution with 1.5 degrees
    of freedom for adaptive diversity.

    Parameters
    ----------
    n : int
        Number of samples.
    dim : int
        Number of dimensions.
    scale : float, optional
        Scaling factor for the T-distribution, by default 1.0.

    Returns
    -------
    np.ndarray
        Random samples from the T-distribution.
    """
    return np.random.standard_t(df=1.5, size=(n, dim)) * scale

def improved_coati_optimization_algorithm(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7,
    w_max: float = 0.9,
    w_min: float = 0.4,
    scale: float = 1.0,
    inertia_factor: float = 0.5,
) -> Tuple[np.ndarray, float]:
    """
    Improved Coati Optimization Algorithm (TNTWCOA) applied to the Bin Packing Problem (BPP).

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
    w_max : float, optional
        Maximum inertia weight, by default 0.9.
    w_min : float, optional
        Minimum inertia weight, by default 0.4.
    scale : float, optional
        Scale factor for adaptive T-distribution variation, by default 1.0.
    inertia_factor : float, optional
        Factor controlling the balance between exploration and exploitation, by default 0.5.

    Returns
    -------
    Tuple[np.ndarray, float]
        The best solution found and its fitness score.
    """
    inertia_factor = min(max(inertia_factor, 0), 1)
    min_value = array_base.min()
    max_value = array_base.max()
    n = array_base.shape[0]
    
    # Chaotic initialization using Tent Chaos
    coati_matrix = generate_initial_matrix_population(array_base, c, population_size, TENTCHAOS=True)
    
    # Initialize personal best solution and fitness
    best_idx = np.argmin(coati_matrix[:, -1])
    best_solution = coati_matrix[best_idx, :-1].copy()
    best_fitness = coati_matrix[best_idx, -1]

    # Control variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        inertia_weight = nonlinear_inertia_weight(it, max_it if max_it else max((time_max * 1e2) // population_size - time.time(), 100), w_max, w_min)

        for i in range(coati_matrix.shape[0]):
            if random.random() < 0.5:
                new_coati = best_solution + inertia_weight * np.random.uniform(-1, 1, n)
            else:
                new_coati = coati_matrix[i, :-1] + inertia_weight * np.random.uniform(-1, 1, n)
            
            new_coati = np.clip(new_coati, min_value, max_value).astype(int)
            coati_matrix[i, :-1] = repair_solution(coati_matrix[i, :-1], new_coati, c)

        # Exploitation phase with adaptive T-distribution
        for i in range(coati_matrix.shape[0]):
            if random.random() < 0.5:
                t_variation = adaptive_t_distribution(1, n, scale).flatten()
                new_coati = coati_matrix[i, :-1] + t_variation
                new_coati = np.clip(new_coati, min_value, max_value).astype(int)
                coati_matrix[i, :-1] = repair_solution(coati_matrix[i, :-1], new_coati, c)

        for i in range(coati_matrix.shape[0]):
            coati_matrix[i, -1] = fitness(coati_matrix[i, :-1], c)

        best_idx = np.argmin(coati_matrix[:, -1])
        if coati_matrix[best_idx, -1] < best_fitness:
            best_fitness = coati_matrix[best_idx, -1]
            best_solution = coati_matrix[best_idx, :-1].copy()

        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fitness
