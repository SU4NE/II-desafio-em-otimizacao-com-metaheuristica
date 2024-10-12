"""
Solution Generation Module

This module contains functions to generate a solution and evaluate its
fitness based on a given array of values.
"""

import math
import random
from typing import List, Tuple

import numpy as np

from .online_algorithms import (best_fit_decreasing, first_fit,
                                first_fit_decreasing)


def generate_container(solution: List[np.ndarray], c: int) -> List[int]:
    """_summary_

    Parameters
    ----------
    solution : List[np.ndarray]
        _description_
    c : int
        _description_

    Returns
    -------
    List[int]
        _description_
    """
    containers = [c] * len(solution)
    for index, value in enumerate(solution):
        containers[index] -= value.sum()
    return containers


def generate_solution(
    solution: np.ndarray, c: int, **kwargs
) -> Tuple[np.ndarray, List]:
    """
    Generates a modified solution array based on the given parameters.

    If the 'FFD', 'BFD', or 'FF' keyword argument is provided and set to True,
    the function can implement heuristics such as First-Fit Decreasing (FFD),
    Best-Fit Decreasing (BFD), or First-Fit (FF) to prioritize the best solutions.

    Parameters
    ----------
    solution : np.ndarray
        An array representing the current solution.
    c: int
        Max line value (container capacity).

    Returns
    -------
    np.ndarray
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

    solution = np.sort(solution)[::-1]
    solution = [np.array([elemento], dtype=int) for elemento in solution]
    containers = generate_container(solution, c)

    return solution, containers


def fitness(solution: List[np.ndarray]) -> int:
    """
    calculates the fitness of the given solution.

    The fitness is defined as the length of the solution array.

    Parameters
    ----------
    solution : List[np.ndarray]
        An array representing the current solution.

    Returns
    -------
    int
        The fitness score, defined as the number of elements in the solution.
    """
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
    population: List[int], gama: float = 1.8, tour_size: int = 3
) -> int:
    """
    Selects the index of an individual from the population using a combination
    of tournament selection and roulette wheel.

    Parameters
    ----------
    population : List[int]
        A list representing the population (e.g., fitness values).
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
    tour_idxs = random.sample(range(len(population)), tour_size)
    tournament = [population[i] for i in tour_idxs]
    tour_sum = sum(v**gama for v in tournament)

    beta = [(v**gama) / tour_sum for v in tournament]

    winner_value = random.choices(tournament, weights=beta, k=1)[0]
    winner_index = tour_idxs[tournament.index(winner_value)]
    return winner_index


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
