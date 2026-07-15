import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_predict():
    url = f"{BASE_URL}/boleteria/predict"

    # Caso 1: Obra NUEVA (Cold Start)
    payload_nueva = {
        "obra": {
            "nombre": "El Principito",
            "genero": "Drama",
            "popularidad_elenco": 6.5,
            "tiene_premios": True
        },
        "temporada": {
            "total_funciones_programadas": 20,
            "numero_funcion_actual": 1,
            "fecha_funcion": (datetime.now() + timedelta(days=5)).isoformat()
        },
        "contexto_actual": {
            "boletas_vendidas_hoy": 0,
            "aforo_total_sala": 300
        }
    }

    print("🔮 Prediciendo Obra NUEVA (Cold Start)...")
    response = requests.post(url, json=payload_nueva)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print("-" * 50)

    # Caso 2: Obra en MITAD DE TEMPORADA (Mid-Season)
    payload_media = {
        "obra": {
            "nombre": "Hamlet",
            "genero": "Clasico",
            "popularidad_elenco": 8.0,
            "tiene_premios": True
        },
        "temporada": {
            "total_funciones_programadas": 30,
            "numero_funcion_actual": 15,
            "fecha_funcion": (datetime.now() + timedelta(days=2)).isoformat()
        },
        "contexto_actual": {
            "boletas_vendidas_hoy": 120,
            "aforo_total_sala": 400
        }
    }

    print("🔮 Prediciendo Obra en MITAD DE TEMPORADA (Mid-Season)...")
    response = requests.post(url, json=payload_media)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_predict()