"""
Comprehensive Backend API Tests for CareerLift AI Career Transition Platform
Iteration 4 - Testing CV Generator, Learning Path, Analytics, User Profile APIs
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://careershift-app.preview.emergentagent.com').rstrip('/')

# Test credentials
TEST_USER_EMAIL = "test2@test.com"
TEST_USER_PASSWORD = "test123"


class TestAuthentication:
    """Authentication endpoint tests"""
    
    def test_login_success(self):
        """Test successful login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == TEST_USER_EMAIL
        assert data["user"]["subscription_tier"] == "pro"  # Pro user
        print(f"✓ Login successful - User: {data['user']['name']}, Tier: {data['user']['subscription_tier']}")
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        print("✓ Invalid credentials correctly rejected")


class TestRolesAPI:
    """AI Roles endpoint tests"""
    
    def test_get_all_roles(self):
        """Test getting all 20 AI roles"""
        response = requests.get(f"{BASE_URL}/api/roles")
        assert response.status_code == 200
        data = response.json()
        assert "roles" in data
        assert len(data["roles"]) == 20
        print(f"✓ Retrieved {len(data['roles'])} AI roles")
    
    def test_get_roles_with_location(self):
        """Test getting roles with location-specific salary"""
        response = requests.get(f"{BASE_URL}/api/roles?location=india")
        assert response.status_code == 200
        data = response.json()
        assert "roles" in data
        # Check that local_salary is present
        for role in data["roles"]:
            if "salary" in role and "india" in role["salary"]:
                assert "local_salary" in role
                break
        print("✓ Roles with location-specific salary retrieved")


