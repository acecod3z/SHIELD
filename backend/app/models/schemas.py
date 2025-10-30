"""
Pydantic data models for SHIELD Security Analysis API

These models define the request/response schemas for the API endpoints
and provide data validation and serialization.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
import base64
import re


class InputType(str, Enum):
    """Enumeration for supported input types."""
    TEXT = "text"
    URL = "url"
    IMAGE = "image"


class ThreatLevel(str, Enum):
    """Enumeration for threat severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AttackType(str, Enum):
    """Enumeration for detected attack types."""
    # Text-based attacks
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    LDAP_INJECTION = "ldap_injection"
    
    # URL-based attacks
    PHISHING = "phishing"
    MALICIOUS_URL = "malicious_url"
    SSRF = "ssrf"
    REDIRECT_ATTACK = "redirect_attack"
    
    # Image-based attacks
    STEGANOGRAPHY = "steganography"
    MALICIOUS_PAYLOAD = "malicious_payload"
    SUSPICIOUS_METADATA = "suspicious_metadata"
    
    # General
    UNKNOWN = "unknown"


class AnalysisRequest(BaseModel):
    """Request model for security analysis."""
    
    input_type: InputType = Field(..., description="Type of input being analyzed")
    content: str = Field(..., description="The actual input content")
    
    # Optional metadata
    user_agent: Optional[str] = Field(None, description="User agent string (for forensics)")
    ip_address: Optional[str] = Field(None, description="Source IP address")
    session_id: Optional[str] = Field(None, description="Session identifier")
    
    @validator('content')
    def validate_content(cls, v, values):
        """Validate content based on input type."""
        input_type = values.get('input_type')
        
        if input_type == InputType.TEXT:
            if len(v.strip()) == 0:
                raise ValueError("Text content cannot be empty")
            if len(v) > 10000:  # 10KB limit for text
                raise ValueError("Text content too large (max 10KB)")
        
        elif input_type == InputType.URL:
            # Basic URL validation
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            if not url_pattern.match(v):
                raise ValueError("Invalid URL format")
        
        elif input_type == InputType.IMAGE:
            # Validate base64 encoded image
            try:
                base64.b64decode(v)
            except Exception:
                raise ValueError("Invalid base64 encoded image")
            
            # Size limit check (5MB encoded)
            if len(v) > 7000000:  # Roughly 5MB when base64 decoded
                raise ValueError("Image too large (max 5MB)")
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_type": "text",
                "content": "SELECT * FROM users WHERE id = 1",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "ip_address": "192.168.1.100"
            }
        }


class ThreatDetection(BaseModel):
    """Model for individual threat detection."""
    
    attack_type: AttackType
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    severity: ThreatLevel
    description: str
    mitigation: Optional[str] = None


class AnalysisResult(BaseModel):
    """Model for analysis results."""
    
    is_malicious: bool
    threat_level: ThreatLevel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    detected_threats: List[ThreatDetection] = Field(default_factory=list)
    analysis_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Phase 1 Integration Point - AI Model Results
    ai_model_version: Optional[str] = None
    processing_time_ms: Optional[float] = None
    
    # Phase 2 Integration Point - Honeypot Data
    honeypot_triggered: bool = False
    honeypot_session_id: Optional[str] = None


class HoneypotRedirect(BaseModel):
    """Model for honeypot redirection information."""
    
    redirect_url: str
    session_id: str
    expires_at: datetime
    initial_command: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint."""
    
    job_id: str = Field(..., description="Unique identifier for this analysis")
    status: str = Field(default="completed", description="Analysis status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Analysis results
    result: Optional[AnalysisResult] = None
    
    # Honeypot redirection (Phase 2)
    honeypot_redirect: Optional[HoneypotRedirect] = None
    
    # Error information
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "analysis_1698765432_abc123",
                "status": "completed",
                "timestamp": "2025-10-30T10:30:00Z",
                "result": {
                    "is_malicious": True,
                    "threat_level": "high",
                    "confidence_score": 0.95,
                    "detected_threats": [
                        {
                            "attack_type": "sql_injection",
                            "confidence": 0.95,
                            "severity": "high",
                            "description": "SQL injection attempt detected in user input",
                            "mitigation": "Use parameterized queries and input validation"
                        }
                    ]
                }
            }
        }


class JobStatus(BaseModel):
    """Model for job status checking."""
    
    job_id: str
    status: str  # pending, processing, completed, failed
    created_at: datetime
    completed_at: Optional[datetime] = None
    progress: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "analysis_1698765432_abc123",
                "status": "processing",
                "created_at": "2025-10-30T10:30:00Z",
                "progress": 0.75
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid input format",
                "detail": "URL format is not valid",
                "timestamp": "2025-10-30T10:30:00Z"
            }
        }