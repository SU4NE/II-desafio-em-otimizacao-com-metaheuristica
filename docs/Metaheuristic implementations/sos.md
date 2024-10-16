O **Symbiotic Organisms Search (SOS)** é uma metaheurística inspirada na relação simbiótica entre organismos na natureza. O algoritmo simula três tipos de interações biológicas: **mutualismo**, **comensalismo**, e **parasitismo**, onde soluções (organismos) cooperam ou competem para evoluir e melhorar a qualidade da solução. O objetivo final é otimizar a alocação de itens no Problema de Empacotamento Unidimensional (Bin Packing Problem - BPP).

### **Fundamentação Teórica**
No **SOS**, os organismos interagem em três fases:
- **Mutualismo**: Duas soluções se beneficiam mutuamente, movendo-se em direção a um vetor compartilhado.
- **Comensalismo**: Uma solução se beneficia da outra, movendo-se em direção a ela, enquanto a segunda solução não é afetada.
- **Parasitismo**: Uma solução gera um parasita, que tenta substituir a outra solução, caso seja melhor.

### **Implementação e Adaptações**
- **Mutualismo**: Organismos são movidos com base em um vetor médio entre dois organismos, representando a cooperação mútua.
- **Comensalismo**: Um organismo se aproxima de outro sem que o segundo seja afetado.
- **Parasitismo**: Um organismo gera uma versão mutante de si mesmo, tentando substituir outro organismo, em um movimento que simula competição direta.

### **Variações Testadas**
- A principal variação foi ajustar o tamanho da população e o número de interações entre organismos. O comportamento das soluções foi explorado para encontrar o balanço entre exploração e explotação.

### **Justificativa para as Escolhas**
O **SOS** foi escolhido devido à sua capacidade de explorar diferentes áreas do espaço de soluções, ao mesmo tempo em que permite um ajuste fino com interações diversificadas. A escolha de três fases de interação aumenta a diversidade de soluções, o que é crucial em problemas de empacotamento.

### **Parâmetros**
- **Tamanho da População**: 7
- **Tempo Máximo**: 60 segundos
- **Fases**: Mutualismo, Comensalismo e Parasitismo.

### **Resultados**
O **SOS** apresentou um desempenho moderado nas instâncias testadas, ficando **no Top 15**. A heurística mostrou-se eficiente em explorar o espaço de busca, mas não foi tão consistente em todas as instâncias.

### **Discussões**
O algoritmo **SOS** demonstrou ser uma boa alternativa para instâncias de tamanho médio, porém, em instâncias mais complexas ou com maiores exigências de refinamento, ele não conseguiu competir com outras heurísticas mais refinadas. Ajustes nos parâmetros e uma exploração mais controlada poderiam melhorar o desempenho, especialmente em fases mais avançadas da busca.
