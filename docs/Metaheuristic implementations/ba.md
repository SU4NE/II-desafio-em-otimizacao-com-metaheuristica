### **Bat Algorithm (BA)**

#### **Fundamentação Teórica**
O **Bat Algorithm (BA)** é inspirado no comportamento de ecolocalização dos morcegos. O algoritmo combina três aspectos principais: **frequência**, **velocidade** e **intensidade do som (loudness)** para guiar a busca por soluções ótimas. A frequência controla a variação das posições dos morcegos, enquanto a loudness regula a busca local, semelhante a um refinamento de solução. O **Bat Algorithm** explora tanto o espaço de busca global quanto realiza buscas locais mais refinadas, ajustando a intensidade do som à medida que o algoritmo converge.

No contexto do **Problema de Empacotamento Unidimensional (BPP)**, cada morcego representa uma solução possível (arranjo dos itens nas caixas), e o objetivo é minimizar o número de caixas usadas.

#### **Implementação e Adaptações**
A implementação do BA para o BPP envolve os seguintes passos:
1. **Atualização da Frequência e Velocidade**: Cada morcego ajusta sua velocidade e posição com base na diferença entre sua posição atual e a melhor posição global. A frequência é ajustada aleatoriamente a cada iteração.
2. **Busca Local com Base na Loudness**: Se o valor da emissão do som for maior que um limiar (definido por \( r \)), o morcego realiza uma busca local, explorando posições ao redor da melhor solução global, o que ajuda a refinar a solução.
3. **Decaimento da Loudness**: Ao longo das iterações, a loudness diminui, indicando que os morcegos estão se concentrando em soluções promissoras, o que favorece a explotação.

Adaptações específicas incluem ajustes na função de busca local para garantir que as soluções encontradas sejam válidas e otimizadas para o problema de empacotamento.

#### **Variações Testadas**
Diferentes variações e configurações foram testadas para melhorar o desempenho:
- **População de morcegos**: O número de morcegos foi ajustado entre 10 e 50 para testar o equilíbrio entre exploração e eficiência computacional.
- **Taxa de emissão de pulso (r)**: Testamos diferentes valores iniciais para a taxa de emissão de pulso, variando entre 0.3 e 0.7.
- **Loudness**: O fator de loudness foi ajustado para valores entre 0.5 e 0.9, para analisar o impacto na busca local.
- **Frequência**: A frequência de movimento foi ajustada em diferentes intervalos, de \(f_{\text{min}} = 0\) a \(f_{\text{max}} = 1\), para controlar a dispersão dos morcegos.

#### **Justificativa para as Escolhas**
O BA foi escolhido por sua flexibilidade em equilibrar exploração global com refinamento local. A combinação de frequências e loudness permite ao algoritmo realizar uma busca global eficiente nas primeiras iterações e, posteriormente, focar em refinar as soluções encontradas. Essa abordagem é particularmente útil para o BPP, que exige uma exploração robusta, seguida de refinamento para minimizar o número de caixas.

#### **Parâmetros**
Os melhores resultados foram alcançados com as seguintes configurações:
- **População de morcegos**: 30
- **Loudness inicial**: 0.5
- **Taxa de emissão de pulso inicial (r)**: 0.5
- **Frequência mínima**: 0
- **Frequência máxima**: 1
- **Fator de decaimento da loudness**: 0.9
- **Máximo de iterações**: 100
- **Tempo máximo de execução**: 60 segundos

#### **Resultados**
O Bat Algorithm apresentou um desempenho competitivo em instâncias de pequeno e médio porte. O algoritmo obteve uma classificação no **Top 10** de desempenho no nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top10), conseguindo boas soluções rapidamente, embora tenha mostrado dificuldade em manter constancia no tempo e em um refinamento eficaz nas iterações finais.

#### **Discussões**
Embora o BA tenha se mostrado eficaz na exploração inicial do espaço de busca, a fase de explotação nas últimas iterações foi limitada, o que pode ser atribuído ao rápido decaimento da loudness. Ajustes mais finos nos parâmetros de loudness e frequência, bem como uma abordagem mais robusta para a busca local, podem ajudar a melhorar o refinamento das soluções, especialmente em problemas de maior complexidade.
