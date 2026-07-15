from .infrastructure.adapters.ml_predictor import SklearnPredictor
from .infrastructure.adapters.csv_repository import CSVHistoricoRepository
from .application.use_cases import PredecirDemandaUseCase, ReentrenarModeloUseCase

def build_predictor() -> SklearnPredictor:
    return SklearnPredictor(model_path="infrastructure/models/global_model.pkl")

def build_repository() -> CSVHistoricoRepository:
    return CSVHistoricoRepository()

def build_predecir_use_case() -> PredecirDemandaUseCase:
    return PredecirDemandaUseCase(build_predictor())

def build_reentrenar_use_case() -> ReentrenarModeloUseCase:
    return ReentrenarModeloUseCase(build_predictor(), build_repository())