import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import random

# ==============================================================================
# 1. GERAÇÃO DE DADOS SIMULADOS
# ==============================================================================
print("Iniciando geração de dados simulados...")

np.random.seed(42)
random.seed(42)
n_rows = 5200 # Garante o mínimo de 5.000 linhas exigido

categorias = {
    'Eletrônicos': ['Smartphone', 'Notebook', 'Fone de Ouvido', 'Smartwatch'],
    'Vestuário': ['Camiseta', 'Calça Jeans', 'Tênis', 'Jaqueta'],
    'Casa': ['Luminária', 'Jogo de Cama', 'Cafeteira', 'Cadeira Escritório'],
    'Livros': ['Ficção Científica', 'Biografia', 'Desenvolvimento Pessoal', 'História']
}

cidades = [('São Paulo', 'SP', 'Brasil'), ('Rio de Janeiro', 'RJ', 'Brasil'), 
           ('Bom Despacho', 'MG', 'Brasil'), ('Curitiba', 'PR', 'Brasil'),
           ('Salvador', 'BA', 'Brasil')]

metodos_pagamento = ['Cartão de Crédito', 'Pix', 'Boleto Bancário']
status_pedido = ['Concluído', 'Concluído', 'Concluído', 'Cancelado', 'Em Processamento'] #Repetindo o status "Concluído" para que tenha maior probabilidade, visto que é o status mais comum

data_inicial = datetime(2025, 1, 1)

dados = []
for i in range(1, n_rows + 1):
    categoria = random.choice(list(categorias.keys()))
    produto = random.choice(categorias[categoria])
    cidade, estado, pais = random.choice(cidades)
    
    # Gerando datas ao longo de 2025 e início de 2026
    data_venda = data_inicial + timedelta(days=random.randint(0, 400), minutes=random.randint(0, 1439))
    
    dados.append({
        'ID_Transacao': f"TX_{10000 + i}",
        'Data_Venda': data_venda.strftime('%Y-%m-%d %H:%M:%S'),
        'ID_Cliente': f"CLI_{random.randint(100, 999)}",
        'Nome_Produto': produto,
        'Categoria_Produto': categoria,
        'Valor_Unitario': round(random.uniform(15.0, 3500.0), 2),
        'Quantidade': random.randint(1, 5),
        'Localidade_Venda': f"{cidade}/{estado}/{pais}",
        'Metodo_Pagamento': random.choice(metodos_pagamento),
        'Status_Pedido': random.choice(status_pedido)
    })

df_raw = pd.DataFrame(dados)

# Inserindo inconsistências propositais para o ETL tratar
df_raw.loc[df_raw.sample(50).index, 'Valor_Unitario'] = np.nan
df_raw.loc[df_raw.sample(30).index, 'Status_Pedido'] = np.nan
df_raw = pd.concat([df_raw, df_raw.sample(40)], ignore_index=True) # Duplicados

# Salva o arquivo bruto solicitado
df_raw.to_csv('ecom_data.csv', index=False)
print("-> Arquivo 'ecom_data.csv' gerado com sucesso!")


# ==============================================================================
# 2. PROCESSO DE ETL / LIMPEZA DE DADOS
# ==============================================================================
print("\nIniciando processo de ETL...")

# Carga
df = pd.read_csv('ecom_data.csv')

# Requisito 1: Tratar valores duplicados e nulos
duplicados_removidos = df.duplicated().sum()
df.drop_duplicates(inplace=True)

# Preenchendo valores nulos de forma lógica
df['Valor_Unitario'] = df.groupby('Nome_Produto')['Valor_Unitario'].transform(lambda x: x.fillna(x.median()))
df['Status_Pedido'] = df['Status_Pedido'].fillna('Desconhecido')

# Requisito 2: Padronizar formatos de dados (Datas e Textos)
df['Data_Venda'] = pd.to_datetime(df['Data_Venda'])
df['Nome_Produto'] = df['Nome_Produto'].str.strip().str.title()
df['Categoria_Produto'] = df['Categoria_Produto'].str.strip().str.title()

# Criando coluna de Faturamento para facilitar o SQL e dashboards futuros
df['Faturamento_Total'] = df['Valor_Unitario'] * df['Quantidade']

print(f"-> Remoção de Duplicados: {duplicados_removidos} linhas removidas.")
print(f"-> Valores nulos tratados.")
print(f"-> Formatos padronizados com sucesso.")


# ==============================================================================
# 3. CRIAÇÃO DO BANCO RELACIONAL E CARGA
# ==============================================================================
print("\nCarregando dados no banco relacional SQLite...")

# Conecta ao banco (será criado localmente como arquivo)
conn = sqlite3.connect('ecommerce_insightflow.db')

# Salva o dataframe tratado como uma tabela no banco de dados
df.to_sql('vendas', conn, if_exists='replace', index=False)

# Validação rápida via SQL
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*), SUM(Faturamento_Total) FROM vendas")
qtd, faturamento_total = cursor.fetchone()

print(f"-> Banco 'ecommerce_insightflow.db' estruturado.")
print(f"-> Total de registros na tabela 'vendas': {qtd}")
print(f"-> Faturamento Total Armazenado: R$ {faturamento_total:,.2f}")

conn.close()
print("\nSprint 1 concluída com sucesso!")