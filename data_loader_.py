# data_loader.py
# Pequeno módulo só para carregar e preparar os dados da F1
# Autores: Liliana, Pedro, David, Filipe

import pandas as pd
import streamlit as st


# --------------------------------------------------
# LOAD DOS CSV
# --------------------------------------------------
# usar cache para evitar ler os CSV várias vezes
# isto ajuda bastante na performance do dashboard

@st.cache_data(ttl=3600)
def load_data():

    # caminho base dos datasets
    # talvez no futuro mudar isto para uma variável global
    base_path = "./dataset/"

    # carregar ficheiros
    circuits = pd.read_csv(base_path + "circuits.csv", index_col="circuitId")

    constructors = pd.read_csv(
        base_path + "constructors.csv",
        index_col="constructorId"
    )

    drivers = pd.read_csv(
        base_path + "drivers.csv",
        index_col="driverId"
    )

    races = pd.read_csv(
        base_path + "races.csv",
        index_col="raceId"
    )

    results = pd.read_csv(
        base_path + "results.csv",
        index_col="resultId"
    )

    qualifying = pd.read_csv(
        base_path + "qualifying.csv",
        index_col="qualifyId"
    )

    # devolver tudo para ser usado no resto da app
    return circuits, constructors, drivers, races, results, qualifying


# --------------------------------------------------
# PREPARAÇÃO DOS DATAFRAMES
# --------------------------------------------------
# esta função faz alguns merges para facilitar análises
# poderia ser otimizado mas está bastante legível assim

@st.cache_data(ttl=3600)
def prepare_data():

    circuits, constructors, drivers, races, results, qualifying = load_data()

    # --------------------------------------------------
    # DATAFRAME PRINCIPAL (pilotos + resultados)
    # --------------------------------------------------

    df = results.merge(
        drivers,
        left_on="driverId",
        right_index=True,
        how="left"
    )

    # adicionar ano da corrida
    df = df.merge(
        races[["year"]],
        left_on="raceId",
        right_index=True,
        how="left"
    )

    # nota: talvez depois adicionar mais colunas aqui


    # --------------------------------------------------
    # DATAFRAME PARA EQUIPAS
    # --------------------------------------------------

    # juntar resultados com construtores
    df_team = results.merge(
        constructors,
        left_on="constructorId",
        right_index=True
    )

    # poderia também adicionar o ano aqui, mas por agora não é necessário


    # --------------------------------------------------
    # DATAFRAME PARA CIRCUITOS
    # --------------------------------------------------

    # primeiro juntar corridas com circuitos
    df_circ = races.merge(
        circuits,
        left_on="circuitId",
        right_index=True
    )

    # depois juntar resultados
    df_circ = df_circ.merge(
        results,
        left_on="raceId",
        right_index=True
    )


    # --------------------------------------------------
    # RETURN FINAL
    # --------------------------------------------------

    return (
        df,
        df_team,
        df_circ,
        circuits,
        constructors,
        drivers,
        races,
        results
    )