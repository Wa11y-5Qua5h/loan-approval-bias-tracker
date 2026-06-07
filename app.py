"""
Loan Bias Predictor - Flask API Server

Usage:
    1. Train the model first: python train_model.py
    2. Start server: python app.py
    3. API runs at http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import json
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# ─── Load Model ───
MODEL_PATH = 'loan_model.pkl'
INFO_PATH  = 'feature_info.json'

model = None
feature_info = None

def load_model():
    global model, feature_info
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✓ Model loaded")
    else:
        print("⚠️  No model found. Run train_model.py first.")
    
    if os.path.exists(INFO_PATH):
        with open(INFO_PATH) as f:
            feature_info = json.load(f)
        print("✓ Feature info loaded")

# ─── Feature Engineering ───
FEATURE_COLS = [
    'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
    'Credit_History', 'Property_Area',
    'TotalIncome', 'LoanAmountLog', 'TotalIncomeLog',
    'EMI', 'BalanceIncome', 'DebtToIncome'
]

def prepare_features(data):
    df = pd.DataFrame([data])
    
    # Encode
    df['Gender']        = {'Male': 1, 'Female': 0}.get(data.get('Gender', 'Male'), 1)
    df['Married']       = {'Yes': 1, 'No': 0}.get(data.get('Married', 'No'), 0)
    df['Education']     = {'Graduate': 0, 'Not Graduate': 1}.get(data.get('Education', 'Graduate'), 0)
    df['Self_Employed'] = {'Yes': 1, 'No': 0}.get(data.get('Self_Employed', 'No'), 0)
    df['Property_Area'] = {'Urban': 2, 'Semiurban': 1, 'Rural': 0}.get(data.get('Property_Area', 'Urban'), 2)
    df['Dependents']    = float(str(data.get('Dependents', 0)).replace('3+', '3'))
    df['Credit_History'] = float(data.get('Credit_History', 1))
    
    # Numeric
    df['ApplicantIncome']   = float(data.get('ApplicantIncome', 0))
    df['CoapplicantIncome'] = float(data.get('CoapplicantIncome', 0))
    df['LoanAmount']        = float(data.get('LoanAmount', 0))
    df['Loan_Amount_Term']  = float(data.get('Loan_Amount_Term', 360))
    
    # Derived features
    df['TotalIncome']    = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['LoanAmountLog']  = np.log1p(df['LoanAmount'])
    df['TotalIncomeLog'] = np.log1p(df['TotalIncome'])
    df['EMI']            = df['LoanAmount'] / (df['Loan_Amount_Term'] + 1e-9)
    df['BalanceIncome']  = df['TotalIncome'] - (df['EMI'] * 1000)
    df['DebtToIncome']   = df['LoanAmount'] / (df['TotalIncome'] + 1)
    
    return df[FEATURE_COLS]

# ─── Routes ───

@app.route('/')
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'api_version': '1.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Run train_model.py first.'}), 503
    
    data = request.json
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    try:
        X = prepare_features(data)
        prob = float(model.predict_proba(X)[0][1])
        approved = prob >= 0.5
        confidence_score = round(abs(prob - 0.5) * 2 * 100, 1)
        
        # Risk factors
        risk_factors = []
        if float(data.get('Credit_History', 1)) == 0:
            risk_factors.append({'factor': 'No credit history', 'impact': 'High'})
        
        loan_amount = float(data.get('LoanAmount', 0))
        total_income = float(data.get('ApplicantIncome', 0)) + float(data.get('CoapplicantIncome', 0))
        if total_income > 0 and loan_amount / total_income > 5:
            risk_factors.append({'factor': 'High loan-to-income ratio', 'impact': 'Medium'})
        
        term = float(data.get('Loan_Amount_Term', 360))
        if term > 0:
            emi_ratio = (loan_amount / term * 1000) / (total_income + 1)
            if emi_ratio > 0.5:
                risk_factors.append({'factor': 'High EMI burden', 'impact': 'Medium'})
        
        dependents = int(
            str(data.get('Dependents', 0)).replace('3+', '3')
)

        if dependents >= 3:
            risk_factors.append({
            'factor': 'High number of dependents',
            'impact': 'Low'
    })
        
        return jsonify({
            'approved': approved,
            'probability': round(prob * 100, 1),
            'risk_score': round((1 - prob) * 100, 1),

            'confidence': (
            'High'
            if confidence_score > 60
            else 'Medium'
            if confidence_score > 30
            else 'Low'
    ),

            'confidence_score': confidence_score,

            'risk_factors': risk_factors,

            'model': (
                feature_info.get('model_name', 'Unknown')
                if feature_info
                else 'Unknown'
    ),

            'timestamp': datetime.utcnow().isoformat()
})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    if feature_info is None:
        return jsonify({'error': 'No model info available'}), 503
    
    return jsonify({
    'model_name': feature_info.get('model_name'),

    'model_results': feature_info.get('model_results'),

    'top_features': dict(
        sorted(
            feature_info.get(
                'feature_importance',
                {}
            ).items(),
            key=lambda x: x[1],
            reverse=True
        )[:8]
    ),

    'bias_report': feature_info.get(
        'bias_report',
        {}
    ),

    'fairness_notice':
        'Gender and marital status are shown for fairness auditing purposes only and should not be used as the sole basis for lending decisions.',

    'timestamp': datetime.utcnow().isoformat()
})

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Predict for multiple applicants at once."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    data = request.json
    applicants = data.get('applicants', [])
    
    results = []
    for i, applicant in enumerate(applicants):
        try:
            X = prepare_features(applicant)
            prob = float(model.predict_proba(X)[0][1])
            results.append({
                'id': i,
                'approved': prob >= 0.5,
                'probability': round(prob * 100, 1)
            })
        except Exception as e:
            results.append({'id': i, 'error': str(e)})
    
    return jsonify({'results': results})
@app.route('/sample')
def sample():
    return jsonify({
        'Gender': 'Male',
        'Married': 'Yes',
        'Dependents': '1',
        'Education': 'Graduate',
        'Self_Employed': 'No',
        'ApplicantIncome': 6000,
        'CoapplicantIncome': 2000,
        'LoanAmount': 120,
        'Loan_Amount_Term': 360,
        'Credit_History': 1,
        'Property_Area': 'Urban'
    })

load_model()

if __name__ == '__main__':
    print("\n🚀 Starting Loan Predictor API at http://localhost:5000")
    app.run(debug=True, port=5000)
