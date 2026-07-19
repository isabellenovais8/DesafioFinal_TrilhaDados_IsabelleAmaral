# Desafio Final - Trilha de Dados 🚀

Este repositório contém o desenvolvimento do desafio final da Trilha de Dados do Projeto Desenvolve, que ocorre em Bom Despacho - MG, focado em transformar dados brutos de um e-commerce em inteligência de negócio através de processos de ETL, análise SQL avançada, dashboards interativos e modelos preditivos.

## 📂 Estrutura do Projeto
```text
├── data/
│   └── ecom_data.csv            # CSV com mais de 5.000 linhas
├── src/
│   └── sprint1_etl.py           # Script para geração do CSV com dados para serem utilizados no projeto
├── requirements.txt             # Dependências do projeto
├── ecommerce_insightflow.db     # Banco de dados SQLite tratado
└── README.md                    # Documentação do projeto
```

## 🛠️ Tecnologias Utilizadas
- Linguagem: Python
- Bibliotecas de Análise: Pandas e NumPy
- Banco de Dados: SQLite3
- Versionamento: Git / GitHub

## 📅 Histórico de Entregas (Sprints)
### 📌 Sprint 1 - Ingestão e ETL (Limpeza de Dados)
Objetivo: Preparar o conjunto de dados e estruturar o armazenamento relacional para as próximas análises.

#### ⚙️ Etapas Executadas:
**1. Geração de Dados Simulados:** Criação automatizada de um dataset sintético de e-commerce com 5.200 registros (superando o mínimo de 5.000 exigido) contendo as 10 colunas estratégicas obrigatórias (ID Transação, Data_Venda, ID_Cliente, Nome Produto, Categoria_Produto, Valor_Unitário, Quantidade, Localidade_Venda, Método_Pagamento e Status_Pedido).

**2. Tratamento de Inconsistências (ETL):**
- Localização e eliminação de 40 linhas duplicadas introduzidas propositalmente para validar a robustez do script de limpeza.
- Tratamento de registros nulos na coluna ``Valor_Unitario``, preenchendo as lacunas vazias de forma lógica com a mediana de preço correspondente àquele produto específico.
- Tratamento de valores nulos na coluna ``Status_Pedido``, realizando a imputação da categoria padrão "Desconhecido".

**3. Padronização de Formatos:**
- Conversão do campo ``Data_Venda`` para o formato primitivo de data/tempo do Pandas (``datetime64``).
- Limpeza de espaçamentos inúteis (strip) e padronização de maiúsculas/minúsculas (Title Case) nas colunas textuais.

**4. Armazenamento Relacional:** Exportação da base de dados limpa diretamente para uma tabela relacional chamada ``vendas`` dentro do banco de dados SQLite (``ecommerce_insightflow.db``), garantindo a persistência ideal dos dados para o início da próxima sprint.

#### 🚀 Como Executar o Projeto
1. Certifique-se de ter o Python instalado. Ative o seu ambiente virtual e instale as dependências executando:
```text
pip install -r requirements.txt
```

2. Nota sobre o Banco de Dados: O arquivo de banco de dados relacional ``ecommerce_insightflow.db`` já está incluído e consolidado na raiz deste repositório com os dados devidamente tratados.

3. Caso deseje reexecutar todo o ecossistema do pipeline de geração de dados e processamento de ETL do zero, basta rodar o comando:
```text
python src/sprint1_etl.py
```

### 📌 Sprint 2 - Análise Exploratória (EDA) e SQL
**Objetivo:** Extrair métricas descritivas, investigar padrões de negócio e aplicar análises estatísticas utilizando Python e consultas estruturadas em SQL.

#### 📂 Nova Estrutura de Arquivos:
```text
├── sql/
│   └── queries_sprint2.sql      # Script com a consulta SQL
├── src/
│   ├── sprint1_etl.py
│   └── sprint2_analysis.py      # Script de automação para execução das consultas
```

#### ⚙️ Etapas Executadas:
**1. Estatísticas Descritivas (Requisito 1):** Utilização do método ``.describe()`` do Pandas para extrair automaticamente métricas de tendência central (média, mediana) e dispersão (desvio padrão, valores mínimos e máximos) para as variáveis ``Valor_Unitario`` e ``Quantidade``.

**2. Consultas SQL Complexas (Requisito 2):** Desenvolvimento de uma query otimizada utilizando **CTEs encadeadas e a Window Function** ``DENSE_RANK() OVER (PARTITION BY... )`` para mapear o ranking de faturamento dos produtos dentro de cada categoria biológica/comercial de forma nativa no SQLite, filtrando apenas o TOP 3 mais relevante de cada setor.

**3. Análise de Correlação e Outliers (Requisito 3):**
- Aplicação da Matriz de Correlação de Pearson para avaliar a força da relação entre preço, quantidade e faturamento total.
- Implementação da **Regra do IQR (Intervalo Interquartil)** para detecção matemática de outliers na precificação dos produtos (``Valor_Unitario``), isolando registros que fogem do padrão esperado do e-commerce.

#### 🚀 Como Executar as Análises da Sprint 2
```text
python src/sprint2_analysis.py
```