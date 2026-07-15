from dataclasses import dataclass
from datetime import datetime
from .value_objects import Genero

@dataclass
class FuncionTeatro:
    """Representa una función específica a predecir"""
    nombre_obra: str
    genero: Genero
    fecha_hora: datetime
    aforo_total: int
    total_funciones_temporada: int
    numero_funcion_actual: int
    popularidad_elenco: float  # 1.0 a 10.0
    tiene_premios: bool
    boletas_vendidas_hoy: int
    dias_antes_funcion: int    # Número de días hasta la función

@dataclass
class PrediccionDemanda:
    """Resultado del caso de uso"""
    funcion_id: str
    porcentaje_estimado: float  # 0.0 a 1.0
    aforo_estimado: int
    porcentaje_base_global: float
    factor_ajuste: float
    estado: str  # "Cold Start" o "Adaptado"