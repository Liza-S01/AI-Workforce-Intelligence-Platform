import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
POLICIES_DIR = os.path.join(DATA_DIR, "hr_policies")
RESUMES_DIR = os.path.join(DATA_DIR, "resumes")
JOB_DESC_DIR = os.path.join(DATA_DIR, "job_descriptions")
PREDICTIONS_DIR = os.path.join(DATA_DIR, "predictions")
MODELS_DIR = os.path.join(BASE_DIR, "models", "v1")

API_PORT = int(os.getenv("PORT", 8000))
API_HOST = os.getenv("HOST", "0.0.0.0")

RISK_THRESHOLDS = {
    "HIGH": 0.65,
    "MEDIUM": 0.35,
    "LOW": 0.00
}
