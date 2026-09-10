"""
schemas/enquiry.py
Pydantic request/response models — defines the public API contract.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class EnquiryCreateRequest(BaseModel):
    enquiry_text: str = Field(..., min_length=10, max_length=5000)
    industry: Optional[str] = None
    budget_inr: Optional[float] = Field(default=None, ge=0)
    urgency_hint: Optional[str] = None  # "Low" / "Medium" / "High" if known

    @field_validator("urgency_hint")
    @classmethod
    def validate_urgency(cls, v):
        if v is not None and v not in {"Low", "Medium", "High"}:
            raise ValueError("urgency_hint must be one of: Low, Medium, High")
        return v


class EnquiryResponse(BaseModel):
    id: int
    enquiry_text: str
    industry: Optional[str]
    predicted_category: str
    category_confidence: float
    predicted_priority: str
    priority_confidence: Optional[float]
    budget_inr: Optional[float]
    urgency_hint: Optional[str]
    extracted_email: Optional[str]
    extracted_phone: Optional[str]
    extracted_organizations: List[str] = []
    insight: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
