# Desafio Final - Trilha de Dados 🚀

Bem-vindo(a) ao repositório do projeto **Trilha de Dados**, desenvolvido como parte do Desafio Final do Projeto Desenvolve, que ocorre em Bom Despacho - MG. Este projeto consiste na criação de uma solução analítica ponta a ponta (*end-to-end*) para uma plataforma de e-commerce, cobrindo todo o ciclo de vida dos dados: ETL, armazenamento relacional, análise exploratória (EDA), consultas SQL avançadas, visualização interativa em dashboard e modelagem preditiva com Machine Learning.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python 3.x
* **Manipulação e Análise de Dados:** Pandas, NumPy
* **Banco de Dados Relacional:** SQLite
* **Visualização e Dashboard Interativo:** Streamlit, Plotly
* **Machine Learning & Estatística:** Scikit-Learn (Regressão Linear)
* **Versionamento:** Git e GitHub

---

## 📁 Estrutura do Repositório

```text
.
├── data/
│   └── ecom_data.csv             # Dataset simulado com os registros de vendas
├── sql/
│   └── queries_sprint2.sql       # Consultas SQL analíticas (CTEs + Window Functions)
├── src/
│   ├── sprint1_etl.py            # Pipeline de Ingestão, Limpeza e Carga no Banco
│   ├── sprint2_analysis.py       # Estatística Descritiva, Correlação e IQR Outliers
│   ├── sprint3_dashboard.py      # Aplicação interativa em Streamlit
│   └── sprint4_predictive.py     # Modelo Preditivo de Regressão Linear
├── ecommerce_insightflow.db      # Banco de dados relacional SQLite
├── requirements.txt              # Bibliotecas e dependências do projeto
└── README.md                     # Documentação completa do projeto
```

## 📖 Jornada das Sprints & Metodologia
### 📌 Sprint 1 - Ingestão e ETL (Limpeza de Dados)
Objetivo: Estruturar a pipeline de Ingestão, Tratar inconsistências e popular o banco de dados relacional.

- **Tratamento Realizado:** Remoção de duplicidades, imputação/descarte de dados nulos e conversão de colunas temporais (Data_Venda) para o tipo datetime.
- **Modelagem:** Criação automatizada do banco relacional ecommerce_insightflow.db em SQLite e carga da tabela vendas via Pandas.

### 📌 Sprint 2 - Análise Exploratória (EDA) e SQL
Objetivo: Investigar métricas descritivas, padrões de consumo e aplicar SQL avançado.

- **Estatística Descritiva:** Extração de métricas centrais e de dispersão (média, desvio padrão, mínimos e máximos) para variáveis financeiras e volumétricas.
- **SQL Avançado:** Construção de consulta com CTEs e a Window Function DENSE_RANK() OVER (PARTITION BY Categoria_Produto ORDER BY Faturamento_Total DESC) isolada em sql/queries_sprint2.sql para identificar o TOP 3 produtos mais lucrativos por setor.
- **Detecção de Outliers:** Aplicação do método estatístico do IQR (Intervalo Interquartil) em Valor_Unitario para rastrear distorções de preço no catálogo.

### 📌 Sprint 3 - Visualização e Dashboard Interativo
Objetivo: Construir uma interface gráfica com KPIs de negócio e análise de sazonalidade.

- **Painel Streamlit:** Desenvolvimento de um aplicativo Web local em src/sprint3_dashboard.py.
- **KPIs Principais:** Exibição dinâmica de Faturamento Total, Volume de Pedidos, Ticket Médio e Clientes Ativos.
- **Interatividade:** Gráficos interativos com Plotly (série temporal para sazonalidade e barras horizontais por categoria) responsivos a filtros dinâmicos na barra lateral.

### 📌 Sprint 4 - Storytelling Analítico e Modelo Preditivo
Objetivo: Aplicar Machine Learning para previsão de faturamento do e-commerce.

- **Modelo Preditivo:** Implementação do algoritmo de Regressão Linear (scikit-learn) treinado sobre a série temporal de vendas acumuladas por dia.
- **Avaliação de Desempenho:** Mensuração do erro do modelo utilizando a métrica MAE (Erro Médio Absoluto).
- **Projeção Futura:** Estimativa matemática do volume de faturamento bruto para os próximos 30 dias de operação.

#### 🚀 Como Executar o Projeto
1. Clone o repositório:
```text
git clone [https://github.com/isabellenovais8/DesafioFinal_TrilhaDados_IsabelleAmaral.git](https://github.com/isabellenovais8/DesafioFinal_TrilhaDados_IsabelleAmaral.git)
cd DesafioFinal_TrilhaDados_IsabelleAmaral
```

2. Instale as dependências:
```text
pip install -r requirements.txt
```

3. Execute os scripts em ordem sequencial:
```text
# Passo 1: Executar Ingestão e ETL
python src/sprint1_etl.py

# Passo 2: Executar Análise Exploratória e SQL
python src/sprint2_analysis.py

# Passo 3: Executar a Previsão de Machine Learning
python src/sprint4_predictive.py

# Passo 4: Rodar o Dashboard Interativo no Navegador
streamlit run src/sprint3_dashboard.py
```

*Projeto desenvolvido por Isabelle Amaral para o Desafio Final - Trilha de Dados.*