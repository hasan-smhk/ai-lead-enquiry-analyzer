"""
services/extraction_service.py
Extracts structured entities (email, phone, organizations) from enquiry text.
"""

import re
import logging

logger = logging.getLogger("extraction_service")

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}")

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        import spacy
        logger.info("Loading spaCy model en_core_web_sm...")
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


class ExtractionService:
    def extract(self, text: str) -> dict:
        email_match = EMAIL_RE.search(text)
        phone_match = PHONE_RE.search(text)

        organizations = []
        try:
            doc = _get_nlp()(text)
            organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        except Exception as e:
            logger.warning("spaCy NER failed, skipping org extraction: %s", e)

        return {
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "organizations": organizations,
        }


extraction_service = ExtractionService()
