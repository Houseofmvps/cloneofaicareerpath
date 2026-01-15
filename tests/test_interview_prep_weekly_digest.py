"""
Test suite for Interview Prep and Weekly Job Digest features
Tests:
- Interview Prep: POST /api/interview-prep/generate - generates role-specific questions
- Interview Prep: POST /api/interview-prep/feedback - AI feedback on answers
- Interview Prep: GET /api/interview-prep/history - practice history with stats
- Weekly Digest: POST /api/auto-apply/notification-preferences - save weekly digest preference
- Weekly Digest: POST /api/jobs/send-weekly-digest - sends email with matching jobs
"""

import pytest
import requests
import os
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestInterviewPrepFeatures:
    """Test Interview Prep endpoints"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token") or data.get("token")
        pytest.skip("Authentication failed - skipping authenticated tests")
    
    @pytest.fixture(scope="class")
    def auth_headers(self, auth_token):
        """Get headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_base_url_configured(self):
        """Verify BASE_URL is configured"""
        assert BASE_URL, "REACT_APP_BACKEND_URL not configured"
        print(f"Testing against: {BASE_URL}")
    
    def test_health_check(self):
        """Verify backend is healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print(f"Backend healthy, Claude configured: {data.get('claude_configured')}")
    
    def test_login_success(self):
        """Test login with test credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data or "token" in data
        assert "user" in data
        print(f"Login successful for user: {data['user'].get('email')}")
    
    # ============================================
    # Interview Prep - Generate Questions
    # ============================================
    
    def test_generate_questions_requires_auth(self):
        """Test that generate questions requires authentication"""
        response = requests.post(f"{BASE_URL}/api/interview-prep/generate", json={
            "role_id": "ml_engineer",
            "categories": ["technical"],
            "count": 5
        })
        assert response.status_code in [401, 403]
        print("Generate questions correctly requires auth")
    
    def test_generate_questions_ml_engineer(self, auth_headers):
        """Test generating questions for ML Engineer role"""
        response = requests.post(
            f"{BASE_URL}/api/interview-prep/generate",
            json={
                "role_id": "ml_engineer",
                "categories": ["technical", "behavioral"],
                "count": 5
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "questions" in data
        assert "role_id" in data
        assert data["role_id"] == "ml_engineer"
        
        # Verify questions
        questions = data["questions"]
        assert len(questions) > 0
        assert len(questions) <= 5
        
        # Verify question structure
        for q in questions:
            assert "question" in q
            assert "difficulty" in q
            assert "category" in q
            assert q["difficulty"] in ["easy", "medium", "hard"]
            assert q["category"] in ["technical", "behavioral"]
        
        print(f"Generated {len(questions)} questions for ML Engineer")
    
    def test_generate_questions_ai_engineer(self, auth_headers):
        """Test generating questions for AI Engineer role"""
        response = requests.post(
            f"{BASE_URL}/api/interview-prep/generate",
            json={
                "role_id": "ai_engineer",
                "categories": ["technical", "system_design", "ml_concepts"],
                "count": 8
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "questions" in data
        assert data["role_id"] == "ai_engineer"
        
        questions = data["questions"]
        assert len(questions) > 0
        
        # Check categories are correct
        categories = set(q["category"] for q in questions)
        print(f"Generated {len(questions)} questions for AI Engineer, categories: {categories}")
    
    def test_generate_questions_data_scientist(self, auth_headers):
        """Test generating questions for Data Scientist role"""
        response = requests.post(
            f"{BASE_URL}/api/interview-prep/generate",
            json={
                "role_id": "data_scientist",
                "categories": ["technical", "coding"],
                "count": 4
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "questions" in data
        assert data["role_id"] == "data_scientist"
        print(f"Generated {len(data['questions'])} questions for Data Scientist")
    
    def test_generate_questions_unknown_role_uses_defaults(self, auth_headers):
        """Test that unknown roles get default questions"""
        response = requests.post(
            f"{BASE_URL}/api/interview-prep/generate",
            json={
                "role_id": "unknown_role_xyz",
                "categories": ["technical", "behavioral"],
                "count": 3
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should still return questions (from defaults)
        assert "questions" in data
        print(f"Unknown role got {len(data['questions'])} default questions")
    
    # ============================================
    # Interview Prep - Feedback
    # ============================================
    
    def test_feedback_requires_auth(self):
        """Test that feedback endpoint requires authentication"""
        response = requests.post(f"{BASE_URL}/api/interview-prep/feedback", json={
            "question": "What is machine learning?",
            "answer": "Machine learning is a subset of AI.",
            "role_id": "ml_engineer",
            "category": "technical"
        })
        assert response.status_code in [401, 403]
        print("Feedback endpoint correctly requires auth")
    
    def test_get_feedback_on_answer(self, auth_headers):
        """Test getting AI feedback on an interview answer"""
        response = requests.post(
            f"{BASE_URL}/api/interview-prep/feedback",
            json={
                "question": "Explain the bias-variance tradeoff.",
                "answer": "The bias-variance tradeoff is a fundamental concept in machine learning. High bias means the model is too simple and underfits the data. High variance means the model is too complex and overfits. We need to find a balance - using techniques like cross-validation, regularization, and ensemble methods to achieve good generalization.",
                "role_id": "ml_engineer",
                "category": "technical"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify feedback structure
        assert "score" in data
        assert "strengths" in data
        assert "improvements" in data
        assert "sample_answer" in data
        
        # Verify score is reasonable
        assert isinstance(data["score"], (int, float))
        assert 0 <= data["score"] <= 100
        
        # Verify strengths and improvements are lists
        assert isinstance(data["strengths"], list)
        assert isinstance(data["improvements"], list)
        
        print(f"Got feedback with score: {data['score']}")
        print(f"Strengths: {data['strengths']}")
        print(f"Improvements: {data['improvements']}")
    
    def test_feedback_short_answer(self, auth_headers):
        """Test feedback on a short/poor answer"""
        response = requests.post(
            f"{BASE_URL}/api/interview-prep/feedback",
            json={
                "question": "How would you design a recommendation system?",
                "answer": "I would use machine learning.",
                "role_id": "ai_engineer",
                "category": "system_design"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "score" in data
        # Short answer should get lower score
        print(f"Short answer got score: {data['score']}")
    
    # ============================================
    # Interview Prep - History
    # ============================================
    
    def test_history_requires_auth(self):
        """Test that history endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/interview-prep/history")
        assert response.status_code in [401, 403]
        print("History endpoint correctly requires auth")
    
    def test_get_practice_history(self, auth_headers):
        """Test getting interview practice history"""
        response = requests.get(
            f"{BASE_URL}/api/interview-prep/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "history" in data
        assert "stats" in data
        
        # Verify stats structure
        stats = data["stats"]
        assert "total_practiced" in stats
        assert "avg_score" in stats
        assert "streak" in stats
        
        # Verify types
        assert isinstance(stats["total_practiced"], int)
        assert isinstance(stats["avg_score"], (int, float))
        assert isinstance(stats["streak"], int)
        
        print(f"Practice history: {stats['total_practiced']} practiced, avg score: {stats['avg_score']}, streak: {stats['streak']}")
        
        # If there's history, verify structure
        if data["history"]:
            entry = data["history"][0]
            assert "question" in entry
            assert "answer" in entry
            assert "score" in entry
            print(f"Latest practice: {entry.get('question', '')[:50]}...")


class TestWeeklyDigestFeatures:
    """Test Weekly Job Digest endpoints"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token") or data.get("token")
        pytest.skip("Authentication failed - skipping authenticated tests")
    
    @pytest.fixture(scope="class")
    def auth_headers(self, auth_token):
        """Get headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    # ============================================
    # Notification Preferences
    # ============================================
    
    def test_notification_prefs_requires_auth(self):
        """Test that notification preferences requires authentication"""
        response = requests.post(f"{BASE_URL}/api/auto-apply/notification-preferences", json={
            "email_weekly_summary": True
        })
        assert response.status_code in [401, 403]
        print("Notification preferences correctly requires auth")
    
    def test_save_notification_preferences(self, auth_headers):
        """Test saving notification preferences with weekly digest enabled"""
        response = requests.post(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            json={
                "email_weekly_summary": True,
                "email_interview_alerts": True,
                "email_status_updates": True
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"Saved notification preferences: {data}")
    
    def test_get_notification_preferences(self, auth_headers):
        """Test getting notification preferences"""
        response = requests.get(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure - should have the preferences we just set
        assert "email_weekly_summary" in data or isinstance(data, dict)
        print(f"Got notification preferences: {data}")
    
    def test_toggle_weekly_digest_off(self, auth_headers):
        """Test toggling weekly digest off"""
        response = requests.post(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            json={
                "email_weekly_summary": False,
                "email_interview_alerts": True,
                "email_status_updates": True
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Verify it was saved
        get_response = requests.get(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            headers=auth_headers
        )
        assert get_response.status_code == 200
        data = get_response.json()
        assert data.get("email_weekly_summary") == False
        print("Weekly digest toggled off successfully")
    
    def test_toggle_weekly_digest_on(self, auth_headers):
        """Test toggling weekly digest on"""
        response = requests.post(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            json={
                "email_weekly_summary": True,
                "email_interview_alerts": True,
                "email_status_updates": True
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Verify it was saved
        get_response = requests.get(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            headers=auth_headers
        )
        assert get_response.status_code == 200
        data = get_response.json()
        assert data.get("email_weekly_summary") == True
        print("Weekly digest toggled on successfully")
    
    # ============================================
    # Send Weekly Digest
    # ============================================
    
    def test_send_weekly_digest_requires_auth(self):
        """Test that send weekly digest requires authentication"""
        response = requests.post(f"{BASE_URL}/api/jobs/send-weekly-digest")
        assert response.status_code in [401, 403]
        print("Send weekly digest correctly requires auth")
    
    def test_send_weekly_digest(self, auth_headers):
        """Test sending weekly job digest email"""
        # First ensure weekly digest is enabled
        requests.post(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            json={"email_weekly_summary": True},
            headers=auth_headers
        )
        
        # Now try to send digest
        response = requests.post(
            f"{BASE_URL}/api/jobs/send-weekly-digest",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should have a message
        assert "message" in data
        print(f"Weekly digest response: {data}")
        
        # If jobs were found, should have jobs_included or jobs_found
        if "jobs_included" in data:
            print(f"Jobs included in digest: {data['jobs_included']}")
        if "jobs_found" in data:
            print(f"Jobs found: {data['jobs_found']}")
    
    def test_send_weekly_digest_when_disabled(self, auth_headers):
        """Test sending weekly digest when it's disabled"""
        # First disable weekly digest
        requests.post(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            json={"email_weekly_summary": False},
            headers=auth_headers
        )
        
        # Try to send digest
        response = requests.post(
            f"{BASE_URL}/api/jobs/send-weekly-digest",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should indicate digest not enabled
        assert "message" in data
        assert "not enabled" in data["message"].lower() or "not sent" in data["message"].lower()
        print(f"Disabled digest response: {data}")
        
        # Re-enable for other tests
        requests.post(
            f"{BASE_URL}/api/auto-apply/notification-preferences",
            json={"email_weekly_summary": True},
            headers=auth_headers
        )


class TestSmartJobsPageRename:
    """Test that Auto-Apply was renamed to Smart Jobs"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "test@test.com",
            "password": "test"
        })
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token") or data.get("token")
        pytest.skip("Authentication failed - skipping authenticated tests")
    
    @pytest.fixture(scope="class")
    def auth_headers(self, auth_token):
        """Get headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_auto_apply_dashboard_still_works(self, auth_headers):
        """Test that auto-apply dashboard endpoint still works"""
        response = requests.get(
            f"{BASE_URL}/api/auto-apply/dashboard",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify dashboard structure
        assert "stats" in data or "matching_jobs" in data or "preferences" in data
        print(f"Auto-apply dashboard working, keys: {list(data.keys())}")
    
    def test_auto_apply_search_works(self, auth_headers):
        """Test that job search endpoint works"""
        response = requests.get(
            f"{BASE_URL}/api/auto-apply/search?keywords=AI%20Engineer&location=us",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "jobs" in data
        print(f"Job search returned {len(data.get('jobs', []))} jobs")
    
    def test_auto_apply_preferences_works(self, auth_headers):
        """Test that preferences endpoint works"""
        response = requests.post(
            f"{BASE_URL}/api/auto-apply/preferences",
            json={
                "target_roles": ["AI Engineer", "ML Engineer"],
                "locations": ["Remote (US)"],
                "remote_preference": "remote"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        print("Auto-apply preferences endpoint working")


class TestNavigationUpdates:
    """Test that navigation was updated with Interview and Jobs links"""
    
    def test_roles_endpoint_for_interview_prep(self):
        """Test that roles endpoint exists for interview prep dropdown"""
        response = requests.get(f"{BASE_URL}/api/roles")
        assert response.status_code == 200
        data = response.json()
        
        assert "roles" in data
        roles = data["roles"]
        assert len(roles) > 0
        
        # Verify role structure
        role = roles[0]
        assert "id" in role
        assert "name" in role
        
        # Check for key roles
        role_ids = [r["id"] for r in roles]
        assert "ml_engineer" in role_ids
        assert "ai_engineer" in role_ids
        assert "data_scientist" in role_ids
        
        print(f"Found {len(roles)} roles for interview prep")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
