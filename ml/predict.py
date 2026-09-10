"""
ml/predict.py
Reusable inference interface for both trained models.
"""

import os
import joblib
from preprocess import clean_text

_MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(os.path.dirname(__file__), "models"))
_category_model = None
_priority_model = None


def _load(name):
    path = os.path.join(_MODEL_DIR, f"{name}.joblib")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found at {path}. Run ml/train.py first.")
    return joblib.load(path)


def _get_category_model():
    global _category_model
    if _category_model is None:
        _category_model = _load("category_classifier")
    return _category_model


def _get_priority_model():
    global _priority_model
    if _priority_model is None:
        _priority_model = _load("priority_classifier")
    return _priority_model


def _predict_with_proba(model, text: str) -> dict:
    cleaned = clean_text(text)
    proba = model.predict_proba([cleaned])[0]
    prob_map = {cls: round(float(p), 4) for cls, p in zip(model.classes_, proba)}
    top = max(prob_map, key=prob_map.get)
    return {"label": top, "confidence": prob_map[top], "probabilities": prob_map}


def predict_category(text: str) -> dict:
    return _predict_with_proba(_get_category_model(), text)


def predict_priority(text: str) -> dict:
    return _predict_with_proba(_get_priority_model(), text)


def predict_all(text: str) -> dict:
    return {"category": predict_category(text), "priority_from_text": predict_priority(text)}
