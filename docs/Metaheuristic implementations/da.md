O **Dragonfly Algorithm (DA)**, embora seja uma metaheurística promissora e tenha demonstrado bons resultados em alguns problemas de otimização, foi utilizado como uma abordagem experimental no **Problema de Empacotamento Unidimensional (BPP)**. O algoritmo foi projetado para simular o comportamento social das libélulas, onde o movimento de uma libélula é influenciado pelas melhores soluções (comida) e pelas piores (inimigos). 

### **Fundamentação Teórica**
O **DA** utiliza interações entre libélulas, focando em manter um equilíbrio entre exploração (busca de novas soluções) e explotação (refinamento de soluções já conhecidas). Cada libélula (solução) ajusta sua posição com base em três principais fatores:
- **Alinhamento**: A média da diferença entre a posição da libélula e seus vizinhos.
- **Comida**: A melhor solução encontrada até o momento, que atrai as libélulas.
- **Inimigo**: A pior solução, que repele as libélulas.

Para o **BPP**, o **DA** foi implementado com a ideia de ajustar a organização dos itens nas caixas, minimizando o número de caixas utilizadas.

### **Implementação e Adaptações**
A implementação seguiu o modelo clássico do **DA**, com algumas adaptações específicas para o BPP:
1. **Atualização das posições**: As posições das libélulas (soluções) foram ajustadas com base na atração pela melhor solução (comida) e na repulsão da pior solução (inimigo).
2. **Busca com vizinhos**: A média das posições dos vizinhos influencia a movimentação da libélula, o que garante que as soluções explorem o espaço de forma coordenada.
3. **Reparação das soluções**: Após cada movimento, as soluções foram reparadas para garantir que fossem válidas no contexto do problema de empacotamento, ou seja, respeitassem a capacidade das caixas.

### **Variações Testadas**
Diferentes variações foram aplicadas para testar o desempenho:
- **Tamanho da população**: Foram testados tamanhos de população de 5, 7 e 10 libélulas.
- **Fator aleatório (r)**: Diferentes níveis de fator aleatório foram ajustados para avaliar a influência na exploração global e local.
- **Número de iterações**: Ajustamos o número de iterações, variando de 50 a 200, para verificar o impacto no refinamento das soluções.

### **Justificativa para as Escolhas**
O DA foi escolhido por sua capacidade de equilibrar exploração e explotação, que é essencial para o BPP. No entanto, o algoritmo foi utilizado também como uma oportunidade de aprendizado, dado que ainda não é amplamente testado nesse tipo de problema específico.

### **Parâmetros**
As melhores configurações observadas foram:
- **Tamanho da população**: 7 libélulas
- **Fator aleatório (r)**: 0.5
- **Máximo de iterações**: 100
- **Tempo máximo de execução**: 60 segundos

### **Resultados**
O **Dragonfly Algorithm** apresentou resultados medianos nas instâncias testadas, ficando no **Top 15** do nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top15). Embora tenha sido capaz de encontrar soluções razoáveis, seu desempenho foi limitado em instâncias maiores, onde a exploração e explotação se mostraram insuficientes para garantir soluções otimizadas.

### **Discussões**
O **DA** se mostrou eficaz para aprender mais sobre a dinâmica da metaheurística, mas, em comparação com outras abordagens, apresentou algumas dificuldades em instâncias mais complexas. A limitação pode estar na forma como o algoritmo trata a atração/repulsão das soluções, o que pode não ser ideal para o BPP, que exige um refinamento mais rigoroso. O uso do **DA** foi mais uma experiência de aprendizado, e futuros ajustes e melhorias podem aumentar sua eficácia para esse tipo de problema.
