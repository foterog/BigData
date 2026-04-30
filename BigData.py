import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard IoT")

file = st.file_uploader("Sube tu archivo CSV")

if file:
    df = pd.read_csv(file)

    st.write(df.head())

    # Estadísticas
    st.write("Temperatura promedio:", df["temperature"].mean())

    # Gráfica
    plt.plot(df["temperature"])
    st.pyplot(plt)
