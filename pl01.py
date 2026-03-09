# Autores: Liliana, Pedro, David, Filipe

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------
st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Dashboard Fórmula 1")
st.markdown("Explorando dados históricos da Fórmula 1 com **Pandas + Streamlit + Plotly**")

# Logo e vídeo
st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=200)
st.markdown("""
<iframe width="420" height="236"
src="https://www.youtube.com/embed/2a_ejgpQNVo"
title="Formula 1 Video"
frameborder="0"
allowfullscreen></iframe>
""", unsafe_allow_html=True)

# -----------------------------
# CARREGAR DADOS
# -----------------------------
@st.cache_data
def load_data():
    circuits = pd.read_csv('./dataset/circuits.csv', index_col='circuitId')
    constructors = pd.read_csv('./dataset/constructors.csv', index_col='constructorId')
    drivers = pd.read_csv('./dataset/drivers.csv', index_col='driverId')
    races = pd.read_csv('./dataset/races.csv', index_col='raceId')
    results = pd.read_csv('./dataset/results.csv', index_col='resultId')
    qualifying = pd.read_csv('./dataset/qualifying.csv', index_col='qualifyId')
    return circuits, constructors, drivers, races, results, qualifying

circuits, constructors, drivers, races, results, qualifying = load_data()

# Merge principal
df = results.merge(drivers, left_on='driverId', right_index=True, how='left')
df = df.merge(races[['year']], left_on='raceId', right_index=True, how='left')

# -----------------------------
# FILTROS GLOBAIS
# -----------------------------
st.sidebar.header("Filtros Globais")
ano_min, ano_max = int(df['year'].min()), int(df['year'].max())
year_slider = st.sidebar.slider("Ano", ano_min, ano_max, (ano_min, ano_max))

pilotos_list = df['driverRef'].unique()
piloto_filter = st.sidebar.multiselect("Selecionar piloto(s)", pilotos_list, pilotos_list)

equipes_list = constructors['constructorRef'].unique()
equipa_filter = st.sidebar.multiselect("Selecionar equipa(s)", equipes_list, equipes_list)

# Aplicar filtros
df = df[df['driverRef'].isin(piloto_filter)]
df = df[df['year'].between(year_slider[0], year_slider[1])]
df_team = results.merge(constructors, left_on='constructorId', right_index=True)
df_team = df_team[df_team['constructorRef'].isin(equipa_filter)]
df_team = df_team[df_team['raceId'].map(lambda x: races.loc[x,'year']).between(year_slider[0], year_slider[1])]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Resumo Geral")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pilotos", df['driverRef'].nunique())
col2.metric("Total Corridas", df['raceId'].nunique())
col3.metric("Total Equipas", df_team['constructorRef'].nunique())
col4.metric("Total Circuitos", circuits.shape[0])
st.divider()

# -----------------------------
# TABS PRINCIPAIS
# -----------------------------
tabs = st.tabs([
"🏆 Pontos",
"🥇 Vitórias",
"🏁 Equipas",
"📍 Circuitos",
"📊 Consistência",
"🌍 Mapas"
])

# Função para garantir colunas numéricas
def safe_numeric(df, cols):
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df

# -----------------------------
# TAB 1 - TOP 10 PONTOS
# -----------------------------
with tabs[0]:
    st.subheader("Top 10 Pilotos com mais pontos")
    points_df = df.groupby('driverRef')['points'].sum().sort_values(ascending=False).head(10).to_frame("Pontos").reset_index()
    points_df = safe_numeric(points_df, ['Pontos'])
    fig = px.bar(points_df, x='driverRef', y='Pontos', text='Pontos', color='Pontos', color_continuous_scale='Reds')
    col1, col2 = st.columns([2,1])
    col1.plotly_chart(fig, width='stretch')
    col2.dataframe(points_df.style.format({'Pontos': "{:.0f}"}))

# -----------------------------
# TAB 2 - TOP 10 VITÓRIAS
# -----------------------------
with tabs[1]:
    st.subheader("Top 10 Pilotos com mais vitórias")
    wins_series = df[df['positionOrder']==1]['driverRef'].value_counts().head(10)
    wins_df = pd.DataFrame({'Piloto': wins_series.index, 'Vitórias': wins_series.values})
    wins_df = safe_numeric(wins_df, ['Vitórias'])
    fig = px.bar(wins_df, x='Piloto', y='Vitórias', text='Vitórias', color='Vitórias', color_continuous_scale='Oranges')
    col1, col2 = st.columns([2,1])
    col1.plotly_chart(fig, width='stretch')
    col2.dataframe(wins_df.style.format({'Vitórias': "{:.0f}"}))

