import random
import time
from copy import copy
from dataclasses import dataclass
from typing import List

import numpy as np

from binpacksolver.utils import (check_end, container_insert, fitness,
                                 generate_container, generate_solution,
                                 theoretical_minimum, tournament_roulette)


@dataclass
class Bee:
    """_summary_"""

    source: List[np.ndarray]
    container: List[np.ndarray]
    fitness: int = 0
    counter: int = 0


def __bee_operation(b: Bee, c) -> Bee:
    """_summary_

    Parameters
    ----------
    b : Bee
        _description_
    """
    n = b.fitness
    l = random.randint(0, n - 2)
    r = random.randint(l, n - 1)
    b.source, b.fitness = container_insert((l, r), b.container, b.source, n, c)
    if b.fitness == n:
        b.counter += 1

    return b


def __scout_bees(
    bees: List[Bee], solution: List[np.ndarray], scout: int, employed: int, c: int
):
    """_summary_

    Parameters
    ----------
    bees : List[Bee]
        _description_
    solution : List[np.ndarray]
        _description_
    scout : int
        _description_
    employed : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    for i in range(employed):
        if bees[i].counter >= scout:
            bees[i] = Bee(solution, generate_container(solution, c))
            bees[i].fitness = fitness(bees[i].source)
            solution = bees[i].source.copy()
            random.shuffle(solution)
    return bees


def __employed_bees(bees: List[Bee], c: int) -> List[Bee]:
    """_summary_

    Parameters
    ----------
    bees : List[Bee]
        _description_
    c : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return [__bee_operation(b, c) for b in bees]


def __onlooker_bees(bees: List[Bee], c: int, gama: float, onlooker) -> List[Bee]:
    """_summary_

    Parameters
    ----------
    bees : List[List[Bee]]
        _description_
    c : int
        _description_
    gama : float
        _description_
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
    """_summary_

    Parameters
    ----------
    solution : List[np.ndarray]
        _description_
    c : int
        _description_
    bees : tuple
        _description_

    Returns
    -------
    List[List[np.ndarray]]
        _description_
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
):
    """_summary_

    Parameters
    ----------
    array_base : np.ndarray
        _description_
    c : int
        _description_
    time_max : float, optional
        _description_, by default 60
    max_it : int, optional
        _description_, by default None
    employed : int, optional
        _description_, by default 10
    onlooker : int, optional
        _description_, by default 10
    scout : int, optional
        _description_, by default 10
    gama : float, optional
        _description_, by default 1.8

    Returns
    -------
    _type_
        _description_
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


# pylint: enable=R0913
