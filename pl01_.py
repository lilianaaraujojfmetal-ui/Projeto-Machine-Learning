# Autores: Liliana, Pedro, David, Filipe
# Nota: reorganizei algumas partes enquanto estava a testar o dashboard

import pandas as pd
import streamlit as st
import plotly.express as px

from data_loader import prepare_data


# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="F1 Dashboard",
    layout="wide"
)

st.title("🏎️ Dashboard Fórmula 1")

st.markdown(
    "Exploração de dados históricos da **Fórmula 1** usando Pandas, Streamlit e Plotly."
)

# --------------------------------------------------
# LOGO + VIDEO
# --------------------------------------------------
logo = "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg"
st.image(logo, width=200)

st.markdown("""
<iframe width="420" height="236"
src="https://www.youtube.com/embed/2a_ejgpQNVo"
title="Formula 1 Video"
frameborder="0"
allowfullscreen>
</iframe>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CACHE DE DADOS
# --------------------------------------------------
# Streamlit vai guardar o resultado para evitar
# recalcular os dados sempre que o utilizador mexe nos filtros

@st.cache_data(ttl=3600)
def load_f1_data():

    df, df_team, df_circ, circuits, constructors, drivers, races, results = prepare_data()

    return df, df_team, df_circ, circuits, constructors, drivers, races, results


# carregar dados
df, df_team, df_circ, circuits, constructors, drivers, races, results = load_f1_data()


# --------------------------------------------------
# SIDEBAR - FILTROS
# --------------------------------------------------
st.sidebar.header("Filtros")

min_year = int(df['year'].min())
max_year = int(df['year'].max())

year_range = st.sidebar.slider(
    "Ano",
    min_year,
    max_year,
    (min_year, max_year)
)

drivers_available = df['driverRef'].unique()

selected_drivers = st.sidebar.multiselect(
    "Selecionar piloto(s)",
    drivers_available,
    drivers_available
)

teams_available = constructors['constructorRef'].unique()

selected_teams = st.sidebar.multiselect(
    "Selecionar equipa(s)",
    teams_available,
    teams_available
)


# --------------------------------------------------
# APLICAR FILTROS
# --------------------------------------------------
df = df[df['driverRef'].isin(selected_drivers)]
df = df[df['year'].between(year_range[0], year_range[1])]

df_team = df_team[df_team['constructorRef'].isin(selected_teams)]

# esta parte podia ser otimizada, mas funciona bem
df_team = df_team[
    df_team['raceId']
    .map(lambda r: races.loc[r, 'year'])
    .between(year_range[0], year_range[1])
]


# --------------------------------------------------
# KPIs
# --------------------------------------------------
st.subheader("📊 Resumo Geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pilotos", df['driverRef'].nunique())
col2.metric("Total Corridas", df['raceId'].nunique())
col3.metric("Total Equipas", df_team['constructorRef'].nunique())
col4.metric("Total Circuitos", circuits.shape[0])

st.divider()


# --------------------------------------------------
# TABS
# --------------------------------------------------
tabs = st.tabs([
"🏆 Pontos",
"🥇 Vitórias",
"🏁 Equipas",
"📍 Circuitos",
"📊 Consistência",
"🌍 Mapas"
])


# --------------------------------------------------
# FUNÇÃO AUXILIAR
# --------------------------------------------------
def force_numeric(df, cols):

    for c in cols:

        df[c] = pd.to_numeric(df[c], errors='coerce')

        df[c] = df[c].fillna(0)

        df[c] = df[c].astype(int)

    return df


# --------------------------------------------------
# TAB 1 - PONTOS
# --------------------------------------------------
with tabs[0]:

    st.subheader("Top 10 pilotos com mais pontos")

    points = (
        df.groupby('driverRef')['points']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    points_df = points.to_frame("Pontos").reset_index()
    points_df = points_df.rename(columns={'driverRef': 'Piloto'})

    points_df = force_numeric(points_df, ['Pontos'])

    fig = px.bar(
        points_df,
        x='Piloto',
        y='Pontos',
        text='Pontos',
        color='Pontos',
        color_continuous_scale='Reds'
    )

    fig.update_traces(textposition='outside', textfont=dict(size=12, family="Arial Black"))

    col1, col2 = st.columns([2,1])

    col1.plotly_chart(fig, use_container_width=True)
    col2.dataframe(points_df, hide_index=True)


# --------------------------------------------------
# TAB 2 - VITÓRIAS
# --------------------------------------------------
with tabs[1]:

    st.subheader("Top 10 pilotos com mais vitórias")

    wins = df[df['positionOrder'] == 1]

    wins_series = wins['driverRef'].value_counts().head(10)

    wins_df = pd.DataFrame({
        "Piloto": wins_series.index,
        "Vitórias": wins_series.values
    })

    wins_df = force_numeric(wins_df, ['Vitórias'])

    fig = px.bar(
        wins_df,
        x='Piloto',
        y='Vitórias',
        text='Vitórias',
        color='Vitórias',
        color_continuous_scale='Oranges'
    )

    fig.update_traces(textposition='outside', textfont=dict(size=12, family="Arial Black"))

    col1, col2 = st.columns([2,1])

    col1.plotly_chart(fig, use_container_width=True)
    col2.dataframe(wins_df, hide_index=True)


# --------------------------------------------------
# TAB 3 - EQUIPAS
# --------------------------------------------------
with tabs[2]:

    st.subheader("Equipas com mais pontos")

    team_points = (
        df_team.groupby('constructorRef')['points']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    team_df = team_points.to_frame("Pontos").reset_index()
    team_df = team_df.rename(columns={'constructorRef': 'Equipa'})

    team_df = force_numeric(team_df, ['Pontos'])

    fig = px.bar(
        team_df,
        x='Equipa',
        y='Pontos',
        text='Pontos',
        color='Pontos',
        color_continuous_scale='Blues'
    )

    fig.update_traces(textposition='outside', textfont=dict(size=12, family="Arial Black"))

    col1, col2 = st.columns([2,1])

    col1.plotly_chart(fig, use_container_width=True)
    col2.dataframe(team_df, hide_index=True)


# --------------------------------------------------
# TAB 4 - CIRCUITOS
# --------------------------------------------------
with tabs[3]:

    st.subheader("Circuitos com mais abandonos")

    dnf = df_circ[df_circ["statusId"] != 1]

    circ = (
        dnf.groupby('circuitRef')
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    circ_df = circ.to_frame("Abandonos").reset_index()
    circ_df = circ_df.rename(columns={'circuitRef': 'Circuito'})

    circ_df["Abandonos"] = pd.to_numeric(circ_df["Abandonos"])

    fig = px.bar(
        circ_df,
        x='Circuito',
        y='Abandonos',
        text='Abandonos'
    )

    fig.update_traces(textposition='outside', textfont=dict(size=12, family="Arial Black"))

    col1, col2 = st.columns([2,1])

    col1.plotly_chart(fig, use_container_width=True)
    col2.dataframe(circ_df, hide_index=True)


# --------------------------------------------------
# TAB 5 - CONSISTÊNCIA
# --------------------------------------------------
with tabs[4]:

    st.subheader("Consistência dos pilotos")

    consistency = (
        df.groupby('driverRef')['points']
        .median()
        .sort_values(ascending=False)
        .head(10)
    )

    consistency_df = consistency.to_frame("Mediana Pontos").reset_index()
    consistency_df = consistency_df.rename(columns={'driverRef': 'Piloto'})

    consistency_df = force_numeric(consistency_df, ['Mediana Pontos'])

    fig1 = px.line(
        consistency_df,
        x='Piloto',
        y='Mediana Pontos',
        text='Mediana Pontos',
        markers=True
    )

    fig1.update_traces(textposition="top center", textfont=dict(size=12, family="Arial Black"))

    fig2 = px.box(
        df,
        x='driverRef',
        y='points',
        color='driverRef',
        labels= {'driverRef' : 'Piloto',
                 'points' : 'Pontos'
                 }
    )

    col1, col2 = st.columns(2)

    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# TAB 6 - MAPAS
# --------------------------------------------------
with tabs[5]:

    st.subheader("Localização dos circuitos")

    races_map = races.merge(
        circuits,
        left_on='circuitId',
        right_index=True
    )

    races_map = races_map.rename(columns={'country': 'País'})

    fig = px.scatter_geo(
        races_map,
        lat='lat',
        lon='lng',
        hover_name='circuitRef',
        color='País'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Nacionalidade dos pilotos com vitórias")

    wins = df[df['positionOrder'] == 1]

    nationality = (
        wins.groupby('nationality')
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    nationality_df = nationality.to_frame("Vitórias").reset_index()

    nationality_df = force_numeric(nationality_df, ['Vitórias'])

    fig2 = px.treemap(
        nationality_df,
        path=['nationality'],
        values='Vitórias',
        color='Vitórias'
    )

    st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# EXTRA
# --------------------------------------------------
with st.expander("📈 Evolução de pontos por temporada"):

    evo = df.groupby(['driverRef','year'])['points'].sum().reset_index()

    evo = force_numeric(evo, ['points'])

    evo = evo.rename(columns={
        'driverRef': 'Piloto',
        'year': 'Ano',
        'points': 'Pontos'
    })

    fig = px.line(
        evo,
        x='Ano',
        y='Pontos',
        color='Piloto',
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)