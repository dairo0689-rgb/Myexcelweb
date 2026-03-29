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
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Gestión de Part Numbers")

# --- FUNCIÓN PARA LIMPIAR NOTACIÓN CIENTÍFICA ---
def corregir_formato_numero(valor):
    """Convierte valores tipo 2.98E+12 a strings numéricos completos"""
    if pd.isna(valor) or str(valor).strip() == "":
        return ""
    
    # Convertimos a string y quitamos espacios
    val_str = str(valor).replace(',', '.').strip()
    
    try:
        # Si detecta notación científica (E+), lo convierte a entero y luego a string
        if "E+" in val_str.upper():
            return "{:.0f}".format(float(val_str))
        
        # Si es un número decimal que termina en .0, lo limpiamos
        if val_str.endswith('.0'):
            return val_str[:-2]
            
        return val_str
    except:
        return val_str

try:
    # 1. Leer el archivo forzando todo a String (Texto)
    # Esto evita que Pandas arruine los números desde el inicio
    df = pd.read_csv("PN_APP.csv", sep=None, engine='python', encoding='latin1', dtype=str)

    # 2. LIMPIEZA Y CORRECCIÓN DE COLUMNAS NUMÉRICAS
    # Aplicamos la corrección a todas las columnas que suelen tener IDs largos
    columnas_numericas = ['PART NUMBER', 'PART NUMBER.1', 'BARCODE']
    
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = df[col].apply(corregir_formato_numero)

    # Limpieza general de nulos y columnas vacías
    df = df.replace(['None', 'none', 'nan', 'NaN', 'NAN'], np.nan)
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # 3. INTERFAZ: Buscador
    busqueda = st.text_input("🔍 Buscar por nombre o número de parte:", placeholder="Ej: Wire o 298029...")

    if busqueda:
        # Buscamos en todas las filas convirtiendo todo a string para comparar
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_filtrado = df[mask]
    else:
        df_filtrado = df

    # 4. MOSTRAR TABLA
    st.write(f"Mostrando **{len(df_filtrado)}** registros:")
    
    # Usamos column_config para forzar a Streamlit a tratar las columnas como TEXTO
    # Esto evita que la interfaz les ponga comas de miles o puntos decimales.
    st.dataframe(
        df_filtrado.fillna(""), 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "PART NUMBER": st.column_config.TextColumn("PART NUMBER"),
            "PART NUMBER.1": st.column_config.TextColumn("PART NUMBER.1"),
            "BARCODE": st.column_config.TextColumn("BARCODE")
        }
    )

except FileNotFoundError:
    st.error("No se encontró el archivo 'PN_APP.csv'. Asegúrate de que esté en la misma carpeta que este script.")
except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")

