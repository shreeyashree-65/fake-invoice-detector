from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from feature_engineering import extract_features

app = Flask(__name__)
model = joblib.load('models/fraud_detector.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = extract_features(data)
    prediction = model.predict([features])
    result = 'Fake' if prediction[0] == 1 else 'Genuine'
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
