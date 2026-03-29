import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gestión de Part Numbers", layout="wide")

# --- BLOQUE DE DISEÑO PERSONALIZADO (CSS) ---
st.markdown("""
    <style>
    /* Estilo para los títulos de las columnas */
    [data-testid="stHeader"] {
        background-color: #791f37 !important; /* Azul oscuro empresarial */
    }
    
    /* Forzar negrilla y color en las cabeceras del DataFrame */
    th {
        background-color: #1f4e79 !important; 
        color: white !important; 
        font-weight: 900 !important; 
        font-size: 14px !important;
        text-transform: uppercase;
    }

    /* Estilo general de la tabla */
    .stDataFrame {
        border: 2px solid #1f4e79;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Part Numbers")

try:
    # 1. Leer el archivo
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1')

    # 2. LIMPIEZA PROFUNDA
    df = df.replace(['None', 'none', 'nan', '', ' '], np.nan)
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: Wire")

    if busqueda:
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df = df[mask]

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df)}** registros:")
    
    # Usamos st.dataframe con una configuración que resalta los encabezados
    st.dataframe(
        df.fillna(""), 
        use_container_width=True, 
        hide_index=True
    )

except Exception as e:
    st.error(f"Error: {e}")



