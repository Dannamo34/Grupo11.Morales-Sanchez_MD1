import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# ========================
# CONFIGURACIÓN
# ========================

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ========================
# STREAMLIT CONFIG
# ========================

st.set_page_config(
    page_title="Dashboard Climático Colombia",
    page_icon="🌤",
    layout="wide"
)

st.title("🌤 Dashboard Climático Colombia")
st.markdown("### Análisis en tiempo real del clima")

# ========================
# CARGAR DATOS
# ========================

df = pd.read_sql("SELECT * FROM clima", engine)

if df.empty:
    st.warning("No hay datos en la base de datos")
    st.stop()

# ========================
# MÉTRICAS PRINCIPALES
# ========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Promedio Temp", f"{df['temperatura'].mean():.1f} °C")
col2.metric("💧 Promedio Humedad", f"{df['humedad'].mean():.1f} %")
col3.metric("💨 Promedio Viento", f"{df['velocidad_viento'].mean():.1f} km/h")
col4.metric("🔥 Promedio Sensación", f"{df['sensacion_termica'].mean():.1f} °C")

st.divider()

# ========================
# GRÁFICAS INTERACTIVAS
# ========================

colA, colB = st.columns(2)

with colA:
    fig_temp = px.bar(
        df,
        x="ciudad",
        y="temperatura",
        color="temperatura",
        color_continuous_scale="thermal",
        title="Temperatura por Ciudad"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with colB:
    fig_hum = px.bar(
        df,
        x="ciudad",
        y="humedad",
        color="humedad",
        color_continuous_scale="blues",
        title="Humedad por Ciudad"
    )
    st.plotly_chart(fig_hum, use_container_width=True)

colC, colD = st.columns(2)

with colC:
    fig_viento = px.scatter(
        df,
        x="ciudad",
        y="velocidad_viento",
        size="velocidad_viento",
        color="velocidad_viento",
        color_continuous_scale="viridis",
        title="Velocidad del Viento"
    )
    st.plotly_chart(fig_viento, use_container_width=True)

with colD:
    fig_sensacion = px.bar(
        df,
        x="ciudad",
        y="sensacion_termica",
        color="sensacion_termica",
        color_continuous_scale="reds",
        title="Sensación Térmica"
    )
    st.plotly_chart(fig_sensacion, use_container_width=True)

st.divider()

st.subheader("📊 Datos Completos")
st.dataframe(df, use_container_width=True)