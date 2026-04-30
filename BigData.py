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

    with col1:
        avg_temp = df_filtered['temperature'].mean()
        st.metric("Promedio Temperatura", f"{avg_temp:.2f} °C")

    with col2:
        avg_energy = df_filtered['energy_consumption'].mean()
        st.metric("Promedio Consumo", f"{avg_energy:.2f} kWh")

    with col3:
        max_vib = df_filtered['vibration'].max()
        st.metric("Máximo Vibración", f"{max_vib:.2f}")

    with col4:
        st.write("**Conteo de estados:**")
        st.write(df_filtered['State'].value_counts())

    # --- 3. VISUALIZACIONES ---
    st.header("3. Visualizaciones")

    # A. Serie de tiempo (Temperatura vs Tiempo)
    st.subheader("📈 Serie de tiempo: Temperatura vs tiempo")
    # Streamlit maneja muy bien las series de tiempo con st.line_chart
    chart_data = df_filtered.set_index('timestamp')[['temperature']]
    st.line_chart(chart_data)

    col_a, col_b = st.columns(2)

    with col_a:
        # B. Distribución (Histograma de consumo)
        st.subheader("📊 Histograma de consumo")
        fig, ax = plt.subplots()
        ax.hist(df_filtered['energy_consumption'], bins=20, color='skyblue', edgecolor='black')
        ax.set_xlabel("Consumo energético")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

    with col_b:
        # C. Relación (Temperatura vs Consumo)
        st.subheader("🔍 Temperatura vs Consumo")
        fig2, ax2 = plt.subplots()
        ax2.scatter(df_filtered['temperature'], df_filtered['energy_consumption'], alpha=0.5, color='green')
        ax2.set_xlabel("Temperatura")
        ax2.set_ylabel("Consumo")
        st.pyplot(fig2)

    # --- 5. SECCIÓN DE INSIGHTS ---
    st.header("5. Sección de insights (interpretación)")
    
    # Lógica de advertencia de temperatura
    if avg_temp > 30:
        st.warning(f"⚠️ Advertencia: La temperatura promedio es de {avg_temp:.2f}°C (Superior a 30).")
    else:
        st.success("✅ Temperatura promedio bajo control.")

    # Lógica de alerta por fallos
    if 'FAIL' in df_filtered['state'].values:
        st.error("🚨 Alerta: Se detectaron registros en estado FAIL.")
    else:
        st.info("ℹ️ No hay registros de fallos en el periodo seleccionado.")

else:
    st.info("Por favor, sube el archivo CSV para comenzar.")
