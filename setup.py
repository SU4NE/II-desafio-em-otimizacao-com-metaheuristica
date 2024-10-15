from setuptools import setup

setup(
    name='binpacksolver',
    version='0.1.0',
    description='',
        install_requires=[
        'common-package',
        'tabu_structure @ https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/releases/download/v0.1.0/tabu_structure-0.1.0-cp38-none-win_amd64.whl; platform_system=="Windows"',
        'tabu_structure @ https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/releases/download/v0.1.0/tabu_structure-0.1.0-cp38-cp38-linux_x86_64.whl; platform_system=="Linux"'
    ],
)