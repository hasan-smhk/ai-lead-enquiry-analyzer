"""
tests/unit/test_preprocess.py
Unit tests for ml/preprocess.py text cleaning and validation.
"""

import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml"))
from preprocess import clean_text, validate_enquiry_text, ValidationError


def test_clean_text_lowercases_and_trims():
    result = clean_text("  Hello WORLD  ")
    assert result == "hello world"


def test_clean_text_removes_urls():
    result = clean_text("Visit https://example.com for details")
    assert "https" not in result
    assert "example.com" not in result


def test_clean_text_removes_special_characters():
    result = clean_text("Need help!!! ### urgent???")
    assert "#" not in result


def test_clean_text_handles_non_string_input():
    assert clean_text(None) == ""
    assert clean_text(12345) == ""


def test_validate_enquiry_text_raises_on_empty():
    with pytest.raises(ValidationError):
        validate_enquiry_text("")


def test_validate_enquiry_text_raises_on_too_short():
    with pytest.raises(ValidationError):
        validate_enquiry_text("hi")


def test_validate_enquiry_text_accepts_valid_text():
    result = validate_enquiry_text("We need a chatbot for our website urgently")
    assert isinstance(result, str)
    assert len(result) > 0


def test_validate_enquiry_text_raises_on_too_long():
    with pytest.raises(ValidationError):
        validate_enquiry_text("a" * 6000)
