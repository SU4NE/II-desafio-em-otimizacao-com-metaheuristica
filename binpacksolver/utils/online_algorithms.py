"""
Module for implementing various Bin Packing algorithms.
"""

from typing import List

import numpy as np


def first_fit(
    items: np.ndarray, capacity: int, bins: List[np.ndarray]
) -> List[np.ndarray]:
    """
    Implements the First-Fit algorithm for the Bin Packing problem.

    Parameters
    ----------
    items : np.ndarray
        A list of item sizes to be placed in bins.
    capacity : int
        The maximum capacity of each bin.
    bins : list[list[int]]
        A list of existing bins where items will be placed.

    Returns
    -------
    List[np.ndarray]
        A list of bins where each bin is a list of items.
    """
    for item in items:
        current_fill = np.array([np.sum(bin_p) for bin_p in bins])
        available_bins = np.where(current_fill + item <= capacity)[0]

        if available_bins.size > 0:
            bins[available_bins[0]] = np.append(bins[available_bins[0]], item)
        else:
            bins.append(np.array([item]))

    return bins


def first_fit_decreasing(items: np.ndarray, capacity: int) -> List[np.ndarray]:
    """
    Implements the First-Fit Decreasing algorithm for the Bin Packing problem.

    Parameters
    ----------
    items : list[int]
        A list of item sizes to be placed in bins.
    capacity : int
        The maximum capacity of each bin.

    Returns
    -------
    List[np.ndarray]
        A list of bins where each bin is a list of items.
    """
    sorted_items = sorted(items, reverse=True)
    return first_fit(sorted_items, capacity, [[]])


def best_fit_decreasing(
    items: np.ndarray, capacity: int, bins: List[np.ndarray]
) -> List[np.ndarray]:
    """
    Implements the Best-Fit Decreasing algorithm for the Bin Packing problem.

    Parameters
    ----------
    items : list[int]
        A list of item sizes to be placed in bins.
    capacity : int
        The maximum capacity of each bin.
    bins : list[list[int]]
        A list of existing bins where items will be placed.

    Returns
    -------
    List[np.ndarray]
        A list of bins where each bin is a list of items.
    """
    sorted_items = np.sort(items)[::-1]

    for item in sorted_items:
        if bins:
            space_left = capacity - np.array([bin_p.sum() for bin_p in bins])
            valid_bins = np.where(space_left >= item)[0]

            if valid_bins.size > 0:
                best_fit_index = valid_bins[np.argmin(space_left[valid_bins] - item)]
                bins[best_fit_index] = np.append(bins[best_fit_index], item)
            else:
                bins.append(np.array([item]))
        else:
            bins.append(np.array([item]))

    return bins
