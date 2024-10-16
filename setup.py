from setuptools import setup, find_packages

setup(
    name='binpacksolver',
    version='0.1.0',
    description='A Python package for solving the Bin Packing Problem using various heuristic algorithms, including Particle Swarm Optimization, Gravitational Search Algorithm, and Improved Whale Optimization Algorithm. This package provides an easy-to-use interface for implementing and comparing different metaheuristics to find optimal packing solutions efficiently.',
    packages=find_packages(include=['binpacksolver', 'binpacksolver.*']),
    install_requires=[
        'tabulate>=0.9.0',
        'numpy>=1.24.4',
        'tqdm>=4.66.5',
        'wheel>=0.44.0',
    ],
)
