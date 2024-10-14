"""
Module for implementing the Particle Swarm Optimization (PSO) algorithm 
for the Bin Packing Problem (BPP). The algorithm attempts to optimize the 
packing of items into bins by simulating a swarm of particles, where each 
particle adjusts its position based on its personal best solution and the 
global best solution found by the swarm.

PSO leverages social and cognitive factors to iteratively search for an 
optimal or near-optimal solution by balancing exploration (global search) 
and exploitation (local search) of the solution space.
"""

import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


# pylint: disable=R0913, R0914
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
    """Particle Swarm Optimization with a constraint to prevent negative positions.

    Parameters
    ----------
    array_base : np.ndarray
        Base array for the problem.
    c : int
        A problem-specific parameter.
    time_max : float, optional
        Maximum time for the optimization, by default 60 seconds.
    max_it : int, optional
        Maximum iterations, by default None (unlimited).
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

    # Generate initial population
    pop_bins, _ = generate_initial_population(
        array_base, c, population_size, juice=False, VALID=True
    )

    # Initialize particle positions and velocities randomly
    particles = [np.concatenate(lst) for lst in pop_bins]
    velocities = [np.random.uniform(min_value, max_value, len(p)) for p in particles]

    # Flatten the population and calculate fitness for each particle
    fitness_values = np.array([fitness(p, c) for p in particles])

    # Initialize personal bests (positions and scores)
    personal_best_positions = particles.copy()
    personal_best_scores = fitness_values.copy()

    # Initialize global best (position and score)
    global_best_idx = np.argmin(fitness_values)
    global_best_position = personal_best_positions[global_best_idx]
    global_best_score = personal_best_scores[global_best_idx]

    # Initial variables
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, global_best_score, time_max, start, time.time(), max_it, it):
        for i in range(population_size):
            velocities[i] = (
                w * velocities[i]
                + c1 * np.random.random() * (personal_best_positions[i] - particles[i])
                + c2 * np.random.random() * (global_best_position - particles[i])
            )

            new_position = np.abs(np.array(particles[i] + velocities[i]).astype(int))
            particles[i] = repair_solution(particles[i].copy(), new_position, c)
            current_score = fitness(particles[i], c)

            if current_score < personal_best_scores[i]:
                personal_best_scores[i] = current_score
                personal_best_positions[i] = particles[i]

        best_particle_idx = np.argmin(personal_best_scores)
        if personal_best_scores[best_particle_idx] < global_best_score:
            global_best_score = personal_best_scores[best_particle_idx]
            global_best_position = personal_best_positions[best_particle_idx]

        it += 1

    return generate_solution(global_best_position, c, VALID=True)[0], global_best_score


# pylint: enable=R0913, R0914
