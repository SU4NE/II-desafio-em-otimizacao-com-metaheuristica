"""
Module for implementing the Artificial Bee Colony (ABC) algorithm for optimization problems.
"""

import random
import time
from copy import copy
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, container_insert, fitness,
                                 generate_container, generate_solution,
                                 theoretical_minimum, tournament_roulette)


@dataclass
class Bee:
    """Represents a bee in the artificial bee colony algorithm."""

    source: List[np.ndarray]
    container: List[np.ndarray]
    fitness: int = 0
    counter: int = 0


def __bee_operation(b: Bee, c) -> Bee:
    """
    Performs a bee operation by modifying the source and container.

    Parameters
    ----------
    b : Bee
        The bee to operate on.
    c : int
        Maximum container capacity.

    Returns
    -------
    Bee
        The updated bee after the operation.
    """
    n = b.fitness
    l = random.randint(0, n - 2)
    r = random.randint(l, n - 1)
    while l == r:
        l = random.randint(0, n - 2)
        r = random.randint(l, n - 1)
    b.source, b.fitness, b.container = container_insert(
        (l, r), b.container, b.source, n, c
    )
    if b.fitness == n:
        b.counter += 1

    return b


def __scout_bees(
    bees: List[Bee], solution: List[np.ndarray], scout: int, employed: int, c: int
):
    """
    Resets the scout bees if their counter exceeds the scout limit.

    Parameters
    ----------
    bees : List[Bee]
        List of bees.
    solution : List[np.ndarray]
        The current solution.
    scout : int
        The scout limit for resetting a bee.
    employed : int
        Number of employed bees.
    c : int
        Maximum container capacity.

    Returns
    -------
    List[Bee]
        Updated list of bees after scouting.
    """
    for i in range(employed):
        if bees[i].counter >= scout:
            bees[i] = Bee(solution, generate_container(solution, c))
            bees[i].fitness = fitness(bees[i].source)
            solution = bees[i].source.copy()
            random.shuffle(solution)
    return bees


def __employed_bees(bees: List[Bee], c: int) -> List[Bee]:
    """
    Applies bee operations on the employed bees.

    Parameters
    ----------
    bees : List[Bee]
        List of employed bees.
    c : int
        Maximum container capacity.

    Returns
    -------
    List[Bee]
        Updated list of employed bees.
    """
    return [__bee_operation(b, c) for b in bees]


def __onlooker_bees(bees: List[Bee], c: int, gama: float, onlooker) -> List[Bee]:
    """
    Updates the onlooker bees using roulette selection.

    Parameters
    ----------
    bees : List[Bee]
        List of bees.
    c : int
        Maximum container capacity.
    gama : float
        Parameter for roulette selection.
    onlooker : int
        Number of onlooker bees.

    Returns
    -------
    List[Bee]
        Updated list of onlooker bees.
    """
    sources = [bee.fitness for bee in bees]

    for _ in range(onlooker):
        idx = tournament_roulette(sources, gama)
        b = __bee_operation(copy(bees[idx]), c)
        if b.fitness < bees[idx].fitness:
            bees[idx] = b

    return bees


def __generate_bees_solution(
    solution: List[np.ndarray], c: int, employed: int
) -> List[Bee]:
    """
    Generates initial bee solutions for the employed bees.

    Parameters
    ----------
    solution : List[np.ndarray]
        Initial solution.
    c : int
        Maximum container capacity.
    employed : int
        Number of employed bees.

    Returns
    -------
    List[Bee]
        List of bees with initial solutions.
    """
    bees: List[Bee] = []

    for _ in range(employed):
        bees.append(Bee(solution, generate_container(solution, c)))
        bees[-1].fitness = fitness(bees[-1].source)
        solution = bees[-1].source.copy()
        random.shuffle(solution)

    return bees


# pylint: disable=R0913 R0914
def artificial_bee_colony(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    employed: int = 10,
    onlooker: int = 10,
    scout: int = 10,
    gama: float = 1.8,
) -> Tuple[List[np.ndarray], int]:
    """
    Solves the BPP using the artificial bee colony algorithm.

    Parameters
    ----------
    array_base : np.ndarray
        Initial item array.
    c : int
        Maximum container capacity.
    time_max : float, optional
        Max time allowed for execution, by default 60.
    max_it : int, optional
        Max iterations, by default None.
    employed : int, optional
        Number of employed bees, by default 10.
    onlooker : int, optional
        Number of onlooker bees, by default 10.
    scout : int, optional
        Scout limit before resetting a bee, by default 10.
    gama : float, optional
        Parameter for roulette selection, by default 1.8.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        Best solution found and its fitness value.
    """
    solution: np.ndarray = array_base.copy()
    best_fit: int = fitness(solution)
    base_solution, _ = generate_solution(solution, c)
    bees = __generate_bees_solution(base_solution.copy(), c, employed)
    th_min: int = theoretical_minimum(array_base, c)
    it: int = 0
    time_start: float = time.time()
    while check_end(th_min, best_fit, time_max, time_start, time.time(), max_it, it):
        bees = __employed_bees(bees, c)
        __onlooker_bees(bees, c, gama, onlooker)
        __scout_bees(bees, base_solution.copy(), scout, employed, c)
        base_solution, best_fit = [], float("inf")
        for bee in bees:
            if bee.fitness < best_fit:
                best_fit = bee.fitness
                base_solution = bee.source
        it += 1
    return base_solution, best_fit


# pylint: enable=R0913 R0914
