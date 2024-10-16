# II Desafio em Otimizacao com Metaheuristica PUC GO
# Sumário

- [Equipe](#equipe)
- [Projeto](#projeto)
  - [Sobre o Desafio](#sobre-o-desafio)
  - [Dados](#dados)
  - [Hardware e Software Utilizados](#hardware-e-software-utilizados)
  - [Metaheurísticas Testadas](#metaheurísticas-testadas)
  - [Resultados](#resultados) 
  - [Testes](#Testes)
    - [Tempo com cada população](#Tempo-com-cada-população)
    - [Moda da resposta em relação a cada população](#Moda-da-resposta-em-relação-a-cada-população)
    - [Análise final dos testes](#Análise-final-dos-testes)
  - [Conclusão](#conclusão)

## Equipe:
<div>
  
  [<img src="https://avatars.githubusercontent.com/u/98399932?v=4" alt="João Victor Porto" width="100">](https://github.com/Joao-vpf)
  [<img src="https://avatars.githubusercontent.com/u/104952737?v=4" alt="João Pedro Lemes" width="100">](https://github.com/Lixomensch)
  
</div>

## Projeto:
### Sobre o Desafio:
O Problema de Empacotamento Unidimensional (ou bin packing) é um clássico problema de otimização combinatória que se concentra em organizar um conjunto de itens em caixas de forma eficiente. Nesse problema são dados um conjunto de n itens. Cada item i possui um peso ou tamanho wi, indicando que esse item consome wi unidades da capacidade de uma caixa. Também é dado um valor C, indicando a capacidade máxima de uma caixa.Partindo do pressuposto que temos um número ilimitado de caixas disponíveis, o objetivo do Problema de Empacotamento Unidimensional é empacotar todos os itens nas caixas de forma que o número total de caixas utilizadas seja o menor possível.

### Dados:
[![Static Badge](https://img.shields.io/badge/Edital%20do%20Desafio%20-%20PDF%20-%20red?style=for-the-badge&logo=files&logoColor=red
)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Edital/Edital%20do%20II%20Desafio%20de%20Otimiza%C3%A7%C3%A3o%20-%20Problema%20de%20Empacotamento%20Unidimensional%202024.pdf)
[![Static Badge](https://img.shields.io/badge/Instâncias%20Utilizadas%20-%20txt%20-%20red?style=for-the-badge&logo=files&logoColor=red
)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/data/dados.zip)
[![Static Badge](https://img.shields.io/badge/Testes%20Realizados%20-%20txt%20-%20red?style=for-the-badge&logo=files&logoColor=red
)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Benchmark)

### Hardware e Software Utilizados:

#### Software:
- Foram utilizados Visual Studio Code e Visual Studio como IDES.
- Algoritmo foi executado em um sistema operacional Windows com Miniconda.

#### Hardware
- Processador: Ryzen 5600g
- Memoria Ram: 32Gb
- Ssd Nvme: 1Tb

### Metaheurísticas Testadas:
