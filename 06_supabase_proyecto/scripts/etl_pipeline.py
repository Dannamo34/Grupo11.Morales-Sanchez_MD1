import pandas as pd
import os
import time
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv
from extractor import extract_pokemons

# cargar variables
load_dotenv()

# conexión Supabase
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def run_etl(limit=20):
    inicio = time.time()

    try:
        # =============================
        # EXTRACT
        # =============================
        print(f"📊 Extrayendo {limit} Pokémon...")
        df = extract_pokemons(limit)

        registros_extraidos = len(df)

        if df.empty:
            raise Exception("No se extrajeron datos")

        # =============================
        # LOAD (bulk insert)
        # =============================
        df.to_sql("pokemon", engine, if_exists="append", index=False)
        registros_guardados = len(df)
        registros_fallidos = 0

        estado = "SUCCESS"
        mensaje = "Carga completada correctamente"

        print(f"✅ Bulk insert completado: {registros_guardados} registros")

    except Exception as e:
        registros_extraidos = 0
        registros_guardados = 0
        registros_fallidos = 1
        estado = "ERROR"
        mensaje = str(e)

        print(f"❌ Error en ETL: {mensaje}")

    # =============================
    # MÉTRICAS ETL
    # =============================
    fin = time.time()
    tiempo_total = fin - inicio

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO metricas_etl (
                registros_extraidos,
                registros_guardados,
                registros_fallidos,
                tiempo_ejecucion_segundos,
                estado,
                mensaje
            )
            VALUES (
                :extraidos,
                :guardados,
                :fallidos,
                :tiempo,
                :estado,
                :mensaje
            )
        """), {
            "extraidos": registros_extraidos,
            "guardados": registros_guardados,
            "fallidos": registros_fallidos,
            "tiempo": tiempo_total,
            "estado": estado,
            "mensaje": mensaje
        })

        conn.commit()

    print(f"✅ ETL completado — Guardados: {registros_guardados} | Fallidos: {registros_fallidos}")


if __name__ == "__main__":
    cantidad = int(input("¿Cuántos Pokémon deseas cargar? "))
    run_etl(cantidad)