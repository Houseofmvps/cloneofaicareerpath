#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class FocusedAITester:
    def __init__(self, base_url="https://careershift-app.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_result(self, test_name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED: {details}")
            self.failed_tests.append({"test": test_name, "error": details})

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=60)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=60)

            print(f"   Status: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.log_result(name, True)
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text[:200]}"
                self.log_result(name, False, error_msg)
                return False, {}

        except requests.exceptions.Timeout:
            self.log_result(name, False, "Request timeout (60s)")
            return False, {}
        except Exception as e:
            self.log_result(name, False, f"Request error: {str(e)}")
            return False, {}

    def register_user(self):
        """Register a new test user"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_user_data = {
            "name": f"AI Test User {timestamp}",
            "email": f"aitest{timestamp}@example.com",
            "password": "TestPass123!"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=test_user_data
        )
        
        if success:
            self.token = response.get('access_token')
            self.user_id = response.get('user', {}).get('id')
            print(f"   User ID: {self.user_id}")
            print(f"   Token received: {'Yes' if self.token else 'No'}")
        
        return success

    def test_cv_generation(self):
        """Test CV Generation with score consistency fix"""
        if not self.token:
            self.log_result("CV Generation", False, "No auth token available")
            return False
        
        cv_request = {
            "resume_text": """John Smith - Senior Software Engineer with 5+ years experience in Python, machine learning, and cloud technologies.

EXPERIENCE:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python, TensorFlow, and PyTorch serving 1M+ users
  - Developed REST APIs with FastAPI and Django handling 10K+ requests/second
  - Deployed models on AWS using Docker, Kubernetes, and SageMaker
  - Led team of 4 engineers on machine learning projects
  - Improved model accuracy by 25% through advanced feature engineering

• Software Engineer at DataCorp (2018-2020)
  - Developed data processing pipelines using Python, Spark, and Airflow
  - Built recommendation systems using collaborative filtering and deep learning
  - Optimized database queries reducing response time by 40%
  - Implemented CI/CD pipelines using Jenkins and Docker

EDUCATION:
Master's in Computer Science, Stanford University (2018)
Bachelor's in Software Engineering, UC Berkeley (2016)

SKILLS: Python, JavaScript, TensorFlow, PyTorch, AWS, Docker, Kubernetes, FastAPI, Django, SQL, MongoDB, Machine Learning, Deep Learning, MLOps, Git, Linux""",
            "target_role_id": "ml_engineer",
            "target_region": "us"
        }
        
        success, response = self.run_test(
            "CV Generation (POST /api/cv/generate)",
            "POST",
            "cv/generate",
            200,
            data=cv_request
        )
        
        if success:
            cv_id = response.get('cv_id', '')
            target_role = response.get('target_role', '')
            versions = response.get('versions', [])
            verified_analysis = response.get('verified_analysis', False)
            
            print(f"   CV ID: {cv_id}")
            print(f"   Target Role: {target_role}")
            print(f"   Versions: {len(versions)}")
            print(f"   Verified Analysis (shared function): {verified_analysis}")
            
            if versions:
                version = versions[0]
                ats_score = version.get('ats_score', 0)
                human_score = version.get('human_appeal_score', 0)
                print(f"   ATS Score: {ats_score}")
                print(f"   Human Appeal Score: {human_score}")
                
                # Store scores for consistency test
                self.cv_ats_score = ats_score
                self.cv_human_score = human_score
                self.cv_content = version.get('content', '')
        
        return success

    def test_resume_scanner(self):
        """Test Resume Scanner with same content as CV Generator"""
        if not self.token:
            self.log_result("Resume Scanner", False, "No auth token available")
            return False
        
        # Use the same resume text as CV generation for consistency test
        scan_request = {
            "resume_text": """John Smith - Senior Software Engineer with 5+ years experience in Python, machine learning, and cloud technologies.

EXPERIENCE:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python, TensorFlow, and PyTorch serving 1M+ users
  - Developed REST APIs with FastAPI and Django handling 10K+ requests/second
  - Deployed models on AWS using Docker, Kubernetes, and SageMaker
  - Led team of 4 engineers on machine learning projects
  - Improved model accuracy by 25% through advanced feature engineering

• Software Engineer at DataCorp (2018-2020)
  - Developed data processing pipelines using Python, Spark, and Airflow
  - Built recommendation systems using collaborative filtering and deep learning
  - Optimized database queries reducing response time by 40%
  - Implemented CI/CD pipelines using Jenkins and Docker

EDUCATION:
Master's in Computer Science, Stanford University (2018)
Bachelor's in Software Engineering, UC Berkeley (2016)

