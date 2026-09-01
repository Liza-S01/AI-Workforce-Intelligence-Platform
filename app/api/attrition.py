from fastapi import APIRouter, HTTPException
from app.validation.employee_schema import EmployeePredictRequest, EmployeePredictResponse
from app.ml.predictor import predictor
from app.utils.logger import logger

router = APIRouter(prefix="/predict", tags=["ML Predictions"])

@router.post("/attrition", response_model=EmployeePredictResponse)
def predict_attrition(request: EmployeePredictRequest):
    """
    Run inference on employee profile to predict attrition risk probability and top contributing drivers.
    """
    try:
        logger.info(f"Received prediction request for Employee ID: {request.EmployeeID}")
        response = predictor.predict(request)
        return response
    except Exception as e:
        logger.error(f"Prediction endpoint error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
