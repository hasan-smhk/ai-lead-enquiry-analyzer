"""
main.py
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.logging_config import logger
from backend.app.db.session import Base, engine
from backend.app.api import enquiries

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Lead & Enquiry Analyzer",
    description="Analyzes customer enquiries, extracts entities, categorizes and prioritizes leads.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(enquiries.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    logger.info("AI Lead & Enquiry Analyzer service started.")


# Serve the frontend dashboard (must be mounted last, after all API routes)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
