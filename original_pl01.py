import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Dashboard Formula 1")
st.write("Explorando dados históricos da F1 com Pandas e Streamlit")
st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=200)
st.markdown(
    """
    <iframe width="420" height="236"
    src="https://www.youtube.com/embed/2a_ejgpQNVo"
    title="Formula 1 Video"
    frameborder="0"
    allowfullscreen>
    </iframe>
    """,
    unsafe_allow_html=True
)

# Load datasets

# ======================

circuits=pd.read_csv('./dataset/circuits.csv',index_col='circuitId')

constructor_results=pd.read_csv('./dataset/constructor_results.csv',index_col='constructorResultsId')

constructor_standings=pd.read_csv('./dataset/constructor_standings.csv',index_col='constructorStandingsId')

constructors=pd.read_csv('./dataset/constructors.csv')

driver_standings=pd.read_csv('./dataset/driver_standings.csv',index_col='driverStandingsId')

drivers=pd.read_csv('./dataset/drivers.csv',index_col='driverId')

lap_times=pd.read_csv('./dataset/lap_times.csv',index_col='raceId')

pit_stops=pd.read_csv('./dataset/pit_stops.csv',index_col='raceId')

qualifying=pd.read_csv('./dataset/qualifying.csv',index_col='qualifyId')

races=pd.read_csv('./dataset/races.csv',index_col='raceId')

results=pd.read_csv('./dataset/results.csv',index_col='resultId')

seasons=pd.read_csv('./dataset/seasons.csv',index_col='year')

sprint_results=pd.read_csv('./dataset/sprint_results.csv',index_col='resultId')

status=pd.read_csv('./dataset/status.csv',index_col='statusId')



tab1_1, tab1_2, tab2_1, tab2_2, tab3, tab4_1, tab4_2, tab5, tab6 = st.tabs(
    ["Top 10 pilotos com mais pontos",
     "top 10 pilotos com mais vitórias",
     "Que equipas dominaram a Fórmula 1? por pontos",
     "Que equipas dominaram a Fórmula 1? por mais vitórias",
     "Começar em primeiro aumenta as hipóteses de ganhar?",
     "Em que circuitos há mais abandonos? E a que condutores se refere (Top10)",
     "A que condutores se refere os circuitos com mais abondonos (Top10)",
     "Qual o top10 das nacionalidades dos pilotos com mais vitórias?",
     "Quem tem melhor consistência ao longo da carreira? (mediana dos pontos)"]
)

df1 = results.merge(drivers, left_on='driverId', right_index=True, how='left')
df1 = df1.rename(columns={'number_x' : 'number',})
df1=df1.drop(columns=['number_y'])

#Top 10 pilotos com mais pontos | Retirar os decimais
with tab1_1:
 points = df1.groupby('driverRef')['points'].sum().sort_values(ascending=False).head(10)
col1, col2 = st.columns(2)
with col1:
 st.subheader("Gráfico")
 st.bar_chart(points)
with col2:
 st.subheader("Tabela")
 st.table(points)
# print(points.head(10))

#top 10 pilotos com mais vitórias

with tab1_2:
 wins = df1[df1['positionOrder'] == 1]['driverRef'].value_counts().head(10)
col1, col2 = st.columns(2)
with col1:
 st.subheader("Gráfico")
 st.bar_chart(wins)
with col2:
 st.subheader("Tabela")
 st.table(wins)

#2 - Que equipas dominaram a Fórmula 1? por pontos
df2 = results.merge(
    constructors,
    left_on='constructorId',
    right_index=True,
    how='left'
)

with tab2_1:
    df2 = df2.drop(columns=['constructorId_y','constructorId_x'])
    points_constructor = (df2.groupby('constructorRef')['points'].sum().sort_values(ascending=False).head(10))
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gráfico")
        st.bar_chart(points_constructor)
 
    with col2:
        st.subheader("Tabela")
        st.table(points_constructor)

#2 - Que equipas dominaram a Fórmula 1? por mais vitórias
wins_constructors = df2[df2['positionOrder'] == 1]['constructorRef'].value_counts()
wins_constructors.head(10)

#3 - Começar em primeiro aumenta as hipóteses de ganhar?

df3 = qualifying.merge(
    results,
    on=['raceId','driverId'],
    how='left'
)

df3 = df3.rename(columns={
    'position_x': 'position',
    'number_x': 'number',
    'constructorId_x': 'constructor',
})

df3=df3.drop(columns=['constructorId_y','number_y','position_y'])


pole_wins = df3[df3['position'] == 1]
wins = pole_wins[pole_wins['positionOrder'] == 1]
print(len(wins))
prob = len(wins) / len(pole_wins)
print(prob)

#4 - Em que circuitos há mais abandonos? E a que condutores se refere (Top10)

df4 = races.merge(
    circuits,
    left_on='circuitId',
    right_index=True,
    how='left'
)

df4 = df4.rename(columns={
    'name_x': 'name',
    'url_x': 'url',
})

df4=df4.drop(columns=['url_y','name_y'])

df5 = df4.merge(
    results,
    left_on='raceId',
    right_index=True,
    how='left'
)

df5 = df5.rename(columns={
    'time_x': 'time',
})

df5=df5.drop(columns=['time_y'])

df6 = df5.merge(
    drivers,
    left_on='driverId',
    right_index=True,
    how='left'
)

df6 = df6.rename(columns={
    'url_x': 'url',
    'number_x':'number'
})

df6=df6.drop(columns=['url_y','number_y'])

df6['time'].convert_dtypes(str)
abandonos = df6[df6['time'] == '\\N']

print(f'{abandonos.shape[0]} pilotos abandonaram a corrida.\n')

abandonos_circuito = abandonos.groupby('name').size().sort_values(ascending=False)
 
print("Os circuitos com mais abandonos foram:\n")
print(abandonos_circuito.head(10))

abandonos_condutores = abandonos.groupby('driverRef').size().sort_values(ascending=False)
 
print("\nOs pilotos com mais abandonos foram:\n")
print(abandonos_condutores.head(10))

#5 - Qual o top10 das nacionalidades dos pilotos com mais vitórias?
vitorias = df1[df1['position'] == '1']
 
nacionalidades = vitorias.groupby('nationality').size().sort_values(ascending=False)
 
print("Nacionalidades com mais vitórias na Fórmula 1:\n")
print(nacionalidades.head(10))

#6 - Quem tem melhor consistência ao longo da carreira? (mediana dos pontos)
mediana_pontos = df1.groupby('driverRef')['points'].median().sort_values(ascending=False)
print("Pilotos mais consistentes (mediana dos pontos):\n")

print(mediana_pontos.head(10))
