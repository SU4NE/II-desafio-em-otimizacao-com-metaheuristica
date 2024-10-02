from BinPackSolver.utils import first_fit, tabu_search, lower_bound, is_complete, pack_set, weight
import random

def pack(b_items, lixo, capacity_b):

    b_items = sorted(b_items + lixo, reverse=True)

    items_in_b = []
    items_in_tc = []
    
    used_capacity = 0
    
    for item in b_items:
        if used_capacity + item <= capacity_b:
            items_in_b.append(item)
            used_capacity += item
        else:
            items_in_tc.append(item)
    return items_in_b, items_in_tc

def descent(bins, capacity, lixo):
    while True:
        random.shuffle(bins)
        
        for b in bins:
            b, lixo = pack(b, lixo, capacity)

            if weight(lixo) <= 2 * capacity:
                bx = pack_set(lixo,[],[],capacity)
                bins.append(bx)
                bx = pack_set(lixo,[],[],capacity)
                bins.append(bx)
                return
            
def cns(sol, capacity, lixo, iterations_limit=100):
    iterations = 0
    
    while iterations < iterations_limit:

        if is_complete(sol):
            break

        sol = tabu_search(sol, capacity, lixo)
        sol = descent(sol, capacity, lixo)
        
        iterations += 1

    return sol


def cns_bp(items, capacity):
    items = [item for item in items if item < capacity]
    
    lb = lower_bound(items, capacity)
    
    random.shuffle(items)
    
    S = first_fit(items, capacity)
    
    m = len(S)
    
    while m > lb:
        m -= 1
        
        lixo = [item for sublist in S[m-2:] for item in sublist]
        P = S[:m-2]
        
        S_prime = cns(P, capacity, lixo)
        
        if not is_complete(S_prime, items):
            break
        
        S = S_prime
    
    return S
