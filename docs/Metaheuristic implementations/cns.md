### **Consistent Neighborhood Search (CNS) e Tabu Search**

#### **Fundamentação Teórica**
O **Consistent Neighborhood Search (CNS)** combinado com o **Tabu Search** é uma metaheurística projetada para explorar eficientemente o espaço de busca, evitando mínimos locais e otimizando soluções de problemas complexos. O CNS visa melhorar soluções iterativamente, ajustando itens entre caixas, enquanto o **Tabu Search** impede que o algoritmo revisite soluções recentemente exploradas, mantendo uma lista de soluções tabu.

No contexto do **Problema de Empacotamento Unidimensional (BPP)**, o CNS tenta reorganizar itens já colocados em caixas e explorar diferentes combinações, enquanto o Tabu Search garante que o algoritmo evite ciclos repetitivos que podem prender o algoritmo em soluções subótimas.

#### **Implementação e Adaptações**
A implementação combina as seguintes fases:
1. **Busca em Vizinhaças (Neighborhood Search)**: Durante a busca, o algoritmo tenta mover itens entre caixas, reavaliando constantemente a melhor forma de reorganizar os itens dentro do limite de capacidade.
2. **Estrutura Tabu**: A lista tabu mantém os movimentos recentemente explorados, evitando que o algoritmo volte a soluções exploradas anteriormente. Esse mecanismo é crucial para evitar ciclos e manter a diversidade das soluções.
3. **Busca em Declive (Descent Search)**: Após um conjunto de operações no Tabu Search, é realizada uma busca em declive para melhorar ainda mais a solução, permitindo pequenas alterações incrementais para refinar a solução final.

Adaptações foram feitas no tempo de execução, controle da lista tabu e no número de tentativas permitidas para melhorar a eficiência.

#### **Variações Testadas**
Diferentes variações foram exploradas:
- **Número de tentativas para movimentação**: Testamos diferentes números de tentativas para ajustes locais (de 1.000 a 100.000).
- **Tempo máximo por operação**: Diferentes tempos foram testados para limitar o tempo gasto em cada operação de vizinhança.
- **Estrutura tabu**: Tamanhos da lista tabu foram ajustados para evitar movimentos cíclicos, testando listas de tamanhos 5, 10 e 20.

#### **Justificativa para as Escolhas**
A combinação de CNS com o Tabu Search foi escolhida devido à sua abordagem sistemática de exploração do espaço de soluções, o que é útil para problemas que tendem a apresentar soluções subótimas frequentes. O Tabu Search oferece uma forma eficiente de escapar de mínimos locais, enquanto o CNS oferece uma abordagem de busca intensiva para refinar as soluções encontradas.

#### **Parâmetros**
Os melhores resultados foram obtidos com as seguintes configurações:
- **Número de tentativas máximas**: 100.000
- **Tamanho da lista Tabu**: 10
- **Tempo máximo por operação**: 1 segundo
- **Máximo de iterações**: 100
- **Tempo máximo de execução**: 60 segundos

#### **Resultados**
Infelizmente, o desempenho do CNS combinado com o Tabu Search não foi satisfatório nas instâncias testadas. O algoritmo não obteve os resultados esperados, ficando fora do **Top 15** do [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Graphics/Top15). A implementação não atingiu a qualidade mencionada no artigo de referência [Pre-print Comparative Study of Heuristics for the One-dimensional Bin Packing Problem](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Artigos/Pre-printComparativestudyofheuristicsfortheOne-dimensionalBinPackingProblem.pdf), e o tempo de execução foi mais longo que o desejado, comprometendo a eficiência.

#### **Discussões**
O desempenho abaixo do esperado pode ser atribuído à inexperiência na implementação desta heurística específica. Embora o CNS e o Tabu Search sejam abordagens promissoras para problemas de otimização, a aplicação ao BPP neste caso mostrou-se desafiadora. A qualidade da solução obtida foi inferior ao esperado, com uma exploração insuficiente do espaço de busca. Ajustes mais finos na estrutura tabu e nas operações de busca local, bem como uma exploração mais aprofundada da variação de parâmetros, poderiam potencialmente melhorar os resultados obtidos com essa abordagem.
