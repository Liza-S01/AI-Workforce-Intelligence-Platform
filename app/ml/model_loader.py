import os
import joblib
import json
from app.utils.config import MODELS_DIR
from app.utils.logger import logger

class ModelLoader:
    _instance = None
    
    def __init__(self):
        self.model_path = os.path.join(MODELS_DIR, "attrition_pipeline.joblib")
        self.meta_path = os.path.join(MODELS_DIR, "metadata.json")
        self.pipeline_data = None
        self.metadata = None
        self.load()

    def load(self):
        try:
            if os.path.exists(self.model_path):
                self.pipeline_data = joblib.load(self.model_path)
                logger.info(f"Loaded attrition model pipeline from {self.model_path}")
            else:
                logger.warning(f"Model file not found at {self.model_path}")
            
            if os.path.exists(self.meta_path):
                with open(self.meta_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded model metadata: version {self.metadata.get('version')}")
        except Exception as e:
            logger.error(f"Error loading model artifacts: {e}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelLoader()
        return cls._instance

model_loader = ModelLoader.get_instance()
