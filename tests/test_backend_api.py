"""
Backend API Tests for CareerLift AI Career Transition Platform
Tests: Auth, Usage, Roles, CV History, Learning Path History, Payments
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://careershift-app.preview.emergentagent.com').rstrip('/')

# Test credentials
TEST_EMAIL = "test2@test.com"
TEST_PASSWORD = "test123"


class TestHealthAndRoles:
    """Test public endpoints - no auth required"""
    
    def test_roles_endpoint_returns_20_roles(self):
        """GET /api/roles should return 20 AI roles"""
        response = requests.get(f"{BASE_URL}/api/roles")
        assert response.status_code == 200
        data = response.json()
        assert "roles" in data
        assert len(data["roles"]) == 20
        
        # Verify role structure
        first_role = data["roles"][0]
        assert "id" in first_role
        assert "name" in first_role
        assert "description" in first_role
        assert "salary_range" in first_role
        assert "top_skills" in first_role
        assert "transition_weeks" in first_role
    
    def test_roles_with_location_parameter(self):
        """GET /api/roles?location=india should return roles with local salary"""
        response = requests.get(f"{BASE_URL}/api/roles?location=india")
        assert response.status_code == 200
        data = response.json()
        assert len(data["roles"]) == 20
        
        # Verify local_salary is present
        first_role = data["roles"][0]
        assert "local_salary" in first_role


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_login_success(self):
        """POST /api/auth/login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == TEST_EMAIL
        assert "subscription_tier" in data["user"]
    
    def test_login_invalid_credentials(self):
        """POST /api/auth/login with invalid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "invalid@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
    
    def test_register_duplicate_email(self):
        """POST /api/auth/register with existing email should fail"""
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": TEST_EMAIL,
            "password": "newpassword",
            "name": "Duplicate User"
        })
        assert response.status_code == 400


class TestUsageEndpoint:
    """Test usage tracking endpoint - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Authentication failed")
    
    def test_usage_endpoint_returns_all_fields(self, auth_token):
        """GET /api/usage should return cv_credits and learning_path_credits"""
        response = requests.get(
            f"{BASE_URL}/api/usage",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields are present
        assert "cv_generations_used" in data
        assert "cv_generations_limit" in data
        assert "learning_paths_used" in data
        assert "learning_paths_limit" in data
        assert "analyses_used" in data
        assert "analyses_limit" in data
        
        # CRITICAL: These fields were missing before the fix
        assert "cv_credits" in data
        assert "learning_path_credits" in data
        
        # Verify data types
        assert isinstance(data["cv_credits"], int)
        assert isinstance(data["learning_path_credits"], int)
    
    def test_usage_without_auth_fails(self):
        """GET /api/usage without auth should return 403"""
        response = requests.get(f"{BASE_URL}/api/usage")
        assert response.status_code == 403


class TestCVHistory:
    """Test CV history endpoint - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Authentication failed")
    
    def test_cv_history_endpoint(self, auth_token):
        """GET /api/cv/history should return cv_generations array"""
        response = requests.get(
            f"{BASE_URL}/api/cv/history",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "cv_generations" in data
        assert isinstance(data["cv_generations"], list)
    
    def test_cv_history_without_auth_fails(self):
        """GET /api/cv/history without auth should return 403"""
        response = requests.get(f"{BASE_URL}/api/cv/history")
        assert response.status_code == 403


class TestLearningPathHistory:
    """Test learning path history endpoint - requires auth"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Authentication failed")
    
    def test_learning_path_history_endpoint(self, auth_token):
        """GET /api/learning-path/history should return learning_paths array"""
        response = requests.get(
            f"{BASE_URL}/api/learning-path/history",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "learning_paths" in data
        assert isinstance(data["learning_paths"], list)
    
    def test_learning_path_history_without_auth_fails(self):
        """GET /api/learning-path/history without auth should return 403"""
        response = requests.get(f"{BASE_URL}/api/learning-path/history")
        assert response.status_code == 403


class TestPaymentEndpoints:
    """Test payment endpoints - MOCKED"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Authentication failed")
    
    def test_subscription_endpoint(self, auth_token):
        """GET /api/payments/subscription should return subscription info"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "subscription_tier" in data
        assert "cv_credits" in data
        assert "learning_path_credits" in data
    
    def test_mock_upgrade_endpoint(self, auth_token):
        """POST /api/payments/mock-upgrade should upgrade user to pro (MOCKED)"""
        response = requests.post(
            f"{BASE_URL}/api/payments/mock-upgrade",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_mock_purchase_endpoint(self, auth_token):
        """POST /api/payments/mock-purchase should add credits (MOCKED)"""
        response = requests.post(
            f"{BASE_URL}/api/payments/mock-purchase?product_type=cv_single",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
