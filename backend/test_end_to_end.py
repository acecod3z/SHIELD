#!/usr/bin/env python3
"""
End-to-End Test: Simulates the frontend to backend flow
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from app.services.analysis import analysis_service
from app.models.schemas import AnalysisRequest, InputType

async def test_end_to_end():
    """Test the complete flow that the frontend would trigger."""
    
    print("🧪 END-TO-END INTEGRATION TEST")
    print("="*50)
    print("Simulating the flow: Frontend → Backend → SQL Detector")
    print()
    
    # Test cases that a user might enter in the frontend
    test_cases = [
        {
            "name": "Safe Query",
            "input": "SELECT name FROM users WHERE id = 123",
            "expected": "should be classified as SAFE"
        },
        {
            "name": "SQL Injection Attack",
            "input": "admin'; DROP TABLE users; --",
            "expected": "should be classified as MALICIOUS"
        },
        {
            "name": "Union-based Injection",
            "input": "1' UNION SELECT username, password FROM admin --",
            "expected": "should be classified as MALICIOUS"
        },
        {
            "name": "Boolean-based Injection",
            "input": "user123' OR 1=1 --",
            "expected": "should be classified as MALICIOUS"
        }
    ]
    
    print(f"Testing {len(test_cases)} scenarios...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Input: '{test_case['input']}'")
        print(f"Expected: {test_case['expected']}")
        
        try:
            # Create the same request the frontend would send
            request = AnalysisRequest(
                input_type=InputType.TEXT,
                content=test_case['input'],
                ip_address="127.0.0.1",
                user_agent="Test Browser"
            )
            
            # Process through the analysis service (same as the API endpoint)
            result = await analysis_service.analyze_input(request)
            
            # Display results
            status = "MALICIOUS" if result.is_malicious else "SAFE"
            confidence = result.confidence_score * 100
            
            print(f"Result: {status} (Confidence: {confidence:.1f}%)")
            print(f"Threat Level: {result.threat_level}")
            
            if result.detected_threats:
                print(f"Threats Detected: {len(result.detected_threats)}")
                for threat in result.detected_threats:
                    print(f"  - {threat.attack_type}: {threat.description}")
            else:
                print("No threats detected")
            
            print(f"Processing Time: {result.processing_time_ms:.2f}ms")
            print()
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_end_to_end())