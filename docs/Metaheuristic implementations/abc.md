### **Artificial Bee Colony (ABC)**

#### **Fundamentação Teórica**
O **Artificial Bee Colony (ABC)** é inspirado no comportamento natural das abelhas ao procurar e coletar alimentos. O algoritmo utiliza três tipos de abelhas: **abelhas empregadas**, que exploram soluções candidatas (fontes de alimento); **abelhas observadoras**, que avaliam as fontes com base na qualidade (fitness); e **abelhas scouts**, que procuram aleatoriamente novas fontes de alimento quando uma solução não apresenta mais melhorias.

No contexto do Problema de Empacotamento Unidimensional (BPP), cada fonte de alimento representa uma solução (distribuição de itens em caixas), e o objetivo é minimizar o número de caixas usadas para empacotar todos os itens.

#### **Implementação e Adaptações**
A implementação do ABC para o BPP inclui três principais fases:
1. **Fase das Abelhas Empregadas**: Cada abelha empregada explora uma solução gerando pequenas alterações (busca local). Se a nova solução tiver um melhor fitness (menos caixas usadas), ela substitui a anterior.
2. **Fase das Abelhas Observadoras**: Baseada na qualidade das soluções encontradas pelas abelhas empregadas, as observadoras escolhem probabilisticamente uma solução para explorar.
3. **Fase das Abelhas Scouts**: Quando uma abelha não consegue melhorar sua solução após várias tentativas, ela se torna uma abelha scout e explora uma nova solução aleatoriamente.

Adaptações incluem um mecanismo de busca local para melhorar soluções em cada fase e um limite para tentativas fracassadas, forçando a redefinição de soluções estagnadas.

#### **Variações Testadas**
Durante o desenvolvimento, foram testadas diferentes variações e parâmetros:
- **Número de abelhas empregadas**: Variamos entre 7 e 15 abelhas para encontrar o melhor equilíbrio entre exploração e explotação.
- **Parâmetro gama**: Ajustamos o valor de gama para melhorar a probabilidade de seleção das abelhas observadoras, testando valores entre 1.5 e 2.0.
- **Limite de tentativas fracassadas (Scout)**: Testamos limites diferentes para abelhas que não conseguiam melhorar suas soluções, com valores entre 5 e 15 tentativas.

#### **Justificativa para as Escolhas**
O ABC foi escolhido por sua simplicidade e capacidade de explorar amplamente o espaço de busca, enquanto mantém uma estratégia eficiente de explotação por meio das abelhas observadoras. A estrutura natural do ABC permite um equilíbrio entre a exploração global (abelhas scouts) e a explotação local (abelhas empregadas e observadoras), tornando-o uma escolha adequada para o BPP.

#### **Parâmetros**
Os melhores resultados foram alcançados com os seguintes parâmetros:
- **Número de abelhas empregadas**: 10
- **Número de abelhas observadoras**: 7
- **Limite de tentativas fracassadas (Scout)**: 10
- **Parâmetro gama**: 1.8
- **Máximo de iterações**: 100
- **Tempo máximo de execução**: 60 segundos

#### **Resultados**
O ABC apresentou um desempenho consistente nas instâncias testadas conseguindo o [Top 6](https://github.com/SU4NE/II-desafio-em-otimizacao-com-metaheuristica/tree/main/docs/Graphics/Top6) na nossa classificação, contudo dentre os outros nesse nivel obteve um tempo de execução medio alto.

#### **Discussões**
Embora o ABC tenha uma excelente capacidade de exploração inicial, a explotação pode ser limitada, especialmente em problemas maiores. A fase das abelhas scouts é vantajosa para diversificação do espaço de busca, mas pode ser ineficiente quando há uma necessidade maior de refinar soluções. Ajustes no número de abelhas e nos parâmetros de busca poderiam melhorar o desempenho em instâncias mais complexas do BPP.