class TestCoursesAPI:
    """Courses endpoint tests"""
    
    def test_get_all_courses(self):
        """Test getting all courses with real URLs"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        data = response.json()
        assert "courses" in data
        courses = data["courses"]
        assert len(courses) >= 28  # Should have 28 real courses
        
        # Verify course structure
        for course_id, course in courses.items():
            assert "name" in course
            assert "url" in course
            assert "platform" in course
            assert course["url"].startswith("http")  # Real URLs
        
        print(f"✓ Retrieved {len(courses)} courses with real URLs")
    
    def test_course_urls_are_real(self):
        """Verify course URLs are real (Coursera, Fast.ai, etc.)"""
        response = requests.get(f"{BASE_URL}/api/courses")
        data = response.json()
        courses = data["courses"]
        
        expected_platforms = ["Coursera", "Fast.ai", "DeepLearning.AI", "Hugging Face", "Kaggle", "Stanford", "AWS", "Google"]
        found_platforms = set()
        
        for course_id, course in courses.items():
            found_platforms.add(course.get("platform", "").split()[0])
        
        # Check that we have courses from multiple platforms
        assert len(found_platforms) >= 5
        print(f"✓ Courses from platforms: {', '.join(list(found_platforms)[:8])}")


class TestUserProfileAPI:
    """User Profile endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.json().get("access_token")
    
    def test_get_user_profile(self, auth_token):
        """Test /api/user/profile returns complete user data"""
        response = requests.get(
            f"{BASE_URL}/api/user/profile",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify user data
        assert "user" in data
        assert data["user"]["email"] == TEST_USER_EMAIL
        
        # Verify subscription data
        assert "subscription" in data
        assert "tier" in data["subscription"]
        assert "is_pro" in data["subscription"]
        
        # Verify credits
        assert "credits" in data
        assert "cv_credits" in data["credits"]
        assert "learning_path_credits" in data["credits"]
        assert "analysis_credits" in data["credits"]
        
        # Verify usage
        assert "usage" in data
        assert "cv_generations" in data["usage"]
        assert "learning_paths" in data["usage"]
        assert "analyses" in data["usage"]
        
        print(f"✓ User profile complete - Tier: {data['subscription']['tier']}, CV Credits: {data['credits']['cv_credits']}")
    
    def test_profile_requires_auth(self):
        """Test that profile endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/user/profile")
        assert response.status_code in [401, 403]
        print("✓ Profile endpoint correctly requires authentication")


class TestAnalyticsDashboardAPI:
    """Analytics Dashboard endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.json().get("access_token")
    
    def test_get_analytics_dashboard(self, auth_token):
        """Test /api/analytics/dashboard returns usage analytics"""
        response = requests.get(
            f"{BASE_URL}/api/analytics/dashboard",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify analytics fields
        assert "cv_generations" in data
        assert "learning_paths" in data
        assert "analyses" in data
        assert "total_downloads" in data
        assert "downloads_by_format" in data
        assert "course_clicks" in data
        
        print(f"✓ Analytics dashboard - CVs: {data['cv_generations']}, Paths: {data['learning_paths']}, Downloads: {data['total_downloads']}")
    
    def test_analytics_requires_auth(self):
        """Test that analytics endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/analytics/dashboard")
        assert response.status_code in [401, 403]
        print("✓ Analytics endpoint correctly requires authentication")


class TestUsageAPI:
    """Usage tracking endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.json().get("access_token")
    
    def test_get_usage(self, auth_token):
        """Test /api/usage returns all usage fields"""
        response = requests.get(
            f"{BASE_URL}/api/usage",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        assert "cv_generations_used" in data
        assert "cv_generations_limit" in data
        assert "learning_paths_used" in data
        assert "learning_paths_limit" in data
        assert "analyses_used" in data
        assert "analyses_limit" in data
        assert "cv_credits" in data
        assert "learning_path_credits" in data
        
        # Pro user should have high limits
        assert data["cv_generations_limit"] == 999
        assert data["learning_paths_limit"] == 999
        assert data["analyses_limit"] == 999
        
        print(f"✓ Usage stats - CV: {data['cv_generations_used']}/{data['cv_generations_limit']}, Credits: {data['cv_credits']}")


class TestCVHistoryAPI:
    """CV History endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.json().get("access_token")
    
    def test_get_cv_history(self, auth_token):
        """Test /api/cv/history returns CV generations array"""
        response = requests.get(
            f"{BASE_URL}/api/cv/history",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "cv_generations" in data
        assert isinstance(data["cv_generations"], list)
        print(f"✓ CV history retrieved - {len(data['cv_generations'])} CVs")


class TestLearningPathHistoryAPI:
    """Learning Path History endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.json().get("access_token")
    
    def test_get_learning_path_history(self, auth_token):
        """Test /api/learning-path/history returns learning paths array"""
        response = requests.get(
            f"{BASE_URL}/api/learning-path/history",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "learning_paths" in data
        assert isinstance(data["learning_paths"], list)
        print(f"✓ Learning path history retrieved - {len(data['learning_paths'])} paths")


class TestPaymentAPIs:
    """Payment endpoint tests (MOCKED)"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.json().get("access_token")
    
    def test_get_subscription(self, auth_token):
        """Test /api/payments/subscription returns subscription info"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "subscription_tier" in data
        assert "cv_credits" in data
        print(f"✓ Subscription info - Tier: {data['subscription_tier']}, CV Credits: {data['cv_credits']}")
    
    def test_get_pricing(self):
        """Test /api/payments/pricing returns pricing info"""
        response = requests.get(f"{BASE_URL}/api/payments/pricing")
        assert response.status_code == 200
        data = response.json()
        assert "pricing" in data
        assert "free_limits" in data
        assert "pro_monthly" in data["pricing"]
        assert "cv_single" in data["pricing"]
        assert "cv_bulk_50" in data["pricing"]
        print("✓ Pricing info retrieved")


class TestNavigationEndpoints:
    """Test all navigation-related endpoints"""
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "claude_configured" in data
        print(f"✓ Health check - Status: {data['status']}, Claude: {data['claude_configured']}")
    
    def test_root_endpoint(self):
        """Test root API endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✓ Root endpoint accessible")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
