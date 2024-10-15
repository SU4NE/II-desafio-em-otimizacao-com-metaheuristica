"""
Module for implementing Consistent Neighborhood Search (CNS)
and Tabu Search algorithms for bin packing optimization problems.
"""

import random
import time
from typing import List, Tuple

import numpy as np

from binpacksolver.utils import (TabuStructure, check_end, generate_container,
                                 generate_solution, merge_np,
                                 theoretical_minimum, valid_solution)


def __pack_items(
    bin_items: np.ndarray, unplaced_items: List[np.ndarray], c
) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Packs items into a bin without exceeding its capacity.

    Parameters
    ----------
    bin_items : np.ndarray
        Items already placed in the bin.
    unplaced_items : np.ndarray
        Items that have not been packed yet.
    c : int
        Capacity of the bin.

    Returns
    -------
    Tuple[np.ndarray, List[np.ndarray]]
        A tuple containing the updated bin and the remaining unplaced items.
    """
    combined_items = merge_np(np.concatenate(unplaced_items), bin_items)
    remaining_items = valid_solution(combined_items, c)
    return remaining_items[-1], remaining_items[:-1] if len(remaining_items) > 1 else []


def __descent(
    bins: List[np.ndarray],
    unplaced_items: List[np.ndarray],
    c: int,
    max_attempts: int = 10000,
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Performs a descent-based search to optimize the current bin packing solution.

    Parameters
    ----------
    bins : List[np.ndarray]
        Current set of bins with packed items.
    unplaced_items : List[np.ndarray]
        Items that remain unpacked.
    c : int
        Bin capacity.
    max_attempts : int, optional
        Maximum number of descent attempts, by default 10000.

    Returns
    -------
    Tuple[List[np.ndarray], List[np.ndarray]]
        The updated bins and the list of unplaced items.
    """
    it = 0
    while it < max_attempts:
        it += 1
        random.shuffle(bins)
        for i, bin_ in enumerate(bins):
            bins[i], unplaced_items = __pack_items(bin_, unplaced_items, c)
            if len(unplaced_items) < 3:
                if len(unplaced_items) > 1:
                    unplaced_items, _ = generate_solution(
                        np.concatenate(unplaced_items), c, FF=True
                    )
                bins.extend(unplaced_items)
                return bins, []
    return bins, unplaced_items


def __initialize_containers(
    current_solution: List[np.ndarray], solution: List[np.ndarray], c: int
) -> Tuple[int, int, List[int], int]:
    """
    Initialize container values and sums for bin packing.

    Parameters
    ----------
    current_solution : List[np.ndarray]
        The current solution of bins with placed items.
    solution : List[np.ndarray]
        The list of items placed into bins.
    c : int
        Bin capacity.

    Returns
    -------
    Tuple[int, int, List[int], int]
        n: Number of filled bins,
        m: Total number of bins (including unplaced items),
        containers: List of bin capacities,
        sum_container: Sum of capacities used by unplaced items.
    """
    n = len(current_solution)
    m = len(solution)
    containers = generate_container(solution, c)
    sum_container = sum(containers[n:])
    return n, m, containers, sum_container


def __find_best_move(
    solution: List[np.ndarray],
    containers: List[int],
    tabu: TabuStructure,
    n: int,
    m: int,
) -> Tuple[None, Tuple[Tuple[int, int], Tuple[int, int]], Tuple[int, int]]:
    """
    Find the best move that is not tabu and respects bin constraints.

    Parameters
    ----------
    solution : List[np.ndarray]
        The current solution of bins with items.
    containers : List[int]
        List of capacities left in each bin.
    tabu : TabuStructure
        The tabu list to prevent cycling back to previous states.
    n : int
        Number of filled bins.
    m : int
        Total number of bins (including unplaced items).

    Returns
    -------
    Tuple[None, Tuple[Tuple[int, int], Tuple[int, int]], Tuple[int, int]]
        The best move and corresponding indices for the swap operation.
    """
    best_move = None
    indexes_chage = ((0, 0), (0, 0))
    indexes_save = (0, 0)

    for a in range(n):
        for i, bin_ in enumerate(solution[a]):
            if not tabu.find((bin_, a)):
                for b in range(n, m):
                    for j, bin_unplaced in enumerate(solution[b]):
                        if containers[a] - bin_unplaced + bin_ >= 0 and (
                            not best_move or bin_unplaced > best_move
                        ):
                            best_move = bin_unplaced
                            indexes_save = (bin_, a)
                            indexes_chage = ((i, a), (j, b))

    return best_move, indexes_chage, indexes_save


