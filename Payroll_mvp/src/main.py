# src/main.py
from fastapi import FastAPI
from src.factory import build_payroll_calculator
from src.infrastructure.adapters.fastapi_controller import create_router
from src.infrastructure.config import settings

# Construir el servicio con la factory
calculator = build_payroll_calculator()

# Crear el router inyectando el servicio
router = create_router(calculator)

# Crear la app FastAPI
app = FastAPI(
    title="Motor Soberano de Liquidaciones (MVP)",
    description="Arquitectura Limpia - IA Local con Ollama",
    version="1.0.0"
)
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": settings.llm_model}