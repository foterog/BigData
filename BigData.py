import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard IoT", layout="wide")

# Título (Requisito de imagen 1)
st.title("📊 BigData Dashboard")

# --- CARGA DE DATOS ---
file = st.file_uploader("Sube tu archivo CSV", type=['csv'])

if file:
    df = pd.read_csv(file)

    # Convertir timestamp a datetime para que los filtros funcionen
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- 4. FILTROS INTERACTIVOS ---
    st.sidebar.header("4. Filtros")
    
    # Filtrar por device_id
    device_list = ["Todos"] + list(df['device_id'].unique())
    selected_device = st.sidebar.selectbox("ID del Dispositivo", device_list)

    # Filtrar por rango de fechas
    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()
    date_range = st.sidebar.date_input("Rango de fechas", [min_date, max_date])

    # Aplicar filtros al DataFrame
    df_filtered = df.copy()
    if selected_device != "Todos":
        df_filtered = df_filtered[df_filtered['device_id'] == selected_device]
    
    if len(date_range) == 2:
        start, end = date_range
        df_filtered = df_filtered[(df_filtered['timestamp'].dt.date >= start) & 
                                  (df_filtered['timestamp'].dt.date <= end)]

   # --- 2. ESTADÍSTICAS BÁSICAS ---
st.header("2. Estadísticas básicas (Analítica Descriptiva)")
col1, col2, col3, col4 = st.columns(4)

# Función auxiliar para evitar repetir código de error
def get_col_val(df, col_name, method="mean"):
    if col_name in df.columns:
        return df[col_name].mean() if method == "mean" else df[col_name].max()
    return None

with col1:
    val = get_col_val(df_filtered, 'temperature')
    st.metric("Promedio Temperatura", f"{val:.2f} °C" if val is not None else "N/A")

with col2:
    val = get_col_val(df_filtered, 'energy_consumption')
    st.metric("Promedio Consumo", f"{val:.2f} kWh" if val is not None else "N/A")

with col3:
    val = get_col_val(df_filtered, 'vibration', "max")
    st.metric("Máximo Vibración", f"{val:.2f}" if val is not None else "N/A")

with col4:
    st.write("**Conteo de estados:**")
    # AQUÍ ESTABA EL ERROR: Ahora verificamos antes de ejecutar
    if 'state' in df_filtered.columns:
        st.write(df_filtered['state'].value_counts())
    else:
        st.warning("Columna 'state' no encontrada")

# ... (Sección de gráficas igual a la anterior) ...

# --- 5. SECCIÓN DE INSIGHTS ---
st.header("5. Sección de insights (interpretación)")

if 'temperature' in df_filtered.columns:
    avg_temp = df_filtered['temperature'].mean()
    if avg_temp > 30:
        st.warning(f"⚠️ Advertencia: Temperatura promedio de {avg_temp:.2f}°C (Superior a 30).")
    else:
        st.success("✅ Temperatura bajo control.")

if 'state' in df_filtered.columns:
    if 'FAIL' in df_filtered['state'].values:
        st.error("🚨 Alerta: Se detectaron registros en estado FAIL.")
    else:
        st.info("ℹ️ No hay registros de fallos.")
else:
    st.info("No se pueden generar insights de estado (columna ausente).")
