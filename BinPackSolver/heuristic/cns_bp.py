from binpacksolver.utils import first_fit, TabuCNS
import random
import time

class CNSBinPacking:
    def __init__(self, items, capacity):
        self.items = items.copy()
        self.capacity = capacity
        self.lower_bound = self._compute_lower_bound()
        self.solution = []
        

    def _compute_lower_bound(self):
        return (sum(self.items) + self.capacity - 1) // self.capacity

    def _is_solution_complete(self, solution):
        all_packed_items = [item for bin_ in solution for item in bin_]
        return all_packed_items == self.items

    def _pack_items(self, bin_items, unplaced_items, bin_capacity):
        combined_items = bin_items + unplaced_items
        new_bin = []
        remaining_items = []
        used_capacity = 0

        for item in combined_items:
            if used_capacity + item <= bin_capacity:
                new_bin.append(item)
                used_capacity += item
            else:
                remaining_items.append(item)

        return new_bin, remaining_items

    def _descent(self, bins, unplaced_items, time_limit=1):
        start_time = time.time()
        while (time.time() - start_time) < time_limit:
            random.shuffle(bins)
            for i, bin_ in enumerate(bins):
                bins[i], unplaced_items = self._pack_items(bin_, unplaced_items, self.capacity)
                if sum(unplaced_items) <= 2 * self.capacity:
                    new_bin1 = first_fit(unplaced_items, self.capacity)
                    new_bin2 = first_fit(unplaced_items, self.capacity)
                    bins.append(new_bin1)
                    bins.append(new_bin2)
                    return bins
        return bins

    def _cns(self, partial_solution, unplaced_items, time_limit=10, iterations_limit=100):
        iterations = 0
        while iterations < iterations_limit:
            if self._is_solution_complete(partial_solution):
                break
            tabu = TabuCNS(partial_solution, self.capacity, unplaced_items)
            partial_solution = tabu.run()
            partial_solution = self._descent(partial_solution, unplaced_items, time_limit)
            iterations += 1
        return partial_solution

    def solve(self):
        random.shuffle(self.items)
        current_solution = first_fit(self.items, self.capacity)
        num_bins = len(current_solution)

        while num_bins > self.lower_bound:
            num_bins -= 1
            unplaced_items = [item for bin_ in current_solution[num_bins-2:] for item in bin_]
            partial_solution = current_solution[:num_bins-2]
            new_solution = self._cns(partial_solution, unplaced_items)

            if not self._is_solution_complete(new_solution):
                break

            current_solution = new_solution

        self.solution = current_solution
        return self.solution
