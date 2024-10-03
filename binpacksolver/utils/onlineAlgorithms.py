import numpy as np


def first_fit(items: np.ndarray, capacity: int) -> np.ndarray:
    """
    Implements the First-Fit algorithm for the Bin Packing problem.

    Parameters:
    items (np.ndarray): An array of item sizes to be placed in bins.
    capacity (int): The maximum capacity of each bin.

    Returns:
    np.ndarray: An array representing the remaining space in each bin used.
    """
    bins = []

    for item in items:
        placed = False

        for i in range(len(bins)):
            if bins[i] >= item:
                bins[i] -= item
                placed = True
                break

        if not placed:
            bins.append(capacity - item)

    return np.array(bins)


def first_fit_decreasing(items: np.ndarray, capacity: int) -> np.ndarray:
    """
    Implements the First-Fit Decreasing algorithm for the Bin Packing.

    Parameters:
    items (np.ndarray): An array of item sizes to be placed in bins.
    capacity (int): The maximum capacity of each bin.

    Returns:
    np.ndarray: An array representing the remaining space in each bin used.
    """
    sorted_items = np.sort(items, reverse=True)

    bins = []

    for item in sorted_items:
        placed = False

        for i in range(len(bins)):
            if bins[i] >= item:
                bins[i] -= item
                placed = True
                break

        if not placed:
            bins.append(capacity - item)

    return np.array(bins)


def best_fit_decreasing(items: np.ndarray, capacity: int) -> np.ndarray:
    """
    Implements the Best-Fit Decreasing algorithm for the Bin Packing.

    Parameters:
    items (np.ndarray): An array of item sizes to be placed in bins.
    capacity (int): The maximum capacity of each bin.

    Returns:
    np.ndarray: An array representing the remaining space in each bin used.
    """
    sorted_items = np.sort(items, reverse=True)

    bins = []

    for item in sorted_items:
        best_fit_index = -1
        min_space_left = capacity + 1

        for i in range(len(bins)):
            space_left = bins[i]
            if item <= space_left and (space_left - item) < min_space_left:
                best_fit_index = i
                min_space_left = space_left - item

        if best_fit_index != -1:
            bins[best_fit_index] -= item
        else:
            bins.append(capacity - item)

    return np.array(bins)