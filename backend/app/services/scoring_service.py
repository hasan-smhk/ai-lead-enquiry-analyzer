"""
services/scoring_service.py
Determines final priority: prefers structured fields (budget_inr, urgency_hint)
when provided by the client; falls back to the text-based ML priority model
when those fields are missing (e.g., raw email/chat enquiries).
"""

import logging
from backend.app.services.ml_service import ml_service

logger = logging.getLogger("scoring_service")

VALID_URGENCY = {"Low", "Medium", "High"}
HIGH_BUDGET_THRESHOLD = 500_000
MEDIUM_BUDGET_THRESHOLD = 100_000
PRIORITY_RANK = {"Low": 0, "Medium": 1, "High": 2}


class ScoringService:
    def score(self, text: str, budget_inr: float = None, urgency_hint: str = None) -> dict:
        if budget_inr is not None or urgency_hint is not None:
            priority = self._score_from_structured_fields(budget_inr, urgency_hint)
            logger.info("Priority derived from structured fields: %s", priority)
            return {"priority": priority, "confidence": None, "source": "structured_fields"}

        result = ml_service.predict_priority_from_text(text)
        logger.info("Priority derived from ML text model: %s", result["label"])
        return {"priority": result["label"], "confidence": result["confidence"], "source": "ml_model"}

    def _score_from_structured_fields(self, budget_inr, urgency_hint) -> str:
        urgency = urgency_hint if urgency_hint in VALID_URGENCY else "Low"
        budget_priority = self._budget_to_priority(budget_inr)
        return urgency if PRIORITY_RANK[urgency] >= PRIORITY_RANK[budget_priority] else budget_priority

    @staticmethod
    def _budget_to_priority(budget) -> str:
        if budget is None:
            return "Low"
        if budget >= HIGH_BUDGET_THRESHOLD:
            return "High"
        if budget >= MEDIUM_BUDGET_THRESHOLD:
            return "Medium"
        return "Low"


scoring_service = ScoringService()
