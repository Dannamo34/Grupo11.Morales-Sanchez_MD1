# 02 - ETL Proyecto Pokémon

## 📌 Descripción
Este módulo realiza el proceso ETL (Extract, Transform, Load) utilizando la API pública PokeAPI.

Extrae información de Pokémon, la transforma en un DataFrame y la guarda en formato CSV.

---

## ⚙ Tecnologías utilizadas
- Python
- Requests
- Pandas
- PokeAPI

---

## 📂 Estructura

- scripts/extractor.py → Script principal
- data/pokemon_data.csv → Datos generados
- logs/etl.log → Registro de ejecución
- requirements.txt → Dependencias

---

## ▶ Cómo ejecutar

Activar entorno virtual:

source venv/bin/activate

Ejecutar el script:

python scripts/extractor.py

El archivo CSV se generará en:

data/pokemon_data.csv

---

## 🔄 Proceso ETL

1. Extract → Se consumen datos desde la API.
2. Transform → Se limpian y organizan los datos.
3. Load → Se guardan en formato CSV.