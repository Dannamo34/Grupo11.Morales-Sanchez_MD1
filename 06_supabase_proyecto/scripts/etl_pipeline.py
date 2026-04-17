import pandas as pd
import time
from sqlalchemy import text
from dotenv import load_dotenv
from scripts.extractor import extract_pokemons
from scripts.database import get_engine

load_dotenv()

engine = get_engine()

def run_etl(limit=20):
    inicio = time.time()

    try:
        print(f"📊 Extrayendo {limit} Pokémon...")
        df = extract_pokemons(limit)

        registros_extraidos = len(df)

        if df.empty:
            raise Exception("No se extrajeron datos")

        # =============================
        # LOAD SIN DUPLICADOS
        # =============================
        registros_guardados = 0

        for _, row in df.iterrows():
            try:
                row.to_frame().T.to_sql("pokemon", engine, if_exists="append", index=False)
                registros_guardados += 1
            except:
                pass

        registros_fallidos = registros_extraidos - registros_guardados

        estado = "SUCCESS"
        mensaje = "Carga completada correctamente"

    except Exception as e:
        registros_extraidos = 0
        registros_guardados = 0
        registros_fallidos = 1
        estado = "ERROR"
        mensaje = str(e)[:200]  # 🔥 evita error varchar

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

    print(f"✅ ETL completado")