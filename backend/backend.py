from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.predictor import predict, model, MODEL_VERSION
from schema.user_input import InsuranceRequestUserInput
from schema.pred_response import PredictionResponse

app = FastAPI(
    title='Insurance Premium Predictor',
    description='Predict insurance premium categories based on user details.',
)


@app.get('/')
def root():
    return {'message': 'Insurance Premium Predictor API is running.'}


@app.get('/health')
def health_check():
    return {
        'status': 'ok',
        'version': '1.0.1',
        'model_status': model is not None,
        'model_version': MODEL_VERSION,
    }


@app.post('/predict', response_model=PredictionResponse)
def predict_premium(request: InsuranceRequestUserInput):
    result = predict({
        'bmi': request.bmi,
        'age_group': request.age_group,
        'lifestyle_risk': request.lifestyle_risk,
        'city_tier': request.city_tier,
        'income_lpa': request.income_lpa,
        'occupation': request.occupation,
    })
    return JSONResponse(content=result)
