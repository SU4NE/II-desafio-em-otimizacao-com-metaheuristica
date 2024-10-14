import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, core_refurbishment, enrichment,
                                 fission, fusion,
                                 generate_initial_matrix_population,
                                 theoretical_minimum)


def __operations(reactors, elite):
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
            fusion(particles, elite)
        else:
            fission(particles)

    core_refurbishment(reactors, elite)
    enrichment(elite)

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
        __operations(reactors, elite)

    return elite[0]
