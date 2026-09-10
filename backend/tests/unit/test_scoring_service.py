"""
tests/unit/test_scoring_service.py
Unit tests for priority scoring logic based on structured fields.
"""

from backend.app.services.scoring_service import scoring_service


def test_high_budget_forces_high_priority():
    result = scoring_service.score(text="some enquiry", budget_inr=600000, urgency_hint="Low")
    assert result["priority"] == "High"
    assert result["source"] == "structured_fields"


def test_high_urgency_hint_forces_high_priority():
    result = scoring_service.score(text="some enquiry", budget_inr=1000, urgency_hint="High")
    assert result["priority"] == "High"


def test_medium_budget_gives_medium_priority():
    result = scoring_service.score(text="some enquiry", budget_inr=150000, urgency_hint="Low")
    assert result["priority"] == "Medium"


def test_low_budget_and_low_urgency_gives_low_priority():
    result = scoring_service.score(text="some enquiry", budget_inr=5000, urgency_hint="Low")
    assert result["priority"] == "Low"


def test_missing_structured_fields_falls_back_to_ml():
    result = scoring_service.score(text="We need this urgently, big project, huge budget")
    assert result["source"] == "ml_model"
    assert result["priority"] in {"Low", "Medium", "High"}
    assert result["confidence"] is not None


def test_invalid_urgency_hint_defaults_safely():
    result = scoring_service.score(text="some enquiry", budget_inr=None, urgency_hint="not-a-real-value")
    assert result["priority"] in {"Low", "Medium", "High"}
