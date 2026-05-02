import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

# 🔹 cargar variables de entorno
load_dotenv()

def _get_db_config():
    # ==============================
    # 1. Streamlit Cloud (PRIORIDAD)
    # ==============================
    try:
        import streamlit as st

        host = st.secrets.get("DB_HOST")

        if host and host != "localhost":
            return {
                "host": host,
                "port": st.secrets.get("DB_PORT", "6543"),
                "user": st.secrets.get("DB_USER", "postgres"),
                "password": st.secrets.get("DB_PASSWORD", ""),
                "dbname": st.secrets.get("DB_NAME", "postgres"),
            }

    except Exception:
        pass

    # ==============================
    # 2. LOCAL (.env)
    # ==============================
    return {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_NAME"),
    }


def get_engine():
    config = _get_db_config()

    # 🚨 VALIDACIÓN (evita errores silenciosos)
    if not all(config.values()):
        raise ValueError(f"❌ Variables de entorno incompletas: {config}")

    # 🔒 codificar usuario y contraseña
    user = quote_plus(config["user"])
    password = quote_plus(config["password"])

    # 🔥 URL CORRECTA (POOLER 6543)
    DATABASE_URL = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{config['host']}:{config['port']}/{config['dbname']}"
    )

    # ⚡ engine optimizado para Supabase
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "sslmode": "require"   # 🔥 obligatorio en Supabase
        },
        pool_pre_ping=True,
        echo=False
    )

    print("✅ Conexión a la base de datos lista")

    return engine


# 🔹 instancia global (para importar directo)
engine = get_engine() 