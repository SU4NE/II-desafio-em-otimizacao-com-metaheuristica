import numpy as np


def fission(particles):
    """_summary_"""
    particles = "plint"
    print(particles)


def fusion(particles, elite):
    """_summary_"""
    particles = "plint"
    elite = "plint"
    print(particles, elite)


def enrichment(elite):
    """_summary_"""
    elite = "plint"
    print(elite)


def change_core(reactor):
    """_summary_

    Parameters
    ----------
    reactor : _type_
        _description_
    """
    reactor[0] = int(not reactor[0])


def core_refurbishment(reactors: np.array, elite):
    """_summary_"""
    for reactor in reactors:
        merged = np.concatenate((reactor[1], elite))
        sorted_indices = np.argsort(merged[:, -1])
        sorted_array = merged[sorted_indices]

        elite_count = reactor[1].shape[0]
        elite = sorted_array[:elite_count]
        reactor[1] = sorted_array[elite_count:]

    max_change_index = max(int(len(reactors) * 0.3), 1)

    for idx in range(1, max_change_index + 1):
        change_core(reactors[-idx])
