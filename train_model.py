"""
Loan Bias Predictor - ML Training Script
Dataset: https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset

Usage:
    1. Download the dataset from Kaggle and place train.csv in the same directory
    2. Run: python train_model.py
    3. This will generate loan_model.pkl and feature_info.json
"""

import pandas as pd
import numpy as np
import json
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. LOAD & EXPLORE DATA
# ─────────────────────────────────────────────
def load_data(path="train.csv"):
    df = pd.read_csv(path)
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nTarget distribution:\n{df['Loan_Status'].value_counts()}")
    return df

# ─────────────────────────────────────────────
# 2. PREPROCESSING
# ─────────────────────────────────────────────
def preprocess(df):
    df = df.copy()
    
    # Drop Loan_ID (not predictive)
    if 'Loan_ID' in df.columns:
        df.drop('Loan_ID', axis=1, inplace=True)
    
    # Fill missing values
    cat_cols = ['Gender', 'Married', 'Dependents', 'Self_Employed', 'Credit_History']
    num_cols = ['LoanAmount', 'Loan_Amount_Term']
    
    for col in cat_cols:
        if col in df.columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    for col in num_cols:
        if col in df.columns:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Encode Dependents: '3+' → 3
    df['Dependents'] = df['Dependents'].replace('3+', 3).astype(float)
    
    # Feature engineering
    df['TotalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['LoanAmountLog'] = np.log1p(df['LoanAmount'])
    df['TotalIncomeLog'] = np.log1p(df['TotalIncome'])
    df['EMI'] = df['LoanAmount'] / df['Loan_Amount_Term']
    df['BalanceIncome'] = df['TotalIncome'] - (df['EMI'] * 1000)
    df['DebtToIncome'] = df['LoanAmount'] / (df['TotalIncome'] + 1)
    
    # Encode categoricals
    le = LabelEncoder()
    binary_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    
    for col in binary_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col].astype(str))
    
    # Encode target if present
    if 'Loan_Status' in df.columns:
        df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    
    return df

# ─────────────────────────────────────────────
# 3. BIAS ANALYSIS
# ─────────────────────────────────────────────
def analyze_bias(df_original):
    """Analyze approval rates across demographic groups."""
    bias_report = {}
    
    df = df_original.copy()
    df['Approved'] = (df['Loan_Status'] == 'Y').astype(int)
    
    # Gender bias
    if 'Gender' in df.columns:
        gender_rates = df.groupby('Gender')['Approved'].agg(['mean', 'count']).round(3)
        bias_report['gender'] = gender_rates.to_dict()
    
    # Marital status bias
    if 'Married' in df.columns:
        married_rates = df.groupby('Married')['Approved'].agg(['mean', 'count']).round(3)
        bias_report['married'] = married_rates.to_dict()
    
    # Education bias
    if 'Education' in df.columns:
        edu_rates = df.groupby('Education')['Approved'].agg(['mean', 'count']).round(3)
        bias_report['education'] = edu_rates.to_dict()
    
    # Property area bias
    if 'Property_Area' in df.columns:
        area_rates = df.groupby('Property_Area')['Approved'].agg(['mean', 'count']).round(3)
        bias_report['property_area'] = area_rates.to_dict()
    
    print("\n─── BIAS ANALYSIS ───")
    for group, data in bias_report.items():
        print(f"\n{group.upper()} approval rates:")
        print(data)
    
    return bias_report

# ─────────────────────────────────────────────
# 4. TRAIN MODELS
# ─────────────────────────────────────────────
FEATURE_COLS = [
    'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
    'Credit_History', 'Property_Area',
    'TotalIncome', 'LoanAmountLog', 'TotalIncomeLog',
    'EMI', 'BalanceIncome', 'DebtToIncome'
]

