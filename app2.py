import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.graph_objects as go

# 1. Configuração da página (Removi o 'wide' para os gráficos não ficarem esticados demais em telas UltraWide)
st.set_page_config(page_title="Dashboard Energético", layout="centered")

st.header("📊 Análise de Eficiência e Economia")

@st.cache_data
def load_data():
    try:
        file_path = 'dimensionamento.xlsx' 
        df = pd.read_excel(file_path, skiprows=23)
        df = df.drop(columns=['Payback', 'Unnamed: 27', 0], errors='ignore')
        df_ano1 = df[df['Ano'] == 1].copy()
        return df_ano1
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

df_ano1 = load_data()

if df_ano1 is not None:
    
    # --- GRÁFICO 1: MATPLOTLIB ---
    st.subheader("💡 Eficiência: Consumo vs Geração")
    
    # Aumentei o figsize para (12, 6) para melhor proporção em layout vertical
    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#F8F9FA')

    barras = ax.bar(df_ano1['Mês'], df_ano1['Consumo faturado (kWh)'], 
                    color='#FF6347', alpha=0.4, width=0.6, label='Consumo Faturado')
    
    ax.plot(df_ano1['Mês'], df_ano1['Energia gerada (kWh)'], 
            color='#2E8B57', marker='o', markersize=8, linewidth=4, label='Energia Gerada', zorder=3)

    ax.set_xticks(range(len(df_ano1['Mês'])))
    ax.set_xticklabels(df_ano1['Mês'], fontsize=10)

    for i, bar in enumerate(barras):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{int(yval)}', 
                ha='center', va='bottom', color='#FF6347', fontweight='bold', fontsize=9)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Ajustei a legenda para não ficar muito colada
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=11)
    
    plt.tight_layout()
    st.pyplot(fig)

    # Espaçador visual
    st.markdown("---")

    # --- GRÁFICO 2: PLOTLY ---
    st.subheader("💰 Comparativo de Custos e Economia")
    
    fig_plotly = go.Figure()

    fig_plotly.add_trace(go.Scatter(
        x=df_ano1['Mês'], y=df_ano1['Vai pagar'],
        mode='lines+markers', name='Gasto Atual',
        line=dict(color='#E74C3C', width=3),
        hovertemplate='Atual: R$ %{y:.0f}<extra></extra>'
    ))

    fig_plotly.add_trace(go.Scatter(
        x=df_ano1['Mês'], y=df_ano1['Você pagava'],
        mode='lines', name='Gasto Anterior',
        line=dict(color='#999999', width=2),
        fill='tonexty', fillcolor='rgba(39, 174, 96, 0.2)',
        hovertemplate='Anterior: R$ %{y:.0f}<extra></extra>'
    ))

    fig_plotly.add_trace(go.Scatter(
        x=df_ano1['Mês'], y=(df_ano1['Você pagava'] + df_ano1['Vai pagar']) / 2,
        mode='text', text=df_ano1['Economia'].apply(lambda x: f'R$ {x:.0f}'),
        textfont=dict(color="#071B10", size=11, family="Arial Black"), showlegend=False, hoverinfo='skip'
    ))

    fig_plotly.update_layout(
        height=500, # DEFININDO ALTURA FIXA PARA MANTER PROPORÇÃO
        plot_bgcolor='#FAFAFA', 
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=80),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        hovermode="x unified"
    )
    fig_plotly.update_yaxes(tickprefix="R$ ", gridcolor='#eeeeee')
    fig_plotly.update_xaxes(showgrid=False)

    st.plotly_chart(fig_plotly, use_container_width=True)

else:
    st.warning("Aguardando arquivo 'dimensionamento.xlsx' no diretório do projeto.")