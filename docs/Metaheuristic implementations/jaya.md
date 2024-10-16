O **Jaya Optimization Algorithm** foi testado para resolver o **Problema de Empacotamento Unidimensional (BPP)**, utilizando sua abordagem única de mover soluções para mais perto das melhores e se afastar das piores. A meta principal era minimizar o número de caixas utilizadas no empacotamento, com foco em simplificação e eficiência de implementação.

### **Fundamentação Teórica**
O **Jaya** é uma metaheurística baseada no conceito de otimização sem parâmetros que busca diretamente melhorar as soluções sem a necessidade de ajustes complexos. O algoritmo promove o movimento das soluções para perto do melhor resultado enquanto se afasta do pior. Sua simplicidade e ausência de parâmetros como fatores de inércia, coeficientes de aceleração, entre outros, o tornam uma abordagem interessante para problemas de otimização.

### **Implementação e Adaptações**
- **Movimento Direcionado**: Cada iteração do algoritmo ajusta as soluções para mais perto da melhor solução atual, enquanto se afasta da pior.
- **Geração de Novos Candidatos**: Novas soluções são geradas a cada iteração através de ajustes nas posições dos elementos, que são posteriormente reparadas para garantir a validade da solução.
- **Adaptação de Parâmetros**: O algoritmo foi adaptado para manipular populações de soluções e garantir que os limites de capacidade das caixas fossem respeitados após cada iteração.

### **Variações Testadas**
- **Tamanho da População**: Diferentes tamanhos de populações foram avaliados para otimizar o equilíbrio entre exploração e explotação.
- **Número de Iterações**: O número de iterações foi controlado para assegurar uma convergência eficaz sem exceder os limites de tempo.

### **Justificativa para as Escolhas**
A simplicidade do **Jaya Optimization** e sua eficiência computacional o tornaram uma excelente escolha para explorar uma abordagem otimizada para o BPP. A ausência de parâmetros complexos facilita sua implementação e aplicação em diferentes cenários de otimização, tornando-o ideal para problemas como o BPP.

### **Parâmetros**
Os principais parâmetros utilizados foram:
- **População**: 7 soluções iniciais
- **Tempo máximo**: 60 segundos
- **Número de Iterações**: Controlado pelo tempo de execução e convergência

### **Resultados**
O **Jaya Optimization Algorithm** alcançou uma posição no [Top 6](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top6) das heurísticas testadas, com um desempenho muito eficiente em termos de exploração do espaço de busca e explotação de soluções promissoras. Ele conseguiu minimizar o número de caixas utilizadas de maneira eficaz, apresentando soluções próximas do mínimo teórico.

### **Discussões**
O Jaya demonstrou ser uma metaheurística robusta, especialmente pela simplicidade em ajustar as soluções. No entanto, em algumas instâncias maiores, ele mostrou certa limitação na explotação fina de soluções, que poderia ser melhorada com variações mais agressivas na busca local. O foco em aprendizado foi alcançado com sucesso, já que o Jaya mostrou ser uma excelente ferramenta para problemas de otimização como o BPP.
