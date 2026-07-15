from datetime import datetime
from ..domain.entities import FuncionTeatro, PrediccionDemanda
from .ports import IPredictor, IHistoricoRepository

class PredecirDemandaUseCase:
    def __init__(self, predictor: IPredictor):
        self.predictor = predictor

    def execute(self, input_data: dict) -> dict:
        # ---- Parseo de fecha ----
        fecha_raw = input_data['temporada']['fecha_funcion']
        if isinstance(fecha_raw, datetime):
            fecha = fecha_raw
        elif isinstance(fecha_raw, str):
            fecha = datetime.fromisoformat(fecha_raw)
        else:
            raise ValueError(f"Formato de fecha no soportado: {type(fecha_raw)}")

        dias_restantes = (fecha - datetime.now()).days
        if dias_restantes < 0:
            dias_restantes = 0

        # ---- Validaciones ----
        num_actual = input_data['temporada']['numero_funcion_actual']
        if num_actual < 1:
            raise ValueError("numero_funcion_actual debe ser al menos 1")

        aforo = input_data['contexto_actual']['aforo_total_sala']
        if aforo <= 0:
            raise ValueError("aforo_total_sala debe ser mayor a 0")

        # ---- Construir entidad ----
        funcion = FuncionTeatro(
            nombre_obra=input_data['obra']['nombre'],
            genero=input_data['obra']['genero'],
            fecha_hora=fecha,
            aforo_total=aforo,
            total_funciones_temporada=input_data['temporada'].get('total_funciones_programadas', 10),
            numero_funcion_actual=num_actual,
            popularidad_elenco=input_data['obra'].get('popularidad_elenco', 5.0),
            tiene_premios=input_data['obra'].get('tiene_premios', False),
            boletas_vendidas_hoy=input_data['contexto_actual']['boletas_vendidas_hoy'],
            dias_antes_funcion=dias_restantes
        )

        # ---- Predicción ----
        prediccion = self.predictor.predict(funcion)

        # ---- Recomendación ----
        if prediccion.porcentaje_estimado < 0.35:
            recomendacion = "🚨 ALERTA: Bajo llenado. Aplicar descuento urgente o campaña."
        elif prediccion.porcentaje_estimado < 0.60:
            recomendacion = "📊 Ocupación media. Monitorear ventas de última hora (48h)."
        else:
            recomendacion = "✅ Demanda sólida. Mantener precio y estrategia."

        return {
            "obra": funcion.nombre_obra,
            "fecha": funcion.fecha_hora.isoformat(),
            "prediccion_final": round(prediccion.porcentaje_estimado * 100, 1),
            "aforo_estimado": prediccion.aforo_estimado,
            "base_global": round(prediccion.porcentaje_base_global * 100, 1),
            "factor_ajuste": round(prediccion.factor_ajuste, 2),
            "estado": prediccion.estado,
            "recomendacion": recomendacion
        }


class ReentrenarModeloUseCase:
    def __init__(self, predictor: IPredictor, repo: IHistoricoRepository):
        self.predictor = predictor
        self.repo = repo

    def execute(self) -> dict:
        historico = self.repo.get_all_historicos()
        if len(historico) < 30:
            return {
                "status": "No hay suficientes datos históricos (mínimo 30 registros)",
                "registros": len(historico)
            }
        self.predictor.retrain(historico)
        return {
            "status": "Modelo reentrenado exitosamente",
            "registros_usados": len(historico)
        }