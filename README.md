# II Desafio em Otimizacao com Metaheuristica PUC GO

# Sumário

- [Equipe](#equipe)
- [Projeto](#projeto)
  - [Sobre o Desafio](#sobre-o-desafio)
  - [Dados](#dados)
  - [Hardware e Software Utilizados](#hardware-e-software-utilizados)
  - [Metaheurísticas Testadas](#metaheurísticas-testadas)
  - [Fundamentação Teórica e Implementação](#fundamentação-teórica-e-implementação)
- [Resultados](#resultados) 
  - [Gráficos Representando o Top 3](#gráficos-representando-o-top-3)
    - [MAE Best Solution Mean vs Arquivo por Heurística](#mae-best-solution-mean-vs-arquivo-por-heurística)
    - [MSE Best Solution Mean vs Arquivo por Heurística](#mse-best-solution-mean-vs-arquivo-por-heurística)
    - [RMSE Best Solution Mean vs Arquivo por Heurística](#rmse-best-solution-mean-vs-arquivo-por-heurística)
    - [Comparação de RMSE Teórico e Melhor Solução por Arquitetura](#comparação-de-rmse-teórico-e-melhor-solução-por-arquitetura)
    - [Real Time Mean vs Arquivo por Heurística](#real-time-mean-vs-arquivo-por-heurística)
    - [Best Fit Mean vs Arquivo por Heurística](#best-fit-mean-vs-arquivo-por-heurística)
  - [Explicação](#explicação)
- [Conclusão](#conclusão)
  - [Sobre o Solver](#sobre-o-solver)
  - [Funcionamento](#funcionamento)

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
[![Static Badge](https://img.shields.io/badge/Instâncias%20Utilizadas%20-%20txt%20-%20violet?style=for-the-badge&logo=files&logoColor=violet
)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/data/dados.zip)
[![Static Badge](https://img.shields.io/badge/Testes%20Realizados%20-%20txt%20-%20blue?style=for-the-badge&logo=files&logoColor=blue
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

Foram implementadas ao todo 19 metaheurísticas:
- [Artificial Bee Colony (ABC)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/abc.md)
- [Bat Algorithm](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/ba.md)
- [Caotic Grey Wolf Optimization (CGWO)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/acgwo.md)
- [Consistent Neighborhood Search (CNS)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/cns.md)
- [Dragonfly Algorithm](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/da.md)
- [Elephant Herding Optimization (EHO)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/eho.md)
- [Genetic Algorithm CGT (GGA-CGT)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/ggacgt.md)
- [Gravitational Search Algorithm (GSA)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/gsa.md)
- [Imperialist Competitive Algorithm (ICA)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/ica.md)
- [Improved Coati Optimization Algorithm (TnT-WCOA)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/tntwcoa.md)
- [Improved Whale Optimization Algorithm (IWOA)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/iwoa.md)
- [Jaya Optimization](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/jaya.md)
- [Memetic Algorithm (MA)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/ma.md)
- [Multi-Verse Optimizer (MVO)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/mvo.md)
- [Particle Swarm Optimization (PSO)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/pso.md)
- [Simulated Annealing (SA)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/sa.md)
- [Student Psychology Based Optimization (SPBO)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/spbo.md)
- [Symbiotic Organisms Search (SOS)](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/sos.md)
- [Tabu Search](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Metaheuristic%20implementations/tabusearch.md)

### Fundamentação Teórica e Implementação

Cada metaheurística foi selecionada cuidadosamente com base em sua capacidade de equilibrar exploração e explotação nos diferentes espaços de busca apresentados pelo **Problema de Empacotamento Unidimensional (Bin Packing Problem - BPP)**. Ao longo do desenvolvimento, várias adaptações e ajustes finos foram introduzidos nas metaheurísticas para otimizar seu desempenho em diferentes instâncias do problema. Dada a ampla variedade de algoritmos testados, foi realizada uma análise criteriosa para filtrar as melhores abordagens com base em parâmetros de eficiência e qualidade das soluções. Neste documento, destacaremos as três heurísticas mais eficazes, considerando os resultados obtidos. No entanto, para garantir uma visão completa do trabalho, todas as outras metaheurísticas testadas, junto com suas implementações detalhadas, estarão disponíveis [aqui](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Metaheuristic%20implementations).

# Resultados

Após a aplicação dos filtros e análise dos resultados obtidos com as 19 metaheurísticas implementadas, foi possível identificar padrões de desempenho e eficiência com base nos gráficos e métricas coletados. Os gráficos completos com a análise de desempenho podem ser encontrados em [Graficos](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics).

Dentre as heurísticas testadas, três se destacaram pelo seu desempenho superior em termos de qualidade da solução e tempo de execução:

- **Particle Swarm Optimization (PSO)**
- **Gravitational Search Algorithm (GSA)**
- **Improved Whale Optimization Algorithm (IWOA)**

Essas três heurísticas formam o **Top 3** de soluções mais eficientes, conforme apresentado em [Top 3](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/top3).

## Gráficos Representando o Top 3:

#### MAE Best Solution Mean vs Arquivo por Heurística
![MAE Best Solution Mean](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/mae_best_solution_vs_arquivo.jpg)

#### MSE Best Solution Mean vs Arquivo por Heurística
![MSE Best Solution Mean](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/mse_best_solution_vs_arquivo.jpg)

#### RMSE Best Solution Mean vs Arquivo por Heurística
![RMSE Best Solution Mean](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/rmse_best_solution_vs_arquivo.jpg)

#### Comparação de RMSE Teórico e Melhor Solução por Arquitetura
![RMSE Teórico vs Melhor Solução](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/rmse_teorico_e_melhor_solucao.jpg)

#### Real Time Mean vs Arquivo por Heurística
![Real Time Mean](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/real_time_exec_vs_arquivo.jpg)

#### Best Fit Mean vs Arquivo por Heurística
![Best Fit Mean](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/best_fit_vs_arquivo.jpg)

## Explicação:

Os resultados das heurísticas testadas foram avaliados com base em diversas métricas, como RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), MSE (Mean Squared Error) e o tempo de execução médio para cada instância de teste. Abaixo estão os gráficos que ilustram a performance das três melhores heurísticas (**Gravitational Search Algorithm (GSA)**, **Improved Whale Optimization Algorithm (IWOA)** e **Particle Swarm Optimization (PSO)**) com links para os arquivos correspondentes no repositório:

### 1. **[MAE Best Solution Mean vs Arquivo por Heurística](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/mae_best_solution_vs_arquivo.jpg)**:
   - **O que representa**: Este gráfico mostra a **média do erro absoluto (MAE)** para as melhores soluções encontradas por diferentes heurísticas. O MAE avalia a precisão das soluções sem amplificar grandes desvios como o RMSE.
   - **Análise**: **PSO** e **GSA** mantiveram valores baixos de MAE ao longo das diferentes instâncias, demonstrando consistência. No entanto, heurísticas como o **Artificial Bee Colony (ABC)** apresentaram MAE mais elevado em diversas instâncias, sugerindo maior variação entre as soluções encontradas, a heurística **IWOA** dentre as que mais variaram teve os altos mais suaves que as outras heurísticas. Esse comportamento é semelhante ao visto em heurísticas com desempenho inferior, como o **Jaya Optimization**, conforme observado em gráficos como ![este](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/Top6/mae_best_solution_vs_arquivo.jpg)

### 2. **[MSE Best Solution Mean vs Arquivo por Heurística](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/mse_best_solution_vs_arquivo.jpg)**:
   - **O que representa**: O **erro quadrático médio (MSE)** é mostrado para cada arquivo testado por cada heurística. O MSE penaliza grandes erros, tornando-o uma métrica útil para avaliar algoritmos que podem produzir outliers.
   - **Análise**: **GSA**, **PSO**, e **IWOA** (No geral) se destacaram por manterem MSE baixo, enquanto heurísticas como o **Jaya Optimization** e o **Artificial Bee Colony (ABC)** mostraram picos elevados de MSE em várias instâncias, o que reflete um desempenho inconsistente. Este comportamento se reflete de maneira semelhante em heurísticas como o **Gravitational Search Algorithm (GSA)**, que teve uma performance mais estável em relação a outros, conforme visto ![aqui](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/Top6/mse_best_solution_vs_arquivo.jpg)

### 3. **[RMSE Best Solution Mean vs Arquivo por Heurística](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/rmse_best_solution_vs_arquivo.jpg)**:
   - **O que representa**: Este gráfico mostra o **erro quadrático médio (RMSE)** das melhores soluções por heurística. O RMSE é uma métrica sensível a grandes desvios, o que ajuda a avaliar a precisão das soluções.
   - **Análise**: **PSO**, **GSA**, e **IWOA** (No geral) tiveram RMSE consistentemente baixos, o que indica que suas soluções estão próximas do valor ideal. Em contraste, heurísticas como o **Student Psychology Based Optimization (SPBO)** tiveram picos de RMSE em algumas instâncias, sugerindo variações maiores na precisão das soluções. Essas variações são semelhantes ao desempenho inconsistente observado em heurísticas como o **Jaya Optimization**, como pode ser visto ![aqui](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/Top6/rmse_teorico_vs_melhor_solucao.jpg)

### 4. **[Comparação de RMSE Teórico e Melhor Solução por Arquitetura](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/rmse_teorico_vs_melhor_solucao.jpg)**:
   - **O que representa**: Este gráfico compara o **RMSE teórico** com o **RMSE das melhores soluções** encontradas para diferentes heurísticas. Ele mostra quão próximas as soluções encontradas estão do valor teórico ideal.
   - **Análise**: **PSO** e **GSA** novamente demonstram sua eficácia, com soluções muito próximas do RMSE teórico. No entanto, o **Improved Whale Optimization Algorithm (IWOA)** apresenta algumas variações maiores, principalmente em instâncias mais complexas. Em comparação, algoritmos como **Tabu Search** mostraram grandes discrepâncias entre o RMSE teórico e o encontrado, sugerindo desempenho significativamente pior em termos de aproximação ao ideal.

### 5. **[Real Time Mean vs Arquivo por Heurística](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/tempo_exec_vs_arquivo.jpg)**:
   - **O que representa**: Este gráfico mostra o **tempo médio de execução** das heurísticas em cada arquivo de teste, permitindo a análise do trade-off entre qualidade de solução e tempo de execução.
   - **Análise**: Análise: PSO e IWOA apresentaram os maiores tempos médios de execução em comparação com outras heurísticas do Top 6, apesar de serem altamente eficientes em termos de qualidade de solução. Em termos de tempo de execução, o Artificial Bee Colony (ABC) e o Student Psychology Based Optimization mostraram-se entre os mais rápidos, sendo eficientes nesse aspecto. Já o Gravitational Search Algorithm (GSA) e o Jaya Optimization também apresentaram tempos de execução medianos, conforme observado ![aqui](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/Top6/tempo_exec_vs_arquivo.jpg)

### 6. **[Best Fit Mean vs Arquivo por Heurística](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/top3/best_fit_vs_arquivo.jpg)**:
   - **O que representa**: O gráfico exibe a **média do ajuste (fit)** das melhores soluções por heurística, medindo o quão eficiente cada heurística é em minimizar o número de caixas usadas.
   - **Análise**: **PSO**, **GSA** e **IWOA** mantiveram valores consistentes e baixos de ajuste, indicando sua capacidade de empacotar itens de forma eficiente. Por outro lado, heurísticas como o **Artificial Bee Colony (ABC)** apresentaram variações maiores, o que sugere um desempenho inferior em algumas instâncias. Este comportamento é consistente com outras heurísticas que não foram tão eficazes em minimizar o número de caixas, como o **Multi-Verse Optimizer**, conforme analisado ![aqui](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/Top10/best_fit_vs_arquivo.jpg)


# Conclusão

O desafio proposto pelo Problema de Empacotamento Unidimensional se mostrou um campo fértil para o teste de diversas metaheurísticas. A variedade de algoritmos implementados proporcionou uma análise aprofundada sobre a capacidade de cada técnica em encontrar soluções otimizadas, equilibrando exploração e explotação. Com base nos resultados, é possível afirmar que o **PSO**, **GSA**, e **IWOA** foram os algoritmos que apresentaram o melhor desempenho geral, destacando-se como as melhores escolhas para resolver problemas similares de otimização combinatória. Contudo, as demais heurísticas também trouxeram valiosas contribuições ao processo, e suas implementações detalhadas estão disponíveis para futuras consultas e adaptações em outros cenários. Além dos resultados obtidos com as metaheurísticas destacadas no **Top 3**, o módulo implementado inclui um **solver** que permite a execução de várias heurísticas de forma sequencial ou paralela. O **Solver** foi desenvolvido para resolver o **Problema de Empacotamento Unidimensional (Bin Packing Problem)** utilizando as heurísticas mais eficientes identificadas durante o desafio.

### Sobre o Solver:

O **Solver** integra múltiplas heurísticas e foi desenhado para ser flexível, possibilitando a configuração de paralelização (com uso de múltiplas threads) e controle de tempo alocado para cada heurística. Ele implementa um conjunto robusto de algoritmos, permitindo a comparação direta e a escolha de heurísticas que melhor atendam às necessidades específicas da instância do problema.

No contexto desse desafio, o **Solver** demonstrou ser uma ferramenta poderosa ao permitir a execução conjunta das seguintes heurísticas:
- **Particle Swarm Optimization (PSO)**
- **Gravitational Search Algorithm (GSA)**
- **Improved Whale Optimization Algorithm (IWOA)**
- **Jaya Optimization**
- **Artificial Bee Colony**
- **Student Psychology Based Optimization**

O solver pode ser configurado para executar cada uma dessas heurísticas individualmente ou em paralelo, alocando tempo de execução de forma proporcional à sua eficiência e relevância.

### Funcionamento:

1. **Execução Sequencial e Paralela**: Com suporte para múltiplos threads, o **Solver** pode executar as heurísticas em paralelo, o que reduz o tempo de execução total.
2. **Alocação de Tempo**: O tempo total disponível para a solução é alocado de acordo com o número de heurísticas configuradas, priorizando as mais eficientes.
3. **Impressão de Resultados**: Dependendo do nível de verbosidade configurado, o solver imprime informações detalhadas sobre o desempenho de cada heurística.

Esse módulo fornece uma abordagem escalável e personalizável para resolver problemas de otimização, podendo ser adaptado para diferentes configurações e necessidades futuras.
