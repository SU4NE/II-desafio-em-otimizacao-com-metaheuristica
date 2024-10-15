"""
Solution Generation Module

This module contains functions to generate a solution and evaluate its
fitness based on a given array of values.
"""

import math
import random
from typing import Any, List, Tuple, Union

import numpy as np

from .online_algorithms import best_fit_decreasing, first_fit, first_fit_decreasing


def generate_container(solution: List[np.ndarray], c: int) -> List[int]:
    """
    Generates a list of remaining capacities for each bin in the solution.

    Parameters
    ----------
    solution : List[np.ndarray]
        A list of numpy arrays, where each array represents a bin containing
        items with their respective sizes.
    c : int
        The maximum capacity of each bin.

    Returns
    -------
    List[int]
        A list of remaining capacities for each bin, after subtracting the
        total size of items already packed in each bin.
    """
    containers = [c] * len(solution)
    for index, value in enumerate(solution):
        containers[index] -= value.sum()
    return containers


def generate_solution(
    solution: np.ndarray, c: int, **kwargs
) -> Tuple[List[np.ndarray], List[int]]:
    """
    Generates a modified solution based on heuristics or sorting methods.

    The function applies different heuristics based on keyword arguments:
    - First-Fit Decreasing (FFD)
    - Best-Fit Decreasing (BFD)
    - First-Fit (FF)
    - VALID (simple one-item-per-bin initialization)

    If no heuristic is specified, it sorts the solution in descending order
    and packs items into bins.

    Parameters
    ----------
    solution : np.ndarray
        An array representing the current solution.
    c: int
        Max line value (container capacity).

    Returns
    -------
    List[np.ndarray]
        A new solution array, sorted in descending order.
    List[int]
        A list representing the remaining space in each container.
    """
    if kwargs.get("FFD", False):
        solution = first_fit_decreasing(solution, c)
        return solution, generate_container(solution, c)

    if kwargs.get("BFD", False):
        solution = best_fit_decreasing(solution, c, [])
        return solution, generate_container(solution, c)

    if kwargs.get("FF", False):
        solution = first_fit(solution, c, [])
        return solution, generate_container(solution, c)

    if kwargs.get("VALID", False):
        solution = valid_solution(solution, c)
        return solution, generate_container(solution, c)

    solution = np.sort(solution)[::-1]
    solution = [np.array([elemento], dtype=int) for elemento in solution]
    return solution, generate_container(solution, c)


def generate_initial_population(
    solution: np.ndarray, c: int, population: int, juice: bool = False, **kwargs
) -> Tuple[List[List[np.ndarray]], List[List[int]]]:
    """
    Generates an initial population for the bin packing problem.

    Parameters
    ----------
    solution : np.ndarray
        Initial solution representing the items to be packed.
    c : int
        Bin capacity.
    population : int
        Number of individuals in the population.
    juice: bool
        If any individual is going to use BFD.

    Returns
    -------
    Tuple[List[List[np.ndarray]], List[List[int]]]
        A tuple with the generated bins and container capacities for
        each individual in the population.
    """
    valid = kwargs.get("VALID", False)
    pop_bins = [None] * population
    pop_containers = [None] * population

    for i in range(population):
        if valid:
            pop_bins[i], _ = generate_solution(solution, c, VALID=True)
            random.shuffle(solution)
        else:
            pop_bins[i], _ = generate_solution(solution, c)
        pop_containers[i] = generate_container(pop_bins[i], c)

    if juice:
        pop_bins[-1], _ = generate_solution(solution, c, BFD=True)
        pop_containers[-1] = generate_container(pop_bins[-1], c)

    return pop_bins, pop_containers


def generate_initial_matrix_population(
    solution: np.ndarray, c: int, population: int, juice: bool = False, **kwargs
) -> np.ndarray:
    """
    Generates an initial population for the bin packing problem.

    Parameters
    ----------
    solution : np.ndarray
        Initial solution representing the items to be packed.
    c : int
        Bin capacity.
    population : int
        Number of individuals in the population.
    juice: bool
        If True, the last individual will use BFD.

    Returns
    -------
    pop_matrix: np.ndarray
        matrix  of Population of bins.
    """
    pop_bins, _ = generate_initial_population(solution, c, population, juice, **kwargs)

    fitness_values = np.array([fitness(lst) for lst in pop_bins])
    pop_bins = np.vstack([np.concatenate(lst) for lst in pop_bins]).astype(int)

    return np.hstack((pop_bins, fitness_values[:, np.newaxis]))


def fitness(solution: Union[List[np.ndarray], np.ndarray], c: int = -1) -> int:
    """
    Calculates the fitness of the given solution.

    The fitness is defined as the number of bins required to pack the items
    without exceeding the bin capacity `c`. For lists of arrays, it simply
    returns the length of the list (number of bins).

    Parameters
    ----------
    solution : Union[List[np.ndarray], np.ndarray]
        The current solution, either as a list of numpy arrays (bins) or a
        1D numpy array of items.
    c : int, optional
        Capacity of each bin. Required when the solution is a numpy array.
        Default is -1.

    Returns
    -------
    int
        The fitness score, defined as the number of bins required.
    """
    if isinstance(solution, np.ndarray):
        if c == -1:
            raise ValueError(
                "To calculate fitness using np.ndarray capacity cannot be -1"
            )
        cum_sum = 0
        count = 0
        for item in solution:
            if cum_sum + item > c:
                count += 1
                cum_sum = item
            else:
                cum_sum += item
        return count + 1 if cum_sum else 0

    return len(solution)


def theoretical_minimum(solution: np.ndarray, c: int) -> int:
    """
    calculates the theoretical minimum based on the sum of the solution
    and a given capacity c.

    Parameters
    ----------
    solution : np.ndarray
        An array representing the current solution.
    c : int
        An integer representing the capacity.

    Returns
    -------
    int
        The theoretical minimum, rounded up.
    """
    return math.ceil(solution.sum() / c)


def tournament_roulette(
    population: Union[List[int], np.ndarray], gama: float = 1.8, tour_size: int = 3
) -> int:
    """
    Selects the index of an individual from the population using a combination
    of tournament selection and roulette wheel.

    Parameters
    ----------
    population : Union[List[int], np.ndarray]
        A list of fitness values or a 2D matrix where the fitness is in the last column.
    gama : float, optional
        The parameter gama that adjusts the probability distribution in the
        roulette selection, by default 1.8.
    tour_size : int, optional
        The number of individuals selected to participate in the tournament,
        by default 3.

    Returns
    -------
    int
        The index of the winning individual in the original population.
    """
    if isinstance(population, np.ndarray) and population.ndim == 2:
        fitness_values = population[:, -1]
    else:
        fitness_values = population

    tour_idxs = random.sample(range(len(fitness_values)), tour_size)
    tournament = [fitness_values[i] for i in tour_idxs]
    tour_sum = sum(v**gama for v in tournament)
    beta = [(v**gama) / tour_sum for v in tournament]
    winner_value = random.choices(tournament, weights=beta, k=1)[0]
    return tour_idxs[tournament.index(winner_value)]


def find_best_solution(solutions):
    """
    Updates the best solution found in the current solutions.

    Parameters
    ----------
    solutions : list
        The current solutions of individuals.

    Returns
    -------
    list
        The best solution found.
    """
    solutions = sorted(solutions, key=fitness, reverse=True)
    return solutions[0]


def evaluate_solution(containers: List[int]) -> bool:
    """
    Evaluate the containers

    Parameters
    ----------
    containers : List[int]
        A list representing the remaining space in each container.

    Returns
    -------
    bool
        If all containers are valid it returns true otherwise false
    """
    return all(bin_ > -1 for bin_ in containers)


