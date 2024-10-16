A implementação do **Improved Coati Optimization Algorithm (TNTWCOA)** para o **Problema de Empacotamento (Bin Packing Problem - BPP)** se destacou como uma heurística promissora, com o uso de uma combinação de inicialização caótica e uma distribuição adaptativa em T para melhorar o balanceamento entre exploração e explotação. Essa nova abordagem foi discutida em um [artigo](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Artigos/An%20improved%20Coati%20Optimization%20Algorithm%20with%20multiple%20strategies%20for%20engineering%20design%20optimization%20problems.pdf) recente lançado em setembro de 2024, mostrando sua eficácia em vários problemas de otimização. No contexto do nosso desafio, o algoritmo ficou no **Top 10**, chegando perto do **Top 6**, o que demonstra sua consistência e potencial.

### **Fundamentação Teórica**
O **TNTWCOA** se baseia na biologia comportamental do **quati** e combina várias estratégias para otimizar a exploração e explotação. Ele introduz uma fase de **inércia não linear** que ajusta gradualmente o peso das partículas ao longo das iterações, além de uma fase de **distribuição adaptativa em T**, que amplia a diversidade da população.

### **Implementação e Adaptações**
- **Inicialização Caótica**: Utilizou-se uma inicialização baseada no **Tent Chaos**, que gera uma população inicial com características aleatórias, mas distribuídas de forma não linear para explorar melhor o espaço de busca.
- **Peso de Inércia Não Linear**: Foi implementado um mecanismo de peso de inércia não linear para ajustar dinamicamente a exploração e explotação ao longo das iterações, com parâmetros ajustáveis de **w_max** e **w_min**.
- **Distribuição Adaptativa em T**: A fase de explotação utiliza uma distribuição em T adaptativa para gerar variações nos indivíduos da população de forma controlada e melhorar a capacidade de exploração de novas soluções.

### **Variações Testadas**
- **População**: Testou-se o algoritmo com diferentes tamanhos de população, sendo o valor padrão utilizado **7** indivíduos.
- **Peso de Inércia**: Variações nos valores de **w_max** e **w_min** foram aplicadas para testar diferentes intensidades de exploração e explotação.
- **Distribuição em T**: A fase adaptativa utilizou variações em T com diferentes fatores de escala, otimizando a distribuição das soluções.

### **Justificativa para as Escolhas**
Escolhemos o **TNTWCOA** por ser uma heurística de última geração, descrita em um artigo recente, que mostrou resultados promissores em problemas de design de engenharia. A combinação de inicialização caótica com a distribuição adaptativa em T proporciona uma flexibilidade única no balanceamento de exploração e explotação, característica essencial para problemas combinatórios como o BPP.

### **Parâmetros**
- **População**: 7 indivíduos.
- **Peso de Inércia**: Variando de **0.9** a **0.4**.
- **Fator de Distribuição em T**: Escala de **1.0** para adaptação das variações.

### **Resultados**
O **TNTWCOA** conseguiu um desempenho sólido, ficando entre os **Top 10**, muito próximo do **Top 6**. O algoritmo mostrou-se eficiente tanto em instâncias pequenas quanto em grandes, mantendo uma boa estabilidade e resultados consistentes.

### **Discussões**
Apesar de não ter chegado ao **Top 6**, o **TNTWCOA** apresentou-se como uma das heurísticas mais consistentes no desafio, especialmente considerando sua recente criação. O equilíbrio entre exploração inicial e explotação avançada garantiu que o algoritmo fosse capaz de encontrar boas soluções rapidamente. No entanto, com mais ajustes nos parâmetros de peso de inércia e distribuição adaptativa, ele poderia facilmente se posicionar ainda melhor no ranking.

