import pandas as pd
import plotly.express as px
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
# Título, ícone da aba e modo tela cheia
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- ESTILOS PERSONALIZADOS ---
# Aqui usamos CSS para aplicar uma paleta em tons de roxo
st.markdown("""
    <style>
        /* Cor de fundo geral */
        .stApp {
            background-color: #f5f0fa;
        }
        /* Cor dos títulos */
        h1, h2, h3, h4 {
            color: #4B0082;
        }
        /* Cor dos KPIs (métricas principais) */
        [data-testid="stMetricValue"] {
            color: #6A0DAD;
        }
        /* Links e botões */
        a, button, .stButton>button {
            background-color: #7D3C98 !important;
            color: white !important;
            border-radius: 8px;
        }
        a:hover, .stButton>button:hover {
            background-color: #5B2C6F !important;
            color: #fff !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- LEITURA DOS DADOS ---
# Carregando o dataset diretamente do GitHub
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")


# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)


# --- APLICANDO OS FILTROS ---
# O dataframe é filtrado com base nas escolhas do usuário
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]


# --- CONTEÚDO PRINCIPAL ---
# Título e introdução
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")


# --- KPIs (Métricas principais) ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""

# Exibindo as métricas em colunas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")


# --- GRÁFICOS ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

# Gráfico de Top 10 Cargos por salário médio
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_traces(marker_color="#7D3C98")  # cor roxa personalizada
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

# Histograma de salários
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_traces(marker_color="#9B59B6")  # roxo mais claro
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")


col_graf3, col_graf4 = st.columns(2)

# Gráfico de pizza - tipos de trabalho
with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(marker=dict(colors=["#8E44AD","#BB8FCE","#D2B4DE"]))  # tons de roxo
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

# Mapa - salário médio de Cientista de Dados por país
with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='purples',  # escala em roxo
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
        )
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 


# --- TABELA DE DADOS DETALHADOS ---
st.subheader("Dados Detalhados")
st.markdown("Aqui você pode visualizar os dados completos já filtrados.")
st.dataframe(df_filtrado)
