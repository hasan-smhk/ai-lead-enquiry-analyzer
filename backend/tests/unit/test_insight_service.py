"""
tests/unit/test_insight_service.py
Unit tests for human-readable insight generation.
"""

from backend.app.services.insight_service import insight_service


def test_insight_includes_priority_and_category():
    result = insight_service.generate(category="Chatbot", priority="High")
    assert "High priority" in result
    assert "Chatbot" in result


def test_insight_includes_industry_when_provided():
    result = insight_service.generate(category="Mobile App", priority="Medium", industry="Healthcare")
    assert "Healthcare" in result


def test_insight_includes_budget_when_provided():
    result = insight_service.generate(category="Website Development", priority="Low", budget_inr=250000)
    assert "250,000" in result or "250000" in result


def test_insight_includes_email_when_entity_present():
    result = insight_service.generate(
        category="Automation", priority="High",
        entities={"email": "test@example.com", "organizations": []}
    )
    assert "test@example.com" in result


def test_insight_recommends_immediate_followup_for_high_priority():
    result = insight_service.generate(category="AI/ML Solution", priority="High")
    assert "24 hours" in result


def test_insight_recommends_nurture_for_low_priority():
    result = insight_service.generate(category="Training/Courses", priority="Low")
    assert "nurture" in result.lower()
