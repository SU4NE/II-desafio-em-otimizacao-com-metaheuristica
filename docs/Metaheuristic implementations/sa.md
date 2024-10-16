O **Simulated Annealing (SA)**, inspirado no processo de recozimento de metais, é uma técnica clássica de otimização que tenta simular o processo de resfriamento lento, onde soluções de menor qualidade são aceitas com uma certa probabilidade durante o início da busca. Conforme a temperatura do sistema diminui, a chance de aceitar soluções piores também diminui, direcionando o algoritmo para a busca local na vizinhança de soluções promissoras.

### **Fundamentação Teórica**
O **SA** utiliza uma função de temperatura que controla a probabilidade de aceitar soluções piores, permitindo que o algoritmo escape de mínimos locais e, com o tempo, converge para um ótimo local à medida que a temperatura diminui. Isso equilibra a exploração (busca em diferentes regiões do espaço) e a explotação (refinamento de soluções).

### **Implementação e Adaptações**
- **Perturbação de Solução**: Durante cada iteração, uma solução é perturbada movendo itens entre diferentes caixas.
- **Aceitação de Soluções**: As soluções são aceitas com base na diferença entre o fitness da solução atual e da nova solução, e na temperatura atual. Se a nova solução for melhor, ela é automaticamente aceita; se for pior, pode ser aceita com uma certa probabilidade.
- **Resfriamento**: Após cada iteração, a temperatura do sistema é reduzida de acordo com uma taxa de resfriamento (\(\alpha\)) até que a temperatura mínima seja atingida.

### **Variações Testadas**
- **Temperatura Inicial**: O valor inicial foi definido como muito alto para garantir que o algoritmo possa explorar amplamente o espaço de soluções.
- **Taxa de Resfriamento (\(\alpha\))**: O valor de \(\alpha = 0.9\) foi escolhido após experimentação, garantindo que o resfriamento ocorra de forma gradual, evitando uma convergência prematura.
- **Iterações por Temperatura**: Um número fixo de 100 iterações por temperatura foi utilizado para garantir que a busca em cada nível de temperatura seja suficientemente extensa.

### **Justificativa para as Escolhas**
O **SA** foi escolhido por sua simplicidade e eficiência em problemas combinatórios como o BPP. Sua capacidade de aceitar soluções piores durante as fases iniciais permite escapar de mínimos locais, tornando-o robusto em instâncias complexas.

### **Parâmetros**
- **Temperatura Inicial**: \(1e9\)
- **Temperatura Mínima**: \(1e-9\)
- **Taxa de Resfriamento (\(\alpha\))**: 0.9
- **Número de Iterações por Temperatura**: 100

### **Resultados**
Embora o **SA** tenha mostrado bons resultados em termos de exploração inicial do espaço de soluções, ele não conseguiu manter a consistência ao longo do tempo. O algoritmo ficou **fora do Top 15**, mesmo com sua boa performance nas fases iniciais da busca.

### **Discussões**
O **SA** mostrou potencial ao escapar de mínimos locais, mas não foi capaz de competir com outras heurísticas mais robustas, especialmente devido à sua performance variável e à falta de capacidade de explotação mais refinada em instâncias maiores do BPP. Ajustes mais finos nos parâmetros de resfriamento ou uma abordagem híbrida poderiam melhorar a estabilidade dos resultados.
