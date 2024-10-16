O **Multi-Verse Optimizer (MVO)** foi implementado para resolver o **Problema de Empacotamento Unidimensional (BPP)** utilizando os mecanismos de **Buraco Branco**, **Buraco Negro** e **Buraco de Minhoca** para explorar o espaço de busca e refinar as soluções.

### **Fundamentação Teórica**
O **MVO** simula o comportamento de múltiplos universos, onde cada universo representa uma solução potencial para o problema. Através de interações baseadas em mecânicas como Buraco Branco e Buraco Negro, os itens são movidos entre universos, permitindo a exploração de novas soluções. Além disso, o Buraco de Minhoca introduz variabilidade aleatória no movimento dos universos, ajudando a evitar que o algoritmo fique preso em mínimos locais.

### **Implementação e Adaptações**
- **Seleção por Roleta**: Utilizada para escolher universos com base em suas taxas de inflação normalizadas (fitness), permitindo que soluções mais promissoras tenham uma maior chance de influenciar os outros universos.
- **Mecanismo de Buraco Branco/Buraco Negro**: Movimenta itens de universos menos adaptados para os mais adaptados, permitindo que boas soluções se propaguem.
- **Mecanismo de Buraco de Minhoca**: Adiciona variabilidade ao movimento dos universos, possibilitando a exploração de áreas diferentes do espaço de busca.

### **Variações Testadas**
- **Tamanho da População**: Testou-se diferentes tamanhos de população para equilibrar a exploração e o tempo de execução.
- **Probabilidade de Existência de Buraco de Minhoca (WEP)**: O valor da WEP foi ajustado ao longo das iterações, começando em um valor baixo e aumentando gradualmente para focar mais em explotação à medida que o algoritmo progredia.

### **Justificativa para as Escolhas**
O MVO foi escolhido devido à sua abordagem inovadora que combina mecanismos de exploração (Buraco Branco e Buraco Negro) com ajustes aleatórios (Buraco de Minhoca). Isso torna o algoritmo flexível e eficaz na busca por soluções globais enquanto ainda explora soluções locais. A dinâmica entre universos bem e mal adaptados proporciona um balanceamento eficaz entre exploração e explotação.

### **Parâmetros**
- **População**: 7 universos.
- **WEP (Probabilidade de Existência de Buraco de Minhoca)**: Inicialmente 0.2, aumentando até 1.0.
- **TDR (Taxa de Distância de Viagem)**: Controlada para ajustar o quão longe os universos podem se mover.
- **Tempo máximo**: 60 segundos.

### **Resultados**
O **MVO** obteve um desempenho consistente, garantindo uma posição de destaque no **Top 10** do nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top10). Ele conseguiu otimizar o uso de caixas em várias instâncias, demonstrando sua eficácia ao explorar diferentes áreas do espaço de busca.

### **Discussões**
O algoritmo mostrou-se bastante robusto e eficiente, especialmente em instâncias de tamanho médio e grande. No entanto, o tempo de execução foi um pouco mais longo em comparação com outras metaheurísticas, devido à natureza iterativa e ao ajuste de parâmetros ao longo do tempo. O MVO se mostrou uma ótima escolha para problemas onde uma exploração mais ampla do espaço de busca é necessária, mas pode ser ajustado para melhorar a velocidade de convergência em problemas menores.
