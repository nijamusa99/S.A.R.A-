from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from src.domain.entities import PayrollRequest, PayrollResponse
from src.domain.services import PayrollCalculator
from src.application.ports import TextExtractorPort

router = APIRouter(prefix="/api/v1/payroll", tags=["payroll"])

# Dependencias que serán inyectadas desde main.py
def get_calculator() -> PayrollCalculator:
    raise NotImplementedError("Debe ser inyectado desde el bootstrap")

def get_text_extractor() -> TextExtractorPort:
    raise NotImplementedError("Debe ser inyectado desde el bootstrap")

# Endpoint para texto plano
@router.post("/calculate", response_model=PayrollResponse)
async def calculate_payroll(
    request: PayrollRequest,
    calculator: PayrollCalculator = Depends(get_calculator)
):
    try:
        result = await calculator.calculate(request)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Nuevo endpoint para PDF
@router.post("/calculate-from-pdf", response_model=PayrollResponse)
async def calculate_from_pdf(
    file: UploadFile = File(...),
    box_office_total: float = 1000000,
    calculator: PayrollCalculator = Depends(get_calculator),
    text_extractor: TextExtractorPort = Depends(get_text_extractor)
):
    if box_office_total <= 0:
        raise HTTPException(400, "El total de taquilla debe ser mayor que 0")
    
    content = await file.read()
    
    try:
        contract_text = await text_extractor.extract_text(content)
    except RuntimeError as e:
        raise HTTPException(400, detail=str(e))
    
    if not contract_text:
        raise HTTPException(400, "No se pudo extraer texto del PDF")
    
    request = PayrollRequest(
        contract_text=contract_text,
        box_office_total=box_office_total
    )
    
    try:
        result = await calculator.calculate(request)
        return result
    except RuntimeError as e:
        raise HTTPException(503, detail=str(e))
    except Exception as e:
        raise HTTPException(400, detail=f"Error: {str(e)}")