# pylint: disable=R0912
def bw_population(
    population: Union[List[List[np.ndarray]], np.ndarray], n: int = None, **kwargs
) -> Tuple[Any, Any]:
    """
    Finds the indices of the best and worst fitness in the population.

    Parameters
    ----------
    population : Union[List[List[np.ndarray]], np.ndarray]
        A list of individuals (bins) in the population, where each individual
        is a list of numpy arrays representing bins with items, or a 2D numpy array.
    n : int, optional
        The number of individuals to consider in the population.
        If None, it considers the entire population, by default None.

    Returns
    -------
    Tuple[Any, Any]
        A tuple containing the index of the individual with the best fitness
        and the index of the individual with the worst fitness in the population.
    """
    if not n:
        if isinstance(population, np.ndarray):
            n = population.shape[0]
        else:
            n = len(population)

    list_all = kwargs.get("list_all", False)
    c = kwargs.get("C", -1)

    if isinstance(population, np.ndarray):
        if list_all:
            best = (float("inf"), [])
            worst = []
            for idx in range(n):
                fit = fitness(population[idx, :], c)
                if fit <= best[0]:
                    if fit < best[0]:
                        worst.extend(best[1])
                        best = (fit, [idx])
                    else:
                        best[1].append(idx)
                else:
                    worst.append(idx)
            return best[1], worst

        best = (float("inf"), 0)
        worst = (float("-inf"), 0)
        for idx in range(n):
            fit = fitness(population[idx, :], c)
            if fit < best[0]:
                best = (fit, idx)
            if fit > worst[0]:
                worst = (fit, idx)
        return best[1], worst[1]

    if list_all:
        best = (float("inf"), [])
        worst = []
        for idx in range(n):
            fit = fitness(population[idx])
            if fit <= best[0]:
                if fit < best[0]:
                    worst.extend(best[1])
                    best = (fit, [idx])
                else:
                    best[1].append(idx)
            else:
                worst.append(idx)
        return best[1], worst

    best = (float("inf"), 0)
    worst = (float("-inf"), 0)
    for idx in range(n):
        fit = fitness(population[idx])
        if fit < best[0]:
            best = (fit, idx)
        if fit > worst[0]:
            worst = (fit, idx)

    return best[1], worst[1]


# pylint: disable=R0912


def bestfit_population(
    population: Union[List[List[np.ndarray]], np.ndarray], c: int = -1
) -> int:
    """
    Finds the best (minimum) fitness in the population.

    Parameters
    ----------
    population : Union[List[List[np.ndarray]], np.ndarray]
        A population of individuals, where each individual can be represented as:
        - A list of numpy arrays (bins) in the case of a List[List[np.ndarray]].
        - A 2D numpy array where each row represents an individual in the case of a numpy array.
    c : int, optional
        The bin capacity, required if population is a numpy array and used with
        `generate_solution`, by default -1.

    Returns
    -------
    int
        The minimum fitness value across the population.
    """
    if isinstance(population, np.ndarray):
        return min(fitness(population[i, :], c) for i in range(population.shape[0]))
    return min(fitness(bins) for bins in population)


def valid_solution(solution: np.ndarray, c: int) -> List[np.ndarray]:
    """
    Validates a bin packing solution by organizing items into bins without
    exceeding the bin capacity.

    Parameters
    ----------
    solution : np.ndarray
        Array of items to be packed into bins.
    c : int
        Capacity of each bin.

    Returns
    -------
    List[np.ndarray]
        A list of bins, where each bin is a numpy array of items, ensuring that
        the total weight of items in each bin does not exceed the given capacity.
    """
    remaining_items = []
    used_capacity = 0
    remaining_items.append([])

    for item in solution:
        if used_capacity + item <= c:
            remaining_items[-1].append(item)
            used_capacity += item
        else:
            remaining_items[-1] = np.array(remaining_items[-1], dtype=int)
            used_capacity = item
            remaining_items.append([item])

    remaining_items[-1] = np.array(remaining_items[-1], dtype=int)
    return remaining_items


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
    if len(modify) != 0:
        solution = best_fit_decreasing(
            np.array(remaining_values),
            c,
            generate_solution(np.array(modify), c, VALID=True)[0],
        )
    else:
        solution = np.random.shuffle(solution)

    if isinstance(solution, list):
        return np.concatenate(solution)

    return np.array(solution)


def local_search(
    current_solution: np.ndarray, c: int, min_value: int, max_value: int
) -> np.ndarray:
    """
    Executes a local search by perturbing a random dimension of the solution.

    Parameters
    ----------
    current_solution : np.ndarray
        The current solution to be perturbed.
    c : int
        Maximum container capacity (used as a boundary for some variables if needed).
    min_value : int
        Minimum allowable value for any dimension of the solution.
    max_value : int
        Maximum allowable value for any dimension of the solution.

    Returns
    -------
    np.ndarray
        The perturbed solution after the local search.
    """
    perturbed_solution = current_solution.copy()
    dim = current_solution.shape[0]
    index_to_modify = np.random.randint(dim)
    random_factor = np.random.uniform(-1, 1)
    comparison_index = np.random.randint(dim)
    new_value = current_solution[index_to_modify] + random_factor * (
        current_solution[index_to_modify] - current_solution[comparison_index]
    )
    perturbed_solution[index_to_modify] = np.clip(new_value, min_value, max_value)
    return repair_solution(current_solution, perturbed_solution, c)
