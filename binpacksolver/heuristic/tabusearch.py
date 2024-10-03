import numpy as np
import time
from binpacksolver.utils import TabuStructure, fitness, generate_solution


def __operations(C: int, best_fit: int, solution: np.ndarray, tabu: TabuStructure):
    a, b = np.random.choice(len(solution), size=2, replace=False)

    while a == b:
        a, b = np.random.choice(len(solution), size=2, replace=False)

    if tabu.find(a, solution) and tabu.find(b, solution):
        new_solution = solution.copy()
        new_solution[a], new_solution[b] = new_solution[b], new_solution[a]
        new_fit = fitness(solution, C)

        if new_fit < best_fit:
            best_fit = new_fit
            tabu.insert(a, solution)
            tabu.insert(b, solution)
            solution = new_solution

    return best_fit, solution


def tabu_search(
    array_base: np.ndarray,
    C: int,
    time_max: float = 2,
    it_max: int = None,
    tabu: TabuStructure = TabuStructure(3, 5, 2),
    gen_solution: bool = False,
):
    solution: np.ndarray = array_base.copy()
    it: int = 0
    if gen_solution:
        solution = generate_solution(len(array_base), C)
    best_fit: int = fitness(solution, C)
    start_time: float = time.time()
    while (time_max and time.time() - start_time < time_max) or (it and it < it_max):
        best_fit, solution = __operations(C, best_fit, solution, tabu)

    return best_fit, solution
