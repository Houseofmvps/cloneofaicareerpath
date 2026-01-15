#!/usr/bin/env python3

import requests
import json
from datetime import datetime

class QuickAPITest:
    def __init__(self, base_url="https://careershift-app.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None

    def register_fresh_user(self):
        """Register a fresh user to avoid usage limits"""
        timestamp = datetime.now().strftime('%H%M%S')
        user_data = {
            "name": f"Test User {timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "TestPass123!"
        }
        
        response = requests.post(f"{self.base_url}/auth/register", json=user_data, timeout=30)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('access_token')
            print(f"✅ Registered fresh user: {user_data['email']}")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False

    def test_critical_features(self):
        """Test the critical features mentioned in review request"""
        if not self.token:
            print("❌ No auth token available")
            return False

        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        
        print("\n🎯 Testing Critical AI Features:")
        
        # 1. CV Generation (Superior Hybrid Resume)
        print("\n1️⃣ CV Generation (Superior Hybrid Resume)")
        cv_request = {
            "resume_text": """John Doe
Senior Software Engineer with 5 years experience

Experience:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python and TensorFlow
  - Developed REST APIs with FastAPI and Django
  - Worked with AWS cloud services including EC2, S3, and Lambda
  - Led a team of 3 developers on machine learning projects

Education:
Bachelor's degree in Computer Science from State University

Skills: Python, JavaScript, React, SQL, Docker, Kubernetes, Machine Learning, TensorFlow, PyTorch, AWS, FastAPI, Django""",
            "target_role_id": "ml_engineer",
            "region": "us"
        }
        
        try:
            response = requests.post(f"{self.base_url}/cv/generate", json=cv_request, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ CV Generated - ID: {data.get('cv_id', 'N/A')}")
                print(f"   ✅ Target Role: {data.get('target_role', 'N/A')}")
                print(f"   ✅ Versions: {len(data.get('versions', []))}")
            else:
                print(f"   ❌ CV Generation failed: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ CV Generation error: {str(e)}")

        # 2. Resume Scanner
        print("\n2️⃣ Resume Scanner (ATS Analysis)")
        scan_request = {
            "resume_text": """Sarah Johnson
Senior Software Engineer

Experience:
• Senior Software Engineer at Microsoft (2020-2024)
  - Led development of cloud-based ML solutions using Python and Azure
  - Built scalable APIs serving 1M+ requests daily using FastAPI
  - Implemented CI/CD pipelines reducing deployment time by 60%

Skills: Python, JavaScript, React, TensorFlow, PyTorch, AWS, Azure, Docker, Kubernetes, Machine Learning""",
            "target_role_id": "ai_ml_engineer"
        }
        
        try:
            response = requests.post(f"{self.base_url}/resume/scan", json=scan_request, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Resume Scanned - ATS Score: {data.get('ats_score', 0)}/100")
                print(f"   ✅ Human Appeal: {data.get('human_appeal_score', 0)}/100")
                print(f"   ✅ Overall Grade: {data.get('overall_grade', 'N/A')}")
            else:
                print(f"   ❌ Resume Scanner failed: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Resume Scanner error: {str(e)}")

        # 3. Interview Prep (Haiku for questions)
        print("\n3️⃣ Interview Prep (Question Generation with Haiku)")
        question_request = {
            "role_id": "ml_engineer",
            "categories": ["technical", "behavioral"],
            "count": 5
        }
        
        try:
            response = requests.post(f"{self.base_url}/interview-prep/generate", json=question_request, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                questions = data.get('questions', [])
                print(f"   ✅ Questions Generated: {len(questions)}")
                print(f"   ✅ Category Breakdown: {data.get('category_breakdown', {})}")
            else:
                print(f"   ❌ Question Generation failed: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Question Generation error: {str(e)}")

        # 4. Interview Feedback (Sonnet)
        print("\n4️⃣ Interview Feedback (Sonnet)")
        feedback_request = {
            "question": "Explain the bias-variance tradeoff in machine learning",
            "answer": "The bias-variance tradeoff is about balancing model complexity. High bias means underfitting, high variance means overfitting. We use techniques like cross-validation to find the right balance.",
            "role_id": "ml_engineer",
            "category": "technical"
        }
        
        try:
            response = requests.post(f"{self.base_url}/interview-prep/feedback", json=feedback_request, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Feedback Generated - Score: {data.get('score', 0)}/100")
                print(f"   ✅ Strengths: {len(data.get('strengths', []))}")
                print(f"   ✅ Improvements: {len(data.get('improvements', []))}")
            else:
                print(f"   ❌ Interview Feedback failed: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Interview Feedback error: {str(e)}")

        print("\n✅ Critical feature testing completed!")
        return True

def main():
    tester = QuickAPITest()
    
    print("🚀 Quick Test of Critical AI Features After Model Fix")
    print("=" * 60)
    
    if tester.register_fresh_user():
        tester.test_critical_features()
    else:
        print("❌ Could not register fresh user for testing")

if __name__ == "__main__":
    main()