O **Memetic Algorithm** implementado para o **Problema de Empacotamento Unidimensional (BPP)** obteve uma posição no **Top 10** do nosso ranking, combinando conceitos de algoritmos genéticos com a busca local para melhorar soluções. A abordagem com elitismo garantiu que as melhores soluções fossem mantidas ao longo das gerações, enquanto a busca local refinou as soluções intermediárias, resultando em um desempenho sólido.

### **Fundamentação Teórica**
O **Memetic Algorithm (MA)** é uma variante de algoritmos genéticos que incorpora uma busca local para melhorar as soluções de cada geração. Além de aplicar cruzamento e mutação como em algoritmos genéticos tradicionais, ele utiliza métodos de busca local para ajustar as soluções e explorar melhor o espaço de busca. Esse equilíbrio entre a exploração global (crossover e mutação) e a explotação local (busca local) permite alcançar soluções de alta qualidade de forma eficiente.

### **Implementação e Adaptações**
- **Crossover**: Foi utilizado um ponto de cruzamento aleatório para gerar soluções filhas, mesclando as melhores características dos pais.
- **Mutação**: A mutação foi aplicada alterando um valor aleatório da solução, garantindo que novas soluções fossem exploradas.
- **Busca Local**: Após o crossover e mutação, cada solução foi refinada por meio de uma busca local, o que permitiu encontrar soluções otimizadas no espaço de busca.
- **Elitismo**: As melhores soluções foram preservadas em cada geração, assegurando que o algoritmo não perdesse boas soluções ao longo da execução.

### **Variações Testadas**
- **Tamanho da População**: Diferentes tamanhos de população foram testados para encontrar o equilíbrio entre exploração do espaço de busca e velocidade de execução.
- **Taxa de Mutação**: A taxa de mutação foi ajustada para diferentes níveis de variabilidade entre as soluções, permitindo avaliar como a diversidade impactava na qualidade final das soluções.

### **Justificativa para as Escolhas**
O **Memetic Algorithm** foi escolhido por sua capacidade de combinar a busca global de algoritmos genéticos com a explotação refinada de busca local. Esta combinação é particularmente útil em problemas de empacotamento, onde pequenas variações podem levar a soluções significativamente melhores. A inclusão de elitismo também foi fundamental para garantir que as melhores soluções não fossem perdidas no processo de evolução.

### **Parâmetros**
Os principais parâmetros utilizados foram:
- **População**: 8 soluções iniciais (ajustada para um número par)
- **Tempo máximo**: 60 segundos
- **Número de Iterações**: Controlado pelo tempo de execução e convergência

### **Resultados**
O **Memetic Algorithm** alcançou uma posição no [Top 10](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top10) em nosso ranking de heurísticas. Ele se destacou por sua habilidade de refinar soluções, conseguindo empacotamentos eficientes com o uso mínimo de caixas. Sua combinação de exploração e explotação o tornou competitivo, mesmo em instâncias complexas e de grande escala.

### **Discussões**
O desempenho do **Memetic Algorithm** foi sólido, mas sua execução mostrou ser um pouco mais lenta em algumas instâncias quando comparado a outras heurísticas. Isso se deve ao tempo adicional gasto na busca local, que, embora melhore a qualidade das soluções, também aumenta o tempo de execução. No entanto, os resultados alcançados demonstram que esse custo adicional vale a pena, já que soluções otimizadas foram obtidas consistentemente. O algoritmo poderia ser ajustado para otimizar melhor o tempo de execução sem sacrificar a qualidade das soluções.
