import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.graph_objects as go

# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard Energético", layout="wide")

st.title("📊 Análise de Eficiência e Economia Energética")

# --- FUNÇÃO PARA CARREGAR DADOS ---
@st.cache_data # Cache para não ler o Excel toda vez que você interagir com o gráfico
def load_data():
    # Nota: No VS Code, certifique-se que o arquivo está na mesma pasta do script
    # ou altere o caminho abaixo.
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
    
    # --- LAYOUT EM COLUNAS ---
    #col1, col2 = st.columns([1, 1])

    #with col1:
        st.subheader("💡 Eficiência: Consumo vs Geração")
        
        # 1. Configuração Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('#F8F9FA')

        # Barras e Linha
        barras = ax.bar(df_ano1['Mês'], df_ano1['Consumo faturado (kWh)'], 
                        color='#FF6347', alpha=0.4, width=0.5, label='Consumo Faturado')
        
        ax.plot(df_ano1['Mês'], df_ano1['Energia gerada (kWh)'], 
                color='#2E8B57', marker='o', markersize=8, linewidth=4, label='Energia Gerada', zorder=3)

        # Ticks e Rótulos
        ax.set_xticks(range(len(df_ano1['Mês'])))
        ax.set_xticklabels(df_ano1['Mês'], fontsize=10)

        # Data Labels
        for i, bar in enumerate(barras):
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{int(yval)}', 
                    ha='center', va='bottom', color='#FF6347', fontweight='bold', fontsize=8)

        # Estilização
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        plt.tight_layout()
        st.pyplot(fig) # Comando Streamlit para renderizar Matplotlib

   # with col2:
        st.subheader("💰 Comparativo de Custos e Economia")
        
        # 2. Configuração Plotly
        fig_plotly = go.Figure()

        # Trace Gasto Atual
        fig_plotly.add_trace(go.Scatter(
            x=df_ano1['Mês'], y=df_ano1['Vai pagar'],
            mode='lines+markers', name='Gasto Atual',
            line=dict(color='#E74C3C', width=3),
            hovertemplate='Atual: R$ %{y:.0f}<extra></extra>'
        ))

        # Trace Gasto Anterior + Fill
        fig_plotly.add_trace(go.Scatter(
            x=df_ano1['Mês'], y=df_ano1['Você pagava'],
            mode='lines', name='Gasto Anterior',
            line=dict(color='#999999', width=2),
            fill='tonexty', fillcolor='rgba(39, 174, 96, 0.2)',
            hovertemplate='Anterior: R$ %{y:.0f}<extra></extra>'
        ))

        # Rótulos de Economia
        fig_plotly.add_trace(go.Scatter(
            x=df_ano1['Mês'], y=(df_ano1['Você pagava'] + df_ano1['Vai pagar']) / 2,
            mode='text', text=df_ano1['Economia'].apply(lambda x: f'R$ {x:.0f}'),
            textfont=dict(color="#071B10", size=10), showlegend=False, hoverinfo='skip'
        ))

        fig_plotly.update_layout(
            plot_bgcolor='#FAFAFA', margin=dict(l=20, r=20, t=20, b=100),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
            hovermode="x unified"
        )
        fig_plotly.update_yaxes(tickprefix="R$ ")

        st.plotly_chart(fig_plotly, use_container_width=True) # Comando Streamlit para Plotly

else:
    st.warning("Aguardando arquivo 'dimensionamento.xlsx' no diretório do projeto.")