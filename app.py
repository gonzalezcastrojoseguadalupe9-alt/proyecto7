import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuración de la página 
st.set_page_config(page_title="Dashboard de Autos", layout="wide")

# 2. Encabezado y Título
st.title(" Análisis del Mercado de Autos Usados")
st.markdown("""
Esta aplicación permite analizar los datos de anuncios de coches en EE. UU. 
Puedes explorar la relación entre el precio, el kilometraje y el tipo de vehículo.
""")

# 3. Leer datos
@st.cache_data
def load_data():
    data = pd.read_csv("vehicles_us.csv")
    # Limpieza básica
    data = data.dropna(subset=["price", "odometer", "type", "model"])
    # Intentar sacar el fabricante del modelo si no existe la columna
    if 'manufacturer' not in data.columns:
        data['manufacturer'] = data['model'].apply(lambda x: x.split()[0])
    return data

car_data = load_data()

# 4. Sección de Filtros en la Barra Lateral
st.sidebar.header("Filtros de búsqueda")

# Filtro por tipo de vehículo
tipos_seleccionados = st.sidebar.multiselect(
    "Selecciona el tipo de vehículo:",
    options=sorted(car_data["type"].unique()),
    default=[]
)

# Aplicar filtro si hay selección
df_filtrado = car_data.copy()
if tipos_seleccionados:
    df_filtrado = df_filtrado[df_filtrado["type"].isin(tipos_seleccionados)]

# 5. Visualizaciones Principales
st.header("Visualización de Datos")

col1, col2 = st.columns(2)

with col1:
    if st.checkbox("Mostrar Histograma de Kilometraje"):
        st.write("### Distribución del Kilometraje")
        fig_hist = px.histogram(df_filtrado, x="odometer", nbins=30, color_discrete_sequence=['indianred'])
        st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    if st.checkbox("Mostrar Gráfico de Dispersión"):
        st.write("### Precio vs. Kilometraje")
        fig_scatter = px.scatter(df_filtrado, x="odometer", y="price", opacity=0.5, color="type")
        st.plotly_chart(fig_scatter, use_container_width=True)

# 6. Gráfico de Comparación por Tipo (Caja)
st.divider()
st.header("Análisis por Categoría")

tab1, tab2 = st.tabs(["Precios por Tipo", "Distribución de Modelos"])

with tab1:
    st.write("### ¿Cómo varía el precio según el tipo de auto?")
    fig_box = px.box(df_filtrado, x="type", y="price", color="type")
    st.plotly_chart(fig_box, use_container_width=True)

with tab2:
    st.write("### Composición de la flota por tipo")
    fig_pie = px.pie(df_filtrado, names="type", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# 7. Conclusiones
st.divider()
st.write("## Conclusiones del Análisis")
st.info(f"Actualmente visualizando {len(df_filtrado)} anuncios.")

st.write("""
- **Kilometraje:** Se observa una correlación negativa; a mayor kilometraje, el precio tiende a bajar drásticamente.
- **Segmentos:** Los tipos 'truck' y 'SUV' suelen mantener un valor más alto comparado con sedanes, incluso con kilometrajes similares.
- **Datos:** Se eliminaron las filas con valores nulos en precio y kilometraje para asegurar la precisión de las gráficas.
""")