import copy
import random

from binpacksolver.utils import best_fit_decreasing, first_fit, lower_bound


class GGACGTBinPacking:
    """
    Class implementing the GGA-CGT algorithm for bin packing problems.

    Attributes:
        items (list): List of items to be packed.
        max_gen (int): Maximum number of generations for the algorithm.
        n_pop (int): Number of individuals in the population.
        nc (int): Number of individuals to select for crossover.
        nm (int): Number of individuals for mutation.
        bin_capacity (int): Capacity of each bin.
        delta (float): Factor for adaptive mutation.
    """

    def __init__(self, items, **kwargs):
        """
        Initializes the GGACGTBinPacking instance with items and optional parameters.

        Args:
            items (list): List of items to be packed.
            **kwargs: Optional parameters to set max_gen, n_pop, nc, nm, bin_capacity, and delta.
        """
        self.items = items
        self.max_gen = kwargs.get("max_gen", 1000)
        self.n_pop = kwargs.get("n_pop", 100)
        self.nc = kwargs.get("nc", 30)
        self.nm = kwargs.get("nm", 10)
        self.bin_capacity = kwargs.get("bin_capacity", 10)
        self.delta = kwargs.get("delta", 0.7)

    def initialize_population(self):
        """
        Initializes the population by creating individuals through random shuffling
        and using the first fit algorithm.

        Returns:
            list: A list of individuals representing the initial population.
        """
        population = []
        for _ in range(self.n_pop):
            random.shuffle(self.items)
            individual = first_fit(self.items, self.bin_capacity, [[]])
            population.append(individual)
        return population

    def gene_level_crossover(self, parent1, parent2):
        """
        Performs gene-level crossover between two parent individuals to produce a child individual.

        Args:
            parent1 (list): The first parent individual.
            parent2 (list): The second parent individual.

        Returns:
            list: A new child individual created from the parents.
        """
        child = []
        lixo = []

        def not_find(bin_p, child, lixo):
            for bin_child in child:
                if bool(set(bin_child) & set(bin_p)):
                    lixo.extend(bin_p)
                    return False
            return True

        for x, y in zip(parent1, parent2):
            if sum(x) >= sum(y):
                if not_find(x, child, lixo):
                    child.append(x.copy())
            else:
                if not_find(y, child, lixo):
                    child.append(y.copy())

        child = first_fit(lixo, self.bin_capacity, child)
        return child

    def adaptive_mutation(self, individual):
        """
        Applies adaptive mutation to an individual.

        Args:
            individual (list): The individual to mutate.

        Returns:
            list: The mutated individual.
        """
        lixo = []
        individual = sorted(individual, key=sum, reverse=True)
        num_bins = int(len(individual) * self.delta)
        bins = individual[:num_bins]
        individual = individual[num_bins:]

        for bin_p in bins:
            lixo.extend(bin_p)

        individual = best_fit_decreasing(lixo, self.bin_capacity, individual)
        return individual

    def controlled_selection(self, population: list, limit):
        """
        Selects a controlled number of individuals from the population for crossover.

        Args:
            population (list): The current population of individuals.
            nc (int): The number of individuals to select.

        Returns:
            list: Selected individuals for crossover.
        """
        population = sorted(population, key=len, reverse=True)
        bests = population[: limit // 2]
        wosts = population[limit // 2 :]
        return bests + random.sample(wosts, limit // 2)

    def controlled_replacement(self, population: list, offspring):
        """
        Replaces the current population with offspring, maintaining the best individuals.

        Args:
            population (list): The current population of individuals.
            offspring (list): The offspring individuals to be added.

        Returns:
            list: The new population after replacement.
        """
        population = population + offspring
        population = sorted(population, key=len, reverse=True)
        return population[: self.n_pop]

    def update_best_solution(self, population):
        """
        Updates the best solution found in the current population.

        Args:
            population (list): The current population of individuals.

        Returns:
            list: The best solution found.
        """
        population = sorted(population, key=len, reverse=True)
        return population[0]

    def gga_cgt_bin_packing(self):
        """
        Executes the GGA-CGT algorithm for bin packing.

        Returns:
            list: The best solution found after the algorithm execution.
        """
        population = self.initialize_population()
        best_solution = self.update_best_solution(population)
        lb = lower_bound(self.items, self.bin_capacity)

        generation = 0
        while generation < self.max_gen and lb == best_solution:
            selected_individuals = self.controlled_selection(population, self.nc)

            offspring = []
            for i in range(0, len(selected_individuals), 2):
                child1 = self.gene_level_crossover(
                    selected_individuals[i], selected_individuals[i + 1]
                )
                offspring.append(child1)
                child2 = self.gene_level_crossover(
                    selected_individuals[i + 1], selected_individuals[i]
                )
                offspring.append(child2)

            population = self.controlled_replacement(population, offspring)

            elite_individuals = self.controlled_selection(population, self.nm)
            cloned_individuals = [copy.deepcopy(ind) for ind in elite_individuals]

            cloned_individuals = [
                self.adaptive_mutation(ind) for ind in cloned_individuals
            ]

            population = self.controlled_replacement(population, cloned_individuals)

            best_solution = self.update_best_solution(population)
            generation += 1

        return best_solution
