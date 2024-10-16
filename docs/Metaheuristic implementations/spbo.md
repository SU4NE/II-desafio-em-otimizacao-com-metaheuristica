O **Student Psychology Based Optimization (SPBO)** simula o processo de aprendizado dos estudantes, onde cada aluno (solução) melhora sua performance com base na autoaprendizagem e na interação com os melhores alunos da turma. Essa abordagem se baseia no princípio de que o aprendizado pode ocorrer tanto internamente (self-learning) quanto externamente, através da comparação e interação com indivíduos mais bem-sucedidos.

### **Fundamentação Teórica**
O **SPBO** combina duas abordagens de aprendizado:
- **Self-learning**: Cada solução (aluno) pode se ajustar por conta própria, fazendo pequenas modificações em seu estado atual.
- **Interação com o melhor**: Soluções também podem aprender observando as soluções mais bem-sucedidas, ajustando suas posições em direção à melhor solução conhecida.

### **Implementação e Adaptações**
No **SPBO**, a população de soluções (alunos) é inicializada aleatoriamente. A cada iteração, as soluções são atualizadas usando uma combinação de autoaprendizagem e interação com a melhor solução. Durante a implementação, foram feitos ajustes nos fatores de aprendizado e interação para garantir uma boa diversidade de soluções e convergência.

### **Variações Testadas**
- **Fator de autoaprendizagem**: Controla a probabilidade de uma solução se ajustar por conta própria. Foi configurado para 0.3.
- **Fator de interação**: Define a chance de uma solução se ajustar com base na melhor solução da população. Foi configurado para 0.7.

### **Justificativa para as Escolhas**
O **SPBO** foi escolhido por seu nome incomum e seu potencial em manter uma boa diversidade na busca, garantindo uma exploração ampla do espaço de soluções, o que é ideal para o **Problema de Empacotamento**. Além disso, a dualidade de aprendizado torna o algoritmo flexível, com capacidade tanto de exploração quanto de explotação.

### **Parâmetros**
- **Tamanho da População**: 7
- **Fator de autoaprendizagem**: 0.3
- **Fator de interação**: 0.7
- **Tempo máximo**: 60 segundos

### **Resultados**
O **SPBO** teve um desempenho excelente, ficando **no Top 6** entre as heurísticas testadas. Ele demonstrou uma consistência impressionante ao encontrar boas soluções rapidamente e manteve um equilíbrio entre exploração e explotação.

### **Discussões**
A heurística se mostrou muito eficaz devido à sua capacidade de manter soluções diversificadas ao longo das iterações. A interação com a melhor solução ajudou a guiar a busca em direção a soluções de alta qualidade. O **SPBO** se provou uma escolha sólida, tanto pelo aprendizado gerado durante a implementação quanto pelo desempenho final.
