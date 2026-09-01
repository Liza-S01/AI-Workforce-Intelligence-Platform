"""
ML Attrition Model Training, Evaluation, and Serialization Script.
Follows Day 2 Machine Learning specifications from build notes.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, classification_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "employees.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models", "v1")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_and_save():
    print("-> Loading dataset for Attrition ML Pipeline...")
    df = pd.read_csv(DATA_PATH)
    
    # 1. Feature Engineering
    # Target
    df["Attrition_Binary"] = df["Attrition"].map({"Yes": 1, "No": 0})
    if df["Attrition_Binary"].isnull().any():
        df["Attrition_Binary"] = (df["Attrition"].astype(str).str.lower() == "yes").astype(int)
        
    # Engineered features
    df["TenureRatio"] = df["YearsAtCompany"] / (df["TotalWorkingYears"] + 1)
    df["SatisfactionComposite"] = (df["JobSatisfaction"] + df["EnvironmentSatisfaction"] + df["RelationshipSatisfaction"]) / 3.0
    df["IncomePerYear"] = df["MonthlyIncome"] / (df["TotalWorkingYears"] + 1)
    df["PromotionGap"] = df["YearsSinceLastPromotion"] / (df["YearsInCurrentRole"] + 1)

    numeric_features = [
        "Age", "DailyRate", "DistanceFromHome", "HourlyRate", "MonthlyIncome",
        "MonthlyRate", "NumCompaniesWorked", "PercentSalaryHike", "TotalWorkingYears",
        "TrainingTimesLastYear", "YearsAtCompany", "YearsInCurrentRole",
        "YearsSinceLastPromotion", "YearsWithCurrManager", "EnvironmentSatisfaction",
        "JobInvolvement", "JobLevel", "JobSatisfaction", "RelationshipSatisfaction",
        "WorkLifeBalance", "TenureRatio", "SatisfactionComposite", "IncomePerYear", "PromotionGap"
    ]
    
    categorical_features = [
        "BusinessTravel", "Department", "EducationField", "Gender",
        "JobRole", "MaritalStatus", "OverTime"
    ]
    
    # Filter available columns
    numeric_cols = [c for c in numeric_features if c in df.columns]
    cat_cols = [c for c in categorical_features if c in df.columns]
    
    X = df[numeric_cols + cat_cols].copy()
    y = df["Attrition_Binary"].values
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Train size: {len(X_train)}, Test size: {len(X_test)}, Positive rate: {y.mean():.2%}")
    
    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
        ]
    )
    
    # Compare Models
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42)
    }
    
    results = {}
    best_f1 = 0
    best_model_name = "GradientBoosting"
    best_pipe = None
    
    for name, clf in models.items():
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        pipe.fit(X_train, y_train)
        
        preds = pipe.predict(X_test)
        probs = pipe.predict_proba(X_test)[:, 1]
        
        prec = float(precision_score(y_test, preds, zero_division=0))
        rec = float(recall_score(y_test, preds, zero_division=0))
        f1 = float(f1_score(y_test, preds, zero_division=0))
        roc_auc = float(roc_auc_score(y_test, probs))
        
        results[name] = {
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1_Score": round(f1, 4),
            "ROC_AUC": round(roc_auc, 4)
        }
        print(f"   [{name}] Precision: {prec:.3f} | Recall: {rec:.3f} | F1: {f1:.3f} | ROC-AUC: {roc_auc:.3f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipe = pipe

    # Save best pipeline
    model_save_path = os.path.join(MODELS_DIR, "attrition_pipeline.joblib")
    joblib.dump({
        "pipeline": best_pipe,
        "numeric_cols": numeric_cols,
        "cat_cols": cat_cols,
        "feature_names": numeric_cols + cat_cols
    }, model_save_path)
    print(f"-> Saved Best Pipeline ({best_model_name}) to {model_save_path}")
    
    # Save Metadata JSON
    meta = {
        "model_name": "Enterprise Attrition Risk Predictor",
        "version": "v1.0",
        "algorithm": best_model_name,
        "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "metrics": results[best_model_name],
        "comparison_results": results,
        "features": {
            "numeric": numeric_cols,
            "categorical": cat_cols
        },
        "thresholds": {
            "high_risk": 0.65,
            "medium_risk": 0.35,
            "low_risk": 0.00
        }
    }
    with open(os.path.join(MODELS_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("-> Metadata saved to models/v1/metadata.json")

if __name__ == "__main__":
    train_and_save()
