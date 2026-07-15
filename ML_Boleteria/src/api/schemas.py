from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ..domain.value_objects import Genero

class ObraInput(BaseModel):
    nombre: str
    genero: Genero
    popularidad_elenco: Optional[float] = Field(5.0, ge=0, le=10)
    tiene_premios: Optional[bool] = False

class TemporadaInput(BaseModel):
    total_funciones_programadas: Optional[int] = Field(10, ge=1)
    numero_funcion_actual: int = Field(..., ge=1)  # mínimo 1
    fecha_funcion: datetime

class ContextoInput(BaseModel):
    boletas_vendidas_hoy: int = Field(..., ge=0)
    aforo_total_sala: int = Field(..., gt=0)  # mayor que 0

class PredictRequest(BaseModel):
    obra: ObraInput
    temporada: TemporadaInput
    contexto_actual: ContextoInput