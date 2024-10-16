"""
Gravitational Search Algorithm (GSA) for solving the Bin Packing Problem (BPP), 
using gravitational force and particle movement to evolve solutions.
"""

import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def compute_gravitational_force(
    particle: np.ndarray, other_particle: np.ndarray, force_g: float, distance: float
):
    """
    Computes the gravitational force between two particles based on
    the gravitational constant force_g.

    Parameters
    ----------
    particle : np.ndarray
        The current particle (solution).
    other_particle : np.ndarray
        The other particle (solution).
    force_g : float
        The gravitational constant.
    distance : float
        The distance between the two particles.

    Returns
    -------
    np.ndarray
        The gravitational force exerted on the current particle.
    """
    return force_g * (other_particle - particle) / (distance + 1e-9)


def move_particle(
    particle: np.ndarray,
    velocity: np.ndarray,
    force: np.ndarray,
    mass: float,
    min_value: int,
    max_value: int,
):
    """
    Moves the particle based on its velocity and the gravitational force acting on it.

    Parameters
    ----------
    particle : np.ndarray
        The current particle (solution).
    velocity : np.ndarray
        The current velocity of the particle.
    force : np.ndarray
        The force acting on the particle.
    mass : float
        The mass of the particle.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        The new position and velocity of the particle.
    """
    mass = max(mass, 1e-9)
    new_velocity = velocity + force / mass
    new_position = particle + new_velocity
    new_position = np.clip(np.round(new_position), min_value, max_value).astype(int)
    new_velocity = np.clip(new_velocity, -1e3, 1e3)
    return new_position, new_velocity


def gravitational_search_algorithm(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: float = 7,
    grav_decay: float = 0.99,
) -> Tuple[List[np.ndarray], int]:
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
    population_size : float, optional
        _description_, by default 7

    Returns
    -------
    Tuple[List[np.ndarray], int]
        _description_
    """
    min_value = array_base.min()
    max_value = array_base.max()
    n = array_base.shape[0]
    gravitational_matrix = generate_initial_matrix_population(
        array_base, c, population_size, VALID=True
    )
    velocities = np.zeros((population_size, n))
    masses = np.ones(population_size)
    force_g = 1

    # Find the initial best solution
    best_idx = np.argmin(gravitational_matrix[:, -1])
    best_fit = gravitational_matrix[best_idx, -1]
    best_solution = gravitational_matrix[best_idx, :-1]

    # Initial variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fit, time_max, start, time.time(), max_it, it):
        # Calculate the masses based on the fitness values
        fitness_values = gravitational_matrix[:, -1]
        worst_fitness = np.max(fitness_values)
        best_fitness_iteration = np.min(fitness_values)
        if worst_fitness == best_fitness_iteration:
            masses = np.ones(population_size)
        else:
            masses = (worst_fitness - fitness_values) / (
                worst_fitness - best_fitness_iteration + 1e-9
            )
        masses = masses / np.sum(masses)

        for i in range(population_size):
            force = np.zeros(n)
            for j in range(population_size):
                if i != j:
                    distance = np.linalg.norm(
                        gravitational_matrix[i, :-1] - gravitational_matrix[j, :-1]
                    )
                    force += compute_gravitational_force(
                        gravitational_matrix[i, :-1],
                        gravitational_matrix[j, :-1],
                        force_g,
                        distance,
                    )

            # Move the particle based on the resulting force and update its velocity
            new_gravitational, velocities[i] = move_particle(
                gravitational_matrix[i, :-1],
                velocities[i],
                force,
                masses[i],
                min_value,
                max_value,
            )

            # Ensure the solution is valid after movement
            gravitational_matrix[i, :-1] = repair_solution(
                gravitational_matrix[i, :-1], new_gravitational, c
            )

        for i in range(population_size):
            gravitational_matrix[i, -1] = fitness(gravitational_matrix[i, :-1], c)

        best_idx = np.argmin(gravitational_matrix[:, -1])
        best_fit = gravitational_matrix[best_idx, -1]
        best_solution = gravitational_matrix[best_idx, :-1]

        # Decay the gravitational constant
        force_g = force_g * grav_decay

        # Increment iteration count
        it += 1

    return generate_solution(best_solution, c, VALID=True)[0], best_fit
