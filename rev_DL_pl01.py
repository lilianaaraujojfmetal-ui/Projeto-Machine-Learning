# Autores : Liliana, Pedro, David

import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏎️ Dashboard Formula 1", text_alignment="center")
st.write("Explorando dados históricos da F1 com Pandas e Streamlit")

# Elementos multimédia
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

# Merge para análises
df1 = results.merge(drivers, left_on='driverId', right_index=True, how='left')
df1 = df1.rename(columns={'number_x' : 'number',})
df1=df1.drop(columns=['number_y'])

# Criar tabs para cada análise
tab1_1, tab1_2, tab2_1, tab2_2, tab3, tab4_1, tab4_2, tab5, tab6 = st.tabs(
    ["Pilotos com mais pontos",
     "Pilotos com mais vitórias",
     "Equipas(P) dominaram a Fórmula 1?",
     "Equipas(V) dominaram a Fórmula 1?",
     "Pole aumenta as hipóteses de ganhar?",
     "Circuitos com mais abandonos",
     "Pilotos com mais abondonos",
     "Top Nac. dos pilotos com mais vitórias.",
     "Melhor consistência ao longo da carreira."]
)

# 1 Top 10 pilotos com mais pontos
with tab1_1:
    st.subheader("Top 10 pilotos com mais pontos", text_alignment="center")
    points = df1.groupby('driverRef')['points'].sum().sort_values(ascending=False).head(10).astype(int).to_frame(name="Pontos")
    points.index.name = "Piloto"
    points_reset = points.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig1 = px.bar(points_reset, x="Piloto", y="Pontos", text="Pontos") #, title="Top 10 Pilotos com Mais Pontos" | , color_discrete_sequence=['red']
        fig1.update_layout(xaxis_title="Piloto", yaxis_title="Total de Pontos") #title_x=0.5, 
        fig1.update_traces(textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(points.style.set_properties(**{'text-align': 'center'}))

# 2 top 10 pilotos com mais vitórias
with tab1_2:
    st.subheader("Top 10 pilotos com mais vitórias", text_alignment="center")
    wins = df1[df1['positionOrder'] == 1]['driverRef'].value_counts().head(10).to_frame(name="Vitórias")
    wins.index.name="Piloto"
    wins_reset = wins.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig2 = px.bar(wins_reset, x="Piloto", y="Vitórias", text="Vitórias") #, title="Top 10 pilotos com mais vitórias"
        fig2.update_layout(xaxis_title="Piloto", yaxis_title="Total de vitórias") # title_x=0.5, 
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(wins.style.set_properties(**{'text-align': 'center'}))

# 3 - Que equipas dominaram a Fórmula 1? por pontos
with tab2_1:
    st.subheader("Equipas que dominaram a Fórmula 1? por pontos", text_alignment="center")
    df2 = results.merge(constructors, left_on='constructorId', right_index=True, how='left')
    df2 = df2.drop(columns=['constructorId_y','constructorId_x'])
    points_constructor = (df2.groupby('constructorRef')['points'].sum().sort_values(ascending=False).head(10)).astype(int).to_frame(name="Pontos")
    points_constructor.index.name="Equipas"
    points_reset = points_constructor.reset_index()

    col1, col2 = st.columns(2) 

    with col1:
        st.subheader("Gráfico")
        fig3 = px.bar(points_reset, x="Equipas", y="Pontos", text="Pontos")
        fig3.update_layout(xaxis_title="Piloto", yaxis_title="Total de pontos")
        fig3.update_traces(textposition='outside')
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(points_constructor.style.set_properties(**{'text-align': 'center'}))


# 4 - Que equipas dominaram a Fórmula 1? por mais vitórias
with tab2_2:
    st.subheader("Equipas que dominaram a Fórmula 1? Por vitórias", text_alignment="center")
    wins_constructors = df2[df2['positionOrder'] == 1]['constructorRef'].value_counts().head(10).astype(int).to_frame(name="Vitórias")
    wins_constructors.index.name="Equipas"
    wins_reset = wins.reset_index()

    col1, col2 = st.columns(2) 

    with col1:
        st.subheader("Gráfico")
        fig4 = px.bar(wins_reset, x="Piloto", y="Vitórias", text="Vitórias")
        fig4.update_layout(xaxis_title="Equipas", yaxis_title="Total de vitórias")
        fig4.update_traces(textposition='outside')
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(wins_constructors.style.set_properties(**{'text-align': 'center'}))

# 5 - Começar em primeiro aumenta as hipóteses de ganhar?
with tab3:
    st.subheader("Começar em primeiro aumenta as hipóteses de ganhar?", text_alignment="center")
    df3 = qualifying.merge(results, on=['raceId','driverId'], how='left')
    df3 = df3.rename(columns={'position_x': 'position', 'number_x': 'number', 'constructorId_x': 'constructor',})
    df3=df3.drop(columns=['constructorId_y','number_y','position_y'])

    pole_wins = df3[df3['position'] == 1]
    wins = pole_wins[pole_wins['positionOrder'] == 1]
    total_poles = len(pole_wins)
    total_wins = len(wins)

    prob = total_wins / total_poles

    st.write("Vitórias a partir da pole:", total_wins)
    st.write("Probabilidade:", prob)
    st.write("Percentagem:", f"{prob*100:.2f}%")

    prob_data = pd.DataFrame({"Resultado": ["Pole venceu", "Pole não venceu"], "Quantidade": [total_wins, total_poles - total_wins]}).set_index("Resultado")
    prob_reset = prob_data.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig5 = px.bar(prob_reset, x="Resultado", y="Quantidade", text="Quantidade") # , title="Impacto da Pole Position nas Vitórias"
        fig5.update_layout(xaxis_title="Resultado", yaxis_title="Número de Corridas") # title_x=0.5, 
        fig5.update_traces(textposition='outside')
        st.plotly_chart(fig5, use_container_width=True)
  
    with col2:
        st.subheader("Tabela")
        st.table(prob_data.style.set_properties(**{'text-align': 'center'}))

# 6 - Em que circuitos há mais abandonos?
with tab4_1:
    st.subheader("Em que circuitos há mais abandonos?", text_alignment="center")
    df4 = races.merge(circuits, left_on='circuitId', right_index=True, how='left')
    df4 = df4.rename(columns={'name_x': 'name', 'url_x': 'url'})
    df4=  df4.drop(columns=['url_y','name_y'])

    df5 = df4.merge(results, left_on='raceId', right_index=True, how='left')
    df5 = df5.rename(columns={'time_x': 'time'})
    df5=  df5.drop(columns=['time_y'])
    
    df6 = df5.merge(drivers, left_on='driverId', right_index=True, how='left')
    df6 = df6.rename(columns={'url_x': 'url', 'number_x':'number'})
    df6 = df6.drop(columns=['url_y','number_y'])
    df6['time'].convert_dtypes(str)

    abandonos = df6[df6['time'] == '\\N']

    st.write(f"{abandonos.shape[0]} pilotos abandonaram a corrida.")

    abandonos_circuito = abandonos.groupby('name').size().sort_values(ascending=False).head(10).to_frame(name="Abandonos")
    abandonos_circuito.index.name = "Circuito"
    abandonos_reset = abandonos_circuito.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig6 = px.bar(abandonos_reset, x="Circuito", y="Abandonos", text="Abandonos")
        fig6.update_layout(xaxis_title="Circuito", yaxis_title="Número de Abandonos")
        fig6.update_traces(textposition='outside')

        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(abandonos_circuito.style.set_properties(**{'text-align': 'center'}))

# 7 Pilotos com mais abandonos (Top 10)
with tab4_2:
    st.subheader("Pilotos com mais abandonos (Top 10)", text_alignment="center")

    abandonos_Pilotoes = (abandonos.groupby('driverRef').size().sort_values(ascending=False).head(10).to_frame(name="Abandonos"))
    abandonos_Pilotoes.index.name = "Piloto"

    abandonos_reset = abandonos_Pilotoes.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig7 = px.bar(abandonos_reset, x="Piloto", y="Abandonos", text="Abandonos")
        fig7.update_layout(xaxis_title="Piloto", yaxis_title="Número de Abandonos")
        fig7.update_traces(textposition='outside')
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(abandonos_Pilotoes.style.set_properties(**{'text-align': 'center'}))      

# 8 - Qual o top10 das nacionalidades dos pilotos com mais vitórias?
with tab5:
    st.subheader("Nacionalidades dos pilotos com mais vitórias (Top 10)", text_alignment="center")
    vitorias = df1[df1['position'] == '1']
    nacionalidades = (vitorias.groupby('nationality').size().sort_values(ascending=False).head(10).to_frame(name="Vitórias"))
    nacionalidades.index.name = "Nacionalidade"
    nacionalidades_reset = nacionalidades.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig8 = px.bar(nacionalidades_reset, x="Nacionalidade", y="Vitórias", text="Vitórias")
        fig8.update_layout(xaxis_title="Nacionalidade", yaxis_title="Número de Vitórias") # , uniformtext_minsize=8, uniformtext_mode='hide'
        fig8.update_traces(textposition='outside')
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(nacionalidades.style.set_properties(**{'text-align': 'center'}))
    
# 9 - Quem tem melhor consistência ao longo da carreira? (mediana dos pontos)
with tab6:
    st.subheader("Melhor consistência ao longo da carreira? (mediana dos pontos)", text_alignment="center")

    pontos_mediana = df1.groupby('driverRef')['points'].median().sort_values(ascending=False).head(10).astype(int).to_frame(name="Mediana de pontos")
    pontos_mediana.index.name = "Piloto"
    mediana_reset = pontos_mediana.reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gráfico")
        fig9 = px.line(mediana_reset, x="Piloto", y="Mediana de pontos", text="Mediana de pontos", markers=True)
        fig9.update_layout(xaxis_title="Piloto", yaxis_title="Mediana de pontos")
        fig9.update_traces(textposition='top center', line=dict(color='blue', width=8))
        st.plotly_chart(fig9, use_container_width=True)

    with col2:
        st.subheader("Tabela")
        st.table(pontos_mediana.style.set_properties(**{'text-align': 'center'}))