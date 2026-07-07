from src.infrastructure.adapters.ollama_adapter import OllamaExtractor
from src.infrastructure.adapters.memory_repository import InMemoryRepository
from src.domain.services import PayrollCalculator
from src.infrastructure.config import settings
from src.infrastructure.adapters.fastapi_controller import create_router  # lo modificaremos

def build_payroll_calculator():
    """Factory que construye el servicio de dominio con sus dependencias."""
    ai_adapter = OllamaExtractor()
    repo_adapter = InMemoryRepository()
    calculator = PayrollCalculator(
        ai_extractor=ai_adapter,
        repository=repo_adapter,
        withholding_rate=settings.withholding_rate
    )
    return calculator

def build_router():
    """Factory que crea el router FastAPI inyectando el servicio."""
    from src.infrastructure.adapters.fastapi_controller import router
    # En lugar de usar dependency_overrides, inyectamos directamente
    # Necesitamos modificar el controlador para recibir el calculator por constructor o parámetro.
    # Para simplificar, haremos que el router tenga una función que obtenga el calculator desde la factory.
    # O mejor, redefinimos get_calculator para que use la factory.
    # Pero como es más limpio, crearemos un router con dependencia inyectada.
    return router