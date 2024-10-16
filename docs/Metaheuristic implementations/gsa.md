O **Gravitational Search Algorithm (GSA)**, aplicado ao **Problema de Empacotamento Unidimensional (BPP)**, demonstrou um desempenho notável, posicionando-se como uma das melhores metaheurísticas testadas em termos de qualidade das soluções. A ideia central do GSA é utilizar a força gravitacional para mover partículas (soluções) em direção a outras partículas com melhores soluções, simulando o comportamento gravitacional de corpos celestes.

### **Fundamentação Teórica**
O GSA é uma técnica de otimização baseada em um sistema multi-agente onde cada solução é considerada uma partícula com massa, sendo a força gravitacional a principal responsável pela interação entre as soluções. Partículas com melhor fitness (soluções melhores) exercem uma força maior, influenciando as outras partículas a se moverem na direção dessas soluções mais promissoras.

### **Implementação e Adaptações**
- **Força Gravitacional**: A força entre duas partículas foi calculada com base na distância entre elas e a gravidade foi ajustada ao longo do tempo (decaimento gravitacional).
- **Movimento de Partículas**: O movimento de cada partícula foi ajustado pela força resultante das outras partículas, com restrições nos valores para garantir que as soluções permanecessem dentro dos limites do problema.
- **Velocidade e Massa**: A velocidade das partículas foi atualizada iterativamente, com base na força recebida e na massa de cada partícula (a massa é proporcional ao fitness da solução).

### **Variações Testadas**
- **Decaimento Gravitacional**: Diferentes taxas de decaimento da gravidade foram testadas para balancear exploração e explotação.
- **Tamanho da População**: O tamanho da população foi ajustado em vários testes, com valores entre 7 e 10.
- **Atualização de Massa**: Diferentes métodos para calcular a massa das partículas com base no fitness foram experimentados.

### **Justificativa para as Escolhas**
A escolha do **GSA** foi justificada pela sua capacidade de explorar e explotar simultaneamente grandes espaços de busca. A natureza gravitacional do algoritmo promove um balanceamento natural entre a busca local e a global, onde soluções melhores têm um impacto maior nas iterações subsequentes.

### **Parâmetros**
As configurações otimizadas para o **GSA** foram:
- **Tamanho da População**: 7 partículas
- **Decaimento da Gravidade (grav_decay)**: 0.99
- **Tempo máximo de execução**: 60 segundos

### **Resultados**
O **GSA** alcançou a **melhor classificação geral** no desafio, perdendo apenas para o **PSO** em termos de tempo médio de execução. Suas soluções consistentes e de alta qualidade o colocaram no **Top 3** no [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/top3), com destaque para o desempenho em instâncias de tamanho médio e grande.

### **Discussões**
O GSA provou ser uma das heurísticas mais eficazes no contexto do BPP, oferecendo um equilíbrio entre exploração e explotação. A natureza adaptativa do algoritmo permitiu que ele encontrasse soluções competitivas sem ficar preso em mínimos locais. Embora o tempo de execução tenha sido um pouco maior do que o do **PSO**, a qualidade das soluções mais que compensou essa diferença. Ajustes adicionais no decaimento gravitacional e no tamanho da população podem oferecer ainda melhores resultados em problemas mais complexos.
