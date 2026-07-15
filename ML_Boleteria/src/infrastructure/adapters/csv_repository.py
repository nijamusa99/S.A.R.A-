import pandas as pd
import os
from typing import List, Dict, Any
from ...application.ports import IHistoricoRepository

class CSVHistoricoRepository(IHistoricoRepository):
    def __init__(self, file_path="data/historico_ventas.csv"):
        # Asegurar que la carpeta data existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.file_path = file_path
        
        # Si no existe, crear CSV con columnas base
        if not os.path.exists(file_path):
            pd.DataFrame(columns=[
                'fecha', 'genero', 'aforo_total', 'total_funciones_temporada',
                'numero_funcion', 'popularidad', 'tiene_premios', 'dias_antes',
                'ocupacion_final'
            ]).to_csv(file_path, index=False)

    def save_venta_real(self, data: Dict[str, Any]) -> None:
        df = pd.DataFrame([data])
        df.to_csv(self.file_path, mode='a', header=False, index=False)

    def get_all_historicos(self) -> List[Dict[str, Any]]:
        df = pd.read_csv(self.file_path)
        return df.to_dict(orient='records')