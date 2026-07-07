# src/infrastructure/adapters/fastapi_controller.py
from fastapi import APIRouter, HTTPException
from src.domain.entities import PayrollRequest, PayrollResponse
from src.domain.services import PayrollCalculator

class PayrollController:
    def __init__(self, calculator: PayrollCalculator):
        self.calculator = calculator

    async def calculate(self, request: PayrollRequest) -> PayrollResponse:
        try:
            result = await self.calculator.calculate(request)
            return result
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

def create_router(calculator: PayrollCalculator) -> APIRouter:
    """Factory de router que inyecta el calculator en el controlador."""
    router = APIRouter(prefix="/api/v1/payroll", tags=["payroll"])
    controller = PayrollController(calculator)

    @router.post("/calculate", response_model=PayrollResponse)
    async def calculate_payroll(request: PayrollRequest):
        return await controller.calculate(request)

    return router