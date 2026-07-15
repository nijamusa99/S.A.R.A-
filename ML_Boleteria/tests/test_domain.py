import pytest
from datetime import datetime
from src.domain.entities import FuncionTeatro, PrediccionDemanda
from src.domain.value_objects import Genero

def test_funcion_teatro_creation():
    fecha = datetime(2026, 7, 20, 20, 0, 0)
    funcion = FuncionTeatro(
        nombre_obra="Test",
        genero=Genero.COMEDIA,
        fecha_hora=fecha,
        aforo_total=100,
        total_funciones_temporada=10,
        numero_funcion_actual=5,
        popularidad_elenco=7.0,
        tiene_premios=True,
        boletas_vendidas_hoy=30,
        dias_antes_funcion=3
    )
    assert funcion.nombre_obra == "Test"
    assert funcion.genero == Genero.COMEDIA
    assert funcion.aforo_total == 100