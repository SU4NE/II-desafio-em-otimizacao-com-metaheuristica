from collections import deque
from typing import Dict, List, Tuple
import numpy as np
import random


class TabuStructure:
    def __init__(self, N: int, M: int, R: int):
        """Initialize the Tabu Structure.

        Parameters
        ----------
        N : int
            The maximum size of the tabu list.
        M : int
            The maximum size of the elements associated with a single key in the tabu list.
        R : int
            The range used for segmenting the solution.
        """
        self.N: int = N
        self.M: int = min(N, M)
        self.R: int = R
        self.itens: deque = deque()
        self.tabu: Dict[int, List[List]] = {}

    def __segment_info(
        self, index: int, solution: np.ndarray
    ) -> Tuple[int, np.ndarray]:
        """Extract the element and its subarray from the solution.

        Parameters
        ----------
        index : int
            The index of the element in the solution array.
        solution : np.ndarray
            The array representing the current solution.

        Returns
        -------
        Tuple[int, List]
            A tuple containing the element and its corresponding subarray.
        """
        element: int = solution[index]
        solution = list(solution)
        subarray: List = solution[index + 1 : max(len(solution), index + self.R + 1)]
        return element, subarray

    def __check(self, element: int, subarray: List) -> bool:
        """Check if the element and its subarray are in the tabu list.

        Parameters
        ----------
        element : int
            The element to check in the tabu list.
        subarray : List
            The subarray associated with the element.

        Returns
        -------
        bool
            True if the element and subarray are in the tabu list, False otherwise.
        """
        return element in self.tabu and subarray in self.tabu[element]

    def find(self, index: int, solution: np.ndarray) -> bool:
        """Check if an element is in the tabu list along with its subarray.

        Parameters
        ----------
        index : int
            The index of the element in the solution array to check.
        solution : np.ndarray
            The array representing the current solution.

        Returns
        -------
        bool
            True if the element is in the tabu list and the subarray exists,
            False otherwise.
        """
        element, subarray = self.__segment_info(index, solution)
        return self.__check(element, subarray)

    def insert(self, index: int, solution: np.ndarray):
        """Insert an element and its subarray into the tabu list.

        Parameters
        ----------
        index : int
            The index of the element in the solution array to insert.
        solution : np.ndarray
            The array representing the current solution.
        """
        element, subarray = self.__segment_info(index, solution)

        if self.__check(element, subarray):
            if len(self.tabu[element]) > self.M:
                random_item = random.choice(self.tabu[element])
                self.tabu[element].remove(random_item)
            return

        if not element in self.tabu:
            self.tabu[element] = []

        self.tabu[element].append(subarray)
        self.itens.append(element)
        if len(self.tabu) > self.N:
            element = self.itens.popleft()
            if element in self.tabu:
                self.tabu.pop(element)
