"""
Test Interactive Learning Path Features
- Course progress tracking (POST/GET /api/learning-path/{path_id}/course-progress)
- Saved courses (POST/GET/DELETE /api/user/saved-courses)
- All learning paths progress (GET /api/learning-path/all-progress)
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "test"


class TestConfig:
    """Test configuration and setup"""
    
    def test_base_url_configured(self):
        """Verify BASE_URL is configured"""
        assert BASE_URL, "REACT_APP_BACKEND_URL must be set"
        print(f"✓ BASE_URL configured: {BASE_URL}")
    
    def test_health_check(self):
        """Verify backend is healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print(f"✓ Backend healthy: {data}")


class TestAuthentication:
    """Authentication tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        return data["access_token"]
    
    def test_login_success(self):
        """Test login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        print(f"✓ Login successful for {TEST_EMAIL}")


class TestCourseProgressEndpoints:
    """Test course progress tracking endpoints"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authenticated headers"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.fixture
    def learning_path_id(self, auth_headers):
        """Get or create a learning path for testing"""
        # First check if user has any learning paths
        response = requests.get(
            f"{BASE_URL}/api/learning-path/history",
            headers=auth_headers
        )
        if response.status_code == 200:
            paths = response.json().get("learning_paths", [])
            if paths:
                return paths[0]["id"]
        
        # If no paths exist, we'll skip tests that require a path
        pytest.skip("No learning path available for testing - generate one first")
    
    def test_course_progress_endpoint_requires_auth(self):
        """Test that course progress endpoint requires authentication"""
        response = requests.post(
            f"{BASE_URL}/api/learning-path/test-path-id/course-progress",
            json={"week": 1, "course_index": 0, "completed": True}
        )
        assert response.status_code in [401, 403]
        print("✓ Course progress endpoint requires authentication")
    
    def test_course_progress_get_requires_auth(self):
        """Test that GET course progress requires authentication"""
        response = requests.get(
            f"{BASE_URL}/api/learning-path/test-path-id/course-progress"
        )
        assert response.status_code in [401, 403]
        print("✓ GET course progress requires authentication")
    
    def test_course_progress_invalid_path(self, auth_headers):
        """Test course progress with invalid path ID"""
        response = requests.post(
            f"{BASE_URL}/api/learning-path/invalid-path-id/course-progress",
            headers=auth_headers,
            json={"week": 1, "course_index": 0, "completed": True}
        )
        assert response.status_code == 404
        print("✓ Invalid path ID returns 404")
    
    def test_get_course_progress_invalid_path(self, auth_headers):
        """Test GET course progress with invalid path ID"""
        response = requests.get(
            f"{BASE_URL}/api/learning-path/invalid-path-id/course-progress",
            headers=auth_headers
        )
        assert response.status_code == 404
        print("✓ GET course progress with invalid path returns 404")
    
    def test_update_course_progress_success(self, auth_headers, learning_path_id):
        """Test marking a course as complete"""
        response = requests.post(
            f"{BASE_URL}/api/learning-path/{learning_path_id}/course-progress",
            headers=auth_headers,
            json={"week": 1, "course_index": 0, "completed": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "week_completed" in data
        assert "overall_progress" in data
        assert "total_courses_completed" in data
        assert "total_courses" in data
        print(f"✓ Course marked complete: {data['message']}")
        print(f"  - Week completed: {data['week_completed']}")
        print(f"  - Overall progress: {data['overall_progress']}%")
        print(f"  - Courses completed: {data['total_courses_completed']}/{data['total_courses']}")
    
    def test_get_course_progress_success(self, auth_headers, learning_path_id):
        """Test getting course progress"""
        response = requests.get(
            f"{BASE_URL}/api/learning-path/{learning_path_id}/course-progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "course_progress" in data
        assert "week_progress" in data
        assert "stats" in data
        assert "total_courses" in data["stats"]
        assert "completed_courses" in data["stats"]
        print(f"✓ Course progress retrieved successfully")
        print(f"  - Stats: {data['stats']}")
    
    def test_toggle_course_incomplete(self, auth_headers, learning_path_id):
        """Test marking a course as incomplete"""
        response = requests.post(
            f"{BASE_URL}/api/learning-path/{learning_path_id}/course-progress",
            headers=auth_headers,
            json={"week": 1, "course_index": 0, "completed": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert "incomplete" in data["message"].lower()
        print(f"✓ Course marked incomplete: {data['message']}")


class TestSavedCoursesEndpoints:
    """Test saved courses CRUD endpoints"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authenticated headers"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.fixture
    def test_course_data(self):
        """Generate unique test course data"""
        unique_id = uuid.uuid4().hex[:8]
        return {
            "course_name": f"TEST_Course_{unique_id}",
            "course_url": f"https://test.com/course/{unique_id}",
            "platform": "Test Platform",
            "week": 1,
            "learning_path_id": f"test-path-{unique_id}",
            "notes": "Test notes"
        }
    
    def test_saved_courses_requires_auth(self):
        """Test that saved courses endpoints require authentication"""
        # POST
        response = requests.post(
            f"{BASE_URL}/api/user/saved-courses",
            json={"course_name": "Test", "course_url": "http://test.com", "platform": "Test", "week": 1, "learning_path_id": "test"}
        )
        assert response.status_code in [401, 403]
        
        # GET
        response = requests.get(f"{BASE_URL}/api/user/saved-courses")
        assert response.status_code in [401, 403]
        
        # DELETE
        response = requests.delete(f"{BASE_URL}/api/user/saved-courses/test-id")
        assert response.status_code in [401, 403]
        
        print("✓ All saved courses endpoints require authentication")
    
    def test_save_course_success(self, auth_headers, test_course_data):
        """Test saving a course to profile"""
        response = requests.post(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers,
            json=test_course_data
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "course" in data
        assert data["course"]["course_name"] == test_course_data["course_name"]
        assert data["course"]["course_url"] == test_course_data["course_url"]
        assert "id" in data["course"]
        print(f"✓ Course saved successfully: {data['course']['course_name']}")
        return data["course"]["id"]
    
    def test_save_duplicate_course_fails(self, auth_headers, test_course_data):
        """Test that saving duplicate course fails"""
        # Save first time
        response1 = requests.post(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers,
            json=test_course_data
        )
        assert response1.status_code == 200
        
        # Try to save again
        response2 = requests.post(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers,
            json=test_course_data
        )
        assert response2.status_code == 400
        assert "already saved" in response2.json().get("detail", "").lower()
        print("✓ Duplicate course save correctly rejected")
    
    def test_get_saved_courses(self, auth_headers):
        """Test getting all saved courses"""
        response = requests.get(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "saved_courses" in data
        assert isinstance(data["saved_courses"], list)
        print(f"✓ Retrieved {len(data['saved_courses'])} saved courses")
    
    def test_delete_saved_course(self, auth_headers, test_course_data):
        """Test deleting a saved course"""
        # First save a course
        save_response = requests.post(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers,
            json=test_course_data
        )
        assert save_response.status_code == 200
        course_id = save_response.json()["course"]["id"]
        
        # Delete the course
        delete_response = requests.delete(
            f"{BASE_URL}/api/user/saved-courses/{course_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == 200
        assert "removed" in delete_response.json().get("message", "").lower()
        print(f"✓ Course deleted successfully: {course_id}")
    
    def test_delete_nonexistent_course(self, auth_headers):
        """Test deleting a course that doesn't exist"""
        response = requests.delete(
            f"{BASE_URL}/api/user/saved-courses/nonexistent-id",
            headers=auth_headers
        )
        assert response.status_code == 404
        print("✓ Delete nonexistent course returns 404")
    
    def test_mark_saved_course_complete(self, auth_headers, test_course_data):
        """Test marking a saved course as complete"""
        # First save a course
        save_response = requests.post(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers,
            json=test_course_data
        )
        assert save_response.status_code == 200
        course_id = save_response.json()["course"]["id"]
        
        # Mark as complete
        complete_response = requests.patch(
            f"{BASE_URL}/api/user/saved-courses/{course_id}/complete",
            headers=auth_headers
        )
        assert complete_response.status_code == 200
        assert "complete" in complete_response.json().get("message", "").lower()
        print(f"✓ Saved course marked complete: {course_id}")


class TestAllProgressEndpoint:
    """Test the all learning paths progress endpoint"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authenticated headers"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_all_progress_requires_auth(self):
        """Test that all-progress endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/learning-path/all-progress")
        assert response.status_code in [401, 403]
        print("✓ All-progress endpoint requires authentication")
    
    def test_get_all_progress(self, auth_headers):
        """Test getting progress for all learning paths"""
        response = requests.get(
            f"{BASE_URL}/api/learning-path/all-progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "learning_paths" in data
        assert isinstance(data["learning_paths"], list)
        
        # Verify structure of each path summary
        for path in data["learning_paths"]:
            assert "id" in path
            assert "target_role" in path
            assert "overall_progress" in path
            assert "completed_weeks" in path
            assert "total_weeks" in path
            assert "completed_courses" in path
            assert "total_courses" in path
        
        print(f"✓ Retrieved progress for {len(data['learning_paths'])} learning paths")
        for path in data["learning_paths"][:3]:  # Show first 3
            print(f"  - {path['target_role']}: {path['overall_progress']}% ({path['completed_courses']}/{path['total_courses']} courses)")


class TestModuleStructure:
    """Test that new module structure is working"""
    
    def test_config_module_exists(self):
        """Verify config.py module exists and is importable"""
        import sys
        sys.path.insert(0, '/app/backend')
        try:
            from config import MONGO_URL, DB_NAME, JWT_SECRET
            assert MONGO_URL
            assert DB_NAME
            assert JWT_SECRET
            print("✓ config.py module working correctly")
        except ImportError as e:
            pytest.fail(f"config.py import failed: {e}")
    
    def test_database_module_exists(self):
        """Verify database.py module exists"""
        import sys
        sys.path.insert(0, '/app/backend')
        try:
            from database import db, client
            assert db is not None
            assert client is not None
            print("✓ database.py module working correctly")
        except ImportError as e:
            pytest.fail(f"database.py import failed: {e}")
    
    def test_auth_module_exists(self):
        """Verify auth.py module exists"""
        import sys
        sys.path.insert(0, '/app/backend')
        try:
            from auth import hash_password, verify_password, create_token
            assert callable(hash_password)
            assert callable(verify_password)
            assert callable(create_token)
            print("✓ auth.py module working correctly")
        except ImportError as e:
            pytest.fail(f"auth.py import failed: {e}")
    
    def test_models_directory_exists(self):
        """Verify models directory exists with expected files"""
        import os
        models_dir = '/app/backend/models'
        assert os.path.isdir(models_dir), "models directory should exist"
        
        expected_files = ['__init__.py', 'learning_path.py', 'user.py']
        for f in expected_files:
            assert os.path.isfile(os.path.join(models_dir, f)), f"models/{f} should exist"
        print(f"✓ models/ directory structure correct")
    
    def test_services_directory_exists(self):
        """Verify services directory exists"""
        import os
        services_dir = '/app/backend/services'
        assert os.path.isdir(services_dir), "services directory should exist"
        assert os.path.isfile(os.path.join(services_dir, 'job_discovery.py')), "job_discovery.py should exist"
        print("✓ services/ directory structure correct")


class TestCleanup:
    """Cleanup test data"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authenticated headers"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_cleanup_test_courses(self, auth_headers):
        """Clean up TEST_ prefixed saved courses"""
        # Get all saved courses
        response = requests.get(
            f"{BASE_URL}/api/user/saved-courses",
            headers=auth_headers
        )
        if response.status_code == 200:
            courses = response.json().get("saved_courses", [])
            deleted = 0
            for course in courses:
                if course.get("course_name", "").startswith("TEST_"):
                    del_response = requests.delete(
                        f"{BASE_URL}/api/user/saved-courses/{course['id']}",
                        headers=auth_headers
                    )
                    if del_response.status_code == 200:
                        deleted += 1
            print(f"✓ Cleaned up {deleted} test courses")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
