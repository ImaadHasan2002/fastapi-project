# Insurance Premium Predictor

A FastAPI backend + Streamlit frontend that predicts insurance premium categories (Low / Medium / High) using a trained Random Forest model.

## Project Structure

```
fastapi-project/
├── backend/
│   └── backend.py          # FastAPI app with /predict endpoint
├── frontend/
│   └── frontend.py         # Streamlit UI
├── basics/
│   └── basics.py           # FastAPI learning examples
├── models/
│   └── model.pkl           # Trained sklearn pipeline
├── fastapi_ml_model.ipynb  # Notebook used to train the model
├── dummy_insurance.csv     # Sample dataset
├── .env                    # Environment variables (MODEL_PATH, API_URL)
├── requirements.txt
└── pyproject.toml
```

## Prerequisites

- Python 3.13+
- pip or uv

## Setup

1. **Clone the repository**

```bash
git clone <repo-url>
cd fastapi-project
```

2. **Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

The `.env` file at the project root should contain:

```
MODEL_PATH=models/model.pkl
API_URL=http://127.0.0.1:8000/predict
```

## Running

### Start the backend

```bash
cd backend
uvicorn backend:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs are at `http://127.0.0.1:8000/docs`.

### Start the frontend (separate terminal)

```bash
streamlit run frontend/frontend.py
```

Opens the Streamlit app in your browser (default `http://localhost:8501`).

## API Usage

### `POST /predict`

**Request body:**

```json
{
    "age": 30,
    "weight": 70.0,
    "height": 1.75,
    "smoker": false,
    "city": "Mumbai",
    "income_lpa": 10.0,
    "occupation": "private_job"
}
```

**Response:**

```json
{
    "predicted_category": "Low",
    "confidence": 0.85,
    "class_probabilities": {
        "High": 0.05,
        "Low": 0.85,
        "Medium": 0.10
    }
}
```

## Retraining the Model

Open `fastapi_ml_model.ipynb`, run all cells, and the updated `model.pkl` will be saved to the `models/` directory.
