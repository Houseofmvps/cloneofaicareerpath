"""
Test CV Generation - Verify clean text output without markdown formatting
Tests the fix for CV generation that was producing markdown asterisks and missing headers
"""
import pytest
import requests
import os
import re
import json

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://careershift-app.preview.emergentagent.com').rstrip('/')

# Sample resume text for testing
SAMPLE_RESUME = """
John Smith
john.smith@email.com | (415) 555-1234 | San Francisco, CA

PROFESSIONAL SUMMARY
Senior Software Engineer with 6 years of experience building scalable backend systems.
Passionate about AI and machine learning, with hands-on experience in LLM integration and prompt engineering.

EXPERIENCE

Senior Software Engineer | TechCorp Inc | San Francisco, CA
January 2021 - Present
- Built automated documentation system using OpenAI GPT API
- Developed intelligent chatbot using GPT-4 and LangChain
- Led backend architecture for platform serving 200K+ users

Software Engineer | StartupXYZ | San Jose, CA
June 2018 - December 2020
- Developed RESTful APIs using Python and FastAPI
- Implemented microservices architecture on AWS
- Reduced API latency by 40%

EDUCATION
Bachelor of Science in Computer Science
Stanford University | Graduated 2018

SKILLS
Python, JavaScript, Java, SQL, AWS, Docker, Kubernetes, FastAPI, Django, 
Machine Learning, TensorFlow, PyTorch, LLM, GPT, Prompt Engineering, RAG
"""


# Global variable to cache CV generation result
_cv_generation_result = None
_auth_token = None


def get_auth_token():
    """Get or create authentication token"""
    global _auth_token
    if _auth_token:
        return _auth_token
    
    # Create a unique test user
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    email = f"cvtest_{unique_id}@test.com"
    
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={"email": email, "password": "testpass123", "name": f"CV Test User {unique_id}"}
    )
    
    if response.status_code == 200:
        _auth_token = response.json()["access_token"]
        return _auth_token
    
    raise Exception(f"Could not create test user: {response.text}")


def get_cv_generation_result():
    """Get cached CV generation result or generate new one"""
    global _cv_generation_result
    if _cv_generation_result:
        return _cv_generation_result
    
    token = get_auth_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/cv/generate",
        headers=headers,
        json={
            "resume_text": SAMPLE_RESUME,
            "target_role_id": "prompt_engineer",
            "current_role": "Senior Software Engineer",
            "years_experience": 6,
            "skills": ["Python", "JavaScript", "AWS", "LLM", "GPT"]
        }
    )
    
    if response.status_code == 200:
        _cv_generation_result = response.json()
        return _cv_generation_result
    
    raise Exception(f"CV generation failed: {response.status_code} - {response.text}")


