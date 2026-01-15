#!/usr/bin/env python3

import requests
import json
from datetime import datetime

class ComprehensiveTest:
    def __init__(self, base_url="https://careershift-app.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.results = {}

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

    def test_feature(self, name, endpoint, method, data=None, timeout=60):
        """Generic test method"""
        if not self.token:
            self.results[name] = {"status": "❌", "error": "No auth token"}
            return False

        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        
        try:
            if method == "POST":
                response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers=headers, timeout=timeout)
            else:
                response = requests.get(f"{self.base_url}/{endpoint}", headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                self.results[name] = {"status": "✅", "data": response.json()}
                return True
            else:
                self.results[name] = {"status": "❌", "error": f"{response.status_code}: {response.text[:200]}"}
                return False
        except Exception as e:
            self.results[name] = {"status": "❌", "error": f"Exception: {str(e)}"}
            return False

    def run_comprehensive_test(self):
        """Test all critical features mentioned in review request"""
        print("\n🎯 COMPREHENSIVE TESTING OF CRITICAL AI FEATURES")
        print("=" * 60)
        
        # 1. CV Generation (Superior Hybrid Resume)
        print("\n1️⃣ CV Generation (Superior Hybrid Resume)")
        cv_data = {
            "resume_text": """John Doe
Senior Software Engineer with 5 years experience in machine learning

Experience:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python and TensorFlow
  - Developed REST APIs with FastAPI and Django
  - Worked with AWS cloud services including EC2, S3, and Lambda
  - Led a team of 3 developers on machine learning projects
  - Implemented CI/CD pipelines reducing deployment time by 60%

• Software Engineer at StartupCorp (2018-2020)
  - Developed recommendation systems using collaborative filtering
  - Optimized database queries improving performance by 40%
  - Built real-time data processing pipelines

Education:
Bachelor's degree in Computer Science from State University

Skills: Python, JavaScript, React, SQL, Docker, Kubernetes, Machine Learning, TensorFlow, PyTorch, AWS, FastAPI, Django, Scikit-learn, Pandas, NumPy""",
            "target_role_id": "ml_engineer",
            "region": "us"
        }
        
        success = self.test_feature("CV Generation", "cv/generate", "POST", cv_data, 90)
        if success:
            data = self.results["CV Generation"]["data"]
            print(f"   ✅ CV Generated - ID: {data.get('cv_id', 'N/A')}")
            print(f"   ✅ Target Role: {data.get('target_role', 'N/A')}")
            print(f"   ✅ Versions: {len(data.get('versions', []))}")
            if data.get('versions'):
                version = data['versions'][0]
                print(f"   ✅ Version Type: {version.get('name', 'N/A')}")
        else:
            print(f"   ❌ CV Generation failed: {self.results['CV Generation']['error']}")

        # 2. Resume Scanner (ATS Analysis)
        print("\n2️⃣ Resume Scanner (ATS Analysis)")
        scan_data = {
            "resume_text": """Sarah Johnson
Senior Software Engineer

Experience:
• Senior Software Engineer at Microsoft (2020-2024)
  - Led development of cloud-based ML solutions using Python and Azure
  - Built scalable APIs serving 1M+ requests daily using FastAPI
  - Implemented CI/CD pipelines reducing deployment time by 60%
  - Mentored 5 junior developers on machine learning best practices

• Software Engineer at Google (2018-2020)
  - Developed recommendation systems using TensorFlow and PyTorch
  - Optimized database queries improving performance by 40%
  - Collaborated with cross-functional teams on AI product features

Education:
Master's in Computer Science, Stanford University (2018)
Bachelor's in Software Engineering, UC Berkeley (2016)

Skills: Python, JavaScript, React, Node.js, TensorFlow, PyTorch, AWS, Azure, Docker, Kubernetes, SQL, MongoDB, Machine Learning, Deep Learning, REST APIs, Microservices, Agile, Git""",
            "target_role_id": "ml_engineer"
        }
        
        success = self.test_feature("Resume Scanner", "resume/scan", "POST", scan_data, 90)
        if success:
            data = self.results["Resume Scanner"]["data"]
            print(f"   ✅ Resume Scanned - ATS Score: {data.get('ats_score', 0)}/100")
            print(f"   ✅ Human Appeal: {data.get('human_appeal_score', 0)}/100")
            print(f"   ✅ Overall Grade: {data.get('overall_grade', 'N/A')}")
            print(f"   ✅ Keywords Found: {len(data.get('keywords_found', []))}")
            print(f"   ✅ Quick Wins: {len(data.get('quick_wins', []))}")
        else:
            print(f"   ❌ Resume Scanner failed: {self.results['Resume Scanner']['error']}")

        # 3. Interview Prep - Question Generation (Haiku)
        print("\n3️⃣ Interview Prep - Question Generation (Haiku)")
        question_data = {
            "role_id": "ml_engineer",
            "categories": ["technical", "behavioral", "system_design"],
            "count": 10
        }
        
        success = self.test_feature("Interview Questions", "interview-prep/generate", "POST", question_data, 60)
        if success:
            data = self.results["Interview Questions"]["data"]
            questions = data.get('questions', [])
            print(f"   ✅ Questions Generated: {len(questions)}")
            print(f"   ✅ Category Breakdown: {data.get('category_breakdown', {})}")
            if questions:
                print(f"   ✅ Sample Question: {questions[0].get('question', 'N/A')[:100]}...")
        else:
            print(f"   ❌ Interview Questions failed: {self.results['Interview Questions']['error']}")

        # 4. Interview Prep - Feedback (Sonnet)
        print("\n4️⃣ Interview Prep - Feedback (Sonnet)")
        feedback_data = {
            "question": "Explain the bias-variance tradeoff in machine learning and how you would address high variance in a model",
            "answer": "The bias-variance tradeoff is a fundamental concept in machine learning. High bias leads to underfitting where the model is too simple to capture underlying patterns. High variance leads to overfitting where the model is too complex and captures noise. To address high variance, I would use techniques like regularization (L1/L2), cross-validation, ensemble methods like bagging, or collect more training data. I might also reduce model complexity or use dropout in neural networks.",
            "role_id": "ml_engineer",
            "category": "technical"
        }
        
        success = self.test_feature("Interview Feedback", "interview-prep/feedback", "POST", feedback_data, 60)
        if success:
            data = self.results["Interview Feedback"]["data"]
            print(f"   ✅ Feedback Generated - Score: {data.get('score', 0)}/100")
            print(f"   ✅ Strengths: {len(data.get('strengths', []))}")
            print(f"   ✅ Improvements: {len(data.get('improvements', []))}")
            print(f"   ✅ Sample Answer Provided: {'Yes' if data.get('sample_answer') else 'No'}")
        else:
            print(f"   ❌ Interview Feedback failed: {self.results['Interview Feedback']['error']}")

        # 5. Cover Letter Generation
        print("\n5️⃣ Cover Letter Generation")
        cover_letter_data = {
            "resume_text": """John Smith
Senior Data Scientist with 6 years experience in machine learning and AI

Experience:
• Senior Data Scientist at Netflix (2020-2024)
  - Built recommendation algorithms serving 200M+ users
  - Developed A/B testing frameworks for content optimization
  - Led ML model deployment using Python, TensorFlow, and AWS
  - Improved user engagement by 25% through personalization

• Data Scientist at Spotify (2018-2020)
  - Created music recommendation systems using collaborative filtering
  - Analyzed user behavior data to drive product decisions
  - Built real-time ML pipelines processing 1B+ events daily

Education:
PhD in Machine Learning, MIT (2018)
MS in Computer Science, Stanford (2016)

Skills: Python, R, TensorFlow, PyTorch, SQL, Spark, AWS, Docker, Statistics, Deep Learning""",
            "job_description": """We are seeking a Senior ML Engineer to join our AI team at OpenAI. You will work on cutting-edge language models and help scale our infrastructure to serve millions of users.

Requirements:
- 5+ years experience in machine learning
- Strong Python programming skills
- Experience with deep learning frameworks (TensorFlow, PyTorch)
- Cloud platform experience (AWS, GCP, Azure)
- Experience with large-scale ML systems

Responsibilities:
- Design and implement ML models for language understanding
- Optimize model performance and scalability
- Collaborate with research team on new AI capabilities
- Build robust ML infrastructure and pipelines""",
            "company_name": "OpenAI",
            "target_role": "Senior ML Engineer",
            "tone": "professional"
        }
        
        success = self.test_feature("Cover Letter", "cover-letter/generate", "POST", cover_letter_data, 90)
        if success:
            data = self.results["Cover Letter"]["data"]
            versions = data.get('versions', [])
            print(f"   ✅ Cover Letter Generated - ID: {data.get('cover_letter_id', 'N/A')}")
            print(f"   ✅ Company: {data.get('company_name', 'N/A')}")
            print(f"   ✅ Versions: {len(versions)}")
            if versions:
                version = versions[0]
                cover_letter_text = version.get('cover_letter', '')
                print(f"   ✅ Length: {len(cover_letter_text)} characters")
                print(f"   ✅ Tone: {version.get('tone_applied', 'N/A')}")
        else:
            print(f"   ❌ Cover Letter failed: {self.results['Cover Letter']['error']}")

        # 6. Learning Path Generation
        print("\n6️⃣ Learning Path Generation")
        learning_path_data = {
            "target_role": "Machine Learning Engineer",
            "current_skills": ["Python", "JavaScript", "React", "SQL", "Docker"],
            "experience_level": "intermediate",
            "available_hours_per_week": 15,
            "preferred_learning_style": "video",
            "budget": "moderate"
        }
        
        success = self.test_feature("Learning Path", "learning-path/generate", "POST", learning_path_data, 120)
        if success:
            data = self.results["Learning Path"]["data"]
            path_data = data.get('path_data', {})
            path_overview = path_data.get('path_overview', {})
            weeks = path_data.get('weeks', [])
            print(f"   ✅ Learning Path Generated - ID: {data.get('path_id', 'N/A')}")
            print(f"   ✅ Duration: {path_overview.get('duration_weeks', 0)} weeks")
            print(f"   ✅ Hours/week: {path_overview.get('hours_per_week', 0)}")
            print(f"   ✅ Learning phases: {len(weeks)}")
        else:
            print(f"   ❌ Learning Path failed: {self.results['Learning Path']['error']}")

        # 7. Career Analysis
        print("\n7️⃣ Career Analysis (Comprehensive)")
        analysis_data = {
            "resume_data": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0123",
                "education": [{"degree": "Bachelor's in Computer Science", "school": "State University"}],
                "experience": [
                    {
                        "title": "Software Engineer",
                        "company": "TechCorp",
                        "duration": "2020-2024",
                        "description": "Built ML pipelines using Python and TensorFlow"
                    }
                ],
                "skills": ["Python", "Machine Learning", "TensorFlow", "FastAPI", "AWS", "Docker"],
                "certifications": [],
                "summary": "Software Engineer with 5 years experience in machine learning"
            },
            "target_role_id": "ml_engineer",
            "background_context": {
                "years_in_current_field": 5,
                "current_industry": "Technology",
                "target_timeline_months": 6,
                "available_hours_per_week": 15,
                "learning_style": "mixed",
                "budget_for_learning": "moderate",
                "has_portfolio": True,
                "has_github": True,
                "willing_to_relocate": False,
                "preferred_company_size": "medium"
            }
        }
        
        success = self.test_feature("Career Analysis", "analysis/analyze", "POST", analysis_data, 120)
        if success:
            data = self.results["Career Analysis"]["data"]
            analysis = data.get('analysis', {})
            career_fit = analysis.get('career_fit', {})
            ats_score = analysis.get('ats_score', {})
            print(f"   ✅ Analysis Generated - ID: {data.get('analysis_id', 'N/A')}")
            print(f"   ✅ Career Fit Score: {career_fit.get('score', 0)}/100")
            print(f"   ✅ Career Fit Rating: {career_fit.get('rating', 'N/A')}")
            print(f"   ✅ ATS Score: {ats_score.get('score', 0)}/100")
            print(f"   ✅ Transferable Skills: {len(analysis.get('transferable_skills', []))}")
            print(f"   ✅ Skill Gaps: {len(analysis.get('skill_gaps', []))}")
        else:
            print(f"   ❌ Career Analysis failed: {self.results['Career Analysis']['error']}")

        # Summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result["status"] == "✅")
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🎯 CRITICAL AI FEATURES STATUS:")
        for feature, result in self.results.items():
            print(f"   {result['status']} {feature}")
            if result["status"] == "❌":
                print(f"      Error: {result['error']}")
        
        # Determine overall status
        critical_features = ["CV Generation", "Resume Scanner", "Interview Questions", "Interview Feedback"]
        critical_passed = sum(1 for feature in critical_features if self.results.get(feature, {}).get("status") == "✅")
        
        if critical_passed == len(critical_features):
            print(f"\n🎉 ALL CRITICAL AI FEATURES WORKING! ({critical_passed}/{len(critical_features)})")
        else:
            print(f"\n⚠️  SOME CRITICAL FEATURES NEED ATTENTION ({critical_passed}/{len(critical_features)})")
        
        return passed_tests == total_tests

def main():
    tester = ComprehensiveTest()
    
    print("🚀 COMPREHENSIVE BACKEND TEST - All Critical AI Features")
    print("Review Request: CV Generation, Resume Scanner, Interview Prep, Cover Letter, Learning Path, Career Analysis")
    print("Test Credentials: Fresh user registration to avoid usage limits")
    
    if tester.register_fresh_user():
        tester.run_comprehensive_test()
    else:
        print("❌ Could not register fresh user for testing")

if __name__ == "__main__":
    main()