def train(df_processed):
    X = df_processed[FEATURE_COLS]
    y = df_processed['Loan_Status']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    models = {
        'RandomForest': RandomForestClassifier(
            n_estimators=200, max_depth=8, min_samples_split=5,
            random_state=42, class_weight='balanced'
        ),
        'GradientBoosting': GradientBoostingClassifier(
            n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42
        ),
        'LogisticRegression': LogisticRegression(
            C=1.0, max_iter=1000, random_state=42, class_weight='balanced'
        )
    }
    
    best_model = None
    best_score = 0
    results = {}
    
    print("\n─── MODEL TRAINING ───")
    for name, model in models.items():
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        model.fit(X_train, y_train)
        test_acc = accuracy_score(y_test, model.predict(X_test))
        
        results[name] = {
            'cv_mean': round(cv_scores.mean(), 4),
            'cv_std': round(cv_scores.std(), 4),
            'test_accuracy': round(test_acc, 4)
        }
        
        print(f"\n{name}:")
        print(f"  CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        print(f"  Test Accuracy: {test_acc:.4f}")
        print(classification_report(y_test, model.predict(X_test), target_names=['Rejected', 'Approved']))
        
        if test_acc > best_score:
            best_score = test_acc
            best_model = model
            best_name = name
    
    print(f"\n✓ Best model: {best_name} ({best_score:.4f})")
    
    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        fi = pd.Series(best_model.feature_importances_, index=FEATURE_COLS)
        fi = fi.sort_values(ascending=False)
        print(f"\nTop 10 feature importances:\n{fi.head(10)}")
        feature_importance = fi.to_dict()
    else:
        feature_importance = {}
    
    return best_model, best_name, results, feature_importance, X_test, y_test

# ─────────────────────────────────────────────
# 5. SAVE MODEL + METADATA
# ─────────────────────────────────────────────
def save_artifacts(model, model_name, results, feature_importance, bias_report):
    joblib.dump(model, 'loan_model.pkl')
    
    metadata = {
        'model_name': model_name,
        'features': FEATURE_COLS,
        'model_results': results,
        'feature_importance': {k: round(float(v), 5) for k, v in feature_importance.items()},
        'bias_report': bias_report
    }
    
    with open('feature_info.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n✓ Saved: loan_model.pkl, feature_info.json")

# ─────────────────────────────────────────────
# 6. PREDICT FUNCTION (for Flask API)
# ─────────────────────────────────────────────
def predict_loan(model, input_dict):
    """
    input_dict keys: Gender, Married, Dependents, Education, Self_Employed,
                     ApplicantIncome, CoapplicantIncome, LoanAmount,
                     Loan_Amount_Term, Credit_History, Property_Area
    Returns: {'approved': bool, 'probability': float, 'risk_score': float}
    """
    df = pd.DataFrame([input_dict])
    
    # Encode categorical fields
    gender_map = {'Male': 1, 'Female': 0}
    married_map = {'Yes': 1, 'No': 0}
    education_map = {'Graduate': 0, 'Not Graduate': 1}
    self_emp_map = {'Yes': 1, 'No': 0}
    area_map = {'Urban': 2, 'Semiurban': 1, 'Rural': 0}
    
    df['Gender'] = df['Gender'].map(gender_map).fillna(1)
    df['Married'] = df['Married'].map(married_map).fillna(1)
    df['Education'] = df['Education'].map(education_map).fillna(0)
    df['Self_Employed'] = df['Self_Employed'].map(self_emp_map).fillna(0)
    df['Property_Area'] = df['Property_Area'].map(area_map).fillna(1)
    df['Dependents'] = df['Dependents'].replace('3+', 3).astype(float)
    
    # Feature engineering
    df['TotalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['LoanAmountLog'] = np.log1p(df['LoanAmount'])
    df['TotalIncomeLog'] = np.log1p(df['TotalIncome'])
    df['EMI'] = df['LoanAmount'] / df['Loan_Amount_Term']
    df['BalanceIncome'] = df['TotalIncome'] - (df['EMI'] * 1000)
    df['DebtToIncome'] = df['LoanAmount'] / (df['TotalIncome'] + 1)
    
    X = df[FEATURE_COLS]
    prob = model.predict_proba(X)[0][1]
    approved = prob >= 0.5
    
    return {
        'approved': bool(approved),
        'probability': round(float(prob), 4),
        'risk_score': round(float(1 - prob), 4)
    }

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  LOAN BIAS PREDICTOR - ML TRAINING")
    print("=" * 50)
    
    try:
        df_raw = load_data('train.csv')
        bias_report = analyze_bias(df_raw)
        df_processed = preprocess(df_raw)
        model, model_name, results, feature_importance, X_test, y_test = train(df_processed)
        save_artifacts(model, model_name, results, feature_importance, bias_report)
        print("\n✅ Training complete! Run app.py to start the API server.")
    except FileNotFoundError:
        print("\n⚠️  train.csv not found!")
        print("Download from: https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset")
        print("Place train.csv in the backend/ directory and re-run.")

