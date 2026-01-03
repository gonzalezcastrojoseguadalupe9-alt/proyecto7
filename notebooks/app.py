import pandas as pd
import plotly.express as px
import streamlit as st

# Encabezado
st.header("Análisis de anuncios de coches")

# Leer datos
car_data = pd.read_csv("vehicles_us.csv")

# Casillas de verificación
build_histogram = st.checkbox("Construir histograma")
build_scatter = st.checkbox("Construir gráfico de dispersión")

# Histograma
if build_histogram:
    st.write(
        "Histograma del kilometraje (odometer) "
        "de los anuncios de coches"
    )
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersión
if build_scatter:
    st.write(
        "Gráfico de dispersión entre el precio y el kilometraje"
    )
    fig = px.scatter(
        car_data,
        x="odometer",
        y="price"
    )
    st.plotly_chart(fig, use_container_width=True)