SKILLS: Python, JavaScript, TensorFlow, PyTorch, AWS, Docker, Kubernetes, FastAPI, Django, SQL, MongoDB, Machine Learning, Deep Learning, MLOps, Git, Linux""",
            "target_role_id": "ml_engineer"
        }
        
        success, response = self.run_test(
            "Resume Scanner (POST /api/resume/scan)",
            "POST",
            "resume/scan",
            200,
            data=scan_request
        )
        
        if success:
            ats_score = response.get('ats_score', 0)
            human_score = response.get('human_appeal_score', 0)
            overall_grade = response.get('overall_grade', '')
            keywords_found = response.get('keywords_found', [])
            quick_wins = response.get('quick_wins', [])
            
            print(f"   ATS Score: {ats_score}")
            print(f"   Human Appeal Score: {human_score}")
            print(f"   Overall Grade: {overall_grade}")
            print(f"   Keywords Found: {len(keywords_found)}")
            print(f"   Quick Wins: {len(quick_wins)}")
            
            # Store scores for consistency check
            self.scanner_ats_score = ats_score
            self.scanner_human_score = human_score
        
        return success

    def test_score_consistency(self):
        """Test that CV Generator and Resume Scanner return consistent scores"""
        if not hasattr(self, 'cv_ats_score') or not hasattr(self, 'scanner_ats_score'):
            self.log_result("Score Consistency Check", False, "Missing scores from previous tests")
            return False
        
        print(f"\n🎯 SCORE CONSISTENCY CHECK:")
        print(f"   CV Generator    - ATS: {self.cv_ats_score}, Human: {self.cv_human_score}")
        print(f"   Resume Scanner  - ATS: {self.scanner_ats_score}, Human: {self.scanner_human_score}")
        
        ats_diff = abs(self.cv_ats_score - self.scanner_ats_score)
        human_diff = abs(self.cv_human_score - self.scanner_human_score)
        
        print(f"   Differences     - ATS: {ats_diff}, Human: {human_diff}")
        
        # Allow small tolerance for AI variance
        tolerance = 2
        
        if ats_diff <= tolerance and human_diff <= tolerance:
            self.log_result("Score Consistency Check", True)
            print(f"   ✅ Scores are consistent (within {tolerance} point tolerance)")
            return True
        else:
            self.log_result("Score Consistency Check", False, f"Scores differ by more than {tolerance} points")
            return False

    def test_learning_path_generation(self):
        """Test Learning Path Generation with target_role_id"""
        if not self.token:
            self.log_result("Learning Path Generation", False, "No auth token available")
            return False
        
        learning_request = {
            "current_role": "Software Engineer",
            "years_experience": 3,
            "current_skills": ["Python", "JavaScript", "SQL"],
            "target_role_id": "ml_engineer",
            "location": "US"
        }
        
        success, response = self.run_test(
            "Learning Path Generation (POST /api/learning-path/generate)",
            "POST",
            "learning-path/generate",
            200,
            data=learning_request
        )
        
        if success:
            path_id = response.get('path_id', '')
            target_role = response.get('target_role', '')
            path_data = response.get('path_data', {}) or response.get('learning_path', {})
            
            print(f"   Path ID: {path_id}")
            print(f"   Target Role: {target_role}")
            
            if path_data:
                overview = path_data.get('path_overview', {})
                weeks = path_data.get('weeks', [])
                print(f"   Duration: {overview.get('duration_weeks', 0)} weeks")
                print(f"   Learning phases: {len(weeks)}")
        
        return success

    def test_cover_letter_generation(self):
        """Test Cover Letter Generation with claude-sonnet-4-20250514"""
        if not self.token:
            self.log_result("Cover Letter Generation", False, "No auth token available")
            return False
        
        cover_letter_request = {
            "resume_text": """John Smith - Senior Software Engineer with 5+ years experience in Python, machine learning, and cloud technologies.

EXPERIENCE:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python, TensorFlow, and PyTorch serving 1M+ users
  - Developed REST APIs with FastAPI and Django handling 10K+ requests/second
  - Deployed models on AWS using Docker, Kubernetes, and SageMaker
  - Led team of 4 engineers on machine learning projects

EDUCATION:
Master's in Computer Science, Stanford University (2018)

SKILLS: Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes, FastAPI, Machine Learning, Deep Learning""",
            "job_description": """We are seeking a Senior ML Engineer to join our AI team. You will work on cutting-edge machine learning models and help scale our infrastructure.

Requirements:
- 5+ years experience in machine learning
- Strong Python programming skills
- Experience with TensorFlow/PyTorch
- Cloud platform experience (AWS/GCP/Azure)
- Experience with large-scale ML systems

