import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard IoT Industrial", layout="wide")

# Título Principal
st.title("📊 BigData Dashboard")

# --- CARGA DE DATOS ---
file = st.file_uploader("Sube tu archivo CSV", type=['csv'])

if file:
    df = pd.read_csv(file)
    
    # 1. PREPROCESAMIENTO DE FECHAS
    # Intentamos convertir la columna de tiempo. Ajusta 'timestamp' si tu columna se llama distinto.
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # --- 4. FILTROS INTERACTIVOS ---
    st.sidebar.header("4. Filtros Interactivos")
    
    # Filtro por device_id
    if 'device_id' in df.columns:
        device_list = ["Todos"] + list(df['device_id'].unique())
        selected_device = st.sidebar.selectbox("Seleccionar Dispositivo", device_list)
    else:
        st.sidebar.warning("Columna 'device_id' no encontrada")
        selected_device = "Todos"

    # Filtro por rango de fechas
    if 'timestamp' in df.columns:
        min_date = df['timestamp'].min().date()
        max_date = df['timestamp'].max().date()
        date_range = st.sidebar.date_input("Rango de fechas", [min_date, max_date])
    else:
        st.sidebar.warning("Columna 'timestamp' no encontrada")
        date_range = []

    # --- APLICACIÓN DE FILTROS ---
    df_filtered = df.copy()
    
    if selected_device != "Todos":
        df_filtered = df_filtered[df_filtered['device_id'] == selected_device]
    
    if len(date_range) == 2:
        start, end = date_range
        df_filtered = df_filtered[(df_filtered['timestamp'].dt.date >= start) & 
                                  (df_filtered['timestamp'].dt.date <= end)]

    # --- 2. ESTADÍSTICAS BÁSICAS (Analítica Descriptiva) ---
    st.header("2. Estadísticas básicas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if 'temperature' in df_filtered.columns:
            avg_temp = df_filtered['temperature'].mean()
            st.metric("Promedio Temperatura", f"{avg_temp:.2f} °C")
        else:
            st.metric("Promedio Temperatura", "N/A")

    with col2:
        if 'energy_consumption' in df_filtered.columns:
            avg_energy = df_filtered['energy_consumption'].mean()
            st.metric("Promedio Consumo", f"{avg_energy:.2f} kWh")
        else:
            st.metric("Promedio Consumo", "N/A")

    with col3:
        if 'vibration' in df_filtered.columns:
            max_vib = df_filtered['vibration'].max()
            st.metric("Máximo Vibración", f"{max_vib:.2f}")
        else:
            st.metric("Máximo Vibración", "N/A")

    with col4:
        st.write("**Conteo de estados:**")
        if 'state' in df_filtered.columns:
            st.write(df_filtered['state'].value_counts())
        else:
            st.caption("Columna 'state' no encontrada")

    # --- 3. VISUALIZACIONES ---
    st.header("3. Visualizaciones")
    
    # A. Serie de tiempo
    st.subheader("📈 Serie de tiempo: Temperatura vs tiempo")
    if 'temperature' in df_filtered.columns and 'timestamp' in df_filtered.columns:
        # Usamos el gráfico nativo de Streamlit que es más limpio
        st.line_chart(df_filtered.set_index('timestamp')['temperature'])
    else:
        st.info("Faltan datos para mostrar la serie de tiempo.")

    col_left, col_right = st.columns(2)

    with col_left:
        # B. Distribución
        st.subheader("📊 Histograma de consumo")
        if 'energy_consumption' in df_filtered.columns:
            fig, ax = plt.subplots()
            ax.hist(df_filtered['energy_consumption'], bins=15, color='skyblue', edgecolor='black')
            ax.set_xlabel("Consumo")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

    with col_right:
        # C. Relación entre variables
        st.subheader("🔍 Temperatura vs Consumo")
        if 'temperature' in df_filtered.columns and 'energy_consumption' in df_filtered.columns:
            fig2, ax2 = plt.subplots()
            ax2.scatter(df_filtered['temperature'], df_filtered['energy_consumption'], alpha=0.6, color='green')
            ax2.set_xlabel("Temperatura")
            ax2.set_ylabel("Consumo")
            st.pyplot(fig2)

    # --- 5. SECCIÓN DE INSIGHTS ---
    st.header("5. Sección de insights (interpretación)")
    
    # Insight de Temperatura
    if 'temperature' in df_filtered.columns:
        if avg_temp > 30:
            st.warning(f"⚠️ Advertencia: La temperatura promedio es alta ({avg_temp:.2f}°C).")
        else:
            st.success("✅ Temperatura promedio estable.")

    # Insight de Estados
    if 'state' in df_filtered.columns:
        if 'FAIL' in df_filtered['state'].values:
            st.error("🚨 Alerta: Se han detectado registros en estado FAIL.")
        else:
            st.info("ℹ️ No se detectan fallos en la selección actual.")

else:
    st.info("Carga un archivo CSV para visualizar el Dashboard.")
