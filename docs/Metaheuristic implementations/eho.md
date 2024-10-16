O **Elephant Herding Optimization (EHO)** foi implementado com o objetivo de explorar uma metaheurística menos comum, mas promissora, para o **Problema de Empacotamento Unidimensional (BPP)**. O EHO é inspirado no comportamento social dos elefantes, onde os indivíduos de uma população (elefantes) são organizados em grupos chamados de clãs. Cada elefante dentro de um clã atualiza sua posição com base no líder do clã, enquanto alguns indivíduos são isolados para aumentar a diversidade das soluções.

### **Fundamentação Teórica**
O **EHO** usa dois mecanismos principais:
1. **Atualização do clã (clan update)**: Cada elefante ajusta sua posição em direção ao líder do clã, movendo-se em direção a soluções promissoras.
2. **Isolamento (isolation)**: Em cada iteração, alguns elefantes são "isolados", isto é, submetidos a uma mutação aleatória que visa explorar novas regiões do espaço de busca.

### **Implementação e Adaptações**
Para o **BPP**, o EHO foi adaptado da seguinte forma:
- **Clan Update**: Elefantes ajustam suas soluções movendo-se em direção ao líder do clã, garantindo que as soluções sigam uma trajetória otimizada.
- **Isolamento**: O isolamento foi implementado como uma permutação aleatória nas soluções dos elefantes. A ideia é garantir que a exploração seja realizada de maneira eficiente, aumentando a chance de encontrar soluções melhores.
- **Reparação de Soluções**: Assim como outras metaheurísticas, após cada movimento ou isolamento, a solução é reparada para garantir que seja válida para o problema de empacotamento.

### **Variações Testadas**
- **Tamanho da População**: Testamos diferentes tamanhos de população, variando de 3 a 7 elefantes por clã.
- **Fator de Atualização (alpha)**: Testamos diferentes valores de alpha (0.3, 0.5 e 0.7) para controlar o quão rápido os elefantes se movem em direção ao líder.
- **Número de Iterações**: Testamos diferentes números de iterações para verificar o impacto no refinamento das soluções.

### **Justificativa para as Escolhas**
A escolha pelo EHO foi feita com o intuito de explorar uma abordagem nova e pouco testada no contexto do BPP. O EHO oferece um interessante equilíbrio entre exploração e explotação, com os elefantes se movendo em direção a boas soluções enquanto também há uma fase de diversificação com a operação de isolamento. O aprendizado e entendimento da dinâmica dessa heurística foi uma das principais motivações para sua implementação.

### **Parâmetros**
As melhores configurações para o EHO foram:
- **Tamanho da População**: 3 elefantes por clã
- **Fator de Atualização (alpha)**: 0.5
- **Máximo de iterações**: 100
- **Tempo máximo de execução**: 60 segundos

### **Resultados**
O **EHO** apresentou desempenho moderado, ficando entre o **Top 15** no nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top15). Embora o algoritmo tenha obtido soluções razoáveis, sua capacidade de refinar soluções não foi tão eficaz quanto outras heurísticas. O uso de isolamento foi útil para manter a diversidade, mas em alguns casos, a exploração excessiva comprometeu o refinamento das soluções.

### **Discussões**
O uso do **EHO** foi uma boa oportunidade para aprender mais sobre a metaheurística, especialmente pela sua abordagem única de exploração e explotação com a operação de isolamento. Embora o desempenho não tenha sido o melhor entre as metaheurísticas testadas, acreditamos que ajustes no número de elefantes e na estratégia de isolamento poderiam melhorar os resultados. A heurística se mostrou promissora em problemas de médio porte, mas teve dificuldades em instâncias maiores.
