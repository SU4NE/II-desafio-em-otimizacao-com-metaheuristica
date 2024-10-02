
def first_fit(items, capacity):
    bins = []
    for item in items:
        placed = False
        for bin in bins:
            if sum(bin) + item <= capacity:
                bin.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return bins