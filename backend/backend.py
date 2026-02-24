from pathlib import Path
from typing import Annotated, Literal
import os
import pickle
import logging

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / '.env')

logger = logging.getLogger(__name__)

model_path = PROJECT_ROOT / os.getenv('MODEL_PATH', 'models/model.pkl')
if not model_path.exists():
    raise FileNotFoundError(
        f'Model file not found at {model_path}. '
        f'Check MODEL_PATH in your .env file.'
    )

with open(model_path, 'rb') as f:
    model = pickle.load(f)
    logger.info('Model loaded from %s', model_path)

app = FastAPI(
    title='Insurance Premium Predictor',
    description='Predict insurance premium categories based on user details.',
)


TIER_1_CITIES = frozenset([
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai',
    'Kolkata', 'Hyderabad', 'Pune',
])
TIER_2_CITIES = frozenset([
    'Jaipur', 'Chandigarh', 'Indore', 'Lucknow', 'Patna', 'Ranchi',
    'Visakhapatnam', 'Coimbatore', 'Bhopal', 'Nagpur', 'Vadodara',
    'Surat', 'Rajkot', 'Jodhpur', 'Raipur', 'Amritsar', 'Varanasi',
    'Agra', 'Dehradun', 'Mysore', 'Jabalpur', 'Guwahati',
    'Thiruvananthapuram', 'Ludhiana', 'Nashik', 'Allahabad', 'Udaipur',
    'Aurangabad', 'Hubli', 'Belgaum', 'Salem', 'Vijayawada',
    'Tiruchirappalli', 'Bhavnagar', 'Gwalior', 'Dhanbad', 'Bareilly',
    'Aligarh', 'Gaya', 'Kozhikode', 'Warangal', 'Kolhapur', 'Bilaspur',
    'Jalandhar', 'Noida', 'Guntur', 'Asansol', 'Siliguri',
])


class InsuranceRequestUserInput(BaseModel):
    age: Annotated[int, Field(gt=0, lt=120, description='Age of the user', examples=[25])]
    weight: Annotated[float, Field(gt=0, lt=200, description='Weight in kg', examples=[70.0])]
    height: Annotated[float, Field(gt=0, lt=2.5, description='Height in meters', examples=[1.75])]
    smoker: Annotated[bool, Field(description='Whether the user is a smoker', examples=[False])]
    city: Annotated[str, Field(description='City of the user', examples=['Delhi'])]
    income_lpa: Annotated[float, Field(gt=0, description='Annual income in Lakhs', examples=[10.0])]
    occupation: Annotated[
        Literal[
            'student', 'private_job', 'government_job',
            'business_owner', 'unemployed', 'freelancer', 'retired',
        ],
        Field(description='Occupation of the user', examples=['student']),
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def age_group(self) -> Literal['young', 'adult', 'middle_aged', 'senior']:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle_aged'
        return 'senior'

    @computed_field
    @property
    def lifestyle_risk(self) -> Literal['high', 'medium', 'low']:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        return 'low'

    @computed_field
    @property
    def city_tier(self) -> int:
        normalized = self.city.strip().title()
        if normalized in TIER_1_CITIES:
            return 1
        if normalized in TIER_2_CITIES:
            return 2
        return 3


@app.get('/')
def root():
    return {'message': 'Insurance Premium Predictor API is running.'}


@app.post('/predict')
def predict_premium(request: InsuranceRequestUserInput):
    input_df = pd.DataFrame([{
        'bmi': request.bmi,
        'age_group': request.age_group,
        'lifestyle_risk': request.lifestyle_risk,
        'city_tier': request.city_tier,
        'income_lpa': request.income_lpa,
        'occupation': request.occupation,
    }])

    predicted_category = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_.tolist()
    confidence = float(np.max(probabilities))
    class_probabilities = {
        cls: round(float(prob), 4)
        for cls, prob in zip(classes, probabilities)
    }

    return JSONResponse(content={
        'predicted_category': predicted_category,
        'confidence': round(confidence, 4),
        'class_probabilities': class_probabilities,
    })
