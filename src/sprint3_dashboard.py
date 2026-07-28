import sqlite3
import pandas as pd
import streamlit as np
import streamlit as st
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(page_title="Trilha de Dados - Dashboard", layout="wide", page_icon="📊")

# ==========================================
#          CARREGAMENTO DOS DADOS
# ==========================================
@st.cache_data # Cache para não sobrecarregar o banco gerando rapidez no retorno
def carregar_dados():
    conn = sqlite3.connect('ecommerce_insightflow.db')
    # Carrega os dados convertendo a data para o formato correto
    df = pd.read_sql_query("SELECT * FROM vendas", conn, parse_dates=['Data_Venda'])
    conn.close()
    # Cria a coluna de faturamento por item
    df['Faturamento_Item'] = df['Quantidade'] * df['Valor_Unitario']
    # Extrai Ano/Mês para a análise temporal
    df['Ano_Mes'] = df['Data_Venda'].dt.to_period('M').astype(str)
    return df

df = carregar_dados()

# ==========================================
#     BARRA LATERAL (FILTROS DINÂMICOS)
# ==========================================
st.sidebar.header("🔍 Filtros Avançados")

# Filtro por Categoria de Produto
categorias = ['Todas'] + sorted(df['Categoria_Produto'].unique().tolist())
categoria_selecionada = st.sidebar.selectbox("Selecione a Categoria:", categorias)

# Filtro por Método de Pagamento
pagamentos = ['Todos'] + sorted(df['Metodo_Pagamento'].unique().tolist())
pagamento_selecionado = st.sidebar.selectbox("Método de Pagamento:", pagamentos)

# Aplicação dos filtros no dataframe original
df_filtrado = df.copy()
if categoria_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Categoria_Produto'] == categoria_selecionada]
if pagamento_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Metodo_Pagamento'] == pagamento_selecionado]


# ==========================================
#           CABEÇALHO DO DASHBOARD
# ==========================================
st.title("📊 Desafio Final - Trilha de Dados")
st.subheader("Análise Estratégica de Vendas e Desempenho do E-commerce")
st.markdown("---")


# ==========================================
#    REQUISITO 1: CARD DE KPIs PRINCIPAIS
# ==========================================
# Cálculos dos indicadores
faturamento_total = df_filtrado['Faturamento_Item'].sum()
total_pedidos = df_filtrado['ID_Transacao'].nunique()
ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0
total_clientes = df_filtrado['ID_Cliente'].nunique()

# Exibição em colunas no Streamlit
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="💰 Faturamento Total", value=f"R$ {faturamento_total:,.2f}")
with kpi2:
    st.metric(label="📦 Total de Pedidos", value=f"{total_pedidos:,}")
with kpi3:
    st.metric(label="💳 Ticket Médio", value=f"R$ {ticket_medio:,.2f}")
with kpi4:
    st.metric(label="👥 Clientes Ativos", value=f"{total_clientes:,}")

st.markdown("---")


# ==========================================
#   REQUISITOS 2 E 3: GRÁFICOS INTERATIVOS
# ==========================================
col_esquerda, col_direita = st.columns(2)

with col_esquerda:
    # REQUISITO 2: Gráfico de Série Temporal para Sazonalidade
    st.subheader("📈 Evolução Mensal do Faturamento")
    df_temporal = df_filtrado.groupby('Ano_Mes')['Faturamento_Item'].sum().reset_index()
    
    fig_linha = px.line(
        df_temporal, 
        x='Ano_Mes', 
        y='Faturamento_Item',
        labels={'Ano_Mes': 'Período (Ano-Mês)', 'Faturamento_Item': 'Faturamento (R$)'},
        markers=True,
        template="plotly_dark"
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col_direita:
    # Gráfico de Apoio: Categorias mais lucrativas
    st.subheader("🏆 Faturamento por Categoria")
    df_categoria = df_filtrado.groupby('Categoria_Produto')['Faturamento_Item'].sum().reset_index().sort_values(by='Faturamento_Item', ascending=False)
    
    fig_barra = px.bar(
        df_categoria, 
        x='Faturamento_Item', 
        y='Categoria_Produto',
        orientation='h',
        labels={'Faturamento_Item': 'Faturamento (R$)', 'Categoria_Produto': 'Categoria'},
        template="plotly_dark",
        color='Faturamento_Item',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_barra, use_container_width=True)

# Tabela detalhada opcional no final
if st.checkbox("Visualizar base de dados filtrada"):
    st.dataframe(df_filtrado.head(100))