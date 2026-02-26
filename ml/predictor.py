from pathlib import Path
import logging
import os
import pickle

import numpy as np
import pandas as pd
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / '.env')

logger = logging.getLogger(__name__)

MODEL_VERSION = '1.0.1'


def _load_model():
    model_path = PROJECT_ROOT / os.getenv('MODEL_PATH', 'models/model.pkl')
    if not model_path.exists():
        raise FileNotFoundError(
            f'Model file not found at {model_path}. '
            f'Check MODEL_PATH in your .env file.'
        )
    with open(model_path, 'rb') as f:
        loaded = pickle.load(f)
    logger.info('Model loaded from %s', model_path)
    return loaded


model = _load_model()


def predict(input_data: dict) -> dict:
    """Run prediction and return category, confidence, and class probabilities."""
    input_df = pd.DataFrame([input_data])

    predicted_category = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_.tolist()
    confidence = float(np.max(probabilities))
    class_probabilities = {
        cls: round(float(prob), 4)
        for cls, prob in zip(classes, probabilities)
    }

    return {
        'predicted_category': predicted_category,
        'confidence': round(confidence, 4),
        'class_probabilities': class_probabilities,
    }
