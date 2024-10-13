import math
import time

import numpy as np


class TabuCNS:
    """
    Implements a Tabu Search algorithm to solve the bin packing problem using a
    customized neighborhood search (CNS) strategy.

    Parameters
    ----------
    init_solution : list of np.ndarray
        The initial solution where items are packed into bins.
    capacity : int
        The capacity of each bin.
    unplaced_items : np.ndarray
        Items that remain unpacked and need to be placed into bins.
    max_iteration : int, optional
        The maximum number of iterations for the Tabu Search algorithm (default is 100).
    time_limit : float, optional
        The maximum time (in seconds) allowed for the algorithm to run (default is 1 second).

    Attributes
    ----------
    best_solution : list of np.ndarray
        The best solution found by the algorithm.
    current_solution : list of np.ndarray
        The current solution during the search process.
    capacity : int
        The capacity of each bin.
    unplaced_items : np.ndarray
        The items that have not yet been placed into bins.
    time_limit : float
        The time limit for the search process.
    tabu_list : dict
        A dictionary representing the tabu list that keeps track of forbidden moves.
    max_iteration : int
        The maximum number of iterations for the search process.
    """

    # pylint: disable=R0913
    def __init__(
        self, init_solution, capacity, unplaced_items, max_iteration=100, time_limit=1
    ):
        self.best_solution = init_solution
        self.current_solution = init_solution
        self.capacity = capacity
        self.unplaced_items = np.array(unplaced_items)
        self.time_limit = time_limit
        self.tabu_list = {}
        self.max_iteration = max_iteration

    # pylint: disable=R1702
    def run(self):
        """
        Executes the Tabu Search algorithm to find an optimized bin packing solution.

        Returns
        -------
        list of np.ndarray
            The best solution found where items are packed into bins.
        """
        iteration = 0
        start_time = time.time()

        while (
            iteration < self.max_iteration
            and (time.time() - start_time) < self.time_limit
        ):
            best_move = None
            best_move_value = -math.inf

            for bin_ in self.current_solution:
                for item_set_s in bin_:
                    if not self.is_tabu(item_set_s, bin_):
                        for item_set_t in self.unplaced_items:
                            feasible_move, move_value = self.feasible(
                                item_set_s, item_set_t, bin_
                            )
                            if feasible_move and move_value > best_move_value:
                                best_move = (item_set_s, item_set_t, bin_)
                                best_move_value = move_value

            if best_move is None:
                break

            for idx, bin_ in enumerate(self.current_solution):
                if best_move[0] in bin_:
                    item_index = np.where(bin_ == best_move[0])[0][0]
                    bin_ = np.delete(bin_, item_index)
                    bin_ = np.append(bin_, best_move[1])
                    self.current_solution[idx] = bin_
                    break

            lixo_index = np.where(self.unplaced_items == best_move[1])[0][0]
            self.unplaced_items = np.delete(self.unplaced_items, lixo_index)
            self.unplaced_items = np.append(self.unplaced_items, best_move[0])

            if self.evaluate(self.current_solution) < self.evaluate(self.best_solution):
                self.best_solution = [bin_.copy() for bin_ in self.current_solution]
                self.tabu_list.clear()
            else:
                self.update_tabu(best_move)

            self.update_tabu_list()
            iteration += 1

        return self.best_solution

    def is_tabu(self, item_set_s, bin_):
        """
        Checks if a move is tabu.

        Parameters
        ----------
        item_set_s : int
            The item that is being considered for a move.
        bin_ : np.ndarray
            The bin where the item is currently placed.

        Returns
        -------
        bool
            True if the move is tabu, False otherwise.
        """
        return (item_set_s, tuple(bin_)) in self.tabu_list

    def update_tabu(self, move):
        """
        Updates the tabu list by adding the current move with a tenure based on the move frequency.

        Parameters
        ----------
        move : tuple
            The move to be added to the tabu list. It is a tuple containing the item being moved
            and the bin it is moved from.
        """
        move_key = (move[0], tuple(move[2]))
        if move_key in self.tabu_list:
            self.tabu_list[move_key]["frequency"] += 1
        else:
            self.tabu_list[move_key] = {"frequency": 1, "tenure": 0}
        self.tabu_list[move_key]["tenure"] = self.tabu_list[move_key]["frequency"] // 2

    def update_tabu_list(self):
        """
        Updates the tenure of moves in the tabu list.
        Moves with zero or negative tenure are removed.
        """
        for move in list(self.tabu_list.keys()):
            self.tabu_list[move]["tenure"] -= 1
            if self.tabu_list[move]["tenure"] <= 0:
                del self.tabu_list[move]

    def feasible(self, item_set_s, item_set_t, bin_):
        """
        Checks if swapping two items between bins is feasible, meaning the total weight
        of the bin after the move does not exceed the bin's capacity.

        Parameters
        ----------
        item_set_s : int
            The item currently in the bin.
        item_set_t : int
            The item from the unplaced items being considered for swapping.
        bin_ : np.ndarray
            The bin where the swap is being considered.

        Returns
        -------
        tuple
            A tuple containing a boolean indicating whether the move is feasible
            and the change in bin weight resulting from the move.
        """
        current_bin_weight = sum(bin_)
        new_bin_weight = current_bin_weight - item_set_s + item_set_t
        move_value = new_bin_weight - current_bin_weight
        return new_bin_weight <= self.capacity, move_value

    def evaluate(self, solution):
        """
        Evaluates the quality of the current solution by calculating the total weight
        of all bins in the solution.

        Parameters
        ----------
        solution : list of np.ndarray
            The current solution being evaluated.

        Returns
        -------
        int
            The total weight of all bins in the current solution.
        """
        return sum(sum(bin_) for bin_ in solution)
