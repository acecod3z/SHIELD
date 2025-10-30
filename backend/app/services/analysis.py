"""
Analysis Service - Core business logic for SHIELD Security Analysis

This module contains the main analysis workflow and integration stubs
for Phase 1 (AI Models) and Phase 2 (Honeypot System).
"""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import random

from app.models.schemas import (
    AnalysisRequest, AnalysisResult, ThreatDetection, HoneypotRedirect,
    InputType, AttackType, ThreatLevel
)
from app.core.config import settings
from app.services.sql_injection_detector import sql_injection_detector


logger = logging.getLogger(__name__)
security_logger = logging.getLogger("shield.security")


class AnalysisService:
    """Main service for coordinating security analysis."""
    
    def __init__(self):
        self.job_store: Dict[str, Dict] = {}  # In-memory job storage (use Redis in production)
    
    async def analyze_input(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Main analysis workflow that coordinates all analysis steps.
        
        Args:
            request: The analysis request containing input and metadata
            
        Returns:
            AnalysisResult containing the analysis findings
        """
        start_time = datetime.utcnow()
        
        # Log security analysis request
        security_logger.info(
            f"Analysis request received - Type: {request.input_type}, "
            f"IP: {request.ip_address}, Session: {request.session_id}"
        )
        
        try:
            # Phase 1 Integration Point: AI Model Analysis
            is_malicious, detected_threats = await self.ai_analysis_stub(
                request.input_type, 
                request.content
            )
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Determine overall threat level
            threat_level = self._calculate_threat_level(detected_threats)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(detected_threats)
            
            # Create analysis result
            result = AnalysisResult(
                is_malicious=is_malicious,
                threat_level=threat_level,
                confidence_score=confidence_score,
                detected_threats=detected_threats,
                analysis_metadata={
                    "input_type": request.input_type,
                    "content_length": len(request.content),
                    "analysis_timestamp": start_time.isoformat(),
                    "user_agent": request.user_agent,
                    "ip_address": request.ip_address
                },
                ai_model_version="stub-v1.0.0",  # Will be replaced with actual model version
                processing_time_ms=processing_time,
                honeypot_triggered=False  # Will be set if honeypot is triggered
            )
            
            # Log analysis result
            security_logger.info(
                f"Analysis completed - Malicious: {is_malicious}, "
                f"Threats: {len(detected_threats)}, Time: {processing_time:.2f}ms"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            security_logger.error(f"Analysis error - IP: {request.ip_address}, Error: {str(e)}")
            raise
    
    async def ai_analysis_stub(self, input_type: InputType, content: str) -> tuple[bool, List[ThreatDetection]]:
        """
        PHASE 1 INTEGRATION POINT: AI Model Analysis Stub
        
        This function simulates the AI model analysis that will be integrated
        in Phase 1. Replace this with actual AI model calls.
        
        Args:
            input_type: The type of input being analyzed
            content: The actual content to analyze
            
        Returns:
            Tuple of (is_malicious: bool, detected_threats: List[ThreatDetection])
        """
        # Simulate AI model processing time
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        detected_threats = []
        
        # Simulate threat detection based on input type and content patterns
        if input_type == InputType.TEXT:
            threats = self._analyze_text_stub(content)
            detected_threats.extend(threats)
            
        elif input_type == InputType.URL:
            threats = self._analyze_url_stub(content)
            detected_threats.extend(threats)
            
        elif input_type == InputType.IMAGE:
            threats = self._analyze_image_stub(content)
            detected_threats.extend(threats)
        
        is_malicious = len(detected_threats) > 0
        
        logger.info(f"AI Analysis Stub - Input: {input_type}, Malicious: {is_malicious}, Threats: {len(detected_threats)}")
        
        return is_malicious, detected_threats
    
    def _analyze_text_stub(self, content: str) -> List[ThreatDetection]:
        """
        Text-based threat analysis using the SQL injection detector.
        Integrates the SimpleSQLInjectionDetector from model directory.
        """
        threats = []
        
        # Use the SQL injection detector for analysis
        detection_result = sql_injection_detector.predict(content)
        
        if detection_result['is_malicious']:
            # Map risk score to severity
            risk_score = detection_result['risk_score']
            if risk_score >= 50:
                severity = ThreatLevel.CRITICAL
            elif risk_score >= 30:
                severity = ThreatLevel.HIGH
            elif risk_score >= 15:
                severity = ThreatLevel.MEDIUM
            else:
                severity = ThreatLevel.LOW
            
            # Create detailed description from indicators
            indicators_text = "; ".join(detection_result['indicators'][:3])  # Top 3 indicators
            description = f"SQL injection detected: {indicators_text}"
            
            threats.append(ThreatDetection(
                attack_type=AttackType.SQL_INJECTION,
                confidence=detection_result['confidence'],
                severity=severity,
                description=description,
                mitigation="Use parameterized queries and input validation. Avoid dynamic SQL construction with user input."
            ))
            
            logger.info(
                f"SQL injection detected - Risk Score: {risk_score}, "
                f"Confidence: {detection_result['confidence']:.2f}, "
                f"Indicators: {len(detection_result['indicators'])}"
            )
        else:
            logger.info(f"Text analysis: No malicious patterns detected")
        
        # Additional XSS detection (keeping existing functionality)
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in ['<script', 'javascript:', 'onerror', 'onload']):
            threats.append(ThreatDetection(
                attack_type=AttackType.XSS,
                confidence=random.uniform(0.6, 0.9),
                severity=ThreatLevel.MEDIUM,
                description="Potential XSS attack pattern detected",
                mitigation="Sanitize and encode user input before rendering"
            ))
        
        return threats
    
    def _analyze_url_stub(self, content: str) -> List[ThreatDetection]:
        """Stub for URL-based threat analysis."""
        threats = []
        content_lower = content.lower()
        
        # Suspicious URL patterns
        suspicious_domains = ['bit.ly', 'tinyurl.com', 'shortened.link']
        phishing_keywords = ['login', 'verify', 'suspend', 'update', 'secure']
        
        if any(domain in content_lower for domain in suspicious_domains):
            threats.append(ThreatDetection(
                attack_type=AttackType.PHISHING,
                confidence=random.uniform(0.4, 0.7),
                severity=ThreatLevel.MEDIUM,
                description="Shortened URL detected - potential phishing risk",
                mitigation="Verify the destination URL before clicking"
            ))
        
        if any(keyword in content_lower for keyword in phishing_keywords):
            threats.append(ThreatDetection(
                attack_type=AttackType.PHISHING,
                confidence=random.uniform(0.6, 0.85),
                severity=ThreatLevel.HIGH,
                description="URL contains suspicious phishing keywords",
                mitigation="Verify legitimacy through official channels"
            ))
        
        if 'localhost' in content_lower or '127.0.0.1' in content or '192.168.' in content:
            threats.append(ThreatDetection(
                attack_type=AttackType.SSRF,
                confidence=random.uniform(0.7, 0.9),
                severity=ThreatLevel.CRITICAL,
                description="Potential SSRF attack targeting internal resources",
                mitigation="Validate and whitelist allowed external URLs"
            ))
        
        return threats
    
    def _analyze_image_stub(self, content: str) -> List[ThreatDetection]:
        """Stub for image-based threat analysis."""
        threats = []
        
        # Simulate image analysis based on content length and patterns
        content_size = len(content)
        
        # Large images might contain hidden data
        if content_size > 1000000:  # > 1MB
            threats.append(ThreatDetection(
                attack_type=AttackType.STEGANOGRAPHY,
                confidence=random.uniform(0.3, 0.6),
                severity=ThreatLevel.MEDIUM,
                description="Large image file - potential steganography risk",
                mitigation="Scan image for hidden data and malicious payloads"
            ))
        
        # Random suspicious metadata detection (for demo)
        if random.random() < 0.2:  # 20% chance
            threats.append(ThreatDetection(
                attack_type=AttackType.SUSPICIOUS_METADATA,
                confidence=random.uniform(0.5, 0.8),
                severity=ThreatLevel.LOW,
                description="Suspicious metadata patterns detected in image",
                mitigation="Strip metadata before processing or storing image"
            ))
        
        return threats
    
    def _calculate_threat_level(self, threats: List[ThreatDetection]) -> ThreatLevel:
        """Calculate overall threat level based on detected threats."""
        if not threats:
            return ThreatLevel.LOW
        
        # Get the highest severity level
        severity_levels = [threat.severity for threat in threats]
        
        if ThreatLevel.CRITICAL in severity_levels:
            return ThreatLevel.CRITICAL
        elif ThreatLevel.HIGH in severity_levels:
            return ThreatLevel.HIGH
        elif ThreatLevel.MEDIUM in severity_levels:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _calculate_confidence_score(self, threats: List[ThreatDetection]) -> float:
        """Calculate overall confidence score."""
        if not threats:
            return 1.0  # High confidence that it's benign
        
        # Average confidence of detected threats
        total_confidence = sum(threat.confidence for threat in threats)
        return min(total_confidence / len(threats), 1.0)
    
    async def honeypot_engagement_stub(self, attacker_input: str, session_id: str) -> HoneypotRedirect:
        """
        PHASE 2 INTEGRATION POINT: Honeypot Engagement Stub
        
        This function simulates the honeypot engagement system that will be
        integrated in Phase 2. Replace this with actual honeypot logic.
        
        Args:
            attacker_input: The malicious input that triggered the honeypot
            session_id: Unique session identifier for the attacker
            
        Returns:
            HoneypotRedirect containing redirection information
        """
        # Generate honeypot session
        honeypot_session_id = f"honeypot_{uuid.uuid4().hex[:8]}"
        
        # Create fake terminal redirect URL
        redirect_url = f"/honeypot/terminal/{honeypot_session_id}"
        
        # Set session expiration
        expires_at = datetime.utcnow() + timedelta(seconds=settings.HONEYPOT_SESSION_TIMEOUT)
        
        # Log honeypot engagement
        security_logger.warning(
            f"Honeypot engaged - Session: {honeypot_session_id}, "
            f"Original Input: {attacker_input[:100]}..."
        )
        
        return HoneypotRedirect(
            redirect_url=redirect_url,
            session_id=honeypot_session_id,
            expires_at=expires_at,
            initial_command=attacker_input[:50] if len(attacker_input) > 50 else attacker_input
        )
    
    def store_job(self, job_id: str, job_data: Dict[str, Any]):
        """Store job information for status tracking."""
        self.job_store[job_id] = job_data
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve job information."""
        return self.job_store.get(job_id)


# Global service instance
analysis_service = AnalysisService()