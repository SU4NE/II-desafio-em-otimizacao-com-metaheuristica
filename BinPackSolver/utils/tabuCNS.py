import time
import math

class TabuCNS:
    def __init__(self, init_solution, capacity, lixo, max_iteration = 100, time_limit=1):
        self.best_solution = init_solution
        self.current_solution = init_solution.copy()
        self.capacity = capacity
        self.lixo = lixo
        self.time_limit = time_limit
        self.tabu_list = {}
        self.max_iteration = max_iteration

    def run(self):
        iteration = 0
        start_time = time.time()
        
        while iteration < self.max_iteration and (time.time() - start_time) < self.time_limit:
            best_move = None
            best_move_value = -math.inf

            for bin_ in self.current_solution:
                for item_set_s in bin_:
                    if not self.is_tabu(item_set_s, bin_):
                        for item_set_t in self.lixo:
                            menor, move_value = self.feasible(item_set_s, item_set_t, bin_)
                            if menor and move_value > best_move_value:  
                                best_move = (item_set_s, item_set_t, bin_)
                                best_move_value = move_value

            if best_move is None:
                break

            for bin_ in self.current_solution:
                if best_move[0] in bin_:
                    bin_.remove(best_move[0])
                    bin_.append(best_move[1])
                    break
            self.lixo.remove(best_move[1])
            self.lixo.append(best_move[0])

            if self.evaluate(self.current_solution) < self.evaluate(self.best_solution):
                self.best_solution = [bin_.copy() for bin_ in self.current_solution]
                self.tabu_list.clear()
            else:
                self.update_tabu(best_move)

            self.update_tabu_list()
            iteration += 1

        return self.best_solution

    def is_tabu(self, item_set_s, bin_):
        return (item_set_s, tuple(bin_)) in self.tabu_list

    def update_tabu(self, move):
        move_key = (move[0], tuple(move[2]))
        if move_key in self.tabu_list:
            self.tabu_list[move_key]['frequency'] += 1
        else:
            self.tabu_list[move_key] = {'frequency': 1, 'tenure': 0}
        self.tabu_list[move_key]['tenure'] = self.tabu_list[move_key]['frequency'] // 2

    def update_tabu_list(self):
        for move in list(self.tabu_list.keys()):
            self.tabu_list[move]['tenure'] -= 1
            if self.tabu_list[move]['tenure'] <= 0:
                del self.tabu_list[move]

    def feasible(self, item_set_s, item_set_t, bin_):
        peso_bin_atual = sum(bin_)
        novo_peso_bin = peso_bin_atual - item_set_s + item_set_t
        move_value = novo_peso_bin - peso_bin_atual
        return novo_peso_bin <= self.capacity, move_value

    def evaluate(self, solution):
        return sum(sum(bin_) for bin_ in solution)
