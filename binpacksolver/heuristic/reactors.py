import time

import numpy as np

from binpacksolver.utils import (check_end, core_refurbishment, enrichment,
                                 fission, fusion, generate_solution,
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


def __assemble_reactor(items: np.ndarray, c: int, reactor_type: int, n_part: int):
    """_summary_

    Parameters
    ----------
    items : np.ndarray
        _description_
    c : int
        _description_
    reactor_type : int
        _description_
    n_part : int
        _description_

    Returns
    -------
    _type_
        _description_
    """
    particles = [generate_solution(items, c) for _ in range(n_part)]
    reactor = {"type": reactor_type, "particles": particles}

    return reactor


def power_plant(items: np.ndarray, c: int, **kwargs):
    """_summary_

    Parameters
    ----------
    items : np.ndarray
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
    n_part = kwargs.get("n_particles", 10)
    time_max = int(kwargs.get("time_max", 100))
    max_it = int(kwargs.get("max_it", 100))

    reactors = []
    elite = [generate_solution(items, c) for _ in range(n_part)]

    for _ in range(n_fusion):
        reactors.append(__assemble_reactor(items, c, 0, n_part))

    for _ in range(n_fission):
        reactors.append(__assemble_reactor(items, c, 1, n_part))

    th = theoretical_minimum(items, c)
    time_start = time.time()

    while check_end(th, elite[0], time_max, time_start, None, max_it, 0):
        __operations(reactors, elite)

    return elite[0]
