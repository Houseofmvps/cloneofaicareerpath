#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class CareerLiftAPITester:
    def __init__(self, base_url="https://careershift-app.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.analysis_id = None

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
                response = requests.get(url, headers=test_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=30)

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
            self.log_result(name, False, "Request timeout (30s)")
            return False, {}
        except Exception as e:
            self.log_result(name, False, f"Request error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test API health endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        if success:
            print(f"   Claude configured: {response.get('claude_configured', False)}")
        return success

    def test_get_roles(self):
        """Test getting AI roles - Should return 21 roles after data extraction"""
        success, response = self.run_test(
            "Get AI Roles",
            "GET", 
            "roles",
            200
        )
        if success:
            roles = response.get('roles', [])
            print(f"   Found {len(roles)} roles")
            if len(roles) != 21:
                self.log_result("Roles Count Validation", False, f"Expected 21 roles, got {len(roles)}")
                return False
            else:
                self.log_result("Roles Count Validation", True)
        return success

    def test_register_user(self):
        """Test user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_user_data = {
            "name": f"Test User {timestamp}",
            "email": f"test{timestamp}@example.com",
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

    def test_login_user(self):
        """Test user login with existing credentials"""
        # Try to login with the registered user
        if not hasattr(self, 'test_email'):
            # Use a test account
            login_data = {
                "email": "test@example.com",
                "password": "TestPass123!"
            }
        else:
            login_data = {
                "email": self.test_email,
                "password": "TestPass123!"
            }
        
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login", 
            200,
            data=login_data
        )
        
        if success:
            self.token = response.get('access_token')
            self.user_id = response.get('user', {}).get('id')
        
        return success

    def test_get_me(self):
        """Test getting current user info"""
        if not self.token:
            self.log_result("Get Current User", False, "No auth token available")
            return False
            
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return success

    def test_resume_parse_text(self):
        """Test resume parsing with text"""
        sample_resume = """
        John Doe
        Software Engineer
        
        Experience:
        - 5 years of experience in Python development
        - Worked with machine learning frameworks like TensorFlow and PyTorch
        - Built REST APIs using FastAPI and Django
        - Experience with AWS cloud services
        
        Education:
        Bachelor's degree in Computer Science
        
        Skills: Python, JavaScript, React, SQL, Docker, Kubernetes, Machine Learning
        """
        
        # Test with form data (text)
        url = f"{self.base_url}/resume/parse"
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        form_data = {'text': sample_resume}
        
        try:
            response = requests.post(url, data=form_data, headers=headers, timeout=30)
            success = response.status_code == 200
            
            if success:
                self.log_result("Resume Parse (Text)", True)
                result = response.json()
                resume_data = result.get('resume_data', {})
                print(f"   Skills detected: {len(resume_data.get('skills', []))}")
                print(f"   Years experience: {resume_data.get('years_experience', 'Not detected')}")
                return True, result
            else:
                error_msg = f"Status {response.status_code}: {response.text[:200]}"
                self.log_result("Resume Parse (Text)", False, error_msg)
                return False, {}
                
        except Exception as e:
            self.log_result("Resume Parse (Text)", False, str(e))
            return False, {}

    def test_career_analysis(self):
        """Test career analysis endpoint"""
        if not self.token:
            self.log_result("Career Analysis", False, "No auth token available")
            return False
        
        # First get resume data
        resume_success, resume_response = self.test_resume_parse_text()
        if not resume_success:
            self.log_result("Career Analysis", False, "Resume parsing failed")
            return False
        
        resume_data = resume_response.get('resume_data', {})
        
        analysis_request = {
            "resume_data": resume_data,
            "target_role_id": "ai_ml_engineer",  # Use first role from the list
            "background_context": {
                "current_role": "Software Engineer",
                "years_experience": 5,
                "education_level": "Bachelor's in Computer Science",
                "primary_skills": ["Python", "Machine Learning", "FastAPI"],
                "career_goals": "Transition to AI/ML Engineer role"
            }
        }
        
        success, response = self.run_test(
            "Career Analysis",
            "POST",
            "analyze",
            200,
            data=analysis_request
        )
        
        if success:
            self.analysis_id = response.get('analysis_id')
            print(f"   Analysis ID: {self.analysis_id}")
            analysis_result = response.get('analysis', {})
            career_fit = analysis_result.get('career_fit', {})
            print(f"   Career fit score: {career_fit.get('score', 'N/A')}")
            print(f"   Career fit rating: {career_fit.get('rating', 'N/A')}")
        
        return success

    def test_get_analysis(self):
        """Test getting analysis by ID"""
        if not self.token or not self.analysis_id:
            self.log_result("Get Analysis", False, "No auth token or analysis ID available")
            return False
        
        success, response = self.run_test(
            "Get Analysis by ID",
            "GET",
            f"analyses/{self.analysis_id}",
            200
        )
        return success

    def test_get_analyses_list(self):
        """Test getting user's analyses list"""
        if not self.token:
            self.log_result("Get Analyses List", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get Analyses List",
            "GET",
            "analyses",
            200
        )
        
        if success:
            analyses = response.get('analyses', [])
            print(f"   Found {len(analyses)} analyses")
        
        return success

    def test_get_usage(self):
        """Test getting usage statistics"""
        if not self.token:
            self.log_result("Get Usage Stats", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get Usage Statistics",
            "GET",
            "usage",
            200
        )
        
        if success:
            print(f"   Analyses used: {response.get('analyses_used', 0)}/{response.get('analyses_limit', 0)}")
            print(f"   CV generations used: {response.get('cv_generations_used', 0)}/{response.get('cv_generations_limit', 0)}")
        
        return success

    def test_mock_upgrade(self):
        """Test mock upgrade endpoint"""
        if not self.token:
            self.log_result("Mock Upgrade", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Mock Upgrade to Pro",
            "POST",
            "payments/mock-upgrade",
            200
        )
        
        if success:
            print(f"   New subscription tier: {response.get('subscription_tier', 'N/A')}")
        
        return success

    def test_mock_checkout(self):
        """Test mock checkout endpoint"""
        if not self.token:
            self.log_result("Mock Checkout", False, "No auth token available")
            return False
        
        # Use query parameter instead of request body
        success, response = self.run_test(
            "Mock Checkout",
            "POST",
            "payments/checkout?product_type=pro_subscription",
            200
        )
        
        if success:
            print(f"   Checkout URL: {response.get('checkout_url', 'N/A')}")
        
        return success

    def test_interview_question_generation(self):
        """Test interview question generation endpoint (uses Haiku)"""
        if not self.token:
            self.log_result("Interview Question Generation", False, "No auth token available")
            return False
        
        # Test basic question generation
        request_data = {
            "role_id": "ml_engineer",
            "categories": ["technical", "behavioral", "system_design"],
            "count": 10
        }
        
        success, response = self.run_test(
            "Interview Question Generation (Basic)",
            "POST",
            "interview-prep/generate",
            200,
            data=request_data
        )
        
        if success:
            questions = response.get('questions', [])
            category_breakdown = response.get('category_breakdown', {})
            print(f"   Generated {len(questions)} questions")
            print(f"   Category breakdown: {category_breakdown}")
            
            # Validate response structure
            if len(questions) != 10:
                self.log_result("Question Count Validation", False, f"Expected 10 questions, got {len(questions)}")
                return False
            
            # Check if questions have required fields
            for i, q in enumerate(questions[:3]):  # Check first 3 questions
                required_fields = ['question', 'category', 'id']
                missing_fields = [field for field in required_fields if field not in q]
                if missing_fields:
                    self.log_result("Question Structure Validation", False, f"Question {i} missing fields: {missing_fields}")
                    return False
            
            self.log_result("Question Structure Validation", True)
        
        return success

    def test_interview_question_generation_with_company(self):
        """Test interview question generation with company context"""
        if not self.token:
            self.log_result("Interview Question Generation (Company)", False, "No auth token available")
            return False
        
        # Test with company-specific questions
        request_data = {
            "role_id": "ai_engineer",
            "categories": ["technical", "behavioral"],
            "count": 10,
            "company": "google"
        }
        
        success, response = self.run_test(
            "Interview Question Generation (Company-specific)",
            "POST",
            "interview-prep/generate",
            200,
            data=request_data
        )
        
        if success:
            questions = response.get('questions', [])
            print(f"   Generated {len(questions)} company-specific questions")
            
            # Check if any questions are company-specific
            company_questions = [q for q in questions if q.get('company') or q.get('source') == 'company']
            print(f"   Company-specific questions: {len(company_questions)}")
        
        return success

    def test_interview_feedback(self):
        """Test interview feedback endpoint (uses Sonnet - Premium)"""
        if not self.token:
            self.log_result("Interview Feedback", False, "No auth token available")
            return False
        
        # Test feedback generation
        request_data = {
            "question": "Explain the bias-variance tradeoff",
            "answer": "The bias-variance tradeoff is about balancing model complexity. High bias means underfitting, high variance means overfitting. We use techniques like cross-validation to find the right balance.",
            "role_id": "ml_engineer",
            "category": "technical"
        }
        
        success, response = self.run_test(
            "Interview Feedback Generation",
            "POST",
            "interview-prep/feedback",
            200,
            data=request_data
        )
        
        if success:
            score = response.get('score', 0)
            strengths = response.get('strengths', [])
            improvements = response.get('improvements', [])
            sample_answer = response.get('sample_answer', '')
            
            print(f"   Score: {score}/100")
            print(f"   Strengths: {len(strengths)} items")
            print(f"   Improvements: {len(improvements)} items")
            print(f"   Sample answer provided: {'Yes' if sample_answer else 'No'}")
            
            # Validate response structure
            required_fields = ['score', 'strengths', 'improvements', 'sample_answer']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Feedback Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate score is reasonable
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                self.log_result("Feedback Score Validation", False, f"Invalid score: {score}")
                return False
            
            self.log_result("Feedback Structure Validation", True)
            self.log_result("Feedback Score Validation", True)
        
        return success

    def test_interview_history(self):
        """Test interview history endpoint"""
        if not self.token:
            self.log_result("Interview History", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Interview History",
            "GET",
            "interview-prep/history",
            200
        )
        
        if success:
            history = response.get('history', [])
            stats = response.get('stats', {})
            
            print(f"   History entries: {len(history)}")
            print(f"   Total practiced: {stats.get('total_practiced', 0)}")
            print(f"   Average score: {stats.get('avg_score', 0)}")
            print(f"   Current streak: {stats.get('streak', 0)}")
            
            # Validate response structure
            required_fields = ['history', 'stats']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("History Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate stats structure
            stats_fields = ['total_practiced', 'avg_score', 'streak']
            missing_stats = [field for field in stats_fields if field not in stats]
            if missing_stats:
                self.log_result("History Stats Validation", False, f"Missing stats: {missing_stats}")
                return False
            
            self.log_result("History Structure Validation", True)
            self.log_result("History Stats Validation", True)
        
        return success

    def test_interview_companies(self):
        """Test getting companies list endpoint"""
        success, response = self.run_test(
            "Get Interview Companies",
            "GET",
            "interview-prep/companies",
            200
        )
        
        if success:
            companies = response.get('companies', [])
            print(f"   Available companies: {len(companies)}")
            
            # Check structure of first company if available
            if companies:
                first_company = companies[0]
                required_fields = ['id', 'name']
                missing_fields = [field for field in required_fields if field not in first_company]
                if missing_fields:
                    self.log_result("Company Structure Validation", False, f"Missing fields: {missing_fields}")
                    return False
                
                print(f"   Sample company: {first_company.get('name', 'N/A')}")
                self.log_result("Company Structure Validation", True)
        
        return success

    def test_get_specific_role(self):
        """Test getting specific role details"""
        success, response = self.run_test(
            "Get ML Engineer Role",
            "GET",
            "roles/ml_engineer",
            200
        )
        
        if success:
            role_name = response.get('name', '')
            salary_range = response.get('salary_range', '')
            top_skills = response.get('top_skills', [])
            hiring_patterns = response.get('hiring_patterns', {})
            
            print(f"   Role: {role_name}")
            print(f"   Salary: {salary_range}")
            print(f"   Skills: {len(top_skills)} listed")
            print(f"   Hiring patterns: {len(hiring_patterns)} regions")
            
            # Validate required fields
            required_fields = ['id', 'name', 'description', 'salary_range', 'top_skills']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Role Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            self.log_result("Role Structure Validation", True)
        
        return success

    def test_hiring_patterns(self):
        """Test getting hiring patterns"""
        success, response = self.run_test(
            "Get Hiring Patterns",
            "GET",
            "hiring-patterns",
            200
        )
        
        if success:
            patterns = response.get('hiring_patterns', {})
            print(f"   Regions covered: {len(patterns)}")
            
            # Check structure
            if patterns:
                first_region = list(patterns.keys())[0]
                region_data = patterns[first_region]
                required_fields = ['companies', 'preference']
                missing_fields = [field for field in required_fields if field not in region_data]
                if missing_fields:
                    self.log_result("Hiring Patterns Structure Validation", False, f"Missing fields: {missing_fields}")
                    return False
                
                print(f"   Sample region ({first_region}): {len(region_data.get('companies', []))} companies")
                self.log_result("Hiring Patterns Structure Validation", True)
        
        return success

    def test_user_profile(self):
        """Test getting user profile"""
        if not self.token:
            self.log_result("User Profile", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get User Profile",
            "GET",
            "user/profile",
            200
        )
        
        if success:
            user_data = response.get('user', {})
            usage_data = response.get('usage', {})
            stats_data = response.get('stats', {})
            
            print(f"   User: {user_data.get('email', 'N/A')}")
            print(f"   Subscription: {user_data.get('subscription_tier', 'N/A')}")
            print(f"   Total CVs: {stats_data.get('total_cv_generations', 0)}")
            print(f"   Total Analyses: {stats_data.get('total_analyses', 0)}")
            
            # Validate structure
            required_sections = ['user', 'usage', 'stats']
            missing_sections = [section for section in required_sections if section not in response]
            if missing_sections:
                self.log_result("Profile Structure Validation", False, f"Missing sections: {missing_sections}")
                return False
            
            self.log_result("Profile Structure Validation", True)
        
        return success

    def test_analytics_dashboard(self):
        """Test getting analytics dashboard"""
        if not self.token:
            self.log_result("Analytics Dashboard", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get Analytics Dashboard",
            "GET",
            "analytics/dashboard",
            200
        )
        
        if success:
            cv_count = response.get('cv_generations', 0)
            lp_count = response.get('learning_paths', 0)
            analysis_count = response.get('analyses', 0)
            downloads = response.get('total_downloads', 0)
            
            print(f"   CV Generations: {cv_count}")
            print(f"   Learning Paths: {lp_count}")
            print(f"   Analyses: {analysis_count}")
            print(f"   Downloads: {downloads}")
            
            # Validate required fields
            required_fields = ['cv_generations', 'learning_paths', 'analyses', 'total_downloads']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Analytics Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            self.log_result("Analytics Structure Validation", True)
        
        return success

    def test_cv_generation(self):
        """Test CV generation with Superior Hybrid Resume model"""
        if not self.token:
            self.log_result("CV Generation", False, "No auth token available")
            return False
        
        # Sample resume data for testing (must be at least 100 characters)
        cv_request = {
            "resume_text": """John Doe
Software Engineer with 5 years experience

Experience:
- Senior Software Engineer at TechCorp (2020-2024)
- Built ML pipelines using Python and TensorFlow
- Developed REST APIs with FastAPI and Django
- Worked with AWS cloud services including EC2, S3, and Lambda
- Led a team of 3 developers on machine learning projects
- Implemented CI/CD pipelines using Docker and Kubernetes

Education:
Bachelor's degree in Computer Science from State University

Skills: Python, JavaScript, React, SQL, Docker, Kubernetes, Machine Learning, TensorFlow, PyTorch, AWS, FastAPI, Django""",
            "target_role_id": "ml_engineer",
            "region": "us",
            "settings": {
                "style": "modern",
                "color_scheme": "blue"
            }
        }
        
        success, response = self.run_test(
            "CV Generation (Superior Hybrid Resume)",
            "POST",
            "cv/generate",
            200,
            data=cv_request
        )
        
        if success:
            cv_id = response.get('cv_id', '')
            target_role = response.get('target_role', '')
            versions = response.get('versions', [])
            
            print(f"   CV ID: {cv_id}")
            print(f"   Target Role: {target_role}")
            print(f"   Versions: {len(versions)}")
            
            # Validate structure - the actual response format
            required_fields = ['cv_id', 'target_role', 'versions']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("CV Generation Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check if versions contain the Superior Hybrid Resume
            hybrid_version = None
            for version in versions:
                if version.get('name') == 'Superior Hybrid Resume':
                    hybrid_version = version
                    break
            
            if not hybrid_version:
                self.log_result("CV Superior Hybrid Model Validation", False, "Superior Hybrid Resume version not found")
                return False
            
            print(f"   Superior Hybrid Resume found: {hybrid_version.get('type', 'N/A')}")
            
            self.log_result("CV Generation Structure Validation", True)
            self.log_result("CV Superior Hybrid Model Validation", True)
        
        return success

    def test_cv_history(self):
        """Test getting CV generation history"""
        if not self.token:
            self.log_result("CV History", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Get CV History",
            "GET",
            "cv/history",
            200
        )
        
        if success:
            history = response.get('history', [])
            print(f"   CV History entries: {len(history)}")
            
            # If there are entries, validate structure
            if history:
                first_entry = history[0]
                required_fields = ['id', 'target_role', 'created_at']
                missing_fields = [field for field in required_fields if field not in first_entry]
                if missing_fields:
                    self.log_result("CV History Structure Validation", False, f"Missing fields: {missing_fields}")
                    return False
                
                print(f"   Latest CV: {first_entry.get('target_role', 'N/A')}")
                self.log_result("CV History Structure Validation", True)
        
        return success

    def test_get_courses(self):
        """Test getting courses - Should return 44 courses (16 Scrimba, 23 free)"""
        success, response = self.run_test(
            "Get All Courses",
            "GET",
            "courses",
            200
        )
        
        if success:
            courses = response.get('courses', [])
            print(f"   Found {len(courses)} total courses")
            
            # Count Scrimba courses
            scrimba_courses = [c for c in courses if c.get('platform') == 'Scrimba']
            print(f"   Scrimba courses: {len(scrimba_courses)}")
            
            # Count free courses
            free_courses = [c for c in courses if 'free' in c.get('cost', '').lower()]
            print(f"   Free courses: {len(free_courses)}")
            
            # Validate total count
            if len(courses) != 44:
                self.log_result("Courses Count Validation", False, f"Expected 44 courses, got {len(courses)}")
                return False
            
            # Validate Scrimba count
            if len(scrimba_courses) != 16:
                self.log_result("Scrimba Courses Count Validation", False, f"Expected 16 Scrimba courses, got {len(scrimba_courses)}")
                return False
            
            # Validate free courses count
            if len(free_courses) != 27:
                self.log_result("Free Courses Count Validation", False, f"Expected 27 free courses, got {len(free_courses)}")
                return False
            
            self.log_result("Courses Count Validation", True)
            self.log_result("Scrimba Courses Count Validation", True)
            self.log_result("Free Courses Count Validation", True)
        
        return success

    def test_get_scrimba_courses(self):
        """Test getting Scrimba courses specifically - Should return 16 courses"""
        success, response = self.run_test(
            "Get Scrimba Courses",
            "GET",
            "courses/scrimba",
            200
        )
        
        if success:
            courses = response.get('courses', [])
            print(f"   Found {len(courses)} Scrimba courses")
            
            # Validate count
            if len(courses) != 16:
                self.log_result("Scrimba Courses Endpoint Count Validation", False, f"Expected 16 Scrimba courses, got {len(courses)}")
                return False
            
            # Validate all are Scrimba courses
            non_scrimba = [c for c in courses if c.get('platform') != 'Scrimba']
            if non_scrimba:
                self.log_result("Scrimba Courses Platform Validation", False, f"Found {len(non_scrimba)} non-Scrimba courses in Scrimba endpoint")
                return False
            
            # Check for recommended courses
            recommended_courses = [c for c in courses if c.get('recommended', False)]
            print(f"   Recommended Scrimba courses: {len(recommended_courses)}")
            
            self.log_result("Scrimba Courses Endpoint Count Validation", True)
            self.log_result("Scrimba Courses Platform Validation", True)
        
        return success

    def test_get_pricing(self):
        """Test getting pricing tiers"""
        success, response = self.run_test(
            "Get Pricing Tiers",
            "GET",
            "payments/pricing",
            200
        )
        
        if success:
            pricing = response.get('pricing', {})
            free_limits = response.get('free_limits', {})
            
            print(f"   Pricing tiers: {len(pricing)}")
            print(f"   Free limits defined: {len(free_limits)}")
            
            # Validate pricing structure
            expected_pricing_keys = ['pro_monthly', 'cv_single', 'cv_bulk_50']
            missing_pricing = [key for key in expected_pricing_keys if key not in pricing]
            if missing_pricing:
                self.log_result("Pricing Structure Validation", False, f"Missing pricing tiers: {missing_pricing}")
                return False
            
            # Validate free limits structure
            expected_limits_keys = ['cv_generations', 'learning_paths', 'analyses']
            missing_limits = [key for key in expected_limits_keys if key not in free_limits]
            if missing_limits:
                self.log_result("Free Limits Structure Validation", False, f"Missing free limits: {missing_limits}")
                return False
            
            # Check pro monthly pricing
            pro_monthly = pricing.get('pro_monthly', {})
            if pro_monthly.get('price') != 29:
                self.log_result("Pro Monthly Price Validation", False, f"Expected $29, got ${pro_monthly.get('price')}")
                return False
            
            self.log_result("Pricing Structure Validation", True)
            self.log_result("Free Limits Structure Validation", True)
            self.log_result("Pro Monthly Price Validation", True)
        
        return success

    def test_resume_scanner(self):
        """Test Resume Scanner feature - POST /api/resume/scan"""
        if not self.token:
            self.log_result("Resume Scanner", False, "No auth token available")
            return False
        
        # Sample resume text for scanning (must be realistic)
        resume_text = """Sarah Johnson
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

Skills: Python, JavaScript, React, Node.js, TensorFlow, PyTorch, AWS, Azure, Docker, Kubernetes, SQL, MongoDB, Machine Learning, Deep Learning, REST APIs, Microservices, Agile, Git"""
        
        scan_request = {
            "resume_text": resume_text,
            "target_role_id": "ai_ml_engineer"  # Fixed: use target_role_id instead of target_role
        }
        
        success, response = self.run_test(
            "Resume Scanner (ATS Analysis)",
            "POST",
            "resume/scan",
            200,
            data=scan_request
        )
        
        if success:
            ats_score = response.get('ats_score', 0)
            human_appeal_score = response.get('human_appeal_score', 0)
            keywords_found = response.get('keywords_found', [])
            keywords_missing = response.get('keywords_missing', [])
            quick_wins = response.get('quick_wins', [])
            overall_grade = response.get('overall_grade', '')
            
            print(f"   ATS Score: {ats_score}/100")
            print(f"   Human Appeal Score: {human_appeal_score}/100")
            print(f"   Overall Grade: {overall_grade}")
            print(f"   Keywords found: {len(keywords_found)}")
            print(f"   Keywords missing: {len(keywords_missing)}")
            print(f"   Quick wins: {len(quick_wins)}")
            
            # Validate response structure based on actual API
            required_fields = ['ats_score', 'human_appeal_score', 'keyword_match_percent', 'overall_grade', 
                             'keywords_found', 'keywords_missing', 'strengths', 'improvements', 
                             'formatting_issues', 'quick_wins', 'target_role', 'scan_id']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Resume Scanner Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate scores are reasonable
            if not isinstance(ats_score, (int, float)) or ats_score < 0 or ats_score > 100:
                self.log_result("Resume Scanner ATS Score Validation", False, f"Invalid ATS score: {ats_score}")
                return False
            
            if not isinstance(human_appeal_score, (int, float)) or human_appeal_score < 0 or human_appeal_score > 100:
                self.log_result("Resume Scanner Human Appeal Validation", False, f"Invalid human appeal score: {human_appeal_score}")
                return False
            
            self.log_result("Resume Scanner Structure Validation", True)
            self.log_result("Resume Scanner ATS Score Validation", True)
            self.log_result("Resume Scanner Human Appeal Validation", True)
        
        return success

    def test_resume_scanner_usage(self):
        """Test Resume Scanner usage tracking - GET /api/resume/scan/usage"""
        if not self.token:
            self.log_result("Resume Scanner Usage", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Resume Scanner Usage Tracking",
            "GET",
            "resume/scan/usage",
            200
        )
        
        if success:
            scans_used = response.get('scans_used', 0)
            scans_limit = response.get('scans_limit', 0)
            is_pro = response.get('is_pro', False)
            can_scan = response.get('can_scan', False)
            
            print(f"   Scans used: {scans_used}/{scans_limit}")
            print(f"   Is Pro: {is_pro}")
            print(f"   Can scan: {can_scan}")
            
            # Validate structure based on actual API
            required_fields = ['scans_used', 'scans_limit', 'is_pro', 'can_scan']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Resume Scanner Usage Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check 2 scans/month limit for free users
            if not is_pro and scans_limit != 2:
                self.log_result("Resume Scanner Limit Validation", False, f"Expected 2 scans limit for free users, got {scans_limit}")
                return False
            
            self.log_result("Resume Scanner Usage Structure Validation", True)
            self.log_result("Resume Scanner Limit Validation", True)
        
        return success

    def test_resume_scanner_history(self):
        """Test Resume Scanner history - GET /api/resume/scan/history"""
        if not self.token:
            self.log_result("Resume Scanner History", False, "No auth token available")
            return False
        
        success, response = self.run_test(
            "Resume Scanner History",
            "GET",
            "resume/scan/history",
            200
        )
        
        if success:
            scans = response.get('scans', [])
            total = response.get('total', 0)
            print(f"   Scan history entries: {len(scans)}")
            print(f"   Total scans: {total}")
            
            # If there are entries, validate structure
            if scans:
                first_entry = scans[0]
                required_fields = ['id', 'target_role', 'ats_score', 'created_at']
                missing_fields = [field for field in required_fields if field not in first_entry]
                if missing_fields:
                    self.log_result("Resume Scanner History Structure Validation", False, f"Missing fields: {missing_fields}")
                    return False
                
                print(f"   Latest scan: {first_entry.get('target_role', 'N/A')} (Score: {first_entry.get('ats_score', 0)})")
                self.log_result("Resume Scanner History Structure Validation", True)
        
        return success

    def test_cover_letter_generation(self):
        """Test Cover Letter generation - POST /api/cover-letter/generate"""
        if not self.token:
            self.log_result("Cover Letter Generation", False, "No auth token available")
            return False
        
        cover_letter_request = {
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
            "target_role": "Senior ML Engineer",  # Fixed: use target_role instead of role_title
            "tone": "professional"
        }
        
        success, response = self.run_test(
            "Cover Letter Generation",
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
            company_research = response.get('company_research', {})
            job_match_analysis = response.get('job_match_analysis', {})
            
            print(f"   Cover Letter ID: {cover_letter_id}")
            print(f"   Company: {company_name}")
            print(f"   Target Role: {target_role}")
            print(f"   Versions: {len(versions)}")
            
            # Validate response structure based on actual API
            required_fields = ['cover_letter_id', 'company_name', 'target_role', 'versions']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Cover Letter Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Validate versions structure
            if versions and len(versions) > 0:
                first_version = versions[0]
                version_required_fields = ['version_name', 'cover_letter', 'tone_applied']
                missing_version_fields = [field for field in version_required_fields if field not in first_version]
                if missing_version_fields:
                    self.log_result("Cover Letter Version Structure Validation", False, f"Missing version fields: {missing_version_fields}")
                    return False
                
                cover_letter_content = first_version.get('cover_letter', '')
                if len(cover_letter_content) < 200:
                    self.log_result("Cover Letter Content Validation", False, f"Cover letter too short: {len(cover_letter_content)} chars")
                    return False
                
                # Check if it mentions the company and role
                if "OpenAI" not in cover_letter_content or "ML Engineer" not in cover_letter_content:
                    self.log_result("Cover Letter Personalization Validation", False, "Cover letter not properly personalized")
                    return False
                
                self.log_result("Cover Letter Version Structure Validation", True)
                self.log_result("Cover Letter Content Validation", True)
                self.log_result("Cover Letter Personalization Validation", True)
            
            self.log_result("Cover Letter Structure Validation", True)
        
        return success

    def test_learning_path_generation(self):
        """Test Learning Path generation - POST /api/learning-path/generate with target_role_id (frontend-style)"""
        if not self.token:
            self.log_result("Learning Path Generation", False, "No auth token available")
            return False
        
        # Test with frontend-style payload using target_role_id
        learning_path_request = {
            "current_role": "Software Engineer",
            "years_experience": 3,
            "current_skills": ["Python", "JavaScript"],
            "target_role_id": "ml_engineer",
            "location": "United States"
        }
        
        success, response = self.run_test(
            "Learning Path Generation (Frontend-style with target_role_id)",
            "POST",
            "learning-path/generate",
            200,
            data=learning_path_request
        )
        
        if success:
            path_id = response.get('path_id', '')
            target_role = response.get('target_role', '')
            path_data = response.get('path_data', {}) or response.get('learning_path', {})
            usage = response.get('usage', {})
            
            path_overview = path_data.get('path_overview', {})
            weeks = path_data.get('weeks', [])
            
            print(f"   Path ID: {path_id}")
            print(f"   Target Role: {target_role}")
            print(f"   Duration: {path_overview.get('duration_weeks', 0)} weeks")
            print(f"   Learning phases: {len(weeks)}")
            print(f"   Usage: {usage.get('used', 0)}/{usage.get('limit', 0)}")
            
            # Validate response structure - check for both path_data and learning_path
            required_fields = ['path_id', 'target_role', 'usage']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Learning Path Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            # Check if either path_data or learning_path exists
            if not path_data:
                self.log_result("Learning Path Structure Validation", False, "Neither path_data nor learning_path found in response")
                return False
            
            # Validate target_role resolves correctly from ml_engineer
            if target_role != "Machine Learning Engineer":
                self.log_result("Learning Path Role Resolution Validation", False, f"Expected 'Machine Learning Engineer', got '{target_role}'")
                return False
            else:
                self.log_result("Learning Path Role Resolution Validation", True)
            
            # Validate path_data structure
            if path_data:
                path_required_fields = ['path_overview', 'weeks']
                missing_path_fields = [field for field in path_required_fields if field not in path_data]
                if missing_path_fields:
                    self.log_result("Learning Path Data Structure Validation", False, f"Missing path_data fields: {missing_path_fields}")
                    return False
                
                # Validate duration is 16 weeks as expected
                duration_weeks = path_overview.get('duration_weeks', 0)
                if not isinstance(duration_weeks, int) or duration_weeks != 16:
                    self.log_result("Learning Path Duration Validation", False, f"Expected 16 weeks, got {duration_weeks}")
                    return False
                
                # Check if weeks have proper structure and there are 16 weeks
                if not weeks or len(weeks) == 0:
                    self.log_result("Learning Path Weeks Validation", False, "No weeks found in learning path")
                    return False
                
                first_week = weeks[0]
                week_required_fields = ['week', 'focus', 'hours']
                missing_week_fields = [field for field in week_required_fields if field not in first_week]
                if missing_week_fields:
                    self.log_result("Learning Path Week Structure Validation", False, f"Missing week fields: {missing_week_fields}")
                    return False
                
                self.log_result("Learning Path Week Structure Validation", True)
                self.log_result("Learning Path Weeks Validation", True)
                self.log_result("Learning Path Data Structure Validation", True)
                self.log_result("Learning Path Duration Validation", True)
            
            self.log_result("Learning Path Structure Validation", True)
        
        return success

    def test_learning_path_error_scenarios(self):
        """Test Learning Path error scenarios - missing target_role_id"""
        if not self.token:
            self.log_result("Learning Path Error Scenarios", False, "No auth token available")
            return False
        
        # Test with missing target_role_id (should return clean error message)
        invalid_request = {
            "current_role": "Software Engineer",
            "years_experience": 3,
            "current_skills": ["Python", "JavaScript"],
            "location": "United States"
            # Missing target_role_id
        }
        
        success, response = self.run_test(
            "Learning Path Error - Missing target_role_id",
            "POST",
            "learning-path/generate",
            400,  # Expect 400 Bad Request
            data=invalid_request
        )
        
        if success:
            # Check if error message is clean and informative
            error_detail = response.get('detail', '')
            if isinstance(error_detail, str) and 'target role' in error_detail.lower():
                print(f"   Clean error message: {error_detail}")
                self.log_result("Learning Path Error Message Validation", True)
            else:
                self.log_result("Learning Path Error Message Validation", False, f"Unclear error message: {error_detail}")
                return False
        
        return success

    def test_career_analysis_comprehensive(self):
        """Test comprehensive Career Analysis - POST /api/analysis/analyze"""
        if not self.token:
            self.log_result("Career Analysis Comprehensive", False, "No auth token available")
            return False
        
        # Use the same resume parsing as before
        resume_success, resume_response = self.test_resume_parse_text()
        if not resume_success:
            self.log_result("Career Analysis Comprehensive", False, "Resume parsing failed")
            return False
        
        resume_data = resume_response.get('resume_data', {})
        
        # Build proper request structure based on actual API
        analysis_request = {
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
                "skills": resume_data.get('skills', ["Python", "Machine Learning", "TensorFlow", "FastAPI"]),
                "certifications": [],
                "summary": "Software Engineer with 5 years experience in machine learning"
            },
            "target_role_id": "ai_ml_engineer",
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
        
        success, response = self.run_test(
            "Career Analysis (Comprehensive)",
            "POST",
            "analysis/analyze",
            200,
            data=analysis_request
        )
        
        if success:
            analysis_id = response.get('analysis_id', '')
            target_role = response.get('target_role', {})
            analysis = response.get('analysis', {})
            
            print(f"   Analysis ID: {analysis_id}")
            print(f"   Target Role: {target_role.get('name', 'N/A')}")
            
            # Check if analysis contains expected sections
            if analysis:
                career_fit = analysis.get('career_fit', {})
                ats_score = analysis.get('ats_score', {})
                transferable_skills = analysis.get('transferable_skills', [])
                skill_gaps = analysis.get('skill_gaps', [])
                learning_path = analysis.get('learning_path', {})
                
                print(f"   Career fit score: {career_fit.get('score', 0)}/100")
                print(f"   Career fit rating: {career_fit.get('rating', 'N/A')}")
                print(f"   ATS score: {ats_score.get('score', 0)}/100")
                print(f"   Transferable skills: {len(transferable_skills)}")
                print(f"   Skill gaps: {len(skill_gaps)}")
                print(f"   Learning timeline: {learning_path.get('total_weeks', 0)} weeks")
                
                # Validate comprehensive analysis structure
                required_sections = ['career_fit', 'ats_score', 'transferable_skills', 'skill_gaps', 'learning_path', 'next_steps']
                missing_sections = [section for section in required_sections if section not in analysis]
                if missing_sections:
                    self.log_result("Career Analysis Comprehensive Structure Validation", False, f"Missing sections: {missing_sections}")
                    return False
                
                # Validate career fit
                if career_fit and isinstance(career_fit.get('score'), (int, float)):
                    if career_fit.get('score') < 0 or career_fit.get('score') > 100:
                        self.log_result("Career Analysis Fit Score Validation", False, f"Invalid career fit score: {career_fit.get('score')}")
                        return False
                    else:
                        self.log_result("Career Analysis Fit Score Validation", True)
                
                # Validate ATS score
                if ats_score and isinstance(ats_score.get('score'), (int, float)):
                    if ats_score.get('score') < 0 or ats_score.get('score') > 100:
                        self.log_result("Career Analysis ATS Score Validation", False, f"Invalid ATS score: {ats_score.get('score')}")
                        return False
                    else:
                        self.log_result("Career Analysis ATS Score Validation", True)
                
                self.log_result("Career Analysis Comprehensive Structure Validation", True)
            
            # Validate main response structure
            required_fields = ['analysis_id', 'target_role', 'analysis']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_result("Career Analysis Response Structure Validation", False, f"Missing fields: {missing_fields}")
                return False
            
            self.log_result("Career Analysis Response Structure Validation", True)
        
        return success

    def test_cv_scanner_score_consistency(self):
        """
        CRITICAL TEST: CV-Scanner Score Consistency
        Tests that CV Generator and Resume Scanner return IDENTICAL scores for the same content
        """
        if not self.token:
            self.log_result("CV-Scanner Score Consistency", False, "No auth token available")
            return False
        
        print("\n🎯 CRITICAL TEST: CV-Scanner Score Consistency")
        print("=" * 60)
        
        # Sample resume text for testing (realistic ML Engineer resume)
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
        
        # Step 1: Generate CV using CV Generator
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
        
        cv_success, cv_response = self.run_test(
            "CV Generation for Score Consistency Test",
            "POST",
            "cv/generate",
            200,
            data=cv_request
        )
        
        if not cv_success:
            self.log_result("CV-Scanner Score Consistency", False, "CV Generation failed")
            return False
        
        # Extract CV content and scores
        versions = cv_response.get('versions', [])
        if not versions:
            self.log_result("CV-Scanner Score Consistency", False, "No CV versions returned")
            return False
        
        cv_version = versions[0]
        cv_content = cv_version.get('content', '')
        cv_ats_score = cv_version.get('ats_score', 0)
        cv_human_appeal_score = cv_version.get('human_appeal_score', 0)
        
        print(f"   CV Generated Successfully")
        print(f"   CV ATS Score: {cv_ats_score}")
        print(f"   CV Human Appeal Score: {cv_human_appeal_score}")
        print(f"   CV Content Length: {len(cv_content)} chars")
        
        if not cv_content:
            self.log_result("CV-Scanner Score Consistency", False, "CV content is empty")
            return False
        
        # Step 2: Scan the SAME content using Resume Scanner
        print("\n2️⃣ STEP 2: Scan the SAME content using Resume Scanner")
        scan_request = {
            "resume_text": cv_content,  # Use the EXACT content from CV Generator
            "target_role_id": target_role_id
        }
        
        scan_success, scan_response = self.run_test(
            "Resume Scanner for Score Consistency Test",
            "POST",
            "resume/scan",
            200,
            data=scan_request
        )
        
        if not scan_success:
            self.log_result("CV-Scanner Score Consistency", False, "Resume Scanner failed")
            return False
        
        # Extract Scanner scores
        scanner_ats_score = scan_response.get('ats_score', 0)
        scanner_human_appeal_score = scan_response.get('human_appeal_score', 0)
        
        print(f"   Resume Scanned Successfully")
        print(f"   Scanner ATS Score: {scanner_ats_score}")
        print(f"   Scanner Human Appeal Score: {scanner_human_appeal_score}")
        
        # Step 3: Compare scores for consistency
        print("\n3️⃣ STEP 3: Compare Scores for Consistency")
        print("=" * 40)
        
        ats_difference = abs(cv_ats_score - scanner_ats_score)
        human_difference = abs(cv_human_appeal_score - scanner_human_appeal_score)
        
        print(f"CV Generator    - ATS: {cv_ats_score}, Human: {cv_human_appeal_score}")
        print(f"Resume Scanner  - ATS: {scanner_ats_score}, Human: {human_difference}")
        print(f"Differences     - ATS: {ats_difference}, Human: {human_difference}")
        
        # Tolerance for AI variance (should be very small or zero)
        tolerance = 2  # Allow up to 2 points difference due to AI variance
        
        consistency_passed = True
        consistency_issues = []
        
        if ats_difference > tolerance:
            consistency_passed = False
            consistency_issues.append(f"ATS score difference too large: {ats_difference} points (CV: {cv_ats_score}, Scanner: {scanner_ats_score})")
        
        if human_difference > tolerance:
            consistency_passed = False
            consistency_issues.append(f"Human Appeal score difference too large: {human_difference} points (CV: {cv_human_appeal_score}, Scanner: {scanner_human_appeal_score})")
        
        # Step 4: Validate model names are correct
        print("\n4️⃣ STEP 4: Validate Model Usage")
        
        # Check if verified_analysis is present (indicates shared analysis function was used)
        verified_analysis = cv_response.get('verified_analysis', {})
        if verified_analysis:
            print(f"   ✅ CV Generator uses shared analysis function (verified_analysis present)")
            self.log_result("CV Generator Shared Analysis Validation", True)
        else:
            print(f"   ⚠️  CV Generator may not be using shared analysis function")
            self.log_result("CV Generator Shared Analysis Validation", False, "verified_analysis field missing")
        
        # Check response structure includes expected fields
        cv_required_fields = ['cv_id', 'target_role', 'versions']
        cv_missing_fields = [field for field in cv_required_fields if field not in cv_response]
        
        scanner_required_fields = ['ats_score', 'human_appeal_score', 'target_role', 'scan_id']
        scanner_missing_fields = [field for field in scanner_required_fields if field not in scan_response]
        
        if cv_missing_fields:
            consistency_passed = False
            consistency_issues.append(f"CV Generator missing fields: {cv_missing_fields}")
        
        if scanner_missing_fields:
            consistency_passed = False
            consistency_issues.append(f"Resume Scanner missing fields: {scanner_missing_fields}")
        
        # Final result
        print("\n🏁 FINAL RESULT:")
        print("=" * 40)
        
        if consistency_passed:
            print("✅ SCORE CONSISTENCY TEST PASSED!")
            print(f"   Both CV Generator and Resume Scanner return consistent scores")
            print(f"   ATS difference: {ats_difference} points (within {tolerance} tolerance)")
            print(f"   Human Appeal difference: {human_difference} points (within {tolerance} tolerance)")
            self.log_result("CV-Scanner Score Consistency", True)
            self.log_result("CV-Scanner ATS Score Consistency", True)
            self.log_result("CV-Scanner Human Appeal Score Consistency", True)
            return True
        else:
            print("❌ SCORE CONSISTENCY TEST FAILED!")
            for issue in consistency_issues:
                print(f"   • {issue}")
            self.log_result("CV-Scanner Score Consistency", False, "; ".join(consistency_issues))
            return False

    def run_all_tests(self):
        """Run comprehensive backend tests focusing on critical features after CV generation fix"""
        print("🚀 Starting CareerLift API Tests - Comprehensive Backend Testing After CV Fix")
        print("=" * 80)
        print("🔍 CRITICAL FEATURES TO TEST (Review Request):")
        print("   - POST /api/cv/generate - CV Generation (Superior Hybrid Resume)")
        print("   - POST /api/resume/scan - Resume Scanner (2 scans/month limit)")
        print("   - POST /api/interview-prep/generate - Interview Prep (Haiku)")
        print("   - POST /api/interview-prep/feedback - Interview Feedback (Sonnet)")
        print("   - POST /api/cover-letter/generate - Cover Letter Generation")
        print("   - POST /api/learning-path/generate - Learning Path Generation")
        print("   - POST /api/analysis/analyze - Career Analysis")
        print("   - Test Credentials: scanner@test.com / test123")
        print("=" * 80)
        
        # CRITICAL ENDPOINTS - Public (no auth required)
        print("\n🔧 Testing Public Endpoints")
        print("-" * 50)
        self.test_health_check()
        self.test_get_roles()
        self.test_get_specific_role()
        self.test_hiring_patterns()
        self.test_interview_companies()
        
        # Authentication tests - CRITICAL LOGIN TEST with review request credentials
        print("\n🔐 Testing Authentication with Review Request Credentials")
        print("-" * 50)
        
        # Try login with scanner@test.com / test123 from review request
        login_data = {
            "email": "scanner@test.com",
            "password": "test123"
        }
        success, response = self.run_test(
            "Login with Scanner Credentials (scanner@test.com/test123)",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        if success:
            self.token = response.get('access_token')
            self.user_id = response.get('user', {}).get('id')
            print(f"   ✅ Scanner login successful - Token received")
        else:
            # Try fallback test credentials
            print("\n⚠️  Scanner login failed, trying test@test.com/test...")
            login_data = {
                "email": "test@test.com",
                "password": "test"
            }
            success, response = self.run_test(
                "Login with Test Credentials (test@test.com/test)",
                "POST",
                "auth/login",
                200,
                data=login_data
            )
            if success:
                self.token = response.get('access_token')
                self.user_id = response.get('user', {}).get('id')
                print(f"   ✅ Test login successful - Token received")
            else:
                # Try registration as final fallback
                print("\n⚠️  Both logins failed, trying registration...")
                self.test_register_user()
        
        # Protected endpoint tests (require authentication)
        if self.token:
            print("\n🎯 Testing CRITICAL AI-POWERED FEATURES (Review Request Focus)")
            print("-" * 50)
            
            # 1. CV Generation (just fixed) - Superior Hybrid Resume
            print("\n1️⃣ CV GENERATION (Superior Hybrid Resume - Just Fixed)")
            self.test_cv_generation()
            self.test_cv_history()
            
            # 2. Resume Scanner (new feature) - 2 scans/month limit
            print("\n2️⃣ RESUME SCANNER (New Feature - 2 Scans/Month Limit)")
            self.test_resume_scanner()
            self.test_resume_scanner_usage()
            self.test_resume_scanner_history()
            
            # 3. Interview Prep - Haiku for questions, Sonnet for feedback
            print("\n3️⃣ INTERVIEW PREP (Haiku + Sonnet Model Split)")
            self.test_interview_question_generation()
            self.test_interview_question_generation_with_company()
            self.test_interview_feedback()
            self.test_interview_history()
            
            # 4. Cover Letter Generation
            print("\n4️⃣ COVER LETTER GENERATION")
            self.test_cover_letter_generation()
            
            # 5. Learning Path Generation (Review Request Focus - Fixed target_role_id issue)
            print("\n5️⃣ LEARNING PATH GENERATION (Review Request Focus)")
            self.test_learning_path_generation()
            self.test_learning_path_error_scenarios()
            
            # 6. Career Analysis (comprehensive)
            print("\n6️⃣ CAREER ANALYSIS (Comprehensive)")
            self.test_career_analysis_comprehensive()
            
            # 7. CV-Scanner Score Consistency (CRITICAL TEST from review request)
            print("\n7️⃣ CV-SCANNER SCORE CONSISTENCY (CRITICAL)")
            self.test_cv_scanner_score_consistency()
            
            # Supporting features
            print("\n📊 Testing Supporting Features")
            print("-" * 50)
            self.test_get_me()
            self.test_user_profile()
            self.test_analytics_dashboard()
            self.test_get_usage()
            self.test_resume_parse_text()
            
        else:
            print("\n❌ No authentication token available - skipping protected endpoint tests")
        
        # Print final results
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE BACKEND TEST RESULTS")
        print("=" * 80)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {len(self.failed_tests)}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%" if self.tests_run > 0 else "0%")
        
        # Focus on critical AI features from review request
        critical_ai_tests = [
            "CV Generation (Superior Hybrid Resume)", "CV Generation Structure Validation", "CV Superior Hybrid Model Validation",
            "Resume Scanner (ATS Analysis)", "Resume Scanner Structure Validation", "Resume Scanner ATS Score Validation",
            "Resume Scanner Usage Tracking", "Resume Scanner Limit Validation",
            "Interview Question Generation (Basic)", "Interview Question Generation (Company-specific)",
            "Interview Feedback Generation", "Feedback Structure Validation",
            "Cover Letter Generation", "Cover Letter Structure Validation", "Cover Letter Content Validation",
            "Learning Path Generation", "Learning Path Structure Validation",
            "Career Analysis (Comprehensive)", "Career Analysis Comprehensive Structure Validation",
            "CV-Scanner Score Consistency", "CV-Scanner ATS Score Consistency", "CV-Scanner Human Appeal Score Consistency",
            "Login with Scanner Credentials (scanner@test.com/test123)"
        ]
        
        critical_failures = [f for f in self.failed_tests if f['test'] in critical_ai_tests]
        
        if critical_failures:
            print(f"\n❌ CRITICAL AI FEATURE FAILURES ({len(critical_failures)}):")
            for failure in critical_failures:
                print(f"   • {failure['test']}: {failure['error']}")
        else:
            print(f"\n✅ ALL CRITICAL AI FEATURES PASSED - Backend working correctly after CV fix!")
        
        # Separate other failures
        other_failures = [f for f in self.failed_tests if f not in critical_failures]
        if other_failures:
            print(f"\n⚠️  OTHER FAILURES ({len(other_failures)}):")
            for failure in other_failures:
                print(f"   • {failure['test']}: {failure['error']}")
        
        # Summary by feature category
        print(f"\n📈 FEATURE CATEGORY SUMMARY:")
        feature_categories = {
            "CV Generation": ["CV Generation", "CV Superior Hybrid Model", "CV History"],
            "Resume Scanner": ["Resume Scanner", "Resume Scanner Usage", "Resume Scanner History"],
            "Interview Prep": ["Interview Question", "Interview Feedback", "Interview History"],
            "Cover Letter": ["Cover Letter"],
            "Learning Path": ["Learning Path"],
            "Career Analysis": ["Career Analysis"]
        }
        
        for category, keywords in feature_categories.items():
            category_tests = [t for t in self.failed_tests if any(kw in t['test'] for kw in keywords)]
            status = "✅ WORKING" if len(category_tests) == 0 else f"❌ {len(category_tests)} ISSUES"
            print(f"   {category}: {status}")
        
        return len(critical_failures) == 0  # Success if no critical AI feature failures

def main():
    tester = CareerLiftAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())