def __tabucns(
    current_solution: List[np.ndarray],
    unplaced_items: List[np.ndarray],
    c: int,
    max_attempts: int = 100000,
    max_attempts_time: int = 1,
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Main function to run the Tabu CNS algorithm.

    Parameters
    ----------
    current_solution : List[np.ndarray]
        The current solution of bins with placed items.
    unplaced_items : List[np.ndarray]
        Items that have not yet been placed in bins.
    c : int
        Bin capacity.
    max_attempts : int, optional
        Maximum number of iterations, by default 100000.
    max_attempts_time : int, optional
        Maximum time in seconds for each iteration, by default 1.

    Returns
    -------
    Tuple[List[np.ndarray], List[np.ndarray]]
        The updated solution and remaining unplaced items.
    """
    it = 0
    tabu: TabuStructure = TabuStructure(len(current_solution) // 2)
    solution = current_solution.copy()
    solution.extend(unplaced_items)
    n, m, containers, sum_container = __initialize_containers(
        current_solution, solution, c
    )
    time_start = time.time()
    while check_end(0, 1, max_attempts_time, time_start, time.time(), max_attempts, it):
        it += 1
        best_move, indexes_chage, indexes_save = __find_best_move(
            solution, containers, tabu, n, m
        )

        if not best_move:
            break

        i, a = indexes_chage[0]
        item_a = solution[a][i]
        j, b = indexes_chage[1]
        item_b = solution[b][j]

        if sum_container + item_a - item_b < sum_container:
            sum_container += item_a - item_b
            containers[a] += item_a - item_b
            solution[b][j], solution[a][i] = solution[a][i], solution[b][j]
            tabu = TabuStructure(len(current_solution) // 2)
        else:
            tabu.insert(indexes_save)

    return solution[:n], solution[n:]


def __operations(
    partial_solution: List[np.ndarray],
    unplaced_items: List[np.ndarray],
    c: int,
    current_sum: int,
    partial_sum: int,
    max_attempts: int = 10,
    max_attempts_time: int = 1,
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Perform a series of operations combining Tabu CNS and Descent algorithms.

    Parameters
    ----------
    partial_solution : List[np.ndarray]
        The current partial solution of bins with items.
    unplaced_items : List[np.ndarray]
        Items that have not yet been placed in bins.
    c : int
        Bin capacity.
    current_sum : int
        Sum of the weights of all items.
    partial_sum : int
        Sum of the weights of items in the partial solution.
    max_attempts : int, optional
        Maximum number of attempts, by default 10.
    max_attempts_time : int, optional
        Maximum time in seconds for each operation, by default 1.

    Returns
    -------
    Tuple[List[np.ndarray], List[np.ndarray]]
        Updated solution and remaining unplaced items after applying operations.
    """
    it = 0
    start = time.time()
    while check_end(
        partial_sum,
        current_sum,
        max_attempts_time,
        start,
        time.time(),
        max_attempts,
        it,
    ):
        it += 1
        partial_solution, unplaced_items = __tabucns(
            partial_solution, unplaced_items, c, max_attempts, max_attempts_time
        )
        partial_sum = sum(box.sum() for box in partial_solution)
        partial_solution, unplaced_items = __descent(
            partial_solution, unplaced_items, c, max_attempts=min(max_attempts, 100)
        )
    return partial_solution, unplaced_items


def consistent_neighborhood_search(
    array_base: np.ndarray,
    c: int,
    time_max: float = 60,
    max_it: int = None,
    max_attempts: int = 100000,
    max_attempts_time: int = 1,
) -> Tuple[List[np.ndarray], int]:
    """
    Performs consistent neighborhood search for bin packing optimization.

    Parameters
    ----------
    array_base : np.ndarray
        The array of items to be packed into bins.
    c : int
        Bin capacity.
    time_max : float, optional
        Maximum allowed time for the search, by default 60 seconds.
    max_it : int, optional
        Maximum number of iterations, by default None.
    max_attempts : int, optional
        Maximum number of attempts for each operation, by default 10.
    max_attempts_time : int, optional
        Maximum time in seconds for each operation, by default 1.

    Returns
    -------
    Tuple[List[np.ndarray], int]
        The final solution and the number of bins used.

    Notes
    -----
    If the search is limited only by iterations (`max_it`) or if `max_it` is set too small,
    the solution quality may deteriorate as the algorithm might not have enough time
    to fully explore the neighborhood and improve the solution. It's recommended to
    provide a reasonable iteration limit or use a time-based stopping criterion.
    """
    th = theoretical_minimum(array_base, c)
    it = 0
    current_solution, _ = generate_solution(array_base, c, BFD=True)
    current_sum = array_base.sum()
    num_bins = len(current_solution)
    start = time.time()
    while check_end(
        th, len(current_solution), time_max, start, time.time(), max_it, it
    ):
        it += 1
        num_bins -= 1
        unplaced_items = current_solution[num_bins:]
        partial_solution = current_solution[:num_bins]
        partial_sum = sum(box.sum() for box in partial_solution)
        aux_solution, unplaced_items = __operations(
            partial_solution,
            unplaced_items,
            c,
            current_sum,
            partial_sum,
            max_attempts,
            max_attempts_time,
        )
        if len(unplaced_items) == 0 and len(current_solution) > len(aux_solution):
            current_solution = aux_solution
        else:
            num_bins += 1

    return current_solution, len(current_solution)
