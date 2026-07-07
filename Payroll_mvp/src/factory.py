from src.infrastructure.adapters.ollama_adapter import OllamaExtractor
from src.infrastructure.adapters.memory_repository import InMemoryRepository
from src.domain.services import PayrollCalculator
from src.infrastructure.config import settings
from src.infrastructure.adapters.pdf_extractor import PDFTextExtractor
from src.application.ports import TextExtractorPort

def build_payroll_calculator():
    ai_adapter = OllamaExtractor()
    repo_adapter = InMemoryRepository()
    return PayrollCalculator(
        ai_extractor=ai_adapter,
        repository=repo_adapter,
        withholding_rate=settings.withholding_rate
    )

def build_text_extractor() -> TextExtractorPort:
    return PDFTextExtractor()