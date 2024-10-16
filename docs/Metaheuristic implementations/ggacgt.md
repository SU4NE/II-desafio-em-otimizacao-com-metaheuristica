O **Genetic Algorithm with Coarse-Grained Tabu Search (GGA-CGT)** foi uma das metaheurísticas testadas para o **Problema de Empacotamento Unidimensional (BPP)**, com base no uso de conceitos de Algoritmos Genéticos (AG) e Tabu Search (TS). O objetivo era melhorar a diversidade das soluções através de cruzamento genético, enquanto evitava a estagnação em soluções locais com a ajuda do Tabu Search.

### **Fundamentação Teórica**
O **GGA-CGT** combina a exploração de novas soluções utilizando um algoritmo genético e um controle mais refinado da busca com o auxílio de uma busca tabu de grão grosso. As operações genéticas típicas como **crossover** e **mutação adaptativa** foram implementadas para gerar diversidade na população de soluções, enquanto o **Tabu Search** evitava que a busca retornasse a soluções recentemente exploradas.

### **Implementação e Adaptações**
- **População Inicial**: A população inicial foi gerada aleatoriamente utilizando o algoritmo **First Fit** para criar soluções iniciais válidas.
- **Crossover**: O crossover foi realizado em nível de gene, ou seja, combinações de soluções foram feitas utilizando partes de dois pais para gerar novos filhos.
- **Mutação Adaptativa**: Aplicamos uma mutação adaptativa nas soluções, onde a intensidade da mutação era controlada pelo parâmetro **delta**.
- **Busca Tabu**: Implementamos uma versão coarse-grained de Tabu Search, garantindo que soluções recentemente exploradas fossem evitadas em novas iterações.

### **Variações Testadas**
- **Número de Cruzamentos (nc)**: Foram testados valores diferentes para o número de indivíduos selecionados para cruzamento.
- **Número de Mutações (nm)**: Variamos o número de indivíduos selecionados para mutação em cada iteração.
- **Fator de Mutação (delta)**: Alteramos o fator de mutação adaptativa, testando valores entre 0.5 e 0.9.
  
### **Justificativa para as Escolhas**
O **GGA-CGT** foi escolhido com base na promessa de fornecer um equilíbrio entre **exploração** e **explotação** utilizando um método genético aliado a uma estratégia tabu. A escolha de usar o Tabu Search com uma granularidade mais grosseira foi baseada na tentativa de balancear a busca em áreas promissoras sem limitar a diversidade das soluções.

### **Parâmetros**
As melhores configurações para o GGA-CGT foram:
- **Tamanho da População**: 10 indivíduos
- **Número de Cruzamentos (nc)**: 3
- **Número de Mutações (nm)**: 1
- **Fator de Mutação (delta)**: 0.7
- **Tempo máximo de execução**: 60 segundos

### **Resultados**
Apesar das expectativas e do potencial teórico do **GGA-CGT**, ele não conseguiu se posicionar entre os **Top 15** no nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top15). Isso pode ser explicado por possíveis dificuldades na adaptação do algoritmo para o BPP, principalmente na aplicação da Busca Tabu junto ao Algoritmo Genético.

### **Discussões**
Embora o **GGA-CGT** seja uma abordagem interessante descrita na literatura, a implementação específica utilizada neste desafio não apresentou resultados satisfatórios. É possível que ajustes mais finos na configuração da Busca Tabu ou no processo de mutação pudessem melhorar o desempenho do algoritmo. Além disso, a natureza aleatória da inicialização pode ter dificultado a exploração de soluções mais competitivas desde o início da busca.
