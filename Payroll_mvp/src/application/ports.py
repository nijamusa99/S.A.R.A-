from abc import ABC, abstractmethod
from src.domain.entities import ContractRules, PayrollResponse

class AIExtractorPort(ABC):
    @abstractmethod
    async def extract_rules(self, contract_text: str) -> ContractRules:
        raise NotImplementedError

class CalculationRepositoryPort(ABC):
    @abstractmethod
    async def save(self, response: PayrollResponse) -> None:
        raise NotImplementedError