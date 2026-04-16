import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def _get_db_config():
    # ==============================
    # 1. Intentar con Streamlit Cloud
    # ==============================
    try:
        import streamlit as st
        host = st.secrets.get("DB_HOST", "")

        # evitar usar localhost en producción
        if host and host != "localhost":
            return {
                "host": host,
                "port": st.secrets.get("DB_PORT", "5432"),
                "user": st.secrets.get("DB_USER", "postgres"),
                "password": st.secrets.get("DB_PASSWORD", ""),
                "dbname": st.secrets.get("DB_NAME", "postgres"),
            }
    except Exception:
        pass  # cuando no estás en streamlit

    # ==============================
    # 2. Fallback a .env (local)
    # ==============================
    host = os.getenv("DB_HOST", "localhost")

    return {
        "host": host,
        "port": os.getenv("DB_PORT", "5432"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "dbname": os.getenv("DB_NAME", "postgres"),
    }


def get_engine():
    config = _get_db_config()

    password = quote_plus(config["password"])

    DATABASE_URL = (
        f"postgresql://{config['user']}:{password}"
        f"@{config['host']}:{config['port']}/{config['dbname']}"
    )

    return create_engine(DATABASE_URL)