class TestCVGenerationCleanOutput:
    """Test that CV generation produces clean text without markdown"""
    
    def test_health_check(self):
        """Verify backend is healthy and Claude is configured"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["claude_configured"] == True, "Claude API must be configured for CV generation"
    
    def test_roles_endpoint(self):
        """Verify roles endpoint returns available AI roles"""
        response = requests.get(f"{BASE_URL}/api/roles")
        assert response.status_code == 200
        data = response.json()
        assert "roles" in data
        assert len(data["roles"]) > 0
        # Check that prompt_engineer role exists
        role_ids = [r["id"] for r in data["roles"]]
        assert "prompt_engineer" in role_ids, "Prompt Engineer role should be available"
    
    def test_cv_generation_returns_data(self):
        """Test that CV generation returns valid data"""
        data = get_cv_generation_result()
        assert data is not None, "CV generation should return data"
        print(f"CV generation returned keys: {list(data.keys())}")
    
    def test_cv_generation_has_natural_cv(self):
        """Test that response includes natural_cv"""
        data = get_cv_generation_result()
        assert "natural_cv" in data, "Response should include natural_cv"
        assert data["natural_cv"] is not None, "natural_cv should not be None"
    
    def test_cv_generation_has_ats_cv(self):
        """Test that response includes ats_cv"""
        data = get_cv_generation_result()
        assert "ats_cv" in data, "Response should include ats_cv"
        assert data["ats_cv"] is not None, "ats_cv should not be None"
    
    def test_natural_cv_has_header_with_name(self):
        """CRITICAL: Test that natural_cv has header with name"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        
        # Check header exists
        assert "header" in natural_cv, f"natural_cv should have header section. Keys: {list(natural_cv.keys())}"
        header = natural_cv["header"]
        
        # Check name exists in header
        assert "name" in header, "header should have name field"
        assert header["name"], "header.name should not be empty"
        print(f"Natural CV header name: {header['name']}")
    
    def test_natural_cv_has_header_with_contact(self):
        """CRITICAL: Test that natural_cv has header with contact info"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        header = natural_cv.get("header", {})
        
        # Check contact exists in header
        assert "contact" in header, "header should have contact field"
        assert header["contact"], "header.contact should not be empty"
        print(f"Natural CV header contact: {header['contact']}")
    
    def test_ats_cv_has_header_with_name(self):
        """CRITICAL: Test that ats_cv has header with name"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        
        # Check header exists
        assert "header" in ats_cv, f"ats_cv should have header section. Keys: {list(ats_cv.keys())}"
        header = ats_cv["header"]
        
        # Check name exists in header
        assert "name" in header, "header should have name field"
        assert header["name"], "header.name should not be empty"
        print(f"ATS CV header name: {header['name']}")
    
    def test_ats_cv_has_header_with_contact(self):
        """CRITICAL: Test that ats_cv has header with contact info"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        header = ats_cv.get("header", {})
        
        # Check contact exists in header
        assert "contact" in header, "header should have contact field"
        assert header["contact"], "header.contact should not be empty"
        print(f"ATS CV header contact: {header['contact']}")
    
    def test_natural_cv_summary_no_markdown(self):
        """CRITICAL: Test that natural_cv summary has NO markdown asterisks"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        summary = natural_cv.get("summary", "")
        
        # Check for markdown patterns
        assert "**" not in summary, f"Summary should NOT contain ** asterisks: {summary[:200]}"
        assert "##" not in summary, f"Summary should NOT contain ## headers: {summary[:200]}"
        print(f"Natural CV summary (first 200 chars): {summary[:200]}")
    
    def test_ats_cv_summary_no_markdown(self):
        """CRITICAL: Test that ats_cv summary has NO markdown asterisks"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        summary = ats_cv.get("summary", "")
        
        # Check for markdown patterns
        assert "**" not in summary, f"Summary should NOT contain ** asterisks: {summary[:200]}"
        assert "##" not in summary, f"Summary should NOT contain ## headers: {summary[:200]}"
        print(f"ATS CV summary (first 200 chars): {summary[:200]}")
    
    def test_natural_cv_experience_bullets_no_markdown(self):
        """CRITICAL: Test that experience bullets have NO markdown"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        experience = natural_cv.get("experience", [])
        
        markdown_found = []
        for exp in experience:
            bullets = exp.get("bullets", [])
            for bullet in bullets:
                if "**" in bullet:
                    markdown_found.append(f"** found in: {bullet[:100]}")
                if bullet and bullet[0] in ["*", "-", "•"]:
                    markdown_found.append(f"Bullet char at start: {bullet[:50]}")
        
        assert len(markdown_found) == 0, f"Markdown found in bullets: {markdown_found}"
        print(f"Checked {len(experience)} experience entries - NO markdown found")
    
    def test_ats_cv_experience_bullets_no_markdown(self):
        """CRITICAL: Test that ATS experience bullets have NO markdown"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        experience = ats_cv.get("experience", [])
        
        markdown_found = []
        for exp in experience:
            bullets = exp.get("bullets", [])
            for bullet in bullets:
                if "**" in bullet:
                    markdown_found.append(f"** found in: {bullet[:100]}")
                if bullet and bullet[0] in ["*", "-", "•"]:
                    markdown_found.append(f"Bullet char at start: {bullet[:50]}")
        
        assert len(markdown_found) == 0, f"Markdown found in ATS bullets: {markdown_found}"
        print(f"Checked {len(experience)} ATS experience entries - NO markdown found")
    
    def test_natural_cv_skills_no_markdown(self):
        """Test that skills are properly formatted without markdown"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        skills = natural_cv.get("skills", {})
        
        # Skills can be string or object
        if isinstance(skills, str):
            assert "**" not in skills, f"Skills should NOT contain ** asterisks"
            print(f"Skills (string): {skills[:200]}")
        elif isinstance(skills, dict):
            for category, skill_list in skills.items():
                if isinstance(skill_list, str):
                    assert "**" not in skill_list, f"Skills category '{category}' should NOT contain ** asterisks"
                print(f"Skills category '{category}': {skill_list}")
    
    def test_ats_cv_skills_no_markdown(self):
        """Test that ATS skills are properly formatted without markdown"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        skills = ats_cv.get("skills", {})
        
        # Skills can be string or object
        if isinstance(skills, str):
            assert "**" not in skills, f"ATS Skills should NOT contain ** asterisks"
            print(f"ATS Skills (string): {skills[:200]}")
        elif isinstance(skills, dict):
            for category, skill_list in skills.items():
                if isinstance(skill_list, str):
                    assert "**" not in skill_list, f"ATS Skills category '{category}' should NOT contain ** asterisks"
                print(f"ATS Skills category '{category}': {skill_list}")
    
    def test_cv_has_ats_score(self):
        """Test that response includes ATS score estimate"""
        data = get_cv_generation_result()
        assert "ats_score_estimate" in data, "Response should include ats_score_estimate"
        score = data["ats_score_estimate"]
        assert isinstance(score, (int, float)), "ATS score should be a number"
        assert 0 <= score <= 100, f"ATS score should be 0-100, got {score}"
        print(f"ATS Score: {score}")
    
    def test_cv_has_keywords_added(self):
        """Test that response includes keywords_added"""
        data = get_cv_generation_result()
        assert "keywords_added" in data or "keywords_matched" in data, "Response should include keywords info"
        if "keywords_added" in data:
            keywords = data["keywords_added"]
            assert isinstance(keywords, list), "keywords_added should be a list"
            print(f"Keywords added: {len(keywords)} keywords")
    
    def test_cv_has_improvement_tips(self):
        """Test that response includes improvement tips"""
        data = get_cv_generation_result()
        if "improvement_tips" in data:
            tips = data["improvement_tips"]
            assert isinstance(tips, list), "improvement_tips should be a list"
            print(f"Improvement tips: {len(tips)} tips")


class TestCVStructure:
    """Test CV structure and content quality"""
    
    def test_natural_cv_has_summary(self):
        """Test that natural_cv has summary"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        assert "summary" in natural_cv, "natural_cv should have summary"
        assert len(natural_cv["summary"]) > 50, "Summary should be substantial"
    
    def test_natural_cv_has_experience(self):
        """Test that natural_cv has experience"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        assert "experience" in natural_cv, "natural_cv should have experience"
        assert len(natural_cv["experience"]) > 0, "Experience should have entries"
    
    def test_natural_cv_has_skills(self):
        """Test that natural_cv has skills"""
        data = get_cv_generation_result()
        natural_cv = data.get("natural_cv", {})
        assert "skills" in natural_cv, "natural_cv should have skills"
    
    def test_ats_cv_has_summary(self):
        """Test that ats_cv has summary"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        assert "summary" in ats_cv, "ats_cv should have summary"
        assert len(ats_cv["summary"]) > 50, "ATS Summary should be substantial"
    
    def test_ats_cv_has_experience(self):
        """Test that ats_cv has experience"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        assert "experience" in ats_cv, "ats_cv should have experience"
        assert len(ats_cv["experience"]) > 0, "ATS Experience should have entries"
    
    def test_ats_cv_has_skills(self):
        """Test that ats_cv has skills"""
        data = get_cv_generation_result()
        ats_cv = data.get("ats_cv", {})
        assert "skills" in ats_cv, "ats_cv should have skills"


def test_print_cv_sample():
    """Print a sample of the generated CV for manual inspection"""
    data = get_cv_generation_result()
    
    print("\n" + "="*60)
    print("CV GENERATION RESULT SAMPLE")
    print("="*60)
    
    natural_cv = data.get("natural_cv", {})
    ats_cv = data.get("ats_cv", {})
    
    print("\n--- NATURAL CV ---")
    if "header" in natural_cv:
        print(f"Header Name: {natural_cv['header'].get('name', 'N/A')}")
        print(f"Header Contact: {natural_cv['header'].get('contact', 'N/A')}")
    print(f"Summary: {natural_cv.get('summary', 'N/A')[:300]}...")
    
    print("\n--- ATS CV ---")
    if "header" in ats_cv:
        print(f"Header Name: {ats_cv['header'].get('name', 'N/A')}")
        print(f"Header Contact: {ats_cv['header'].get('contact', 'N/A')}")
    print(f"Summary: {ats_cv.get('summary', 'N/A')[:300]}...")
    
    print(f"\nATS Score: {data.get('ats_score_estimate', 'N/A')}")
    print(f"Human Voice Score: {data.get('human_voice_score', 'N/A')}")
    print("="*60)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
