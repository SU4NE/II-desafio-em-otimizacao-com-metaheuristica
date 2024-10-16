O **Particle Swarm Optimization (PSO)** foi implementado para o **Problema de Empacotamento Unidimensional (BPP)** utilizando o movimento de partículas no espaço de busca. Cada partícula representa uma possível solução, e seu movimento é influenciado por sua melhor solução pessoal e pela melhor solução global do enxame.

### **Fundamentação Teórica**
O **PSO** é um algoritmo inspirado no comportamento de enxames e bandos, onde as partículas (soluções) se movem através do espaço de busca ajustando suas posições com base em uma combinação da sua melhor posição anterior (cognição) e da melhor posição do grupo (social). Ao ajustar as velocidades das partículas, o algoritmo consegue equilibrar a exploração e a explotação, buscando sempre melhorar as soluções.

### **Implementação e Adaptações**
- **Velocidade das Partículas**: A velocidade de cada partícula é atualizada em função de três fatores: sua inércia, a distância em relação à melhor posição individual e a distância em relação à melhor posição global.
- **Atualização das Posições**: As partículas se movem no espaço de soluções com base na sua velocidade atualizada. O movimento é limitado para garantir que as partículas não saiam dos limites definidos pelo problema.
- **Reparação de Soluções**: Após cada movimento, as partículas têm suas soluções verificadas e ajustadas (reparadas) para garantir que respeitem as restrições do problema, como o limite de capacidade dos contêineres.

### **Variações Testadas**
- **Fatores de Inércia e Aprendizado**: O fator de inércia (w) controla o quanto as partículas mantêm de sua velocidade anterior, enquanto os fatores de aprendizado cognitivo (c1) e social (c2) influenciam o quanto elas se aproximam das melhores soluções individuais e globais. Foram testados diversos valores para esses parâmetros, sendo que os melhores resultados foram obtidos com:
  - **w = 0.5**
  - **c1 = 1.5**
  - **c2 = 1.5**

### **Justificativa para as Escolhas**
O PSO foi escolhido devido à sua habilidade comprovada de convergir rapidamente para boas soluções em uma variedade de problemas de otimização, incluindo o BPP. Além disso, o PSO é altamente flexível e permite uma fácil adaptação dos parâmetros para melhor performance em diferentes tipos de instâncias.

### **Parâmetros**
- **Tamanho da População**: 7 partículas.
- **Inércia (w)**: 0.5.
- **Fatores de Aprendizado (c1 e c2)**: 1.5.
- **Tempo máximo**: 60 segundos.

### **Resultados**
O **PSO** obteve uma classificação **Top 3** no nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/top3), sendo o **melhor algoritmo em termos gerais** devido à sua capacidade de encontrar soluções ótimas em um curto espaço de tempo. O algoritmo demonstrou uma ótima performance em várias instâncias do problema, principalmente em cenários onde o balanceamento entre exploração e explotação é crucial.

### **Discussões**
O PSO mostrou-se extremamente eficaz na exploração e explotação do espaço de soluções, permitindo que o enxame rapidamente convergisse para soluções próximas do ótimo. Em instâncias grandes, o algoritmo continuou a apresentar ótimos resultados, tanto em termos de qualidade das soluções quanto no tempo de execução. Essa combinação de rapidez e eficácia fez com que o PSO se destacasse entre as outras metaheurísticas testadas. Ajustes finos nos fatores de inércia e aprendizado poderiam potencialmente melhorar ainda mais o desempenho do algoritmo em instâncias mais específicas.
