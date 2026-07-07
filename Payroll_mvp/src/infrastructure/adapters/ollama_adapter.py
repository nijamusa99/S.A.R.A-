import json
import httpx
from src.domain.entities import ContractRules, PaymentRule
from src.application.ports import AIExtractorPort
from src.infrastructure.config import settings

class OllamaExtractor(AIExtractorPort):
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)

    async def extract_rules(self, contract_text: str) -> ContractRules:
        prompt = f"""
        Eres un asistente contable experto en contratos artísticos colombianos.
        Extrae la siguiente información del contrato:
        - Nombre del actor.
        - Regla de pago: "fijo" (si dice pago fijo de $X), "porcentaje" (si dice X% de taquilla), o "garantia_minima".
        - Valor numérico.

        Responde ÚNICAMENTE con un JSON válido.
        Ejemplo: {{"actor": "Juan Perez", "tipo_pago": "porcentaje", "valor": 15}}

        Texto del contrato:
        \"\"\"{contract_text}\"\"\"
        """
        payload = {
            "model": settings.llm_model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        try:
            response = await self.client.post(f"{settings.ollama_host}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            raw = data.get("response", "{}").strip()
            parsed = json.loads(raw)
            return ContractRules(
                actor=parsed.get("actor", "Desconocido"),
                rule=PaymentRule(parsed.get("tipo_pago", "fijo")),
                value=float(parsed.get("valor", 0.0))
            )
        except Exception as e:
            print(f"Error en Ollama: {e}")
            raise RuntimeError("No se pudo procesar el contrato con la IA local.")