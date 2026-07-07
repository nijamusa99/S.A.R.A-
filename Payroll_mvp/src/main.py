from fastapi import FastAPI
from src.infrastructure.adapters.fastapi_controller import router, get_calculator, get_text_extractor
from src.factory import build_payroll_calculator, build_text_extractor

# Construir dependencias
calculator = build_payroll_calculator()
text_extractor = build_text_extractor()

# Funciones de override
async def override_get_calculator():
    return calculator

async def override_get_text_extractor():
    return text_extractor

app = FastAPI(
    title="Motor Soberano de Liquidaciones (MVP)",
    description="Clean Architecture - IA Local con Ollama + PDF",
    version="1.0.0"
)

# Aplicar overrides a la aplicación (no al router)
app.dependency_overrides[get_calculator] = override_get_calculator
app.dependency_overrides[get_text_extractor] = override_get_text_extractor

app.include_router(router)

@app.get("/health")
async def health_check():
    from src.infrastructure.config import settings
    return {"status": "ok", "model": settings.llm_model}