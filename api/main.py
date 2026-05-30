import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.schemas import Transaction, Prediction

app = FastAPI(
    title="Fraud Detection API",
    description="API REST que clasifica transacciones bancarias como fraudulentas "
                "o legitimas en tiempo real, usando un modelo de Machine Learning.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/fraud_model.pkl")


@app.get("/")
def root():
    return {"mensaje": "Fraud Detection API activa. Visita /docs para la documentacion."}


@app.get("/health")
def health():
    """Endpoint de salud: confirma que la API esta viva."""
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(tx: Transaction):
    """Recibe una transaccion y devuelve si es fraude + su probabilidad."""
    df = pd.DataFrame([tx.model_dump()])
    proba = float(model.predict_proba(df)[:, 1][0])

    if proba >= 0.7:
        nivel = "ALTO"
    elif proba >= 0.4:
        nivel = "MEDIO"
    else:
        nivel = "BAJO"

    return Prediction(
        is_fraud=proba >= 0.5,
        fraud_probability=round(proba, 4),
        risk_level=nivel,
    )
