import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def _get_db_config():
    # ==============================
    # 1. Streamlit Cloud (PRIORIDAD)
    # ==============================
    try:
        import streamlit as st

        host = st.secrets.get("DB_HOST")

        # SOLO usar si existe y NO es localhost
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
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "dbname": os.getenv("DB_NAME", "postgres"),
    }


def get_engine():
    config = _get_db_config()

    # 🔒 codificar usuario y contraseña (MUY IMPORTANTE)
    user = quote_plus(config["user"])
    password = quote_plus(config["password"])

    # 🔥 URL con SSL (OBLIGATORIO para Supabase)
    DATABASE_URL = (
        f"postgresql://{user}:{password}"
        f"@{config['host']}:{config['port']}/{config['dbname']}"
        f"?sslmode=require"
    )

    # ⚡ engine optimizado
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,   # evita conexiones muertas
        echo=False
    )

    return engine