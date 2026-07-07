from src.domain.entities import PayrollResponse
from src.application.ports import CalculationRepositoryPort

class InMemoryRepository(CalculationRepositoryPort):
    def __init__(self):
        self._db = []

    async def save(self, response: PayrollResponse) -> None:
        self._db.append(response.model_dump())
        print(f"[Persistencia] Guardado. Total: {len(self._db)}")