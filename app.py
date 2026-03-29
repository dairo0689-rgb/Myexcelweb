import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gestión de Part Numbers", layout="wide")

# --- BLOQUE DE DISEÑO PERSONALIZADO (CSS) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] {
        background-color: #3392b5 !important;
    }
    
    th {
        background-color: #1f4e79 !important; 
        color: white !important; 
        font-weight: 900 !important; 
        font-size: 14px !important;
        text-transform: uppercase;
    }

    .stDataFrame {
        border: 2px solid #1f4e79;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Part Numbers")

try:
    # 1. Leer el archivo - FORZAMOS DTYPE=STR PARA EVITAR NOTACIÓN CIENTÍFICA
    # Esto hace que todos los números se lean literalmente como texto
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1', dtype=str)

    # 2. LIMPIEZA PROFUNDA
    df = df.replace(['None', 'none', 'nan', 'NaN', '', ' '], np.nan)
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: Wire")

    if busqueda:
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df = df[mask]

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df)}** registros:")
    
    # Usamos column_config para asegurar que las columnas de números se vean como texto plano
    st.dataframe(
        df.fillna(""), 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "PART NUMBER": st.column_config.TextColumn("PART NUMBER"),
            "PART NUMBER.1": st.column_config.TextColumn("PART NUMBER.1"),
            "BARCODE": st.column_config.TextColumn("BARCODE")
        }
    )

except Exception as e:
    st.error(f"Error: {e}")




