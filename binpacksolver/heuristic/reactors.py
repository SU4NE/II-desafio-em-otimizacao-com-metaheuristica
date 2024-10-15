"""_summary_"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 repair_solution, theoretical_minimum)


def fission(particles):
    """aa."""
    print(particles)


def fusion(particles, elite, c):
    """
    Performs a fusion between the particles and the elite based on the bin capacity (c).

    Parameters
    ----------
    particles : np.ndarray
        A 2D numpy array representing the bins for the particles.
    elite : np.ndarray
        A 2D numpy array representing the bins for the elite.
    c : int
        The bin capacity.

    Returns
    -------
    new_population : np.ndarray
        A new population generated by fusing particles and elite based on the bin capacity.
    """
    new_population = np.zeros_like(particles)

    for i in range(particles.shape[0]):
        child = []
        c_aux = 0

        for j in range(particles.shape[1]):
            if c_aux + particles[i, j] <= c or c_aux + elite[i, j] <= c:
                if c_aux + particles[i, j] > c_aux + elite[i, j]:
                    child.append(particles[i, j])
                    c_aux += particles[i, j]
                else:
                    child.append(elite[i, j])
                    c_aux += elite[i, j]
            else:
                child.append(
                    particles[i, j] if particles[i, j] > elite[i, j] else elite[i, j]
                )
                c_aux = 0

        new_population[i] = repair_solution(particles[i], np.array(child), c)

    return new_population


def enrichment(elite: np.array, c: int):
    """
    Performs an enrichment operation on the elite population by randomly
    swapping two elements in each individual's bins and recalculating the fitness.

    Parameters
    ----------
    elite : np.ndarray
        A 2D numpy array where each row represents an individual (bins) and
        the last column holds the fitness value.
    c : int
        The bin capacity.

    Notes
    -----
    If the swap improves the fitness, the new fitness is kept. Otherwise,
    the swap is reverted to preserve the original solution.
    """
    max_idx = elite.shape[1]
    for i in range(elite.shape[0]):
        left = random.randrange(0, max_idx - 1)
        right = random.randrange(left, max_idx - 1)

        elite[i, left], elite[i, right] = elite[i, right], elite[i, left]
        new_fit = fitness(elite[i, :-1], c)

        if new_fit < elite[i, -1]:
            elite[i, -1] = new_fit
        else:
            elite[i, left], elite[i, right] = elite[i, right], elite[i, left]


def change_core(reactor):
    """_summary_

    Parameters
    ----------
    reactor : _type_
        _description_
    """
    reactor[0] = int(not reactor[0])


def core_refurbishment(reactors: np.array, elite: np.array):
    """_summary_"""
    for reactor in reactors:
        merged = np.concatenate((reactor[1], elite))
        sorted_indices = np.argsort(merged[:, -1])
        sorted_array = merged[sorted_indices]

        elite_count = reactor[1].shape[0]
        elite = sorted_array[:elite_count]
        reactor[1] = sorted_array[elite_count:]

    max_change_index = max(int(len(reactors) * 0.3), 1)

    for idx in range(1, max_change_index + 1):
        change_core(reactors[-idx])


def __operations(reactors, elite, c):
    """_summary_

    Parameters
    ----------
    reactors : _type_
        _description_
    elite : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    for reactor in reactors:
        reactor_type, particles = reactor["type"], reactor["particles"]
        if reactor_type == 0:
            fusion(particles, elite, c)
        else:
            fission(particles)

    core_refurbishment(reactors, elite)
    enrichment(elite, c)

    return elite[0]


def __assemble_reactor(
    array_base: np.ndarray, c: int, reactor_type: int, population_size: int, **kwargs
) -> List:
    """_summary_

    Parameters
    ----------
    array_base : np.ndarray
        _description_
    c : int
        _description_
    reactor_type : int
        _description_
    population_size : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    valid = kwargs.get("VALID", False)
    juice = kwargs.get("JUICE", False)

    particles = generate_initial_matrix_population(
        array_base, c, population_size, juice=juice, VALID=valid
    )

    reactor = {"type": reactor_type, "particles": particles}

    return reactor


def power_plant(
    array_base: np.ndarray, c: int, **kwargs
) -> Tuple[List[np.ndarray], int]:
    """_summary_

    Parameters
    ----------
    array_base : np.ndarray
        _description_
    c : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    n_fusion = int(kwargs.get("n_reactors", 100) * 0.3)
    n_fission = int(kwargs.get("n_reactors", 100) * 0.7)
    population_size = kwargs.get("n_particles", 10)
    time_max = int(kwargs.get("time_max", None))
    max_it = int(kwargs.get("max_it", 100))

    reactors = []
    elite = generate_initial_matrix_population(
        array_base, c, population_size, juice=False, VALID=True
    )

    for _ in range(n_fusion):
        reactors.append(__assemble_reactor(array_base, c, 0, population_size))

    for _ in range(n_fission):
        reactors.append(__assemble_reactor(array_base, c, 1, population_size))

    th = theoretical_minimum(array_base, c)
    time_start = time.time()

    while check_end(th, elite[0], time_max, time_start, None, max_it, 0):
        __operations(reactors, elite, c)

    return elite[0]
