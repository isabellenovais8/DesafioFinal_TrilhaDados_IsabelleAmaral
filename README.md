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

## ⚙️ Etapas Executadas:
**1. Geração de Dados Simulados:** Criação automatizada de um dataset sintético de e-commerce com 5.200 registros (superando o mínimo de 5.000 exigido) contendo as 10 colunas estratégicas obrigatórias (ID Transação, Data_Venda, ID_Cliente, Nome Produto, Categoria_Produto, Valor_Unitário, Quantidade, Localidade_Venda, Método_Pagamento e Status_Pedido).

**2. Tratamento de Inconsistências (ETL):**
- Localização e eliminação de 40 linhas duplicadas introduzidas propositalmente para validar a robustez do script de limpeza.
- Tratamento de registros nulos na coluna ``Valor_Unitario``, preenchendo as lacunas vazias de forma lógica com a mediana de preço correspondente àquele produto específico.
- Tratamento de valores nulos na coluna ``Status_Pedido``, realizando a imputação da categoria padrão "Desconhecido".

**3. Padronização de Formatos:**
- Conversão do campo ``Data_Venda`` para o formato primitivo de data/tempo do Pandas (``datetime64``).
- Limpeza de espaçamentos inúteis (strip) e padronização de maiúsculas/minúsculas (Title Case) nas colunas textuais.

**4. Armazenamento Relacional:** Exportação da base de dados limpa diretamente para uma tabela relacional chamada ``vendas`` dentro do banco de dados SQLite (``ecommerce_insightflow.db``), garantindo a persistência ideal dos dados para o início da próxima sprint.

## 🚀 Como Executar o Projeto
1. Certifique-se de ter o Python instalado. Ative o seu ambiente virtual e instale as dependências executando:
```text
pip install -r requirements.txt
```

2. Nota sobre o Banco de Dados: O arquivo de banco de dados relacional ``ecommerce_insightflow.db`` já está incluído e consolidado na raiz deste repositório com os dados devidamente tratados.

3. Caso deseje reexecutar todo o ecossistema do pipeline de geração de dados e processamento de ETL do zero, basta rodar o comando:
```text
python src/sprint1_etl.py
```