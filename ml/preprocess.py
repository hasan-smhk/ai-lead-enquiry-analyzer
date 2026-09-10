"""
ml/preprocess.py
Text cleaning and validation utilities shared by training and inference.
"""

import re

MIN_TEXT_LENGTH = 10
MAX_TEXT_LENGTH = 5000

_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_MULTISPACE_RE = re.compile(r"\s+")
_ALLOWED_CHARS_RE = re.compile(r"[^a-zA-Z0-9\s.,!?@'-]")


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = _URL_RE.sub(" ", text)
    text = _ALLOWED_CHARS_RE.sub(" ", text)
    text = _MULTISPACE_RE.sub(" ", text)
    return text.strip().lower()


class ValidationError(Exception):
    pass


def validate_enquiry_text(raw_text: str) -> str:
    if raw_text is None or not str(raw_text).strip():
        raise ValidationError("Enquiry text must not be empty.")
    if len(raw_text) > MAX_TEXT_LENGTH:
        raise ValidationError(f"Enquiry text exceeds {MAX_TEXT_LENGTH} characters.")
    cleaned = clean_text(raw_text)
    if len(cleaned) < MIN_TEXT_LENGTH:
        raise ValidationError(f"Enquiry text too short after cleaning (min {MIN_TEXT_LENGTH} chars).")
    return cleaned
