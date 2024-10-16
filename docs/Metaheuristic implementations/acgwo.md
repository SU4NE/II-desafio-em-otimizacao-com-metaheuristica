### **Chaotic Grey Wolf Optimization (ACGWO)**

#### **Fundamentação Teórica**
O **Chaotic Grey Wolf Optimization (ACGWO)** é inspirado no comportamento social de caça dos lobos cinzentos. Esse algoritmo baseia-se na hierarquia social dos lobos (alfa, beta e delta) e na coordenação de suas posições durante o processo de caça. A variação caótica introduzida no CGWO tem o objetivo de melhorar a diversidade da população de soluções, permitindo uma exploração mais eficiente do espaço de busca.

No contexto do **Problema de Empacotamento Unidimensional (BPP)**, os lobos representam soluções candidatas (arranjos de itens nas caixas), e o objetivo é minimizar o número de caixas utilizadas para embalar os itens. A função caótica regula os movimentos dos lobos, garantindo que a busca não se prenda em mínimos locais.

#### **Implementação e Adaptações**
A implementação do CGWO inclui três fases principais:
1. **Fase de Alinhamento Hierárquico**: Os lobos alfa, beta e delta representam as três melhores soluções conhecidas, enquanto os demais lobos ajustam suas posições em relação a esses líderes.
2. **Mapeamento Caótico**: A função caótica utilizada (senoidal) é aplicada em cada iteração para introduzir variações nas posições dos lobos, permitindo uma diversificação mais robusta no espaço de soluções.
3. **Fase de Atualização de Posições**: Cada lobo atualiza sua posição com base nas distâncias calculadas entre ele e os lobos alfa, beta e delta. A adição de um fator caótico ajusta a magnitude do movimento, trazendo um componente estocástico ao processo.

Adaptações específicas incluem ajustes nos parâmetros de controle do movimento dos lobos (fator adaptativo e fator caótico) e a implementação de um fator de ajuste dos lobos, que define o impacto do componente caótico nas soluções.

#### **Variações Testadas**
Diferentes variações do ACGWO foram testadas para melhorar o desempenho:
- **Fator de Ajuste do Lobo (wolf_adjustment)**: Testamos valores entre 0.3 e 0.8 para regular a influência do caos na movimentação dos lobos.
- **Tamanho da População**: Foram testados tamanhos de população de 5 a 15 lobos.
- **Função Caótica**: Testamos diferentes funções caóticas (além do seno, como mapas logísticos e cosseno) para explorar diferentes padrões de variação.
- **Coeficiente Adaptativo (a)**: Foi ajustado de acordo com a iteração atual, permitindo que a intensidade dos movimentos diminuísse ao longo do tempo, favorecendo a explotação nas últimas iterações.

#### **Justificativa para as Escolhas**
O CGWO foi escolhido pela sua capacidade inerente de exploração equilibrada com explotação, além da estrutura de hierarquia social, que é particularmente eficiente para otimização global. A adição do componente caótico melhora a diversidade das soluções, o que é crucial para evitar mínimos locais em instâncias mais complexas do BPP. Além disso, no [artigo](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/blob/main/docs/Artigos/CGWO.pdf) é evidenciado a força nesse algoritmo.

#### **Parâmetros**
Os melhores resultados foram obtidos com as seguintes configurações:
- **Tamanho da População**: 7 lobos
- **Wolf Adjustment**: 0.5
- **Máximo de Iterações**: 100
- **Tempo Máximo de Execução**: 60 segundos
- **Fator Adaptativo (a)**: 2 diminuindo linearmente para 0
- **Função Caótica**: Senoidal

#### **Resultados**
O ACGWO apresentou um desempenho notável nas instâncias testadas, sendo capaz de manter uma boa taxa de exploração enquanto refinava soluções promissoras nas últimas iterações. O algoritmo obteve uma classificação no **Top 15** de desempenho no nosso [ranking](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top15).

#### **Discussões**
Embora o CGWO tenha mostrado bons resultados, o uso de componentes caóticos, embora eficiente para evitar mínimos locais, pode introduzir variações excessivas nas últimas iterações, o que pode atrasar a convergência. Ajustes mais finos no fator adaptativo e no tamanho da população podem melhorar a explotação sem comprometer o tempo de execução.
