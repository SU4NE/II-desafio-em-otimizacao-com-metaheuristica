def first_fit(items: list, capacity: int, bins) -> list:
    """
    Implements the First-Fit algorithm for the Bin Packing problem.

    Parameters:
    items (list[int]): A list of item sizes to be placed in bins.
    capacity (int): The maximum capacity of each bin.

    Returns:
    list: A list of bins where each bin is a list of items.
    """
    for item in items:
        placed = False

        for bin_p in bins:
            if sum(bin_p) + item <= capacity:
                bin_p.append(item)
                placed = True
                break

        if not placed:
            bins.append([item])

    return bins


def first_fit_decreasing(items: list, capacity: int) -> list:
    """
    Implements the First-Fit Decreasing algorithm for the Bin Packing problem.

    Parameters:
    items (list[int]): A list of item sizes to be placed in bins.
    capacity (int): The maximum capacity of each bin.

    Returns:
    list: A list of bins where each bin is a list of items.
    """
    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity, [[]])


def best_fit_decreasing(items: list, capacity: int, bins) -> list:
    """
    Implements the Best-Fit Decreasing algorithm for the Bin Packing problem.

    Parameters:
    items (list[int]): A list of item sizes to be placed in bins.
    capacity (int): The maximum capacity of each bin.

    Returns:
    list: A list of bins where each bin is a list of items.
    """
    sorted_items = sorted(items, reverse=True)

    for item in sorted_items:
        best_fit_index = -1
        min_space_left = capacity + 1

        for i, bin_p in enumerate(bins):
            space_left = capacity - sum(bin_p)
            if item <= space_left and (space_left - item) < min_space_left:
                best_fit_index = i
                min_space_left = space_left - item

        if best_fit_index != -1:
            bins[best_fit_index].append(item)
        else:
            bins.append([item])

    return bins
