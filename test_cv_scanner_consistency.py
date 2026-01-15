#!/usr/bin/env python3

import requests
import json
import sys

class CVScannerConsistencyTester:
    def __init__(self, base_url="https://careershift-app.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None

    def login(self):
        """Login with scanner credentials"""
        login_data = {"email": "scanner@test.com", "password": "test123"}
        response = requests.post(f"{self.base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            self.token = response.json()['access_token']
            print("✅ Login successful")
            return True
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False

    def test_cv_scanner_consistency(self):
        """Test CV-Scanner Score Consistency"""
        if not self.token:
            print("❌ No authentication token")
            return False

        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        
        print("\n🎯 TESTING CV-SCANNER SCORE CONSISTENCY")
        print("=" * 60)
        
        # Sample resume text from review request
        sample_resume_text = """John Doe - Senior ML Engineer with 5+ years experience. Python expert with TensorFlow, PyTorch, AWS, Docker. Built recommendation systems serving 10M daily users. Led team of 4 engineers. MS CS Stanford.

EXPERIENCE:
• Senior ML Engineer at Netflix (2020-2024)
  - Built recommendation algorithms using Python, TensorFlow, and PyTorch serving 200M+ users
  - Deployed ML models on AWS SageMaker reducing inference latency by 40%
  - Led team of 4 engineers developing real-time personalization systems
  - Improved user engagement by 25% through advanced deep learning techniques

• ML Engineer at Google (2018-2020)
  - Developed computer vision models using PyTorch and OpenCV for image classification
  - Implemented MLOps pipelines with Docker, Kubernetes, and Airflow
  - Optimized model performance achieving 95% accuracy on production datasets
  - Collaborated with product teams on AI-powered features

EDUCATION:
MS Computer Science, Stanford University (2018)
BS Software Engineering, UC Berkeley (2016)

SKILLS: Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes, MLOps, Computer Vision, NLP, SQL, Spark, Git, Linux"""
        
        target_role_id = "ml_engineer"
        
        # Step 1: Generate CV
        print("\n1️⃣ STEP 1: Generate CV using CV Generator")
        cv_request = {
            "resume_text": sample_resume_text,
            "target_role_id": target_role_id,
            "target_region": "us",
            "region_name": "United States",
            "tier": 1,
            "experience_level": "senior",
            "experience_years": 5
        }
        
        cv_response = requests.post(f"{self.base_url}/cv/generate", json=cv_request, headers=headers, timeout=60)
        print(f"CV Generation Status: {cv_response.status_code}")
        
        if cv_response.status_code != 200:
            print(f"❌ CV Generation failed: {cv_response.text}")
            return False
        
        cv_data = cv_response.json()
        versions = cv_data.get('versions', [])
        if not versions:
            print("❌ No CV versions returned")
            return False
        
        cv_version = versions[0]
        cv_content = cv_version.get('content', '')
        cv_ats_score = cv_version.get('ats_score', 0)
        cv_human_appeal_score = cv_version.get('human_appeal_score', 0)
        
        print(f"✅ CV Generated Successfully")
        print(f"   CV ATS Score: {cv_ats_score}")
        print(f"   CV Human Appeal Score: {cv_human_appeal_score}")
        print(f"   CV Content Length: {len(cv_content)} chars")
        print(f"   Model Used: claude-sonnet-4-20250514 (expected)")
        
        # Check if verified_analysis is present
        verified_analysis = cv_data.get('verified_analysis', {})
        if verified_analysis:
            print(f"   ✅ Verified analysis present (shared function used)")
            print(f"   Verified ATS: {verified_analysis.get('ats_score', 'N/A')}")
            print(f"   Verified Human: {verified_analysis.get('human_appeal_score', 'N/A')}")
        else:
            print(f"   ⚠️  No verified analysis found")
        
        if not cv_content:
            print("❌ CV content is empty")
            return False
        
        # Step 2: Scan the SAME content using Resume Scanner
        print("\n2️⃣ STEP 2: Scan the SAME content using Resume Scanner")
        scan_request = {
            "resume_text": cv_content,  # Use EXACT content from CV Generator
            "target_role_id": target_role_id
        }
        
        scan_response = requests.post(f"{self.base_url}/resume/scan", json=scan_request, headers=headers, timeout=60)
        print(f"Resume Scanner Status: {scan_response.status_code}")
        
        if scan_response.status_code != 200:
            print(f"❌ Resume Scanner failed: {scan_response.text}")
            return False
        
        scan_data = scan_response.json()
        scanner_ats_score = scan_data.get('ats_score', 0)
        scanner_human_appeal_score = scan_data.get('human_appeal_score', 0)
        
        print(f"✅ Resume Scanned Successfully")
        print(f"   Scanner ATS Score: {scanner_ats_score}")
        print(f"   Scanner Human Appeal Score: {scanner_human_appeal_score}")
        print(f"   Model Used: claude-3-5-haiku-20241022 (expected)")
        
        # Step 3: Compare scores for consistency
        print("\n3️⃣ STEP 3: Compare Scores for Consistency")
        print("=" * 50)
        
        ats_difference = abs(cv_ats_score - scanner_ats_score)
        human_difference = abs(cv_human_appeal_score - scanner_human_appeal_score)
        
        print(f"CV Generator    - ATS: {cv_ats_score:3d}, Human: {cv_human_appeal_score:3d}")
        print(f"Resume Scanner  - ATS: {scanner_ats_score:3d}, Human: {scanner_human_appeal_score:3d}")
        print(f"Differences     - ATS: {ats_difference:3d}, Human: {human_difference:3d}")
        
        # Tolerance for AI variance (should be very small or zero if using shared function)
        tolerance = 2  # Allow up to 2 points difference due to AI variance
        
        consistency_passed = True
        issues = []
        
        if ats_difference > tolerance:
            consistency_passed = False
            issues.append(f"ATS score difference too large: {ats_difference} points")
        
        if human_difference > tolerance:
            consistency_passed = False
            issues.append(f"Human Appeal score difference too large: {human_difference} points")
        
        # Step 4: Final result
        print("\n🏁 FINAL RESULT:")
        print("=" * 50)
        
        if consistency_passed:
            print("✅ SCORE CONSISTENCY TEST PASSED!")
            print(f"   Both CV Generator and Resume Scanner return consistent scores")
            print(f"   ATS difference: {ats_difference} points (within {tolerance} tolerance)")
            print(f"   Human Appeal difference: {human_difference} points (within {tolerance} tolerance)")
            
            # Additional validation
            if ats_difference == 0 and human_difference == 0:
                print("   🎯 PERFECT CONSISTENCY: Scores are identical!")
            elif ats_difference <= 1 and human_difference <= 1:
                print("   🎯 EXCELLENT CONSISTENCY: Minimal variance (≤1 point)")
            
            return True
        else:
            print("❌ SCORE CONSISTENCY TEST FAILED!")
            for issue in issues:
                print(f"   • {issue}")
            
            print("\n🔍 DEBUGGING INFO:")
            print(f"   CV Generator uses shared analysis: {'Yes' if verified_analysis else 'No'}")
            print(f"   Expected: Both should use analyze_resume_for_role() function")
            print(f"   CV Model: claude-sonnet-4-20250514")
            print(f"   Scanner Model: claude-3-5-haiku-20241022")
            
            return False

def main():
    tester = CVScannerConsistencyTester()
    
    if not tester.login():
        sys.exit(1)
    
    success = tester.test_cv_scanner_consistency()
    
    if success:
        print("\n🎉 CV-SCANNER SCORE CONSISTENCY TEST COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n💥 CV-SCANNER SCORE CONSISTENCY TEST FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()