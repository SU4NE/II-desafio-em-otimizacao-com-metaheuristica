"""
Module for implementing the Student Psychology Based Optimization (SPBO) algorithm 
for the Bin Packing Problem (BPP). The algorithm simulates the learning process of students, 
where each student (solution) improves based on self-learning and interaction with the best-performing 
students in the population.
"""
import time
import random
from typing import List, Tuple
import numpy as np
from binpacksolver.utils import (repair_solution,
                                 check_end, fitness,
                                 generate_initial_population,
                                 generate_solution, theoretical_minimum)

# Algoritmo Student Psychology Based Optimization para BPP
def update_student(solution, best_solution, self_learning_factor, interaction_factor, min_value, max_value):
    for i in range(len(solution)):
        # Self-learning
        if random.random() < self_learning_factor:
            solution[i] = solution[i] + random.uniform(-1, 1) * solution[i]
        # Learning through interaction with the best student
        if random.random() < interaction_factor:
            solution[i] = best_solution[i] + random.uniform(-1, 1) * best_solution[i]
            
    return np.clip(solution, min_value, max_value)

def student_psychology_based_optimization(array_base: np.ndarray, c: int, population_size=7, time_max: float = 60, max_it=None, self_learning_factor=0.3, interaction_factor=0.7) -> Tuple[List[np.ndarray], int]:
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
        Probability that a student (solution) learns by interacting with the best solution, by default 0.7.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The best solution found and its fitness score.
    """
    min_value = array_base.min()
    max_value = array_base.max()

    pop_bins, _ = generate_initial_population(
        array_base, c, population_size, juice=False, VALID=True
    )

    # Flatten the population and combine with fitness values
    fitness_values = np.array([fitness(lst) for lst in pop_bins])
    pop_bins_flat = np.vstack([np.concatenate(lst) for lst in pop_bins]).astype(int)
    pop_matrix = np.hstack((pop_bins_flat, fitness_values[:, np.newaxis])).astype(int)
    
    # Identify the best solution in the initial population
    best_idx = np.argmin(pop_matrix[:, -1])
    best_solution = pop_matrix[best_idx, :-1]
    best_fitness = pop_matrix[best_idx, -1]

    # Initial variables for stopping criteria
    th = theoretical_minimum(array_base, c)
    it = 0
    start = time.time()

    while check_end(th, best_fitness, time_max, start, time.time(), max_it, it):
        for i in range(population_size):
            if i != best_idx:
                new_solution = update_student(pop_matrix[i, :-1].copy(), best_solution, self_learning_factor, interaction_factor, min_value, max_value)
                pop_matrix[i, :-1] = repair_solution(pop_matrix[i, :-1].copy(), new_solution, c)
                
        fitness_values = np.array([fitness(solution[:-1], c) for solution in pop_matrix])
        pop_matrix[:, -1] = fitness_values
        best_idx = np.argmin(pop_matrix[:, -1])
        best_solution = pop_matrix[best_idx, :-1]
        best_fitness = pop_matrix[best_idx, -1]
        it += 1
    
    best_idx = np.argmin(pop_matrix[:, -1])
    return (
        generate_solution(pop_matrix[best_idx, :-1], c, VALID=True)[0],
        pop_matrix[best_idx, -1],
    )