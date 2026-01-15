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

    def test_multiple_resumes(self):
        """Test CV-Scanner Score Consistency with multiple resume samples"""
        if not self.token:
            print("❌ No authentication token")
            return False

        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        
        # Test cases with different resume samples
        test_cases = [
            {
                "name": "Senior ML Engineer Resume",
                "resume_text": """John Doe - Senior ML Engineer with 5+ years experience. Python expert with TensorFlow, PyTorch, AWS, Docker. Built recommendation systems serving 10M daily users. Led team of 4 engineers. MS CS Stanford.

EXPERIENCE:
• Senior ML Engineer at Netflix (2020-2024)
  - Built recommendation algorithms using Python, TensorFlow, and PyTorch serving 200M+ users
  - Deployed ML models on AWS SageMaker reducing inference latency by 40%
  - Led team of 4 engineers developing real-time personalization systems
  - Improved user engagement by 25% through advanced deep learning techniques

EDUCATION:
MS Computer Science, Stanford University (2018)

SKILLS: Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes, MLOps, Computer Vision, NLP, SQL, Spark, Git, Linux""",
                "target_role_id": "ml_engineer"
            },
            {
                "name": "Data Scientist Resume",
                "resume_text": """Sarah Johnson - Data Scientist with 4 years experience in machine learning and analytics.

EXPERIENCE:
• Data Scientist at Microsoft (2021-2024)
  - Developed predictive models using Python, scikit-learn, and pandas
  - Built data pipelines processing 1TB+ daily using Apache Spark
  - Created dashboards in Tableau reducing reporting time by 60%
  - Collaborated with product teams on A/B testing frameworks

• Junior Data Analyst at Spotify (2020-2021)
  - Analyzed user behavior data using SQL and Python
  - Built recommendation algorithms improving user retention by 15%

EDUCATION:
BS Statistics, UC Berkeley (2020)

SKILLS: Python, R, SQL, scikit-learn, pandas, Tableau, Spark, Statistics, Machine Learning""",
                "target_role_id": "data_scientist"
            }
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*80}")
            print(f"🧪 TEST CASE {i}: {test_case['name']}")
            print(f"{'='*80}")
            
            # Step 1: Generate CV
            print(f"\n1️⃣ STEP 1: Generate CV")
            cv_request = {
                "resume_text": test_case["resume_text"],
                "target_role_id": test_case["target_role_id"],
                "target_region": "us",
                "region_name": "United States",
                "tier": 1,
                "experience_level": "senior",
                "experience_years": 5
            }
            
            cv_response = requests.post(f"{self.base_url}/cv/generate", json=cv_request, headers=headers, timeout=60)
            
            if cv_response.status_code != 200:
                print(f"❌ CV Generation failed: {cv_response.text}")
                all_passed = False
                continue
            
            cv_data = cv_response.json()
            versions = cv_data.get('versions', [])
            if not versions:
                print("❌ No CV versions returned")
                all_passed = False
                continue
            
            cv_version = versions[0]
            cv_content = cv_version.get('content', '')
            cv_ats_score = cv_version.get('ats_score', 0)
            cv_human_appeal_score = cv_version.get('human_appeal_score', 0)
            
            print(f"✅ CV Generated - ATS: {cv_ats_score}, Human: {cv_human_appeal_score}")
            
            # Step 2: Scan the SAME content
            print(f"\n2️⃣ STEP 2: Scan the SAME content")
            scan_request = {
                "resume_text": cv_content,
                "target_role_id": test_case["target_role_id"]
            }
            
            scan_response = requests.post(f"{self.base_url}/resume/scan", json=scan_request, headers=headers, timeout=60)
            
            if scan_response.status_code != 200:
                print(f"❌ Resume Scanner failed: {scan_response.text}")
                all_passed = False
                continue
            
            scan_data = scan_response.json()
            scanner_ats_score = scan_data.get('ats_score', 0)
            scanner_human_appeal_score = scan_data.get('human_appeal_score', 0)
            
            print(f"✅ Resume Scanned - ATS: {scanner_ats_score}, Human: {scanner_human_appeal_score}")
            
            # Step 3: Compare scores
            print(f"\n3️⃣ STEP 3: Compare Scores")
            ats_difference = abs(cv_ats_score - scanner_ats_score)
            human_difference = abs(cv_human_appeal_score - scanner_human_appeal_score)
            
            print(f"CV Generator    - ATS: {cv_ats_score:3d}, Human: {cv_human_appeal_score:3d}")
            print(f"Resume Scanner  - ATS: {scanner_ats_score:3d}, Human: {scanner_human_appeal_score:3d}")
            print(f"Differences     - ATS: {ats_difference:3d}, Human: {human_difference:3d}")
            
            # Check consistency (tolerance of 2 points)
            tolerance = 2
            if ats_difference <= tolerance and human_difference <= tolerance:
                if ats_difference == 0 and human_difference == 0:
                    print("✅ PERFECT CONSISTENCY: Scores are identical!")
                else:
                    print(f"✅ GOOD CONSISTENCY: Within {tolerance} point tolerance")
            else:
                print(f"❌ INCONSISTENT: Differences exceed {tolerance} point tolerance")
                all_passed = False
        
        return all_passed

def main():
    tester = CVScannerConsistencyTester()
    
    if not tester.login():
        sys.exit(1)
    
    success = tester.test_multiple_resumes()
    
    print(f"\n{'='*80}")
    print("🏁 FINAL RESULTS")
    print(f"{'='*80}")
    
    if success:
        print("🎉 ALL CV-SCANNER SCORE CONSISTENCY TESTS PASSED!")
        print("✅ CV Generator and Resume Scanner return consistent scores")
        print("✅ Shared analysis function (analyze_resume_for_role) working correctly")
        print("✅ Both endpoints use the same scoring logic")
        sys.exit(0)
    else:
        print("💥 SOME CV-SCANNER SCORE CONSISTENCY TESTS FAILED!")
        print("❌ Score inconsistencies detected")
        sys.exit(1)

if __name__ == "__main__":
    main()