import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_historical_data(n=500):
    """
    Genera n registros históricos realistas para entrenar el modelo.
    """
    data = []
    generos = ['Comedia', 'Drama', 'Musical', 'Infantil', 'Stand-up', 'Clasico']
    # Fecha de inicio: hace 2 años
    start_date = datetime.now() - timedelta(days=730)
    
    for _ in range(n):
        # Fecha aleatoria
        days_offset = random.randint(0, 730)
        fecha = start_date + timedelta(days=days_offset)
        
        # Género
        genero = random.choice(generos)
        
        # Aforo aleatorio entre 50 y 500
        aforo = random.randint(50, 500)
        
        # Temporada: entre 4 y 50 funciones
        total_funciones = random.randint(4, 50)
        numero_funcion = random.randint(1, total_funciones)
        
        # Popularidad entre 1 y 10
        popularidad = round(random.uniform(1, 10), 1)
        
        # Premios (probabilidad 30%)
        tiene_premios = random.random() < 0.3
        
        # Días antes de la función (0 a 30)
        dias_antes = random.randint(0, 30)
        
        # Ocupación final (depende de varios factores)
        # Simulación: base + ajustes
        base_ocupacion = 0.5
        # El género influye: Comedia y Stand-up venden más
        genero_factor = {'Comedia': 0.15, 'Stand-up': 0.20, 'Musical': 0.10, 
                         'Drama': 0.0, 'Infantil': 0.05, 'Clasico': -0.05}
        # Días antes: si es 0 (día de la función), la ocupación puede ser alta o baja
        # Si es > 10, es preventa, se vende menos
        if dias_antes > 10:
            tiempo_factor = -0.2
        elif dias_antes > 5:
            tiempo_factor = -0.1
        else:
            tiempo_factor = 0.15  # última hora
        
        # Fin de semana: si es sábado o domingo, sube
        dia_semana = fecha.weekday()
        fin_semana_factor = 0.1 if dia_semana >= 5 else 0
        
        # Popularidad: escala 1-10 -> 0.05 por punto
        popularidad_factor = (popularidad - 5) * 0.03
        
        # Premios: +0.05
        premio_factor = 0.05 if tiene_premios else 0
        
        # Función de despedida o estreno
        if numero_funcion == 1 or numero_funcion == total_funciones:
            extremo_factor = 0.1
        else:
            extremo_factor = 0
        
        # Ocupación final (clipped entre 0.05 y 0.95)
        ocupacion = base_ocupacion + genero_factor.get(genero, 0) + tiempo_factor + fin_semana_factor + popularidad_factor + premio_factor + extremo_factor + np.random.normal(0, 0.08)
        ocupacion = np.clip(ocupacion, 0.05, 0.95)
        
        data.append({
            'fecha': fecha.isoformat(),
            'genero': genero,
            'aforo_total': aforo,
            'total_funciones_temporada': total_funciones,
            'numero_funcion': numero_funcion,
            'popularidad': popularidad,
            'tiene_premios': int(tiene_premios),
            'dias_antes': dias_antes,
            'ocupacion_final': round(ocupacion, 4)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/historico_ventas.csv', index=False)
    print(f"✅ Generados {n} registros históricos en 'data/historico_ventas.csv'")
    print(df.head())

if __name__ == "__main__":
    generate_historical_data(500)