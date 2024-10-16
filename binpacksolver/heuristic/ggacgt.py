"""
Module for implementing the GGA-CGT algorithm for the Bin Packing Problem (BPP).
"""

import heapq
import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (best_fit_decreasing, check_end,
                                 find_best_solution, first_fit, fitness,
                                 has_common_elements, theoretical_minimum)


def __initialize_population(
    items: np.ndarray, n_pop: int, c: int
) -> List[List[np.ndarray]]:
    """
    Initializes the population by creating individuals through random shuffling
    and using the first fit algorithm.

    Parameters
    ----------
    items : np.ndarray
        List of items to be packed.
    n_pop : int
        Number of individuals in the population.
    c : int
        Capacity of each bin.

    Returns
    -------
    List[List[np.ndarray]]
        A list of individuals representing the initial population.
    """
    population = []
    for _ in range(n_pop):
        random.shuffle(items)
        individual = first_fit(items, c, [])
        population.append(individual)
    return population


def __gene_level_crossover(
    parent1: List[np.ndarray], parent2: List[np.ndarray], c: int
) -> List[np.ndarray]:
    """
    Performs gene-level crossover between two parent individuals to produce a child individual.

    Parameters
    ----------
    parent1 : List[np.ndarray]
        The first parent individual.
    parent2 : List[np.ndarray]
        The second parent individual.
    c : int
        Capacity of each bin.

    Returns
    -------
    List[np.ndarray]
        A new child individual created from the parents.
    """
    child: List[np.ndarray] = []
    trash: np.ndarray = np.array([], dtype=int)

    for x, y in zip(parent1, parent2):
        if x.sum() >= y.sum():
            if has_common_elements(x, child, trash):
                child.append(x.copy())
        else:
            if has_common_elements(y, child, trash):
                child.append(y.copy())

    child = first_fit(trash, c, child)
    return child


def __adaptive_mutation(individual: List[np.ndarray], delta: float, c: int):
    """
    Applies adaptive mutation to an individual.

    Parameters
    ----------
    individual :  List[np.ndarray]
        The individual to mutate.
    delta : float
        Factor for adaptive mutation.
    c : int
        Capacity of each bin.

    Returns
    -------
    List[np.ndarray]
        The mutated individual.
    """
    individual = sorted(individual, key=np.sum, reverse=True)
    num_bins = int(len(individual) * delta)
    bins = individual[:num_bins]
    individual = individual[num_bins:]
    trash = np.concatenate(bins)
    return best_fit_decreasing(trash, c, individual)


def __controlled_selection(
    population: List[List[np.ndarray]], limit: int
) -> List[List[np.ndarray]]:
    """
    Selects a controlled number of individuals from the population for crossover.

    Parameters
    ----------
    population : List[List[np.ndarray]]
        The current population of individuals.
    limit : int
        The number of individuals to select.

    Returns
    -------
    List[List[np.ndarray]]
        Selected individuals for crossover.
    """
    bests = heapq.nlargest(limit // 2, population, key=fitness)
    wosts = heapq.nsmallest(limit // 2, population, key=fitness)
    return bests + random.sample(wosts, limit // 2)


def __controlled_replacement(
    population: List[List[np.ndarray]], offspring: List[List[np.ndarray]], n_pop: int
) -> List[List[np.ndarray]]:
    """
    Replaces the current population with offspring, maintaining the best individuals.

    Parameters
    ----------
    population : list
        The current population of individuals.
    offspring : list
        The offspring individuals to be added.
    n_pop : int
        Number of individuals in the population.

    Returns
    -------
    list
        The new population after replacement.
    """
    population.extend(offspring)
    return heapq.nlargest(n_pop, population, key=fitness)


def genetic_algorithm_cgt(
    items: np.ndarray,
    c: int,
    max_it: int = None,
    n_pop: int = 10,
    nc: int = 3,
    nm: int = 1,
    delta: float = 0.7,
    time_max: float = 60,
) -> Tuple[List[np.ndarray], int]:
    """
    Executes the Genetic Algorithm with Coarse-Grained Tabu Search (GGA-CGT) for
    solving the Bin Packing Problem.

    Parameters
    ----------
    items : np.ndarray
        An array containing the sizes of the items to be packed into bins.
    c : int
        The capacity of each bin.
    max_it : int, optional
        The maximum number of generations for the algorithm; default is None.
    n_pop : int, optional
        The number of individuals in the population; default is 10.
    nc : int, optional
        The number of individuals selected for crossover; default is 3.
    nm : int, optional
        The number of individuals selected for mutation; default is 1.
    delta : float, optional
        The factor for adaptive mutation control; default is 0.7.
    time_max : float, optional
        The maximum execution time for the algorithm in seconds; default is 60.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        A tuple containing the best solution found (as a list of np.ndarrays)
        and its associated fitness value.
    """
    th_min: int = theoretical_minimum(items, c)
    population = __initialize_population(items, n_pop, c)
    best_solution: List[np.ndarray] = find_best_solution(population)
    it: int = 0
    time_start: float = time.time()

    while check_end(
        th_min, fitness(best_solution), time_max, time_start, time.time(), max_it, it
    ):
        selected_individuals = __controlled_selection(population, nc)

        offspring = []
        for i in range(0, len(selected_individuals), 2):
            child1 = __gene_level_crossover(
                selected_individuals[i], selected_individuals[i + 1], c
            )
            offspring.append(child1)
            child2 = __gene_level_crossover(
                selected_individuals[i + 1], selected_individuals[i], c
            )
            offspring.append(child2)

        population = __controlled_replacement(population, offspring, n_pop)

        elite_individuals = __controlled_selection(population, nm)
        cloned_individuals = [ind.copy() for ind in elite_individuals]
        cloned_individuals = [
            __adaptive_mutation(ind, delta, c) for ind in cloned_individuals
        ]
        population = __controlled_replacement(population, cloned_individuals, n_pop)

        best_solution = find_best_solution(population)
        it += 1

    return best_solution, fitness(best_solution)
