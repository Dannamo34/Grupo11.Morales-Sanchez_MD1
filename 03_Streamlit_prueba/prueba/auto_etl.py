import time
import schedule
from scripts.extractor import WeatherstackExtractor

def ejecutar_etl():
    print("⏳ Ejecutando ETL automático...")
    extractor = WeatherstackExtractor()
    extractor.ejecutar_extraccion()
    print("✅ ETL completado")

# Ejecutar cada 1 hora
schedule.every(1).hours.do(ejecutar_etl)

print("🚀 Automatización iniciada (ETL cada 1 hora)...")

while True:
    schedule.run_pending()
    time.sleep(60)

