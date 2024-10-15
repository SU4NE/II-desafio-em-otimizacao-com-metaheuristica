"""
Module for implementing the Simulated Annealing algorithm for the Bin Packing Problem (BPP).
The algorithm tries to optimize the packing of items into bins by simulating the process of
annealing in metals, where temperature is gradually reduced.
"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, evaluate_solution, fitness,
                                 generate_solution, theoretical_minimum)


def __perturb_solution(
    best_fit: int, solution: List[np.ndarray], containers: List[int], c: int
) -> Tuple[List[np.ndarray], List[int]]:
    """
    Perturbs the current solution by randomly moving an item from one bin to another.

    Parameters
    ----------
    best_fit : int
        Current best fitness value.
    solution : List[np.ndarray]
        List of bins containing items.
    containers : List[int]
        List of current capacities of the bins.
    c : int
        Capacity of the bins.

    Returns
    -------
    Tuple[List[np.ndarray], List[int]]
        The perturbed solution and updated container capacities.
    """
    if best_fit < 2:
        return solution

    new_solution = solution.copy()
    new_containers = containers.copy()
    source_bin_idx = random.randint(0, best_fit - 1)
    item_to_move = random.randint(
        0,
        fitness(new_solution[source_bin_idx], c) - 1,
    )
    item = new_solution[source_bin_idx][item_to_move]
    new_containers[source_bin_idx] += item

    if new_containers[source_bin_idx] == c:
        del new_solution[source_bin_idx]
        del new_containers[source_bin_idx]
    else:
        new_solution[source_bin_idx] = np.delete(
            new_solution[source_bin_idx], item_to_move
        )

    destination_bin_idx = random.randint(0, fitness(new_solution, c))
    if destination_bin_idx == len(new_solution):
        new_solution.append(np.array([item], dtype=int))
        new_containers.append(c - item)
    else:
        new_solution[destination_bin_idx] = np.append(
            new_solution[destination_bin_idx], item
        )
        new_containers[destination_bin_idx] -= item
        if new_containers[destination_bin_idx] < 0:
            new_bin, new_container = generate_solution(
                new_solution[destination_bin_idx], c, BFD=True
            )
            del new_containers[destination_bin_idx]
            del new_solution[destination_bin_idx]
            new_solution.extend(new_bin)
            new_containers.extend(new_container)

    return new_solution, new_containers


def __accept_solution(new_fitness: int, best_fit: int, temperature: float):
    return (
        True
        if new_fitness < best_fit
        else np.random.random() < np.exp((best_fit - new_fitness) / temperature)
    )


def __operations(
    best_fit: int,
    solution: List[np.ndarray],
    containers: List[int],
    c: int,
    temperature: float,
    iterations_temperature: int,
) -> Tuple[List[np.ndarray], List[int], int]:
    """
    Perform operations for one temperature level.

    Parameters
    ----------
    best_fit : int
        Fitness of the current best solution.
    solution : List[np.ndarray]
        Current solution being optimized.
    containers : List[int]
        List of containers for the items.
    c : int
        Bin capacity.
    temperature : float
        Current temperature of simulated annealing.
    iterations_temperature : int
        Number of iterations to perform at the current temperature.

    Returns
    -------
    Tuple[List[np.ndarray], List[int], int]
        The updated solution, containers, and best fitness.
    """
    for _ in range(iterations_temperature):
        new_solution, new_containers = __perturb_solution(
            best_fit, solution, containers, c
        )
        new_fitness = fitness(new_solution, c)
        if evaluate_solution(new_containers) and __accept_solution(
            new_fitness, best_fit, temperature
        ):
            solution = new_solution
            containers = new_containers
            best_fit = new_fitness

    return solution, containers, best_fit


def simulated_annealing(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    min_temperature: float = 1e-9,
    alpha: float = 0.9,
    iterations_per_temperature: int = 100,
    initial_temperature: float = 1e9,
) -> Tuple[List[np.ndarray], int]:
    """
    Execute the Simulated Annealing algorithm for the Bin Packing Problem.

    Parameters
    ----------
    array_base : np.ndarray
        Array of items to pack.
    c : int
        Capacity of the bins.
    time_max : float, optional
        Maximum allowable time for the search, by default 60.
    min_temperature : float, optional
        Minimum temperature before stopping, by default 1e-9.
    alpha : float, optional
        Cooling rate, by default 0.9.
    iterations_per_temperature : int, optional
        Number of iterations per temperature level, by default 100.
    initial_temperature : float, optional
        Starting temperature, by default 1e9.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness value.
    """
    solution: np.ndarray = array_base.copy()
    solution, containers = generate_solution(solution, c)
    th_min: int = theoretical_minimum(array_base, c)
    best_solution = solution
    best_fit: int = fitness(solution, c)
    temperature: float = initial_temperature
    time_start: float = time.time()

    while check_end(
        th_min,
        best_fit,
        time_max,
        time_start,
        time.time(),
        temperature,
        min_temperature,
    ):
        solution, containers, best_fit = __operations(
            best_fit, solution, containers, c, temperature, iterations_per_temperature
        )

        if best_fit < fitness(best_solution, c):
            best_solution = solution.copy()
        temperature *= alpha

    return best_solution, fitness(best_solution, c)
