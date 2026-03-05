import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# ------------------------
# Configuración de la página
# ------------------------
st.set_page_config(
    page_title="🌤️ Clima ETL Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# ------------------------
# CSS para el fondo y botones
# ------------------------
st.markdown("""
<style>
/* Fondo degradado */
body {
    background: linear-gradient(to right, #f0f8ff, #cce7ff);
}

/* Encabezado más grande y colorido */
h1 {
    color: #0d3b66;
}

/* Botones más bonitos */
.stButton>button {
    background-color: #f4d35e;
    color: #0d3b66;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
    width: 150px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌤️ Dashboard de Clima en Tiempo Real")
st.markdown("Visualiza los datos de clima de diferentes ciudades de manera interactiva y profesional.")

# ------------------------
# Conexión a PostgreSQL
# ------------------------
engine = create_engine(
    "postgresql+psycopg2://clima_user:clima123@localhost:5432/clima_db"
)

# ------------------------
# Cargar datos
# ------------------------
@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_sql("SELECT * FROM clima ORDER BY fecha_extraccion DESC", engine)
        return df
    except Exception as e:
        st.error(f"No se pudo conectar a la base de datos: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # ------------------------
    # Métricas principales en columnas
    # ------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Registros totales", len(df))
    col2.metric("Temperatura promedio", f"{df['temperatura'].mean():.1f} °C")
    col3.metric("Humedad promedio", f"{df['humedad'].mean():.1f} %")

    # ------------------------
    # Filtro de ciudades con botón dinámico
    # ------------------------
    st.subheader("🌆 Selección de ciudades")
    ciudades = st.multiselect(
        "Selecciona ciudades para mostrar en gráficos",
        df["ciudad"].unique(),
        default=df["ciudad"].unique()
    )

    # Botón para actualizar la selección
    if st.button("Actualizar datos"):
        st.experimental_rerun()

    df_filtrado = df[df["ciudad"].isin(ciudades)]

    # ------------------------
    # Tabla de datos recientes
    # ------------------------
    st.subheader("📋 Datos recientes")
    st.dataframe(df_filtrado, use_container_width=True)

    # ------------------------
    # Gráfico de temperatura
    # ------------------------
    st.subheader("🌡️ Temperatura por ciudad")
    fig_temp = px.line(
        df_filtrado,
        x="fecha_extraccion",
        y="temperatura",
        color="ciudad",
        markers=True,
        title="Temperatura en tiempo real",
        labels={"fecha_extraccion": "Fecha", "temperatura": "°C", "ciudad": "Ciudad"},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    # ------------------------
    # Gráfico de humedad promedio
    # ------------------------
    st.subheader("💧 Humedad promedio por ciudad")
    df_hum = df_filtrado.groupby("ciudad", as_index=False)["humedad"].mean()
    fig_hum = px.bar(
        df_hum,
        x="ciudad",
        y="humedad",
        color="ciudad",
        title="Humedad promedio por ciudad",
        labels={"ciudad": "Ciudad", "humedad": "%"},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_hum, use_container_width=True)

else:
    st.warning("No hay datos disponibles para mostrar.")