# -----------------------------
# TAB 3 - EQUIPAS
# -----------------------------
with tabs[2]:
    st.subheader("Equipas com mais pontos")
    points_team = df_team.groupby('constructorRef')['points'].sum().sort_values(ascending=False).head(10).to_frame("Pontos").reset_index()
    points_team = safe_numeric(points_team, ['Pontos'])
    fig = px.bar(points_team, x='constructorRef', y='Pontos', text='Pontos', color='Pontos', color_continuous_scale='Blues')
    col1, col2 = st.columns([2,1])
    col1.plotly_chart(fig, width='stretch')
    col2.dataframe(points_team.style.format({'Pontos': "{:.0f}"}))

# -----------------------------
# TAB 4 - CIRCUITOS
# -----------------------------
with tabs[3]:
    st.subheader("Circuitos com mais abandonos")

    # Merge: rases + circuits + results
    df_circ = races.merge(circuits, left_on="circuitId", right_index=True)
    df_circ = df_circ.merge(results, left_on='raceId', right_index=True)

    # Filtrar resultados de abandono (statusId != 1)
    abandonos = df_circ[df_circ["statusId"] != 1]

    # Agrupar por circuito ('circuitRef') e contar abandonos
    abandonos_circ = (
        abandonos.groupby('circuitRef') 
        .size()
        .sort_values(ascending=False)
        .head(10)
        .to_frame("Abandonos")
        .reset_index()
    )

    # Garantir que a coluna é numérica
    abandonos_circ["Abandonos"] = pd.to_numeric(abandonos_circ["Abandonos"], errors='coerce')

    # Gráfico
    fig = px.bar(
        abandonos_circ,
        x='circuitRef',
        y='Abandonos',
        text='Abandonos',
        color='Abandonos',
        color_continuous_scale='Blues'
    )

    # Layout com colunas
    col1, col2 = st.columns([2,1])
    col1.plotly_chart(fig, use_container_width=True)
    col2.dataframe(abandonos_circ.style.format({"Abandonos": "{:.0f}"}))

# -----------------------------
# TAB 5 - CONSISTÊNCIA
# -----------------------------
with tabs[4]:
    st.subheader("Melhor consistência (mediana de pontos por piloto)")
    consistency = df.groupby('driverRef')['points'].median().sort_values(ascending=False).head(10).to_frame("Mediana Pontos").reset_index()
    consistency = safe_numeric(consistency, ['Mediana Pontos'])
    fig1 = px.line(consistency, x='driverRef', y='Mediana Pontos', markers=True, line_shape='spline', text='Mediana Pontos')
    fig2 = px.box(df, x='driverRef', y='points', color='driverRef')
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, width='stretch')
    col2.plotly_chart(fig2, width='stretch')

# -----------------------------
# TAB 6 - MAPAS
# -----------------------------
with tabs[5]:
    st.subheader("Localização dos circuitos")
    races_map = races.merge(circuits,left_on='circuitId',right_index=True)
    fig = px.scatter_geo(races_map, lat='lat', lon='lng', hover_name='circuitRef', size_max=20, color='country', title='Circuitos da F1')
    st.plotly_chart(fig, width='stretch')

    st.subheader("Nacionalidade dos pilotos com vitórias")
    wins_df = df[df['positionOrder']==1]
    nationality = wins_df.groupby('nationality').size().sort_values(ascending=False).head(10).to_frame("Vitórias").reset_index()
    nationality = safe_numeric(nationality, ['Vitórias'])
    fig2 = px.treemap(nationality, path=['nationality'], values='Vitórias', color='Vitórias', color_continuous_scale='Reds')
    st.plotly_chart(fig2, width='stretch')

# -----------------------------
# GRÁFICOS ADICIONAIS OPCIONAIS
# -----------------------------
with st.expander("📈 Evolução de pontos por temporada"):
    evo_points = df.groupby(['driverRef','year'])['points'].sum().reset_index()
    evo_points = safe_numeric(evo_points, ['points'])
    fig = px.line(evo_points, x='year', y='points', color='driverRef', markers=True, title="Evolução de pontos por piloto")
    st.plotly_chart(fig, width='stretch')