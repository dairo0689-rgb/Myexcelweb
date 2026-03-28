import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Visor de Part Numbers", layout="wide")

st.title("📦 Consulta de Inventario - Part Numbers")

# Intentamos leer tu archivo específico
try:
    df = pd.read_csv("PN_APP.csv")

    
    # Buscador opcional
    busqueda = st.text_input("Buscar por nombre o número de parte:")
    if busqueda:
        df = df[df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().values, axis=1)]

    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.info("Asegúrate de que el nombre del archivo en el código coincida con tu Excel.")
