import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gestión de Part Numbers", layout="wide")

st.title("📦Part Numbers LATAM")

try:
    # 1. Leer el archivo
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1')

    # 2. LIMPIEZA PROFUNDA
    # Reemplazamos "None" (texto), espacios vacíos y NaNs por un valor nulo real
    df = df.replace(['None', 'none', 'nan', '', ' '], np.nan)
    
    # Eliminamos columnas que tengan TODO nulo
    df = df.dropna(axis=1, how='all')
    
    # Eliminamos columnas "Unnamed"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Opcional: Si quieres ocultar columnas específicas que ves que sobran (ejemplo: 'TOOL')
    # puedes descomentar la siguiente línea y poner los nombres:
    # df = df.drop(columns=['TOOL', 'BARCODE'], errors='ignore')

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: CABLE")

    if busqueda:
        # Filtrado que ignora los valores nulos para que no de error
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df = df[mask]

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df)}** registros:")
    
    # Usamos st.dataframe pero limpiamos los valores NaN visualmente
    st.dataframe(df.fillna(""), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error: {e}")

