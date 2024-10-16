O **Improved Whale Optimization Algorithm (IWOA)** foi testado para resolver o **Problema de Empacotamento Unidimensional (BPP)** utilizando movimentações em espiral e linear para atualizar as posições das baleias (soluções). O algoritmo visa melhorar a exploração e explotação durante o processo de otimização, sendo capaz de encontrar boas soluções com uma abordagem inovadora.

### **Fundamentação Teórica**
O IWOA é baseado no comportamento de alimentação de baleias jubarte, simulando sua busca em espiral ao redor de presas. A atualização das posições das soluções (baleias) depende de um fator probabilístico, onde uma solução pode se mover em espiral em direção ao melhor líder atual ou seguir um movimento linear.

### **Implementação e Adaptações**
- **Movimento Espiral e Linear**: As baleias podem se mover tanto em direção ao melhor líder (solução global) de forma linear ou espiral. O fator probabilístico decide o tipo de movimento.
- **Ajustes Dinâmicos**: O fator "a" ajusta dinamicamente a influência das baleias em suas atualizações, controlando a exploração no início e a explotação nas últimas iterações.
- **Reparo de Soluções**: As soluções geradas por cada iteração foram reparadas para garantir que as capacidades das caixas fossem respeitadas.

### **Variações Testadas**
- **Constante de Espiral**: Testamos diferentes valores para a constante de espiral, que influencia a taxa de convergência e o tipo de movimentação da baleia em torno do líder.
- **População**: Diversos tamanhos de população foram avaliados para verificar o impacto na exploração do espaço de busca.

### **Justificativa para as Escolhas**
A escolha do IWOA foi feita pela possibilidade de explorar tanto soluções globais quanto locais em diferentes fases da execução. O equilíbrio entre **exploração** (no início) e **explotação** (na fase final) é uma característica promissora do algoritmo, especialmente em problemas complexos como o BPP.

### **Parâmetros**
Os parâmetros que apresentaram melhor desempenho no IWOA foram:
- **População**: 7 baleias
- **Tempo máximo**: 60 segundos
- **Constante de Espiral**: 1
- **Movimento Linear e Espiral**: Probabilidade igual para ambos os tipos de movimentação

### **Resultados**
O **IWOA** ficou entre as [Top 6](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top6) metaheurísticas testadas, mostrando resultados sólidos e consistentes, com boas soluções encontradas em várias instâncias de diferentes tamanhos. Embora o objetivo inicial fosse apenas explorar a heurística, o desempenho foi melhor do que o esperado.

### **Discussões**
O IWOA apresentou uma excelente capacidade de explorar o espaço de busca e refinar soluções promissoras nas fases finais da execução. A adaptação dinâmica dos fatores que controlam o movimento da baleia foi crucial para o sucesso do algoritmo. Entretanto, em instâncias maiores, o tempo de execução poderia ser otimizado, principalmente pela complexidade do movimento espiral.
