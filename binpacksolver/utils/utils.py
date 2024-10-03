"""
This module provides various utility functions for common tasks 
and operations. These functions can be used in different contexts 
to facilitate optimization processes, array manipulations, and 
other generic operations.
"""
import numpy as np

def check_end(th_min: int, best_fit: int, time_max: float, time_start: float, time_end: float, max_it: int, it: int) -> bool:
    """
    Checks if the termination conditions for an optimization process 
    are met.

    The function evaluates three conditions:
    1. If the maximum number of iterations has been reached.
    2. If the elapsed time exceeds the specified maximum time.
    3. If the best fitness value is greater than the theoretical minimum.

    Parameters
    ----------
    th_min : int
        The theoretical minimum fitness value that must be achieved.
    best_fit : int
        The best fitness value found so far in the optimization process.
    time_max : float
        The maximum allowable time for the optimization process in seconds.
    time_start : float
        The timestamp (in seconds) marking the start of the optimization process.
    time_end : float
        The timestamp (in seconds) marking the end of the optimization process.
    max_it : int
        The maximum number of iterations allowed for the optimization.
    it : int
        The current iteration count.

    Returns
    -------
    bool
        Returns True if the optimization process should continue, 
        False if any termination condition is met.
    """
    if max_it and it > max_it:
        return False
    
    if time_max and time_end - time_start >= time_max:
        return False
    
    return best_fit > th_min


def merge_np(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Merges two sorted NumPy arrays into a single sorted array.

    This function assumes that both input arrays are already sorted in
    ascending order. It combines them into a new array while maintaining
    the order.

    Parameters
    ----------
    a : np.ndarray
        The first sorted array to merge.
    b : np.ndarray
        The second sorted array to merge.

    Returns
    -------
    np.ndarray
        A new sorted array containing all elements from both input arrays.
    """    
    merged_sorted = np.empty(len(a) + len(b), dtype=a.dtype)
    i = 0
    j = 0
    k = 0

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            merged_sorted[k] = a[i]
            i += 1
        else:
            merged_sorted[k] = b[j]
            j += 1
        k += 1

    while i < len(a):
        merged_sorted[k] = a[i]
        i += 1
        k += 1

    while j < len(b):
        merged_sorted[k] = b[j]
        j += 1
        k += 1
    
    return merged_sorted