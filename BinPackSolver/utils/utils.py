def lower_bound(items, capacity):
    return (sum(items) + capacity - 1) // capacity

def is_complete(solution, items):
    all_items = [item for bin in solution for item in bin]
    return set(all_items) == set(items)

def weight(P):
    if not P: return 0
    return sum(item for item in P)

def pack_set(items, bin, best_bin, capacity):
    if not items:
        if weight(bin) > weight(best_bin) or \
            (weight(bin) == weight(best_bin) and \
            len(bin) < len(best_bin)):
                
            best_bin = bin
    else:
        i = items[0]
        items = items[1:]
        
        if weight(bin) + i <= capacity:
            best_bin = pack_set(items, bin + [i], best_bin)
        best_bin = pack_set(items, bin, best_bin)
        
    return best_bin