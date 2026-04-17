import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.database import get_engine
from scripts.etl_pipeline import run_etl
import base64
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Pokemon Analytics Platform",
    page_icon="🔥",
    layout="wide"
)

# =========================
# IMAGEN SEGURA (NO FALLA EN CLOUD)
# =========================
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = os.path.join(BASE_DIR, "poke.jpg")

def get_base64_image(path):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except:
        return None

img_base64 = get_base64_image(IMG_PATH)

# =========================
# ESTILOS PRO + ANIMACIONES
# =========================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

/* Animación */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

/* HEADER */
.header-container {
    text-align: center;
    animation: fadeIn 1s ease-in;
}

.header-img {
    width: 500px;
    margin-bottom: 10px;
}

.header-title {
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* KPI */
.kpi {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    transition: 0.3s;
}

.kpi:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(255,255,255,0.2);
}

.kpi1 {background: linear-gradient(135deg, #22c55e, #4ade80);}
.kpi2 {background: linear-gradient(135deg, #3b82f6, #60a5fa);}
.kpi3 {background: linear-gradient(135deg, #f59e0b, #fbbf24);}
.kpi4 {background: linear-gradient(135deg, #ef4444, #f87171);}

/* BOTONES */
.stButton>button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    height: 3em;
}

/* SIDEBAR CLARO */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #64748b, #94a3b8);
    color: white;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER DINÁMICO
# =========================
header_html = '<div class="header-container">'

if img_base64:
    header_html += f'<img src="data:image/png;base64,{img_base64}" class="header-img">'

header_html += '<div class="header-title">🚀 Pokémon Data Analytics Platform</div></div>'

st.markdown(header_html, unsafe_allow_html=True)

# =========================
# CONEXIÓN
# =========================
engine = get_engine()

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚡ Ejecutar ETL")

cantidad = st.sidebar.slider("Cantidad de Pokémon", 1, 100, 10)

if st.sidebar.button("🚀 Ejecutar ETL"):
    with st.spinner("Procesando datos..."):
        run_etl(cantidad)
    st.success("ETL ejecutado correctamente")

# =========================
# DATA SEGURA
# =========================
try:
    df = pd.read_sql("SELECT * FROM pokemon", engine)
except Exception:
    st.error("❌ Error conectando a Supabase. Revisa los Secrets.")
    st.stop()

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='kpi kpi1'><h3>Total Pokémon</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi kpi2'><h3>Altura Promedio</h3><h2>{round(df['height'].mean(),2)}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi kpi3'><h3>Peso Promedio</h3><h2>{round(df['weight'].mean(),2)}</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi kpi4'><h3>Experiencia</h3><h2>{round(df['base_experience'].mean(),2)}</h2></div>", unsafe_allow_html=True)

# =========================
# FILTROS
# =========================
st.sidebar.header("🔍 Filtros")

tipo = st.sidebar.selectbox("Tipo", ["Todos"] + sorted(df["types"].dropna().unique()))

if tipo != "Todos":
    df = df[df["types"].str.contains(tipo)]

# =========================
# GRÁFICAS
# =========================
st.subheader("📊 Distribución de Experiencia")
fig1 = px.histogram(df, x="base_experience")
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚖️ Peso vs Altura")
    fig2 = px.scatter(df, x="height", y="weight", color="types")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("📈 Top Pokémon")
    top = df.sort_values(by="base_experience", ascending=False).head(10)
    fig3 = px.bar(top, x="name", y="base_experience", color="types")
    st.plotly_chart(fig3, use_container_width=True)

# EXTRA GRÁFICAS
st.subheader("🧬 Tipos de Pokémon")
tipos = df["types"].str.split(", ").explode()
fig4 = px.pie(tipos.value_counts().reset_index(), names="index", values="types")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("📦 Distribución de Peso")
fig5 = px.box(df, y="weight", color="types")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("⚡ Experiencia vs Peso")
fig6 = px.scatter(df, x="base_experience", y="weight", color="types")
st.plotly_chart(fig6, use_container_width=True)

# =========================
# EXPORTAR CSV
# =========================
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Descargar CSV",
    csv,
    "pokemon_data.csv",
    "text/csv"
)

# =========================
# TABLA
# =========================
st.subheader("📋 Datos")
st.dataframe(df, use_container_width=True)

# =========================
# MÉTRICAS ETL
# =========================
st.subheader("📈 Historial ETL")
metricas = pd.read_sql("SELECT * FROM metricas_etl ORDER BY id DESC LIMIT 10", engine)
st.dataframe(metricas, use_container_width=True)