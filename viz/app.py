import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path

# Configuração da Página
st.set_page_config(page_title="Raio-X da Inflação", layout="wide", page_icon="📊")

# Função para carregar os dados
@st.cache_data
def carregar_dados(query):
    current_dir = Path.cwd()
    if current_dir.name == 'viz':
        db_path = current_dir.parent / 'src' / 'inflacao_brasil.db'
    else:
        db_path = current_dir / 'src' / 'inflacao_brasil.db'
        
    conn = sqlite3.connect(db_path)
    # parse_dates já garante que o Pandas entenda a coluna como tempo
    df = pd.read_sql_query(query, conn, parse_dates=['mes']) 
    conn.close()
    return df

# Configurar a sidebar

with st.sidebar:
    st.title("Raio-X da Inflação")
    st.markdown("Uma análise macroeconômica dos últimos 12 meses do IPCA.")
    st.divider()
    
    st.subheader("Insights da Análise")
    
    st.markdown("""
    **1. O Termômetro**
    A curva geral nos mostra a tendência macro. Picos indicam meses onde o custo de vida geral pesou mais, enquanto vales indicam alívio (deflação ou desaceleração).
    
    **2. Os Vilões do Ano**
    Nem tudo sobe igual. Este ranking revela os grupos que mais sofreram reajustes acumulados nos últimos 12 meses, ditando o ritmo da inflação.
    
    **3. Alimentação vs Transportes**
    Os dois maiores pesos no orçamento das famílias. A alimentação costuma ser sazonal, enquanto transportes reagem rápido ao dólar e petróleo.
    
    **4. O Último Retrato**
    No mês mais recente, quem foi o principal responsável por puxar o índice para o alto?
    """)
    
    st.divider()
    st.caption("Projeto desenvolvido com Python, SQLite e Streamlit via API do IBGE (Sidra).")


# Configuração da área principal (Gráficos)

st.title("História da Inflação Brasileira (Últimos 12 Meses)")
st.markdown("Role a página para acompanhar a evolução do cenário macroeconômico até o detalhe do último mês.")
st.write("---")

# Gráfico 1: O Termômetro

st.header("1. O Termômetro da Economia")
query_geral = """
    SELECT 
        mes, 
        valor as Valor 
    FROM 
        fato_ipca 
    WHERE
        categoria LIKE '%Índice geral%' AND variavel_cod = 63 
    ORDER BY
        mes;
"""
df_geral = carregar_dados(query_geral)

fig1 = px.line(df_geral, x='mes', y='Valor', markers=True, text='Valor')
fig1.update_traces(textposition="top center", line_shape='spline')
fig1.update_xaxes(dtick="M1", tickformat="%b\n%Y", title="Mês") 
fig1.update_yaxes(title="Variação Mensal (%)")
st.plotly_chart(fig1, width="stretch")

st.write("---")

# Gráficos 2 e 3
col1, col2 = st.columns(2)

with col1:
    st.header("2. Os Vilões do Ano")
    query_viloes = """
        SELECT 
            categoria as Categoria, 
            SUM(valor) as "Total Acumulado" 
        FROM 
            fato_ipca 
        WHERE 
            Categoria NOT LIKE '%Índice geral%' AND variavel_cod = 63
        GROUP BY 
            Categoria 
        ORDER BY "
            Total Acumulado" DESC 
        LIMIT 6;
    """
    df_viloes = carregar_dados(query_viloes)
    
    fig2 = px.bar(df_viloes, x='Total Acumulado', y='Categoria', orientation='h', text_auto='.2f',
                 color='Total Acumulado', color_continuous_scale='Reds')
    fig2.update_layout(xaxis_title="Variação Acumulada (%)", yaxis_title="")
    st.plotly_chart(fig2, width="stretch")

with col2:
    st.header("3. Alimentação x Transportes")
    query_pesos = """
        SELECT 
            mes, 
            categoria as Categoria, 
            valor as Valor
        FROM 
            fato_ipca 
        WHERE 
            (categoria LIKE '%Alimentação%' OR categoria LIKE '%Transporte%') 
            AND variavel_cod = 63
        ORDER BY 
            mes;
    """
    df_pesos = carregar_dados(query_pesos)
    
    fig3 = px.line(df_pesos, x='mes', y='Valor', color='Categoria', markers=True)
    fig3.update_traces(line_shape='spline')
    fig3.update_xaxes(dtick="M2", tickformat="%b %Y", title="Mês") 
    fig3.update_yaxes(title="Variação (%)")
    # Move a legenda para ficar mais limpo
    fig3.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, title=""))
    st.plotly_chart(fig3, width="stretch")

st.write("---")

# Gráfico 4 - Zoom
st.header("4. Raio-X do Último Mês")
# Pega dinamicamente o último mês que existe na base
query_ultimo = """
    SELECT 
        categoria as Categoria, 
        valor as Valor 
    FROM 
        fato_ipca 
    WHERE 
        mes = (SELECT MAX(mes) FROM fato_ipca)
        AND categoria NOT LIKE '%Índice geral%' 
        AND variavel_cod = 63
        AND valor > 0;
"""

df_ultimo = carregar_dados(query_ultimo)

df_ultimo = df_ultimo.nlargest(15,'Valor')

fig4 = px.treemap(df_ultimo, path=[px.Constant("Inflação do Mês"), 'Categoria'], values='Valor',
                  color='Valor', color_continuous_scale='Blues')
fig4.update_traces(textinfo="label+value")
fig4.update_layout(margin = dict(t=0, l=0, r=0, b=0)) # Remove bordas extras
st.plotly_chart(fig4, width="stretch")

# Área de exploração
with st.expander("Área Técnica: Aqui você pode interagir com o Banco de Dados SQL"):
    st.markdown("Escreva suas queries para explorar o banco SQLite local (`fato_ipca`).")
    query_exemplo_user = st.text_area("SQL:", value="SELECT * FROM fato_ipca LIMIT 5")
    if st.button("Executar Query"):
        try:
            st.dataframe(carregar_dados(query_exemplo_user), width="stretch")
        except Exception as e:
            st.error(f"Erro na query: {e}")