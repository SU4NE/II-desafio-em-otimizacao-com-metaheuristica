"""
Solution Generation Module

This module contains functions to generate a solution and evaluate its
fitness based on a given array of values.
"""

import numpy as np
import math
from typing import List, Tuple

def generate_solution(solution: np.ndarray, C: int, **kwargs) -> Tuple[np.ndarray, List]:
    """
    Generates a modified solution array based on the given parameters.

    If the 'FFD', 'BFD', or 'FD' keyword argument is provided and set to True, 
    the function can implement heuristics such as First-Fit Decreasing (FFD), 
    Best-Fit Decreasing (BFD), or First-Fit (FD) to prioritize the best solutions.

    Parameters
    ----------
    solution : np.ndarray
        An array representing the current solution.
    C: int
        Max line value (container capacity).

    Returns
    -------
    np.ndarray
        A new solution array, sorted in descending order.
    List[int]
        A list representing the remaining space in each container.
    """
    if kwargs.get("FFD", False):
        pass
    
    if kwargs.get("BFD", False):
        pass
    
    if kwargs.get("FD", False):
        pass
    
    solution = np.sort(solution)[::-1]
    containers = [C] * len(solution)  
    
    for index, value in enumerate(solution):
        containers[index] -= int(value)
        
    solution = [np.array([elemento], dtype=int) for elemento in solution]
    
    return solution, containers


def fitness(solution: np.ndarray) -> int:
    """
    Calculates the fitness of the given solution.

    The fitness is defined as the length of the solution array.

    Parameters
    ----------
    solution : np.ndarray
        An array representing the current solution.

    Returns
    -------
    int
        The fitness score, defined as the number of elements in the solution.
    """  
    return len(solution)

def theoretical_minimum(solution: np.ndarray, C: int) -> int:
    """
    Calculates the theoretical minimum based on the sum of the solution
    and a given capacity C.

    Parameters
    ----------
    solution : np.ndarray
        An array representing the current solution.
    C : int
        An integer representing the capacity.

    Returns
    -------
    int
        The theoretical minimum, rounded up.
    """    
    return math.ceil(solution.sum() / C)