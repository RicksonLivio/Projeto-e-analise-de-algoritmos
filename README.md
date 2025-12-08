# 📘 Projeto e Análise de Algoritmos

#### Repositório criado para armazenar os experimentos e materiais desenvolvidos na disciplina Projeto e Análise de Algoritmos, pertencente ao Mestrado Acadêmico em Ciência da Computação — Turma 2025.2.

#### O objetivo deste repositório é organizar códigos, análises, relatórios e demais atividades práticas realizadas ao longo da disciplina, servindo como base de estudos, reprodutibilidade e acompanhamento da evolução dos experimentos.

# 🔍 Experimento de Comparação de Desempenho entre Algoritmos
## 📌 Contexto: Fraudes em Transações Financeiras

#### O objetivo deste experimento é identificar, de forma eficiente, três transações financeiras cujos valores somam exatamente um valor alvo fornecido como entrada.

#### O problema envolve vetores de valores de transações variando de 10³ a 10⁵ elementos, exigindo abordagens capazes de lidar com diferentes níveis de complexidade e volume de dados.

# ⚙️ Algoritmos a Serem Comparados
## 1. Verificação Ingênua — O(n³)

#### Busca exaustiva testando todas as combinações possíveis de três elementos.

## 2. Algoritmo com Ordenação + Divisão e Conquista

#### Após ordenar o vetor, utiliza estratégias de busca mais eficientes para reduzir drasticamente o número de combinações a serem verificadas.

## 3. HashMap para Comparação

#### Aproveita estrutura de hashing para localizar complementos de forma eficiente, reduzindo a complexidade em relação às abordagens tradicionais.

# 🧪 Metodologia do Experimento

#### Para realizar a comparação de desempenho, serão gerados vetores aleatórios simulando valores de transações financeiras. Com base nesses vetores, avaliamos o tempo de execução de cada algoritmo, observando:

#### ► Escalabilidade

#### ► Robustez

#### ► Impacto do tamanho do vetor no desempenho

#### ► Eficiência prática em cenários reais de detecção de fraude