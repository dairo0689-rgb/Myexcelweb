import streamlit as st
import pandas as pd
import numpy as np

# Configuración de página
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
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.9);
        color: #1f4e79;
        text-align: center;
        padding: 5px;
        font-weight: bold;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Gestión de Part Numbers")

# --- FUNCIÓN DE LIMPIEZA DE NÚMEROS ---
def forzar_numero_completo(valor):
    if pd.isna(valor) or str(valor).strip() in ["", "nan", "NaN", "None"]:
        return ""
    try:
        # Limpiar espacios y normalizar formato numérico
        val_str = str(valor).strip().replace(',', '.')
        # Si parece notación científica, convertir a número real y luego a texto sin decimales
        if "E+" in val_str.upper() or "." in val_str:
            return "{:.0f}".format(float(val_str))
        return val_str
    except:
        return str(valor).strip()

try:
    # 1. LEER EL ARCHIVO (Probando UTF-8-SIG para Excel y Ñs)
    try:
        df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='utf-8-sig', dtype=str)
    except:
        df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1', dtype=str)

    # 2. APLICAR LIMPIEZA
    for col in df.columns:
        df[col] = df[col].apply(forzar_numero_completo)

    # Limpiar columnas vacías generadas por Excel
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: Faucet o 298029...")

    if busqueda:
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_mostrar = df[mask]
    else:
        df_mostrar = df

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df_mostrar)}** registros:")
    
    # Creamos la configuración de columnas dinámicamente para que Streamlit no arruine los números
    config_columnas = {col: st.column_config.TextColumn(col) for col in df_mostrar.columns}

    st.dataframe(
        df_mostrar.fillna(""), 
        use_container_width=True, 
        hide_index=True,
        column_config=config_columnas
    )

except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'PN_APP.csv'.")
except Exception as e:
    st.error(f"Error inesperado: {e}")

# --- CRÉDITOS ---
st.markdown('<div class="footer">Created by Dairo Romero</div>', unsafe_allow_html=True)
