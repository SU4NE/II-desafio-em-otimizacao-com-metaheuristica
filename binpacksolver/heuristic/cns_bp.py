import random
import time

import numpy as np

from binpacksolver.utils import TabuCNS, best_fit_decreasing


class CNSBinPacking:
    """
    Solves the bin packing problem using a combination of
    Best Fit Decreasing, Tabu Search, and Customized Neighborhood Search (CNS).

    Parameters
    ----------
    items : list or np.ndarray
        List of item sizes to be packed.
    capacity : int
        Capacity of each bin.

    Attributes
    ----------
    items : np.ndarray
        Array of item sizes to be packed.
    capacity : int
        Capacity of each bin.
    lower_bound : int
        The theoretical minimum number of bins required.
    solution : list
        The final solution, which contains a list of bins with packed items.
    """

    def __init__(self, items, capacity):
        """
        Initializes the bin packing solver with the given items and bin capacity.

        Parameters
        ----------
        items : list or np.ndarray
            List of item sizes to be packed.
        capacity : int
            Capacity of each bin.
        """
        self.items = np.array(items.copy())
        self.capacity = capacity
        self.lower_bound = self._compute_lower_bound()
        self.solution = []

    def _compute_lower_bound(self):
        """
        Computes the theoretical lower bound on the minimum number of bins.

        Returns
        -------
        int
            The calculated lower bound on the number of bins required.
        """
        return (sum(self.items) + self.capacity - 1) // self.capacity

    def _is_solution_complete(self, solution):
        """
        Checks if the solution contains all the items without missing any.

        Parameters
        ----------
        solution : list of np.ndarray
            List of bins where each bin contains a subset of packed items.

        Returns
        -------
        bool
            True if the solution contains all items; otherwise, False.
        """
        all_packed_items = np.concatenate(solution)
        return np.array_equal(np.sort(all_packed_items), np.sort(self.items))

    def _pack_items(self, bin_items, unplaced_items, bin_capacity):
        """
        Packs items into a bin without exceeding its capacity.

        Parameters
        ----------
        bin_items : np.ndarray
            Items already placed in the bin.
        unplaced_items : np.ndarray
            Items that have not been packed yet.
        bin_capacity : int
            Capacity of the bin.

        Returns
        -------
        tuple
            A tuple containing the updated bin and the remaining unplaced items.
        """
        combined_items = np.concatenate((bin_items, unplaced_items))
        new_bin = []
        remaining_items = []
        used_capacity = 0

        for item in combined_items:
            if used_capacity + item <= bin_capacity:
                new_bin.append(item)
                used_capacity += item
            else:
                remaining_items.append(item)

        return np.array(new_bin), np.array(remaining_items)

    def descent(self, bins, unplaced_items, time_limit=1):
        """
        Performs a descent-based search to optimize the current bin packing solution.

        Parameters
        ----------
        bins : list of np.ndarray
            Current set of bins with packed items.
        unplaced_items : np.ndarray
            Items that remain unpacked.
        time_limit : float, optional
            Maximum time allowed for the descent operation (default is 1 second).

        Returns
        -------
        list of np.ndarray
            The updated list of bins after attempting to improve the solution.
        """
        start_time = time.time()
        while (time.time() - start_time) < time_limit:
            random.shuffle(bins)
            for i, bin_ in enumerate(bins):
                bins[i], unplaced_items = self._pack_items(
                    bin_, unplaced_items, self.capacity
                )
                if sum(unplaced_items) <= 2 * self.capacity:
                    new_bins = best_fit_decreasing(unplaced_items, self.capacity, [])
                    bins.extend(new_bins)
                    return bins
        return bins

    def _cns(
        self, partial_solution, unplaced_items, time_limit=10, iterations_limit=100
    ):
        """
        Customized Neighborhood Search (CNS) method for improving the solution by
        iteratively repacking items.

        Parameters
        ----------
        partial_solution : list of np.ndarray
            A partial solution where some items are already packed into bins.
        unplaced_items : np.ndarray
            Items that have not yet been placed in any bin.
        time_limit : float, optional
            Maximum time allowed for each descent operation (default is 10 seconds).
        iterations_limit : int, optional
            Maximum number of iterations to perform (default is 100).

        Returns
        -------
        list of np.ndarray
            The improved solution after applying CNS.
        """
        iterations = 0
        while iterations < iterations_limit:
            if self._is_solution_complete(partial_solution):
                break
            tabu = TabuCNS(partial_solution, self.capacity, unplaced_items)
            partial_solution = tabu.run()
            partial_solution = self.descent(
                partial_solution, unplaced_items, time_limit
            )
            iterations += 1
        return partial_solution

    def solve(self):
        """
        Solves the bin packing problem using a combination of CNS and
        Best Fit Decreasing heuristics.

        Returns
        -------
        list of np.ndarray
            The final solution where items are packed into bins.
        """
        random.shuffle(self.items)
        current_solution = best_fit_decreasing(self.items, self.capacity, [])
        num_bins = len(current_solution)

        while num_bins > self.lower_bound:
            num_bins -= 1
            unplaced_items = np.concatenate(current_solution[num_bins:])
            partial_solution = current_solution[:num_bins]
            new_solution = self._cns(partial_solution, unplaced_items)

            if not self._is_solution_complete(new_solution):
                break

            current_solution = new_solution

        self.solution = current_solution
        return self.solution
