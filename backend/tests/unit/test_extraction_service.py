"""
tests/unit/test_extraction_service.py
Unit tests for regex-based entity extraction (email, phone).
"""

from backend.app.services.extraction_service import extraction_service


def test_extracts_email_correctly():
    text = "Please contact me at ratnesh.kumar@example.com for details"
    result = extraction_service.extract(text)
    assert result["email"] == "ratnesh.kumar@example.com"


def test_extracts_phone_correctly():
    text = "Call me at 9876543210 to discuss the project"
    result = extraction_service.extract(text)
    assert result["phone"] is not None


def test_returns_none_when_no_email_present():
    text = "We need a mobile app for our business, no contact info here"
    result = extraction_service.extract(text)
    assert result["email"] is None


def test_organizations_key_always_present():
    text = "We are looking for automation services"
    result = extraction_service.extract(text)
    assert "organizations" in result
    assert isinstance(result["organizations"], list)
