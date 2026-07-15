from fastapi import APIRouter, HTTPException, FastAPI
from .schemas import PredictRequest
from ..factory import build_predecir_use_case, build_reentrenar_use_case

router = APIRouter(prefix="/boleteria", tags=["Boletería - ML"])

@router.post("/predict")
async def predict_demand(request: PredictRequest):
    try:
        use_case = build_predecir_use_case()
        data = request.model_dump()
        result = use_case.execute(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error en los datos de entrada: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@router.post("/retrain")
async def retrain_model():
    try:
        use_case = build_reentrenar_use_case()
        result = use_case.execute()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en reentrenamiento: {str(e)}")

app = FastAPI(title="S.A.R.A. - Módulo Boletería (ML)")
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "S.A.R.A. - Módulo de ML para Boletería",
        "docs": "/docs",
        "endpoints": ["POST /boleteria/predict", "POST /boleteria/retrain"]
    }