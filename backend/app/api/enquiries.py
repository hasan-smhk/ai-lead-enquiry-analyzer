"""
api/enquiries.py
API routes for submitting and retrieving analyzed enquiries.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.db.session import get_db
from backend.app.db.models import Enquiry
from backend.app.schemas.enquiry import EnquiryCreateRequest, EnquiryResponse
from backend.app.services.ml_service import ml_service
from backend.app.services.extraction_service import extraction_service
from backend.app.services.scoring_service import scoring_service
from backend.app.services.insight_service import insight_service

logger = logging.getLogger("api.enquiries")
router = APIRouter(prefix="/api/v1/enquiries", tags=["Enquiries"])


def _to_response(db_obj: Enquiry) -> EnquiryResponse:
    orgs = db_obj.extracted_organizations.split(",") if db_obj.extracted_organizations else []
    data = {
        **db_obj.__dict__,
        "extracted_organizations": [o for o in orgs if o],
    }
    return EnquiryResponse.model_validate(data)


@router.post("", response_model=EnquiryResponse, status_code=201)
def create_enquiry(payload: EnquiryCreateRequest, db: Session = Depends(get_db)):
    try:
        category_result = ml_service.predict_category(payload.enquiry_text)
        priority_result = scoring_service.score(
            text=payload.enquiry_text,
            budget_inr=payload.budget_inr,
            urgency_hint=payload.urgency_hint,
        )
        entities = extraction_service.extract(payload.enquiry_text)
        insight = insight_service.generate(
            category=category_result["label"],
            priority=priority_result["priority"],
            industry=payload.industry,
            budget_inr=payload.budget_inr,
            entities=entities,
        )

        db_enquiry = Enquiry(
            enquiry_text=payload.enquiry_text,
            industry=payload.industry,
            predicted_category=category_result["label"],
            category_confidence=category_result["confidence"],
            predicted_priority=priority_result["priority"],
            priority_confidence=priority_result["confidence"],
            budget_inr=payload.budget_inr,
            urgency_hint=payload.urgency_hint,
            extracted_email=entities.get("email"),
            extracted_phone=entities.get("phone"),
            extracted_organizations=",".join(entities.get("organizations", [])),
            insight=insight,
        )
        db.add(db_enquiry)
        db.commit()
        db.refresh(db_enquiry)

        logger.info("Enquiry #%d created: category=%s priority=%s",
                     db_enquiry.id, db_enquiry.predicted_category, db_enquiry.predicted_priority)

        return _to_response(db_enquiry)

    except FileNotFoundError as e:
        logger.error("Model not found: %s", e)
        raise HTTPException(status_code=503, detail="ML model unavailable. Please contact admin.")
    except Exception as e:
        logger.exception("Unexpected error while processing enquiry")
        raise HTTPException(status_code=500, detail="Internal server error while processing enquiry.")


@router.get("", response_model=list[EnquiryResponse])
def list_enquiries(
    category: str | None = None,
    priority: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Enquiry)
    if category:
        query = query.filter(Enquiry.predicted_category == category)
    if priority:
        query = query.filter(Enquiry.predicted_priority == priority)

    results = query.order_by(desc(Enquiry.created_at)).limit(limit).all()
    return [_to_response(r) for r in results]


@router.get("/{enquiry_id}", response_model=EnquiryResponse)
def get_enquiry(enquiry_id: int, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return _to_response(enquiry)
