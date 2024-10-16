"""
Particle Swarm Optimization (PSO) for solving the Bin Packing Problem (BPP), 
optimizing particle positions and velocities to find the best solution.
"""

import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def particle_swarm_optimization(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    population_size: int = 7,
    w: float = 0.5,
    c1: float = 1.5,
    c2: float = 1.5,
) -> Tuple[List[np.ndarray], int]:
    """
    Particle Swarm Optimization (PSO) where particles are stored in a matrix form.

    Parameters
    ----------
    array_base : np.ndarray
        Base array for the problem.
    c : int
        A problem-specific parameter.
    time_max : float, optional
        Maximum time for the optimization, by default 60 seconds.
    max_it : int, optional
        Maximum iterations, by default None.
    population_size : int, optional
        Number of particles in the population, by default 7.
    w : float, optional
        Inertia weight, by default 0.5.
    c1 : float, optional
        Cognitive (personal) learning factor, by default 1.5.
    c2 : float, optional
        Social (global) learning factor, by default 1.5.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness score.
    """
    min_value = array_base.min()
    max_value = array_base.max()

    particles_matrix = generate_initial_matrix_population(
        array_base, c, population_size, VALID=True
    )
    velocities = np.random.uniform(
        min_value, max_value, (population_size, array_base.shape[0])
    )
    fitness_values = particles_matrix[:, -1].copy()
    personal_best_positions = particles_matrix[:, :-1].copy()
    personal_best_scores = fitness_values.copy()
    global_best_idx = np.argmin(personal_best_scores)
    global_best_position = personal_best_positions[global_best_idx].copy()
    global_best_score = personal_best_scores[global_best_idx]

    # Initial variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, global_best_score, time_max, start, time.time(), max_it, it):
        for i in range(population_size):
            velocities[i] = (
                w * velocities[i]
                + c1
                * np.random.random()
                * (personal_best_positions[i] - particles_matrix[i, :-1])
                + c2
                * np.random.random()
                * (global_best_position - particles_matrix[i, :-1])
            )

            new_position = np.abs(particles_matrix[i, :-1] + velocities[i]).astype(int)
            particles_matrix[i, :-1] = repair_solution(
                particles_matrix[i, :-1].copy(), new_position, c
            )

            current_fitness = fitness(particles_matrix[i, :-1], c)
            particles_matrix[i, -1] = current_fitness

            if current_fitness < personal_best_scores[i]:
                personal_best_scores[i] = current_fitness
                personal_best_positions[i] = particles_matrix[i, :-1].copy()

        best_particle_idx = np.argmin(personal_best_scores)
        if personal_best_scores[best_particle_idx] < global_best_score:
            global_best_score = personal_best_scores[best_particle_idx]
            global_best_position = personal_best_positions[best_particle_idx].copy()

        it += 1

    return generate_solution(global_best_position, c, VALID=True)[0], global_best_score
