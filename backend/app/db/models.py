"""
db/models.py
SQLAlchemy ORM model for a stored, analyzed enquiry.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from backend.app.db.session import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    enquiry_text = Column(Text, nullable=False)
    industry = Column(String, nullable=True)

    predicted_category = Column(String, nullable=False)
    category_confidence = Column(Float, nullable=False)

    predicted_priority = Column(String, nullable=False)
    priority_confidence = Column(Float, nullable=True)

    budget_inr = Column(Float, nullable=True)
    urgency_hint = Column(String, nullable=True)

    extracted_email = Column(String, nullable=True)
    extracted_phone = Column(String, nullable=True)
    extracted_organizations = Column(Text, nullable=True)  # comma-separated

    insight = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