Responsibilities:
- Design and implement ML models
- Optimize model performance and scalability
- Build robust ML infrastructure and pipelines""",
            "company_name": "TechCorp AI",
            "target_role": "Senior ML Engineer"
        }
        
        success, response = self.run_test(
            "Cover Letter Generation (POST /api/cover-letter/generate)",
            "POST",
            "cover-letter/generate",
            200,
            data=cover_letter_request
        )
        
        if success:
            cover_letter_id = response.get('cover_letter_id', '')
            company_name = response.get('company_name', '')
            target_role = response.get('target_role', '')
            versions = response.get('versions', [])
            
            print(f"   Cover Letter ID: {cover_letter_id}")
            print(f"   Company: {company_name}")
            print(f"   Target Role: {target_role}")
            print(f"   Versions: {len(versions)}")
            
            if versions:
                version = versions[0]
                content = version.get('cover_letter', '')
                print(f"   Content Length: {len(content)} characters")
                
                # Check if content mentions company and role
                if "TechCorp" in content and "ML Engineer" in content:
                    print(f"   ✅ Content is personalized")
                else:
                    print(f"   ⚠️ Content may not be properly personalized")
        
        return success

    def test_career_analysis(self):
        """Test Career Analysis endpoint at /api/analyze"""
        if not self.token:
            self.log_result("Career Analysis", False, "No auth token available")
            return False
        
        analysis_request = {
            "resume_data": {
                "raw_text": """John Smith - Senior Software Engineer with 5+ years experience in Python, machine learning, and cloud technologies.

EXPERIENCE:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python, TensorFlow, and PyTorch serving 1M+ users
  - Developed REST APIs with FastAPI and Django handling 10K+ requests/second
  - Deployed models on AWS using Docker, Kubernetes, and SageMaker

EDUCATION:
Master's in Computer Science, Stanford University (2018)

SKILLS: Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes, FastAPI, Machine Learning""",
                "current_role": "Software Engineer",
                "years_experience": 5,
                "education": "Master's in Computer Science",
                "skills": ["Python", "TensorFlow", "PyTorch", "AWS", "Docker", "Machine Learning"],
                "certifications": [],
                "companies": ["TechCorp"]
            },
            "target_role_id": "ml_engineer",
            "background_context": {
                "current_role": "Software Engineer",
                "years_experience": 5,
                "education_level": "Master's",
                "primary_skills": ["Python", "Machine Learning", "TensorFlow"],
                "career_goals": "Transition to ML Engineer role",
                "location": "US"
            }
        }
        
        success, response = self.run_test(
            "Career Analysis (POST /api/analyze)",
            "POST",
            "analyze",
            200,
            data=analysis_request
        )
        
        if success:
            analysis_id = response.get('analysis_id', '')
            target_role = response.get('target_role', {})
            analysis = response.get('analysis', {})
            
            print(f"   Analysis ID: {analysis_id}")
            print(f"   Target Role: {target_role.get('name', 'N/A')}")
            
            if analysis:
                career_fit = analysis.get('career_fit', {})
                ats_score = analysis.get('ats_score', {})
                print(f"   Career Fit Score: {career_fit.get('score', 0)}/100")
                print(f"   Career Fit Rating: {career_fit.get('rating', 'N/A')}")
                print(f"   ATS Score: {ats_score.get('score', 0)}/100")
        
        return success

    def run_all_tests(self):
        """Run all focused AI feature tests"""
        print("🚀 FOCUSED AI FEATURES TEST")
        print("=" * 50)
        
        # Register user
        if not self.register_user():
            print("❌ Failed to register user, cannot continue")
            return
        
        # Test all AI features
        print(f"\n📋 Testing AI Features:")
        
        # 1. CV Generation
        cv_success = self.test_cv_generation()
        
        # 2. Resume Scanner  
        scanner_success = self.test_resume_scanner()
        
        # 3. Score Consistency Check
        if cv_success and scanner_success:
            self.test_score_consistency()
        
        # 4. Learning Path Generation
        self.test_learning_path_generation()
        
        # 5. Cover Letter Generation
        self.test_cover_letter_generation()
        
        # 6. Career Analysis
        self.test_career_analysis()
        
        # Print summary
        print(f"\n" + "=" * 50)
        print(f"📊 TEST SUMMARY")
        print(f"=" * 50)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {len(self.failed_tests)}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"   • {test['test']}: {test['error']}")
        else:
            print(f"\n✅ ALL TESTS PASSED!")

if __name__ == "__main__":
    tester = FocusedAITester()
    tester.run_all_tests()