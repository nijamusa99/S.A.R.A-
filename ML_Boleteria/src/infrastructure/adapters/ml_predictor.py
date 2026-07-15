import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from typing import List, Dict, Any
from ...domain.entities import FuncionTeatro, PrediccionDemanda
from ...application.ports import IPredictor

class SklearnPredictor(IPredictor):
    def __init__(self, model_path: str = "infrastructure/models/global_model.pkl"):
        # Obtener la raíz del proyecto (ML_Boleteria)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.model_path = os.path.join(base_dir, "src", model_path)
        self.model = self._load_or_train_global_model()

    def predict(self, funcion: FuncionTeatro) -> PrediccionDemanda:
        features = self._build_features(funcion)
        base_pred = float(self.model.predict([features])[0])
        base_pred = np.clip(base_pred, 0.05, 0.95)
        factor = self._calculate_momentum(funcion, base_pred)
        final_pred = np.clip(base_pred * factor, 0.0, 1.0)
        estado = "Cold Start" if funcion.boletas_vendidas_hoy == 0 else "Adaptado"
        return PrediccionDemanda(
            funcion_id=f"{funcion.nombre_obra}_{funcion.fecha_hora.isoformat()}",
            porcentaje_estimado=final_pred,
            aforo_estimado=int(final_pred * funcion.aforo_total),
            porcentaje_base_global=base_pred,
            factor_ajuste=factor,
            estado=estado
        )

    def retrain(self, historical_data: List[Dict[str, Any]]) -> None:
        df = pd.DataFrame(historical_data)
        X = []
        y = []
        from ...domain.value_objects import Genero
        for _, row in df.iterrows():
            fecha = row['fecha']
            if isinstance(fecha, str):
                fecha = datetime.fromisoformat(fecha)
            elif not isinstance(fecha, datetime):
                raise ValueError(f"Formato de fecha no soportado: {type(fecha)}")
            
            genero_enum = Genero(row['genero'])
            funcion = FuncionTeatro(
                nombre_obra="Histórico",
                genero=genero_enum,
                fecha_hora=fecha,
                aforo_total=row['aforo_total'],
                total_funciones_temporada=row['total_funciones_temporada'],
                numero_funcion_actual=row['numero_funcion'],
                popularidad_elenco=row['popularidad'],
                tiene_premios=bool(row['tiene_premios']),
                boletas_vendidas_hoy=0,
                dias_antes_funcion=row['dias_antes']
            )
            X.append(self._build_features(funcion))
            y.append(row['ocupacion_final'])
        
        new_model = RandomForestRegressor(n_estimators=150, random_state=42)
        new_model.fit(X, y)
        joblib.dump(new_model, self.model_path)
        self.model = new_model
        print(f"✅ Modelo reentrenado con {len(y)} registros.")

    # ---------- Métodos auxiliares ----------
    def _build_features(self, funcion: FuncionTeatro) -> List[float]:
        total = funcion.total_funciones_temporada
        actual = funcion.numero_funcion_actual
        progresion = (actual - 1) / (total - 1) if total > 1 else 0.5
        log_dias = np.log(funcion.dias_antes_funcion + 1)
        dia_num = funcion.fecha_hora.weekday()
        es_fin_semana = 1 if dia_num >= 5 else 0
        es_sabado = 1 if dia_num == 5 else 0
        es_domingo = 1 if dia_num == 6 else 0
        genero_map = {'Comedia': 1, 'Stand-up': 2, 'Musical': 3, 'Drama': 4, 'Infantil': 5, 'Clasico': 6}
        genero_num = genero_map.get(funcion.genero.value, 4)
        popularidad_norm = funcion.popularidad_elenco / 10.0
        premio = 1 if funcion.tiene_premios else 0
        return [progresion, log_dias, es_fin_semana, es_sabado, es_domingo, genero_num, popularidad_norm, premio]

    def _calculate_momentum(self, funcion: FuncionTeatro, base_pred: float) -> float:
        if funcion.boletas_vendidas_hoy == 0 or funcion.aforo_total == 0:
            return 1.0
        ventas_esperadas = base_pred * funcion.aforo_total
        if ventas_esperadas < 1:
            return 1.0
        ratio = funcion.boletas_vendidas_hoy / ventas_esperadas
        return np.clip(ratio, 0.4, 1.8)

    def _load_or_train_global_model(self):
        if os.path.exists(self.model_path):
            return joblib.load(self.model_path)
        else:
            print("⚠️ Modelo global no encontrado. Entrenando modelo sintético de ejemplo...")
            np.random.seed(42)
            X = np.random.rand(2000, 8)
            y = 0.4 + 0.3 * (1 - X[:, 1] / 4) + 0.2 * X[:, 2] + 0.1 * np.random.rand(2000)
            y = np.clip(y, 0.1, 0.95)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(model, self.model_path)
            print(f"✅ Modelo sintético guardado en: {self.model_path}")
            return model