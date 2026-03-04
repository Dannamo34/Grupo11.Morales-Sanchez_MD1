import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Pokémon", layout="wide")

st.title("⚡ Dashboard Pokémon")
st.markdown("### Análisis Exploratorio Interactivo")

@st.cache_data
def load_data():
        return pd.read_csv("../02_etl_proyecto/data/pokemon_data.csv")
df = load_data()

# =====================
# MÉTRICAS
# =====================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pokémon", len(df))
col2.metric("Promedio Experiencia", round(df["base_experience"].mean(), 1))
col3.metric("Altura Promedio", round(df["height"].mean(), 1))
col4.metric("Peso Promedio", round(df["weight"].mean(), 1))

st.divider()

# =====================
# FILTRO
# =====================
tipos_unicos = sorted(set(", ".join(df["types"]).split(", ")))

tipo = st.sidebar.selectbox("Filtrar por tipo", ["Todos"] + tipos_unicos)

if tipo != "Todos":
    df = df[df["types"].str.contains(tipo)]

# =====================
# TABLA
# =====================
st.subheader("📋 Datos")
st.dataframe(df, use_container_width=True)

# =====================
# GRÁFICO 1
# =====================
st.subheader("🔥 Experiencia Base por Pokémon")

fig1 = px.bar(
    df,
    x="name",
    y="base_experience",
    color="base_experience",
    color_continuous_scale="reds",
)

st.plotly_chart(fig1, use_container_width=True)

# =====================
# GRÁFICO 2
# =====================
st.subheader("⚖ Relación Altura vs Peso")

fig2 = px.scatter(
    df,
    x="height",
    y="weight",
    size="base_experience",
    hover_name="name",
    color="base_experience",
    color_continuous_scale="viridis",
)

st.plotly_chart(fig2, use_container_width=True)