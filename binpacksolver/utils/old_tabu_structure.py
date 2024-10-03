"""
Tabu Structure Module

This module implements the TabuStructure class, which manages a tabu list 
to store a set of forbidden moves or elements. The structure allows for 
efficient insertion and lookup of elements while maintaining a maximum 
capacity. When the maximum size is exceeded, the oldest elements are 
removed to make room for new entries.

Key Features:
- Efficiently checks for the existence of elements in the tabu list.
- Supports the insertion of new elements, ensuring uniqueness.
- Automatically manages the maximum size of the tabu list.
"""

from collections import deque
from typing import Set, Tuple

class TabuStructure:
    """Tabu structure to store a set of forbidden moves, with limited capacity."""

    def __init__(self, n: int):
        """
        Initializes the Tabu structure.

        Parameters
        ----------
        n : int
            Maximum number of elements allowed in the tabu set.
        """
        self.n: int = n
        self.itens: deque = deque()
        self.tabu: Set[Tuple[int, int]] = set()

    def __check(self, element: Tuple[int, int]) -> bool:
        """
        Checks if the given element is in the tabu set.

        Parameters
        ----------
        element : Tuple[int, int]
            Element to be checked.

        Returns
        -------
        bool
            True if the element is in the tabu set, False otherwise.
        """
        return element in self.tabu

    def find(self, element: Tuple[int, int]) -> bool:
        """
        Public method to check if the element is in the tabu set.

        Parameters
        ----------
        element : Tuple[int, int]
            Element to find in the tabu set.

        Returns
        -------
        bool
            True if the element is found, False otherwise.
        """
        return self.__check(element)

    def insert(self, element: Tuple[int, int]) -> bool:
        """
        Inserts a new element into the tabu set. If the element already exists,
        it returns False without modifying the set. If the set exceeds its
        maximum size, the oldest element is removed.

        Parameters
        ----------
        element : Tuple[int, int]
            The element to add to the tabu set.

        Returns
        -------
        bool
            True if the element was successfully inserted, False if it was
            already in the tabu set.
        """
        if self.__check(element):
            return False

        self.tabu.add(element)
        self.itens.append(element)

        if len(self.tabu) > self.n:
            element = self.itens.popleft()
            self.tabu.discard(element)

        return True


