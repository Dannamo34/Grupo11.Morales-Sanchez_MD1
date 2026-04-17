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
# CARGAR IMAGEN (SEGURO)
# =========================
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        return None
    except Exception:
        return None

img_base64 = get_base64_image("poke.jpg")

# =========================
# ESTILOS + ANIMACIONES 🎨
# =========================
st.markdown(f"""
<style>

/* Fondo */
body {{
    background: linear-gradient(135deg, #0f172a, #020617);
}}

/* Animación */
@keyframes fadeIn {{
    from {{opacity: 0; transform: translateY(-20px);}}
    to {{opacity: 1; transform: translateY(0);}}
}}

/* HEADER */
.header-container {{
    text-align: center;
    animation: fadeIn 1s ease-in;
}}

.header-img {{
    width: 420px;
    margin-bottom: 15px;
    transition: transform 0.3s ease;
}}

.header-img:hover {{
    transform: scale(1.08);
}}

.header-title {{
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* KPIs */
.kpi {{
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    transition: all 0.3s ease;
}}

.kpi:hover {{
    transform: scale(1.05);
    box-shadow: 0px 0px 20px rgba(255,255,255,0.2);
}}

.kpi1 {{background: linear-gradient(135deg, #22c55e, #4ade80);}}
.kpi2 {{background: linear-gradient(135deg, #3b82f6, #60a5fa);}}
.kpi3 {{background: linear-gradient(135deg, #f59e0b, #fbbf24);}}
.kpi4 {{background: linear-gradient(135deg, #ef4444, #f87171);}}

/* BOTONES */
.stButton>button {{
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    height: 3em;
    transition: 0.3s;
}}

.stButton>button:hover {{
    transform: scale(1.05);
}}

/* SIDEBAR MÁS CLARO */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #475569, #64748b);
    color: white;
    border-right: 2px solid #38bdf8;
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

</style>

<div class="header-container">
    {f'<img src="data:image/png;base64,{img_base64}" class="header-img">' if img_base64 else ''}
    <div class="header-title">🚀 Pokémon Data</div>
</div>

""", unsafe_allow_html=True)

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
# DATA
# =========================
df = pd.read_sql("SELECT * FROM pokemon", engine)

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='kpi kpi1'><h3>Total Pokémon</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi kpi2'><h3>Altura Promedio</h3><h2>{round(df['height'].mean(),2)}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi kpi3'><h3>Peso Promedio</h3><h2>{round(df['weight'].mean(),2)}</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi kpi4'><h3>Experiencia Promedio</h3><h2>{round(df['base_experience'].mean(),2)}</h2></div>", unsafe_allow_html=True)

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

fig1 = px.histogram(df, x="base_experience", nbins=20, color_discrete_sequence=["#38bdf8"])
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚖️ Peso vs Altura")
    fig2 = px.scatter(df, x="height", y="weight", color="types", size="base_experience")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("📈 Top Pokémon")
    top = df.sort_values(by="base_experience", ascending=False).head(10)
    fig3 = px.bar(top, x="name", y="base_experience", color="types")
    st.plotly_chart(fig3, use_container_width=True)

# MÁS GRÁFICAS
st.subheader("🧬 Tipos de Pokémon")

tipos = df["types"].str.split(", ").explode()
tipos_count = tipos.value_counts().reset_index()
tipos_count.columns = ["tipo", "cantidad"]

fig4 = px.pie(tipos_count, names="tipo", values="cantidad")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("📦 Distribución de Peso")

fig5 = px.box(df, y="weight", color="types")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("⚡ Experiencia vs Peso")

fig6 = px.scatter(df, x="base_experience", y="weight", color="types", size="height")
st.plotly_chart(fig6, use_container_width=True)

# =========================
# TABLA
# =========================
st.subheader("📋 Datos")
st.dataframe(df, use_container_width=True, height=400)

# =========================
# MÉTRICAS
# =========================
st.subheader("📈 Historial ETL")

metricas = pd.read_sql("SELECT * FROM metricas_etl ORDER BY id DESC LIMIT 10", engine)
st.dataframe(metricas, use_container_width=True)