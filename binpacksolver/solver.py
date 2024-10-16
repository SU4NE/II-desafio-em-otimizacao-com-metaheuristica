"""
This module provides a Solver class for solving the Bin Packing Problem
using multiple heuristic algorithms.

The Solver class allows for the execution of several heuristic optimization
techniques, either sequentially or in parallel, to find an optimal or
near-optimal solution for packing itemsinto containers with a given capacity.
"""

import concurrent.futures
import time
from typing import Callable, List, Tuple

import numpy as np
from tabulate import tabulate
from tqdm import tqdm

from binpacksolver.heuristic import (artificial_bee_colony,
                                     gravitational_search_algorithm,
                                     improved_whale_optimization_algorithm,
                                     jaya_optimization,
                                     particle_swarm_optimization,
                                     student_psychology_based_optimization)
from binpacksolver.utils import theoretical_minimum


class Solver:
    """
    A solver for the Bin Packing Problem using multiple heuristic algorithms.

    This class implements a Bin Packing Problem solver that employs several
    heuristic optimization techniques to find an optimal or near-optimal
    solution for packing items into containers with a given capacity. The solver
    can be configured to run sequentially or in parallel, depending on
    the `max_workers` parameter, and supports a variety of heuristic algorithms.

    Parameters
    ----------
    capacity : int
        The capacity of each container.
    weights : List[int]
        A list of item weights to be packed into containers.
    num_weights : int, optional
        Number of items to pack. Default is the length of `weights`.
    priority_func : List[Callable], optional
        List of heuristic functions to use. Default includes multiple heuristics
        from binpacksolver.
    max_workers : int, optional
        The number of parallel threads to run the heuristics.
        If set to 1 (default), the solver will run sequentially. If more than 1,
        it will run multiple heuristics concurrently.
    time_max : float, optional
        Maximum total time allowed for the solver in seconds. Default is 60 seconds.
    verbose : int, optional
        Controls the level of verbosity.
        - 0: No output.
        - 1: Basic output showing heuristic execution.
        - 2: Detailed information for each heuristic.
        - 3: Full details including time allocation and execution time.

    Attributes
    ----------
    capacity : int
        The capacity of each container.
    weights : np.ndarray
        A numpy array of item weights.
    num_weights : int
        Number of items to pack.
    priority_func : List[Callable]
        List of heuristic functions to use.
    max_workers : int
        Number of parallel threads for heuristics execution.
    time_max : float
        Maximum time allowed for the solver.
    verbose : int
        Verbosity level of the solver.
    time_allocation : List[float]
        A list of time allocations for each heuristic based on `time_max`.
    """

    def __init__(self, capacity, weights, **kwargs):
        """Initializes the Solver for the Bin Packing Problem.

        Parameters
        ----------
        capacity : int
            The capacity of each container.
        weights : List[int]
            A list of item weights to be packed into containers.
        num_weights : int, optional
            Number of items to pack. Default is the length of `weights`.
        priority_func : List[Callable], optional
            List of heuristic functions to use. Default includes multiple
            heuristics from binpacksolver.
        max_workers : int, optional
            Number of parallel threads to run the heuristics.
            If set to 1, the solver will run sequentially. Higher values enable
            parallel execution, which can reduce total run time.
        time_max : float, optional
            Maximum time allowed for the solver in seconds. Default is 60 seconds.
        verbose : int, optional
            Level of output verbosity. Ranges from 0 (no output) to 3 (full details).
        """
        self.capacity = capacity
        self.weights = weights
        self.num_weights = kwargs.get("num_weights", len(self.weights))

        if isinstance(self.weights, list):
            self.weights = np.array(self.weights, dtype=int)

        self.priority_func = [
            particle_swarm_optimization,
            gravitational_search_algorithm,
            improved_whale_optimization_algorithm,
            jaya_optimization,
            artificial_bee_colony,
            student_psychology_based_optimization,
        ]

        self.priority_func = kwargs.get("priority_func", self.priority_func)
        self.max_workers = kwargs.get("max_workers", 1)
        self.time_max = kwargs.get("time_max", 60)
        self.verbose = kwargs.get("verbose", 0)
        self.disable_allocation = kwargs.get("disable_allocation", False)

        if not self.disable_allocation:
            self.time_allocation = self.__allocate_time()

    def __allocate_time(self) -> List[float]:
        """Allocates time to each heuristic based on the total available time.

        Returns
        -------
        List[float]
            A list of time allocations for each heuristic.
        """
        num_heuristics = len(self.priority_func)

        if self.max_workers > 1:
            equal_time = self.time_max * 0.7 / self.max_workers
            remaining_time = self.time_max * 0.3
            time_allocations = [equal_time] * self.max_workers

            total_weight = sum(range(1, num_heuristics - self.max_workers + 1))
            for i in range(num_heuristics - self.max_workers):
                time_allocations.append((i + 1) / total_weight * remaining_time)
        else:
            total_weight = sum(range(1, num_heuristics + 1))
            time_allocations = [
                (i + 1) / total_weight * self.time_max for i in range(num_heuristics)
            ][::-1]

        if self.verbose >= 3:
            print(f"Time allocation per heuristic: {time_allocations}")

        return time_allocations

    def __print_information(
        self, heuristic_name: str, best_solution: int, real_time: float
    ):
        """Prints detailed information about the heuristic run if verbose level is 2.

        Parameters
        ----------
        heuristic_name : str
            The name of the heuristic used.
        best_solution : int
            Best solution found by the heuristic.
        real_time : float
            Time taken to execute the heuristic.
        """
        if self.verbose >= 2:
            table_data = [
                ["Number of Weights", self.num_weights],
                ["Container Capacity", self.capacity],
                ["Best Solution", best_solution],
                [
                    "Min Theoretical Solution",
                    theoretical_minimum(self.weights, self.capacity),
                ],
                ["Execution Time (s)", f"{real_time:.4f}"],
            ]

            print(f"=== Heuristic: {heuristic_name} ===")
            print(
                tabulate(
                    table_data, headers=["Description", "Value"], tablefmt="fancy_grid"
                )
            )
            print("\n" + "=" * 50 + "\n")

    def run_heuristic(
        self,
        heuristic_func: Callable,
        weights: np.ndarray,
        capacity: int,
        time_max: float,
    ) -> Tuple[List[np.ndarray], int, float]:
        """Executes a single heuristic on the bin packing problem.

        Parameters
        ----------
        heuristic_func : Callable
            The heuristic function to execute.
        weights : np.ndarray
            The array of item weights.
        capacity : int
            The capacity of the containers.
        time_max : float
            Maximum time to allocate for this heuristic.

        Returns
        -------
        Tuple[List[np.ndarray], int, float]
            The solution, the best fit (minimum containers used), and the execution time.
        """
        start_time = time.perf_counter()
        best_solution, best_fit = heuristic_func(weights, capacity, time_max=time_max)
        execution_time = time.perf_counter() - start_time
        return best_solution, best_fit, execution_time

    def run(self) -> Tuple[List[np.ndarray], int]:
        """Runs all configured heuristics to solve the bin packing problem.

        Depending on the `max_workers` parameter, the heuristics will be run either sequentially
        or in parallel. The function will return the best solution found by any heuristic.

        Returns
        -------
        Tuple[List[np.ndarray], int]
            The best solution found and its corresponding fit (minimum containers used).
        """
        remaining_time = self.time_max
        best_solution = None
        best_fit = None
        solution_train = self.weights.copy()
        start_time = time.perf_counter()
        total_allocated_time = sum(self.time_allocation)

        if self.disable_allocation:
            heuristic_name = self.priority_func[0].__name__.replace("_", " ").title()
            if self.verbose >= 1:
                print(
                    f"Starting heuristic: {heuristic_name}"
                    + "with the entire time_max: {self.time_max:.4f}s"
                )

            solution, fit, execution_time = self.run_heuristic(
                self.priority_func[0], self.weights, self.capacity, self.time_max
            )
            self.__print_information(heuristic_name, fit, execution_time)

            if self.verbose >= 1:
                print(f"Best solution fit: {fit}")

            if self.verbose >= 2:
                print(f"Best solution {solution}")

            return solution, fit

        with tqdm(total=total_allocated_time, desc="Running Heuristics") as pbar:
            if self.max_workers == 1:
                for i, heuristic in enumerate(self.priority_func):
                    if remaining_time <= 0:
                        break

                    heuristic_name = heuristic.__name__.replace("_", " ").title()
                    allocated_time = self.time_allocation[i]

                    if self.verbose >= 1:
                        print(
                            f"Starting heuristic: {heuristic_name}"+ 
                            "(Allocated Time: {allocated_time:.4f}s)"
                        )

                    solution, fit, execution_time = self.run_heuristic(
                        heuristic, solution_train, self.capacity, allocated_time
                    )
                    if not best_fit or fit <= best_fit:
                        solution_train = np.concatenate(solution)
                        best_solution = solution
                        best_fit = fit
                    remaining_time -= execution_time
                    self.__print_information(heuristic_name, fit, execution_time)
                    pbar.update(allocated_time)

            else:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=self.max_workers
                ) as executor:
                    i = 0
                    while remaining_time > 0 and i < len(self.priority_func):
                        futures = []
                        future_to_heuristic = {}
                        heuristics_to_run = self.priority_func[i : i + self.max_workers]

                        for j, heuristic in enumerate(heuristics_to_run):
                            allocated_time = self.time_allocation[i + j]
                            future = executor.submit(
                                self.run_heuristic,
                                heuristic,
                                solution_train,
                                self.capacity,
                                allocated_time,
                            )
                            futures.append(future)
                            future_to_heuristic[future] = heuristic

                        for future in concurrent.futures.as_completed(futures):
                            solution, fit, execution_time = future.result()
                            if not best_fit or fit <= best_fit:
                                solution_train = np.concatenate(solution)
                                best_solution = solution
                                best_fit = fit
                            remaining_time -= execution_time

                            heuristic_func = future_to_heuristic[future].__name__
                            heuristic_name = heuristic_func.replace("_", " ").title()

                            if self.verbose >= 1:
                                print(f"Completed heuristic: {heuristic_name}")

                            self.__print_information(
                                heuristic_name, fit, execution_time
                            )
                            pbar.update(execution_time)

                        i += self.max_workers

        total_time = time.perf_counter() - start_time
        if self.verbose >= 1:
            print(f"Best solution fit: {best_fit}")

        if self.verbose >= 2:
            print(f"Best solution {best_solution}")

        if self.verbose >= 3:
            print(f"Total execution time: {total_time:.4f} seconds")

        return best_solution, best_fit
