import sqlite3
import pandas as pd
import numpy as np

# 1. Conexão com o banco de dados existente
print("==========================================")
print("       CONEXÃO COM O BANCO DE DADOS       ")
print("==========================================")
conn = sqlite3.connect('ecommerce_insightflow.db')

print("🚀 Conexão estabelecida com o banco de dados!")

# 2. Carregando os dados para realizar as consultas
df = pd.read_sql_query("SELECT * FROM vendas", conn)

# --- REQUISITO 1: Estatísticas Descritivas ---
print("\n==========================================")
print("   REQUISITO 1: ESTATÍSTICAS DESCRITIVAS  ")
print("==========================================")

# Campos de variáveis a ser usadas
print(df[['Valor_Unitario', 'Quantidade']].describe())

# Volumetria geral de texto
print(f"\nTotal de Pedidos Únicos: {df['ID_Transacao'].nunique()}")
print(f"Total de Clientes Únicos: {df['ID_Cliente'].nunique()}")

# --- REQUISITO 2: Consultas SQL Complexas ---
print("\n==========================================")
print("   REQUISITO 2: CONSULTAS SQL COMPLEXAS   ")
print("==========================================")

# Objetivo: Ranking de faturamento dos produtos dentro de suas respectivas categorias
consulta_complexa = """
WITH FaturamentoProdutos AS (
    SELECT 
        Categoria_Produto,
        Nome_Produto,
        SUM(Quantidade) as Total_Itens,
        SUM(Quantidade * Valor_Unitario) as Faturamento_Total
    FROM vendas
    GROUP BY Categoria_Produto, Nome_Produto
),
RankeamentoProdutos AS (
    SELECT 
        Categoria_Produto,
        Nome_Produto,
        Total_Itens,
        Faturamento_Total,
        DENSE_RANK() OVER (PARTITION BY Categoria_Produto ORDER BY Faturamento_Total DESC) as Rank_Faturamento
    FROM FaturamentoProdutos
)
SELECT 
    Categoria_Produto,
    Nome_Produto,
    Total_Itens,
    Faturamento_Total,
    Rank_Faturamento
FROM RankeamentoProdutos
WHERE Rank_Faturamento <= 3; -- Agora o SQLite aceita o filtro perfeitamente!
"""

df_sql = pd.read_sql_query(consulta_complexa, conn)
print("➔ TOP 3 Produtos Mais Lucrativos por Categoria (Via SQL Window Function):")
print(df_sql.head(15))

# --- REQUISITO 3: CORRELAÇÃO E OUTLIERS (EDA) ---
print("\n==========================================")
print("    REQUISITO 3: CORRELAÇÃO E OUTLIERS    ")
print("==========================================")

# 3.1 Cálculo do Faturamento por linha para encontrar correlações reais
df['Faturamento_Item'] = df['Quantidade'] * df['Valor_Unitario']

# Matriz de Correlação de Pearson
print("➔ Matriz de Correlação entre Variáveis Numéricas:")
print(df[['Valor_Unitario', 'Quantidade', 'Faturamento_Item']].corr())

# 3.2 Detecção de Outliers usando a Regra do IQR (Intervalo Interquartil) para Valor_Unitario
Q1 = df['Valor_Unitario'].quantile(0.25)
Q3 = df['Valor_Unitario'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[(df['Valor_Unitario'] < limite_inferior) | (df['Valor_Unitario'] > limite_superior)]

print(f"\n➔ Detecção de Outliers em 'Valor_Unitario':")
print(f"Limite Superior para Outliers: R$ {limite_superior:.2f}")
print(f"Quantidade de Outliers Encontrados: {len(outliers)} registros")

if len(outliers) > 0:
    print("\nAmostra dos potenciais Outliers (Preços muito acima ou abaixo do padrão):")
    print(outliers[['Nome_Produto', 'Categoria_Produto', 'Valor_Unitario']].head(5))

# Fechando a conexão de forma segura
conn.close()
print("\n🏁 Execução da Sprint 2 finalizada com sucesso!")