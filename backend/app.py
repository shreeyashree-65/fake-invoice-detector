from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from src.feature_engineering import InvoiceFeatureExtractor
from datetime import datetime
from typing import Optional
import numpy as np

# Initialize FastAPI app
app = FastAPI(
    title="Fake Invoice Detector API",
    description="AI-powered fake invoice detection system",
    version="1.0.0"
)

# Load trained models
try:
    rf_model = joblib.load('models/random_forest_model.pkl')
    xgb_model = joblib.load('models/xgb_model.pkl')
    print("Models loaded successfully")
except FileNotFoundError:
    print("Models not found. Please train the models first.")
    rf_model = None
    xgb_model = None

# Initialize feature extractor
feature_extractor = InvoiceFeatureExtractor()

# Pydantic models for request/response
class InvoiceData(BaseModel):
    invoice_id: str
    vendor_name: str
    amount: float
    tax_amount: float
    tax_rate: float
    description: str
    date: str

class PredictionResponse(BaseModel):
    is_fake: bool
    confidence: float
    model_used: str
    risk_factors: dict

@app.get("/")
def root():
    return {"message": "Fake Invoice Detector API", "status": "running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": rf_model is not None and xgb_model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_invoice(invoice: InvoiceData):
    if rf_model is None or xgb_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    try:
        # Convert to DataFrame
        invoice_df = pd.DataFrame([invoice.dict()])
        
        # Extract features
        features = feature_extractor.extract_features(invoice_df)
        
        # Get predictions from both models
        rf_prediction = rf_model.predict(features)[0]
        rf_prob = rf_model.predict_proba(features)[0]
        
        xgb_prediction = xgb_model.predict(features)[0]
        xgb_prob = xgb_model.predict_proba(features)[0]
        
        # Use ensemble prediction (average of both models)
        ensemble_prob = (rf_prob + xgb_prob) / 2
        ensemble_prediction = 1 if ensemble_prob[1] > 0.5 else 0
        
        # Calculate confidence
        confidence = max(ensemble_prob) * 100
        
        # Identify risk factors
        risk_factors = identify_risk_factors(features.iloc[0], invoice.dict())
        
        return PredictionResponse(
            is_fake=bool(ensemble_prediction),
            confidence=float(confidence),
            model_used="ensemble",
            risk_factors=risk_factors
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/random_forest")
def predict_random_forest(invoice: InvoiceData):
    if rf_model is None:
        raise HTTPException(status_code=500, detail="Random Forest model not loaded")
    
    try:
        invoice_df = pd.DataFrame([invoice.dict()])
        features = feature_extractor.extract_features(invoice_df)
        prediction = rf_model.predict(features)[0]
        probability = rf_model.predict_proba(features)[0]
        
        return {
            "is_fake": bool(prediction),
            "confidence": float(max(probability) * 100),
            "model_used": "random_forest"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/xgboost")
def predict_xgboost(invoice: InvoiceData):
    if xgb_model is None:
        raise HTTPException(status_code=500, detail="XGBoost model not loaded")
    
    try:
        invoice_df = pd.DataFrame([invoice.dict()])
        features = feature_extractor.extract_features(invoice_df)
        prediction = xgb_model.predict(features)[0]
        probability = xgb_model.predict_proba(features)[0]
        
        return {
            "is_fake": bool(prediction),
            "confidence": float(max(probability) * 100),
            "model_used": "xgboost"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/features")
def get_feature_names():
    return {"features": feature_extractor.get_feature_names()}

def identify_risk_factors(features, invoice_data):
    """Identify specific risk factors based on feature values"""
    risk_factors = {}
    
    # Check vendor name similarity
    if features['vendor_name_similarity'] < 0.7:
        risk_factors['vendor_name'] = "Low similarity to known legitimate vendors"
    
    # Check amount roundness
    if features['amount_roundness'] > 0.5:
        risk_factors['amount'] = "Suspiciously round amount"
    
    # Check tax accuracy
    if features['tax_accuracy'] < 0.9:
        risk_factors['tax_calculation'] = "Inaccurate tax calculation"
    
    # Check description legitimacy
    if features['description_legitimacy'] < 1:
        risk_factors['description'] = "Vague or suspicious description"
    
    # Check weekend invoice
    if features['is_weekend'] == 1:
        risk_factors['date'] = "Invoice issued on weekend"
    
    # Check invoice ID pattern
    if features['invoice_id_pattern'] < 0.5:
        risk_factors['invoice_id'] = "Unusual invoice ID pattern"
    
    return risk_factors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
