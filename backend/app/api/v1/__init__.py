"""
API v1 Router Configuration

This module configures the API router for version 1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.routes import api_router as analysis_router

# Create main API router - this is what gets imported by main.py
api_router = APIRouter()

# Include route modules
api_router.include_router(analysis_router, prefix="", tags=["Analysis"])

# Additional route modules can be added here in the future
# api_router.include_router(honeypot_router, prefix="/honeypot", tags=["Honeypot"])
# api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])