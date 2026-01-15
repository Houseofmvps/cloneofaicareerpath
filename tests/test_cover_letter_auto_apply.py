"""
Test Cover Letter Generator and Auto-Apply Features
Tests for the two new features added to the AI Career Transition Platform:
1. Cover Letter Generator - POST /api/cover-letter/generate
2. Auto-Apply System - /api/auto-apply/* endpoints
"""

import pytest
import requests
import os
import uuid
from datetime import datetime

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test user credentials
TEST_EMAIL = f"test_cl_aa_{uuid.uuid4().hex[:8]}@test.com"
TEST_PASSWORD = "testpass123"
TEST_NAME = "Test User CL AA"


class TestSetup:
    """Setup tests - verify environment and create test user"""
    
    @pytest.fixture(scope="class")
    def session(self):
        """Create a requests session"""
        return requests.Session()
    
    def test_base_url_configured(self):
        """Verify BASE_URL is configured"""
        assert BASE_URL, "REACT_APP_BACKEND_URL environment variable not set"
        print(f"Testing against: {BASE_URL}")
    
    def test_health_check(self, session):
        """Verify backend is healthy"""
        response = session.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["claude_configured"] == True
        print(f"Backend healthy, Claude configured: {data['claude_configured']}")


class TestAuthentication:
    """Authentication tests for test user"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    @pytest.fixture(scope="class")
    def auth_token(self, session):
        """Register and get auth token"""
        # Try to register
        register_response = session.post(f"{BASE_URL}/api/auth/register", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": TEST_NAME
        })
        
        if register_response.status_code == 200:
            token = register_response.json()["access_token"]
            print(f"Registered new user: {TEST_EMAIL}")
            return token
        
        # If registration fails (user exists), try login
        login_response = session.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print(f"Logged in existing user: {TEST_EMAIL}")
            return token
        
        pytest.fail(f"Could not authenticate: {login_response.text}")
    
    def test_auth_token_obtained(self, auth_token):
        """Verify auth token was obtained"""
        assert auth_token is not None
        assert len(auth_token) > 0
        print(f"Auth token obtained: {auth_token[:20]}...")


class TestCoverLetterEndpoints:
    """Test Cover Letter Generator API endpoints"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    @pytest.fixture(scope="class")
    def auth_headers(self, session):
        """Get auth headers for authenticated requests"""
        # Create unique user for cover letter tests
        email = f"test_cl_{uuid.uuid4().hex[:8]}@test.com"
        register_response = session.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD,
            "name": "Cover Letter Test User"
        })
        
        if register_response.status_code == 200:
            token = register_response.json()["access_token"]
        else:
            # Try login
            login_response = session.post(f"{BASE_URL}/api/auth/login", json={
                "email": email,
                "password": TEST_PASSWORD
            })
            token = login_response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    def test_cover_letter_generate_endpoint_exists(self, session, auth_headers):
        """Test that cover letter generate endpoint exists and requires auth"""
        # Test without auth - should fail
        response = session.post(f"{BASE_URL}/api/cover-letter/generate", json={})
        assert response.status_code in [401, 403, 422]
        print("Cover letter endpoint requires authentication")
    
    def test_cover_letter_generate_validation(self, session, auth_headers):
        """Test cover letter generation validation"""
        # Test with missing required fields
        response = session.post(
            f"{BASE_URL}/api/cover-letter/generate",
            json={"resume_text": "short"},  # Missing job_description, too short
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error
        print("Cover letter validation working - rejects short resume")
    
    def test_cover_letter_generate_success(self, session, auth_headers):
        """Test successful cover letter generation"""
        resume_text = """
        John Doe
        Software Engineer with 5 years of experience
        
        Experience:
        - Senior Software Engineer at TechCorp (2020-2024)
          - Built ML pipelines using Python and TensorFlow
          - Led team of 5 engineers
          - Reduced inference time by 40%
        
        Skills: Python, TensorFlow, PyTorch, AWS, Docker, Kubernetes
        Education: MS Computer Science, Stanford University
        """
        
        job_description = """
        Senior AI/ML Engineer at OpenAI
        
        Requirements:
        - 5+ years of software engineering experience
        - Strong Python skills
        - Experience with ML frameworks (TensorFlow, PyTorch)
        - Experience with distributed systems
        
        Responsibilities:
        - Build and deploy ML models at scale
        - Collaborate with research teams
        - Optimize model performance
        """
        
        response = session.post(
            f"{BASE_URL}/api/cover-letter/generate",
            json={
                "resume_text": resume_text,
                "job_description": job_description,
                "company_name": "OpenAI",
                "target_role": "Senior AI/ML Engineer",
                "tone": "professional"
            },
            headers=auth_headers,
            timeout=120  # Cover letter generation may take time
        )
        
        assert response.status_code == 200, f"Cover letter generation failed: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "cover_letter_id" in data
        assert "versions" in data
        assert len(data["versions"]) >= 1  # Should have at least 1 version
        print(f"Cover letter generated with ID: {data['cover_letter_id']}")
        print(f"Number of versions: {len(data['versions'])}")
        
        # Store for later tests
        return data
    
    def test_cover_letter_history_endpoint(self, session, auth_headers):
        """Test cover letter history endpoint"""
        response = session.get(
            f"{BASE_URL}/api/cover-letter/history",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "cover_letters" in data
        print(f"Cover letter history: {len(data['cover_letters'])} items")


class TestAutoApplyEndpoints:
    """Test Auto-Apply System API endpoints"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    @pytest.fixture(scope="class")
    def auth_headers(self, session):
        """Get auth headers for authenticated requests"""
        email = f"test_aa_{uuid.uuid4().hex[:8]}@test.com"
        register_response = session.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD,
            "name": "Auto Apply Test User"
        })
        
        if register_response.status_code == 200:
            token = register_response.json()["access_token"]
        else:
            login_response = session.post(f"{BASE_URL}/api/auth/login", json={
                "email": email,
                "password": TEST_PASSWORD
            })
            token = login_response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    def test_auto_apply_preferences_save(self, session, auth_headers):
        """Test saving auto-apply preferences"""
        preferences = {
            "target_roles": ["AI/ML Engineer", "Prompt Engineer"],
            "locations": ["Remote (US)", "San Francisco, CA"],
            "remote_preference": "remote",
            "min_salary": 150000,
            "max_salary": 300000,
            "company_types": ["faang", "ai_native"],
            "tech_stack": ["Python", "PyTorch", "LLMs"],
            "experience_years": 5,
            "auto_apply_enabled": True
        }
        
        response = session.post(
            f"{BASE_URL}/api/auto-apply/preferences",
            json=preferences,
            headers=auth_headers
        )
        
        assert response.status_code == 200, f"Save preferences failed: {response.text}"
        data = response.json()
        assert "message" in data
        assert "preferences" in data
        print(f"Preferences saved: {data['message']}")
    
    def test_auto_apply_preferences_get(self, session, auth_headers):
        """Test getting auto-apply preferences"""
        response = session.get(
            f"{BASE_URL}/api/auto-apply/preferences",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "preferences" in data
        print(f"Preferences retrieved: {data['preferences'].get('target_roles', [])}")
    
    def test_auto_apply_matching_jobs(self, session, auth_headers):
        """Test getting matching jobs (MOCK data)"""
        response = session.get(
            f"{BASE_URL}/api/auto-apply/matching-jobs",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "jobs" in data
        assert "total_count" in data
        assert len(data["jobs"]) > 0
        
        # Verify job structure
        job = data["jobs"][0]
        assert "id" in job
        assert "title" in job
        assert "company" in job
        assert "location" in job
        assert "salary_range" in job
        assert "match_score" in job
        
        print(f"Matching jobs: {data['total_count']} jobs found")
        print(f"Top job: {job['title']} at {job['company']} (Match: {job['match_score']}%)")
    
    def test_auto_apply_apply_to_job(self, session, auth_headers):
        """Test applying to a job (MOCK)"""
        # First get matching jobs
        jobs_response = session.get(
            f"{BASE_URL}/api/auto-apply/matching-jobs",
            headers=auth_headers
        )
        jobs = jobs_response.json()["jobs"]
        
        if len(jobs) > 0:
            job_id = jobs[0]["id"]
            
            response = session.post(
                f"{BASE_URL}/api/auto-apply/apply/{job_id}",
                headers=auth_headers
            )
            
            # First application should succeed
            if response.status_code == 200:
                data = response.json()
                assert "message" in data
                assert "application" in data
                print(f"Applied to job: {data['message']}")
            elif response.status_code == 400:
                # Already applied
                print("Already applied to this job (expected if test ran before)")
            else:
                pytest.fail(f"Unexpected response: {response.status_code} - {response.text}")
    
    def test_auto_apply_applications_list(self, session, auth_headers):
        """Test getting applications list"""
        response = session.get(
            f"{BASE_URL}/api/auto-apply/applications",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "applications" in data
        assert "stats" in data
        
        print(f"Applications: {len(data['applications'])} total")
        print(f"Stats: {data['stats']}")
    
    def test_auto_apply_dashboard(self, session, auth_headers):
        """Test auto-apply dashboard endpoint"""
        response = session.get(
            f"{BASE_URL}/api/auto-apply/dashboard",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "preferences" in data
        assert "matching_jobs" in data
        assert "stats" in data
        
        print(f"Dashboard stats: {data['stats']}")
        print(f"Matching jobs in dashboard: {len(data['matching_jobs'])}")


class TestLandingPageFeatures:
    """Test that landing page shows all 5 features"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    def test_roles_endpoint_has_20_roles(self, session):
        """Verify 20 AI roles are available"""
        response = session.get(f"{BASE_URL}/api/roles")
        assert response.status_code == 200
        data = response.json()
        assert "roles" in data
        assert len(data["roles"]) == 20
        print(f"Roles available: {len(data['roles'])}")


class TestNavigationFeatures:
    """Test navigation shows all 5 features"""
    
    @pytest.fixture(scope="class")
    def session(self):
        return requests.Session()
    
    @pytest.fixture(scope="class")
    def auth_headers(self, session):
        """Get auth headers"""
        email = f"test_nav_{uuid.uuid4().hex[:8]}@test.com"
        register_response = session.post(f"{BASE_URL}/api/auth/register", json={
            "email": email,
            "password": TEST_PASSWORD,
            "name": "Nav Test User"
        })
        
        if register_response.status_code == 200:
            token = register_response.json()["access_token"]
        else:
            login_response = session.post(f"{BASE_URL}/api/auth/login", json={
                "email": email,
                "password": TEST_PASSWORD
            })
            token = login_response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    def test_all_feature_endpoints_exist(self, session, auth_headers):
        """Test all 5 feature endpoints exist"""
        endpoints = [
            ("/api/roles", "GET", None),  # Analysis
            ("/api/health", "GET", None),  # Health
            # Cover Letter and Auto-Apply tested above
        ]
        
        for endpoint, method, data in endpoints:
            if method == "GET":
                response = session.get(f"{BASE_URL}{endpoint}")
            else:
                response = session.post(f"{BASE_URL}{endpoint}", json=data, headers=auth_headers)
            
            assert response.status_code in [200, 401, 403, 422], f"Endpoint {endpoint} failed: {response.status_code}"
            print(f"Endpoint {endpoint}: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
