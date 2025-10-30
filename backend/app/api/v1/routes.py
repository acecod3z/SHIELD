"""
SHIELD API v1 Routes

This module contains all the API endpoints for the SHIELD Security Analysis platform.
Includes the main analysis endpoint and job status checking.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models.schemas import (
    AnalysisRequest, AnalysisResponse, JobStatus, ErrorResponse,
    AnalysisResult, HoneypotRedirect
)
from app.services.analysis import analysis_service
from app.core.config import settings


logger = logging.getLogger(__name__)
security_logger = logging.getLogger("shield.security")

# Create the main API router that will be imported by main.py
api_router = APIRouter(tags=["Security Analysis"])


def generate_job_id() -> str:
    """Generate a unique job ID."""
    timestamp = int(datetime.utcnow().timestamp())
    unique_id = uuid.uuid4().hex[:8]
    return f"analysis_{timestamp}_{unique_id}"


@api_router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze input for security threats",
    description="""
    Analyze various types of input (text, URL, image) for potential security threats.
    
    The analysis process:
    1. Validates and processes the input
    2. Runs AI-powered threat detection (Phase 1 integration point)
    3. If malicious input is detected, may trigger honeypot engagement (Phase 2)
    4. Returns detailed analysis results with threat classifications
    
    Input types supported:
    - **text**: Plain text and string-based inputs for SQL injection, XSS, command injection detection
    - **url**: URLs for phishing, malicious links, SSRF detection  
    - **image**: Base64-encoded images for steganography, malicious payload detection
    """,
)
async def analyze_input(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
) -> AnalysisResponse:
    """
    Main analysis endpoint that processes security analysis requests.
    
    Args:
        request: The analysis request containing input type and content
        background_tasks: FastAPI background tasks for async processing
        
    Returns:
        AnalysisResponse with results or honeypot redirection
        
    Raises:
        HTTPException: If validation fails or processing errors occur
    """
    job_id = generate_job_id()
    
    try:
        # Log incoming request
        logger.info(f"Analysis request {job_id} - Type: {request.input_type}")
        security_logger.info(
            f"Analysis started - Job: {job_id}, Type: {request.input_type}, "
            f"IP: {request.ip_address}, Content length: {len(request.content)}"
        )
        
        # Store job for tracking
        job_data = {
            "job_id": job_id,
            "status": "processing",
            "created_at": datetime.utcnow(),
            "request": request.dict(),
        }
        analysis_service.store_job(job_id, job_data)
        
        # Perform analysis
        analysis_result = await analysis_service.analyze_input(request)
        
        # Update job status
        job_data.update({
            "status": "completed",
            "completed_at": datetime.utcnow(),
            "result": analysis_result.dict()
        })
        analysis_service.store_job(job_id, job_data)
        
        # Prepare response
        response = AnalysisResponse(
            job_id=job_id,
            status="completed",
            result=analysis_result
        )
        
        # Phase 2 Integration Point: Honeypot Engagement
        if analysis_result.is_malicious and settings.HONEYPOT_ENABLED:
            try:
                honeypot_redirect = await analysis_service.honeypot_engagement_stub(
                    attacker_input=request.content,
                    session_id=request.session_id or job_id
                )
                
                response.honeypot_redirect = honeypot_redirect
                analysis_result.honeypot_triggered = True
                analysis_result.honeypot_session_id = honeypot_redirect.session_id
                
                # Log honeypot activation
                security_logger.warning(
                    f"Honeypot activated - Job: {job_id}, Session: {honeypot_redirect.session_id}"
                )
                
            except Exception as e:
                logger.error(f"Honeypot engagement failed for job {job_id}: {str(e)}")
                # Continue without honeypot if it fails
        
        # Log completion
        logger.info(
            f"Analysis completed - Job: {job_id}, Malicious: {analysis_result.is_malicious}, "
            f"Threats: {len(analysis_result.detected_threats)}"
        )
        
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error for job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Analysis failed for job {job_id}: {str(e)}")
        security_logger.error(f"Analysis error - Job: {job_id}, Error: {str(e)}")
        
        # Update job status
        job_data = analysis_service.get_job(job_id)
        if job_data:
            job_data.update({
                "status": "failed",
                "completed_at": datetime.utcnow(),
                "error": str(e)
            })
            analysis_service.store_job(job_id, job_data)
        
        raise HTTPException(
            status_code=500,
            detail="Internal analysis error occurred"
        )


@api_router.get(
    "/status/{job_id}",
    response_model=JobStatus,
    summary="Check analysis job status",
    description="""
    Check the status of a previously submitted analysis job.
    
    Possible statuses:
    - **pending**: Job is queued for processing
    - **processing**: Job is currently being analyzed
    - **completed**: Analysis finished successfully
    - **failed**: Analysis encountered an error
    
    Use this endpoint for long-running analysis jobs or to implement
    polling-based status updates in the frontend.
    """,
)
async def get_job_status(job_id: str) -> JobStatus:
    """
    Get the status of an analysis job.
    
    Args:
        job_id: The unique job identifier returned from the analyze endpoint
        
    Returns:
        JobStatus containing current job information
        
    Raises:
        HTTPException: If job ID is not found
    """
    try:
        job_data = analysis_service.get_job(job_id)
        
        if not job_data:
            logger.warning(f"Job status requested for unknown job: {job_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Job {job_id} not found"
            )
        
        # Calculate progress based on status
        progress_map = {
            "pending": 0.0,
            "processing": 0.5,
            "completed": 1.0,
            "failed": 1.0
        }
        
        status_response = JobStatus(
            job_id=job_id,
            status=job_data["status"],
            created_at=job_data["created_at"],
            completed_at=job_data.get("completed_at"),
            progress=progress_map.get(job_data["status"], 0.0)
        )
        
        logger.info(f"Status check - Job: {job_id}, Status: {job_data['status']}")
        
        return status_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status check failed for job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve job status"
        )


@api_router.get(
    "/health",
    summary="API health check",
    description="Simple health check endpoint to verify API availability."
)
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "SHIELD Analysis API",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "ai_models": "stub",  # Will be "active" in Phase 1
            "honeypot": "stub" if settings.HONEYPOT_ENABLED else "disabled"  # Will be "active" in Phase 2
        }
    }


# Example endpoints for testing (can be removed in production)
@api_router.post(
    "/test/benign",
    summary="Test endpoint for benign input",
    description="Test endpoint that always returns a benign result for testing purposes."
)
async def test_benign():
    """Test endpoint for benign analysis results."""
    return AnalysisResponse(
        job_id="test_benign_123",
        status="completed",
        result=AnalysisResult(
            is_malicious=False,
            threat_level="low",
            confidence_score=0.95,
            detected_threats=[],
            analysis_metadata={"test": True}
        )
    )


@api_router.post(
    "/test/malicious",
    summary="Test endpoint for malicious input",
    description="Test endpoint that always returns a malicious result for testing purposes."
)
async def test_malicious():
    """Test endpoint for malicious analysis results."""
    from app.models.schemas import ThreatDetection, AttackType, ThreatLevel
    
    return AnalysisResponse(
        job_id="test_malicious_123",
        status="completed",
        result=AnalysisResult(
            is_malicious=True,
            threat_level="high",
            confidence_score=0.85,
            detected_threats=[
                ThreatDetection(
                    attack_type=AttackType.SQL_INJECTION,
                    confidence=0.85,
                    severity=ThreatLevel.HIGH,
                    description="Test SQL injection detection",
                    mitigation="Use parameterized queries"
                )
            ],
            analysis_metadata={"test": True}
        )
    )