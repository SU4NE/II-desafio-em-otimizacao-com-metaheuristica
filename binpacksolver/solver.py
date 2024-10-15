import concurrent.futures
import time

import tabulate

# pylint: disable=W0401
from .heuristic import *

# pylint: enable=W0401


def __imprimir_informacoes(func, n, c, best_solution, real_time):
    """
    Imprime as informações do teste de forma organizada em uma tabela.

    Parâmetros
    ----------
    func : function
        Função heurística utilizada no teste.
    n : int
        Número de itens.
    c : int
        Capacidade do recipiente.
    best_solution : object
        Melhor solução encontrada pela heurística.
    real_time : float
        Tempo de execução da heurística.
    """
    print(func.__name__)
    tabela_dados = [
        ["Número de Itens", n],
        ["Capacidade do Recipiente", c],
        ["Best Solution", best_solution],
        ["Real Time (s)", real_time],
    ]

    print(
        tabulate(tabela_dados, headers=["Descrição", "Valor"], tablefmt="fancy_grid")
        + "\n"
    )


def solver_bpp(itens, c, heuristics=None):
    """_summary_

    Parameters
    ----------
    itens : _type_
        _description_
    c : _type_
        _description_
    heuristics : _type_, optional
        _description_, by default None
    """
    if heuristics is None:
        heuristics = [
            tabu_search,
            genetic_algorithm_cgt,
            consistent_neighborhood_search,
            artificial_bee_colony,
            simulated_annealing,
            jaya_optimization,
            multi_verse_optimizer,
            particle_swarm_optimization,
            student_psychology_based_optimization,
            caotic_grey_wolf_optimization,
            memetic_algorithm,
            imperialist_competitive_algorithm,
        ]

    heu_param = {
        "tabu_search": [itens, c, 100, 4],
        "genetic_algorithm_cgt": [itens, c, 100, 10, 3, 1, 0.7, 60],
        "consistent_neighborhood_search": [itens, c, 60, 100, 100000, 1],
        "artificial_bee_colony": [itens, c, 60, 100, 7, 3, 5, 1.8, 3],
        "simulated_annealing": [itens, c, 60, 1e-9, 0.9, 100, 1e9],
        "jaya_optimization": [itens, c, 60, 100, 7],
        "multi_verse_optimizer": [itens, c, 60, 100, 7, 1.0, 0.2],
        "particle_swarm_optimization": [itens, c, 60, 100, 7, 0.5, 1.5, 1.5],
        "student_psychology_based_optimization": [itens, c, 60, 100, 0.3, 0.7],
        "caotic_grey_wolf_optimization": [itens, c, 60, 100, 7, 0.5],
        "memetic_algorithm": [itens, c, 60, 100, 8],
        "imperialist_competitive_algorithm": [itens, c, 60, 100, 3, 5, 0.7, 0.9],
    }

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for heu in heuristics:
            future = executor.submit(heu, *heu_param[heu.__name__])
            future.heuristic_func = heu
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            best_solution = future.result()
            heuristic_func = getattr(future, "heuristic_func", None)
            __imprimir_informacoes(
                heuristic_func, len(itens), c, best_solution, time.time() - start
            )
