#!/usr/bin/env python3
"""
Test script for SQL injection detection integration.
This script tests the enhanced SQL injection detector with and without the ML model.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.services.sql_injection_detector import sql_injection_detector


def test_sql_injection_detection():
    """Test the SQL injection detection with various inputs."""
    print("="*80)
    print("🧪 TESTING ENHANCED SQL INJECTION DETECTION")
    print("="*80)
    
    # Test cases with expected results
    test_cases = [
        # Safe queries
        ("SELECT * FROM users WHERE id = 1", "SAFE"),
        ("UPDATE products SET price = 29.99 WHERE id = 5", "SAFE"),
        ("INSERT INTO logs (message) VALUES ('User login')", "SAFE"),
        
        # Malicious queries
        ("SELECT * FROM users WHERE id = 1 OR 1=1", "MALICIOUS"),
        ("'; DROP TABLE users; --", "MALICIOUS"),
        ("SELECT * FROM users UNION SELECT username, password FROM admin", "MALICIOUS"),
        ("SELECT * FROM users WHERE id = 1'; exec('xp_cmdshell')", "MALICIOUS"),
        ("1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 --", "MALICIOUS"),
    ]
    
    print(f"🔍 Testing {len(test_cases)} queries...\n")
    
    correct_predictions = 0
    total_predictions = len(test_cases)
    
    for i, (query, expected) in enumerate(test_cases, 1):
        print(f"Test {i:2d}: {query[:50]}")
        
        try:
            result = sql_injection_detector.predict(query)
            prediction = result['prediction']
            confidence = result['confidence']
            risk_score = result['risk_score']
            method = result.get('method', 'unknown')
            
            # Check if prediction is correct
            is_correct = prediction == expected
            if is_correct:
                correct_predictions += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"        Result: {status} {prediction} (Expected: {expected})")
            print(f"        Confidence: {confidence:.2f}, Risk Score: {risk_score}")
            print(f"        Method: {method}")
            
            if result.get('indicators'):
                print(f"        Indicators: {len(result['indicators'])} detected")
                for indicator in result['indicators'][:3]:  # Show first 3
                    print(f"          - {indicator}")
            
            print()
            
        except Exception as e:
            print(f"        ERROR: {str(e)}")
            print()
    
    # Calculate accuracy
    accuracy = correct_predictions / total_predictions
    print("="*80)
    print("📊 TEST RESULTS")
    print("="*80)
    print(f"Correct Predictions: {correct_predictions}/{total_predictions}")
    print(f"Accuracy: {accuracy:.1%}")
    print()
    
    # Test model status
    print("🤖 MODEL STATUS")
    print("="*80)
    print(f"Model Loaded: {'✅ Yes' if sql_injection_detector.model_loaded else '❌ No (using fallback)'}")
    if hasattr(sql_injection_detector, 'model_accuracy'):
        print(f"Model Accuracy: {sql_injection_detector.model_accuracy:.1%}")
    print()
    
    return accuracy


def test_feature_extraction():
    """Test the feature extraction functionality."""
    print("🔧 TESTING FEATURE EXTRACTION")
    print("="*80)
    
    test_query = "SELECT * FROM users WHERE id = 1 OR 1=1"
    
    try:
        features = sql_injection_detector.enhanced_feature_extraction([test_query])
        print(f"✅ Feature extraction successful")
        print(f"   Query: {test_query}")
        print(f"   Features extracted: {features.shape[1]} features")
        print(f"   Feature vector shape: {features.shape}")
        print(f"   Sample features: {features[0][:10].tolist()}")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Feature extraction failed: {str(e)}")
        print()
        return False


if __name__ == "__main__":
    print("🚀 SHIELD SQL INJECTION DETECTION - INTEGRATION TEST")
    print()
    
    # Test feature extraction
    feature_test_passed = test_feature_extraction()
    
    # Test SQL injection detection
    accuracy = test_sql_injection_detection()
    
    # Final summary
    print("🎯 FINAL SUMMARY")
    print("="*80)
    print(f"Feature Extraction: {'✅ PASS' if feature_test_passed else '❌ FAIL'}")
    print(f"Detection Accuracy: {accuracy:.1%}")
    print(f"Integration Status: {'✅ SUCCESS' if accuracy >= 0.5 else '❌ NEEDS IMPROVEMENT'}")
    print()
    
    if accuracy >= 0.7:
        print("🎉 EXCELLENT! The integration is working well!")
    elif accuracy >= 0.5:
        print("👍 GOOD! The integration is functional with room for improvement.")
    else:
        print("⚠️  ATTENTION NEEDED! The integration needs debugging.")
    
    print("\n" + "="*80)