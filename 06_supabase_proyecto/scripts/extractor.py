import requests
import pandas as pd
import time
import os

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

# Ruta correcta hacia la carpeta data
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/pokemon_data.csv")


def get_pokemon_data(pokemon_id):
    try:
        response = requests.get(f"{BASE_URL}{pokemon_id}", timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "base_experience": data["base_experience"],
            "types": ", ".join([t["type"]["name"] for t in data["types"]])
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error con Pokémon {pokemon_id}: {http_err}")

    except requests.exceptions.ConnectionError:
        print(f"Error de conexión con Pokémon {pokemon_id}")

    except requests.exceptions.Timeout:
        print(f"Tiempo de espera agotado con Pokémon {pokemon_id}")

    except Exception as err:
        print(f"Error inesperado con Pokémon {pokemon_id}: {err}")

    return None


def extract_pokemons(limit=20):
    pokemon_list = []

    for i in range(1, limit + 1):
        print(f"Extrayendo Pokémon {i}...")
        pokemon = get_pokemon_data(i)

        if pokemon:
            pokemon_list.append(pokemon)

        time.sleep(0.5)  # evitar sobrecargar la API

    return pd.DataFrame(pokemon_list)


if __name__ == "__main__":
    opcion = input("¿Quieres (1) extraer varios Pokémon o (2) ver solo uno? ")

    if opcion == "1":
        cantidad = input("¿Cuántos Pokémon deseas extraer? ")
        df = extract_pokemons(int(cantidad))

        # Guardar en carpeta data
        df.to_csv(DATA_PATH, index=False)

        print(f"Extracción completada. Archivo guardado en {DATA_PATH}")

    elif opcion == "2":
        pokemon_id = input("Ingresa el nombre o ID del Pokémon: ")
        pokemon = get_pokemon_data(pokemon_id)

        if pokemon:
            print("\nInformación del Pokémon:\n")
            for clave, valor in pokemon.items():
                print(f"{clave}: {valor}")
        else:
            print("No se encontró el Pokémon.")

    else:
        print("Opción no válida.")
        
        