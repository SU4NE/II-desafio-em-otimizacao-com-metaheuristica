A implementação do **Tabu Search (TS)** para o **Problema de Empacotamento (Bin Packing Problem - BPP)** foi desenvolvida, mas, infelizmente, ficou fora do **Top 15** em termos de desempenho. O Tabu Search é um algoritmo de otimização baseado em busca local que evita cair em mínimos locais ao usar uma estrutura tabu para impedir que certas soluções já exploradas sejam revisitadas por um período de tempo. A heurística tem o potencial de refinar soluções exploradas, mas a implementação neste caso não conseguiu apresentar bons resultados, principalmente devido à falta de tempo para ajustes mais refinados.

### **Fundamentação Teórica**
O **Tabu Search** trabalha com a ideia de evitar ciclos de busca repetitiva em torno de soluções previamente visitadas. Isso é feito ao colocar certos movimentos em uma lista tabu, que é uma memória de curto prazo que impede que o algoritmo revisite essas soluções durante um determinado número de iterações.

### **Implementação e Adaptações**
Durante a implementação, foram feitas adaptações no tamanho da lista tabu (controlada pelo parâmetro **alpha**) e na função de busca por novas soluções. A cada iteração, dois elementos da solução atual são trocados, e essa operação é bloqueada por um número de iterações controlado pela lista tabu.

### **Variações Testadas**
- **Alpha**: O valor de **alpha** foi testado com diferentes valores para tentar ajustar o tamanho da lista tabu e evitar ciclos, com **4** sendo o valor padrão utilizado.
- **Estrutura Tabu**: Foi implementada uma estrutura específica para impedir revisitações de movimentos durante um certo número de iterações.

### **Justificativa para as Escolhas**
O **Tabu Search** foi escolhido por ser uma abordagem robusta para busca local, especialmente em problemas onde mínimos locais são um problema. No entanto, a complexidade de ajustes e refatoração para problemas de otimização combinatória como o BPP exigem maior atenção no ajuste dos parâmetros e nas operações.

### **Parâmetros**
- **Alpha**: 4 (afeta o tamanho da lista tabu)
- **Tempo máximo**: 60 segundos

### **Resultados**
O algoritmo não conseguiu resultados competitivos, ficando fora do **Top 15**. Isso se deve principalmente à necessidade de maior refatoração e ajuste de parâmetros para permitir que a busca tabu desempenhasse de forma mais eficiente, especialmente em instâncias maiores.

### **Discussões**
Apesar do potencial, o **Tabu Search** nesta implementação não foi capaz de competir com outras heurísticas mais sofisticadas. Com mais tempo de ajuste e experimentação de variações no tamanho da lista tabu e no processo de busca local, o algoritmo poderia ter se mostrado mais promissor.
