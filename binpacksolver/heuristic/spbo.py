"""
Module for implementing the Student Psychology Based Optimization (SPBO) 
algorithm for the Bin Packing Problem (BPP). The algorithm simulates the 
learning process of students, where each student (solution) improves 
based on self-learning and interaction with the best-performing students 
in the population.
"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (check_end, fitness,
                                 generate_initial_matrix_population,
                                 generate_solution, repair_solution,
                                 theoretical_minimum)


def update_student(
    solution: np.ndarray,
    best_solution: np.ndarray,
    self_learning_factor: float,
    interaction_factor: float,
    min_value: int,
    max_value: int,
) -> np.ndarray:
    """
    Update a student's solution based on self-learning and interaction with
    the best-performing student.

    Parameters
    ----------
    solution : np.ndarray
        The current solution (student) to be updated.
    best_solution : np.ndarray
        The best solution found so far in the population.
    self_learning_factor : float
        The probability of self-learning for the student.
    interaction_factor : float
        The probability of learning through interaction with the best solution.
    min_value : int
        The minimum allowable value for elements of the solution.
    max_value : int
        The maximum allowable value for elements of the solution.

    Returns
    -------
    np.ndarray
        The updated solution with values constrained between `min_value`
        and `max_value`.
    """
    n = len(solution)
    for i in range(n):
        # Self-learning
        if random.random() < self_learning_factor:
            solution[i] = solution[i] + random.uniform(-1, 1) * solution[i]
        # Learning through interaction with the best student
        if random.random() < interaction_factor:
            solution[i] = best_solution[i] + random.uniform(-1, 1) * best_solution[i]

    return np.clip(solution, min_value, max_value)


def student_psychology_based_optimization(
    array_base: np.ndarray,
    c: int,
    population_size=7,
    time_max: float = 60,
    max_it=None,
    self_learning_factor=0.3,
    interaction_factor=0.7,
) -> Tuple[List[np.ndarray], int]:
    """
    Student Psychology Based Optimization (SPBO) algorithm for Bin Packing Problem (BPP).

    Parameters
    ----------
    array_base : np.ndarray
        Base array containing items to be packed into bins.
    c : int
        The bin capacity.
    population_size : int, optional
        Number of students (solutions) in the population, by default 30.
    time_max : float, optional
        Maximum time allowed for the optimization process, by default 60 seconds.
    max_it : int, optional
        Maximum number of iterations, by default None (unlimited).
    self_learning_factor : float, optional
        Probability that a student (solution) learns by self-learning, by default 0.3.
    interaction_factor : float, optional
        Probability that a student (solution) learns by interacting with the best solution,
        by default 0.7.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness score.
    """
    min_value = array_base.min()
    max_value = array_base.max()

    students_matrix = generate_initial_matrix_population(
        array_base, c, population_size, VALID=True
    )

    # Identify the best solution in the initial population
    best_idx = np.argmin(students_matrix[:, -1])
    best_solution = students_matrix[best_idx, :-1]
    best_fitness = students_matrix[best_idx, -1]

    # Initial variables for stopping criteria
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        for i in range(population_size):
            if i != best_idx:
                new_solution = update_student(
                    students_matrix[i, :-1].copy(),
                    best_solution,
                    self_learning_factor,
                    interaction_factor,
                    min_value,
                    max_value,
                )
                students_matrix[i, :-1] = repair_solution(
                    students_matrix[i, :-1].copy(), new_solution, c
                )

        fitness_values = np.array(
            [fitness(solution[:-1], c) for solution in students_matrix]
        )
        students_matrix[:, -1] = fitness_values
        best_idx = np.argmin(students_matrix[:, -1])
        best_solution = students_matrix[best_idx, :-1]
        best_fitness = students_matrix[best_idx, -1]
        it += 1

    best_idx = np.argmin(students_matrix[:, -1])
    return (
        generate_solution(students_matrix[best_idx, :-1], c, VALID=True)[0],
        students_matrix[best_idx, -1],
    )
