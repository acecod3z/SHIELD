"""
SHIELD Backend - Main Application Entry Point

This is the main FastAPI application entry point for the SHIELD Web Interface backend.
Designed for future integration of AI security analysis models (Phase 1) and 
Honeypot System (Phase 2).
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging

# Initialize logging
setup_logging()

# Create FastAPI application
app = FastAPI(
    title="SHIELD Security Analysis API",
    description="AI-powered security analysis platform for detecting malicious inputs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "SHIELD Security Analysis API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "analyze": "/api/v1/analyze",
            "status": "/api/v1/status/{job_id}",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SHIELD Backend",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )