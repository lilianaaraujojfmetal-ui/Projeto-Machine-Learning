import pandas as pd
import streamlit as st

# -----------------------------
# LOAD DOS CSV
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


# -----------------------------
# PREPARAÇÃO DOS DATAFRAMES
# -----------------------------
@st.cache_data
def prepare_data():

    circuits, constructors, drivers, races, results, qualifying = load_data()

    # Merge principal (pilotos + resultados)
    df = results.merge(drivers, left_on='driverId', right_index=True, how='left')
    df = df.merge(races[['year']], left_on='raceId', right_index=True, how='left')

    # DataFrame para equipas
    df_team = results.merge(constructors, left_on='constructorId', right_index=True)

    # DataFrame para circuitos
    df_circ = races.merge(circuits, left_on="circuitId", right_index=True)
    df_circ = df_circ.merge(results, left_on='raceId', right_index=True)

    return df, df_team, df_circ, circuits, constructors, drivers, races, results