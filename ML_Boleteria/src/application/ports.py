from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..domain.entities import FuncionTeatro, PrediccionDemanda

class IPredictor(ABC):
    """Puerto para el motor de ML"""
    @abstractmethod
    def predict(self, funcion: FuncionTeatro) -> PrediccionDemanda:
        pass

    @abstractmethod
    def retrain(self, historical_data: List[Dict[str, Any]]) -> None:
        """Reentrena el modelo con nuevos datos históricos"""
        pass

class IHistoricoRepository(ABC):
    """Puerto para almacenar/recuperar histórico de ventas"""
    @abstractmethod
    def save_venta_real(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_all_historicos(self) -> List[Dict[str, Any]]:
        pass