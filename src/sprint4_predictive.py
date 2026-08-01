import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

print("==========================================")
print(" 🚀 SPRINT 4: MODELAGEM PREDITIVA (ML)   ")
print("==========================================")

# 1. Carregamento e Preparação dos Dados
conn = sqlite3.connect('ecommerce_insightflow.db')
df = pd.read_sql_query("SELECT * FROM vendas", conn, parse_dates=['Data_Venda'])
conn.close()

# Agrupando faturamento por dia para criar a série temporal de previsão
df['Faturamento_Item'] = df['Quantidade'] * df['Valor_Unitario']
df_diario = df.groupby('Data_Venda')['Faturamento_Item'].sum().reset_index()

# Ordena por data
df_diario = df_diario.sort_values('Data_Venda')

# Criação de Feature de Tempo (Dia sequencial)
df_diario['Dia_Sequencial'] = np.arange(len(df_diario))

# 2. Divisão em Variáveis de Treino e Teste
X = df_diario[['Dia_Sequencial']]  # Feature (Tempo)
y = df_diario['Faturamento_Item']  # Target (Faturamento)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# 3. Treinamento da Regressão Linear
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# 4. Avaliação do Modelo
y_pred = modelo.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n📊 Métricas de Desempenho do Modelo:")
print(f"➔ Erro Médio Absoluto (MAE): R$ {mae:,.2f}")
print(f"➔ Coeficiente de Determinação (R² Score): {r2:.4f}")

# 5. Previsão para os Próximos 30 Dias
ultimo_dia = df_diario['Dia_Sequencial'].max()
dias_futuros = pd.DataFrame({'Dia_Sequencial': [ultimo_dia + i for i in range(1, 31)]})

previsoes_futuras = modelo.predict(dias_futuros)
faturamento_previsto_proximo_mes = previsoes_futuras.sum()

print("\n🔮 PREVISÃO PARA O PRÓXIMO MÊS:")
print(f"➔ Faturamento Estimado para os Próximos 30 Dias: R$ {faturamento_previsto_proximo_mes:,.2f}")
print("==========================================\n")
