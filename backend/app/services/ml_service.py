"""
services/ml_service.py
Wraps the trained ML models (ml/predict.py) for use by the API layer.
"""

import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml"))
from predict import predict_category, predict_priority  # noqa: E402

logger = logging.getLogger("ml_service")


class MLService:
    def predict_category(self, text: str) -> dict:
        result = predict_category(text)
        logger.info("Category predicted: %s (confidence=%.2f)", result["label"], result["confidence"])
        return result

    def predict_priority_from_text(self, text: str) -> dict:
        result = predict_priority(text)
        logger.info("Priority (from text) predicted: %s (confidence=%.2f)", result["label"], result["confidence"])
        return result


ml_service = MLService()
