"""
Test PDF OCR Parsing - Iteration 5
Tests the OCR fallback for image-based/scanned PDFs

The main bug was that PyPDF2 extracted 0 characters from image-based PDFs.
We added OCR support using pytesseract and pdf2image as a fallback.
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://careershift-app.preview.emergentagent.com').rstrip('/')
TEST_PDF_PATH = "/tmp/test_resume.pdf"


class TestPDFOCRParsing:
    """Tests for PDF parsing with OCR fallback"""
    
    def test_pdf_file_exists(self):
        """Verify test PDF file exists"""
        assert os.path.exists(TEST_PDF_PATH), f"Test PDF not found at {TEST_PDF_PATH}"
        file_size = os.path.getsize(TEST_PDF_PATH)
        assert file_size > 0, "Test PDF file is empty"
        print(f"✓ Test PDF exists: {file_size} bytes")
    
    def test_resume_parse_endpoint_with_image_pdf(self):
        """Test POST /api/resume/parse with image-based PDF - main OCR test"""
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'file': ('test_resume.pdf', f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/api/resume/parse", files=files)
        
        # Status code assertion
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        # Data assertions
        data = response.json()
        assert "resume_data" in data, "Response missing 'resume_data' key"
        
        resume_data = data["resume_data"]
        
        # Verify raw_text extraction (OCR should extract at least 2000 chars)
        raw_text = resume_data.get("raw_text", "")
        assert len(raw_text) >= 2000, f"Expected at least 2000 chars, got {len(raw_text)}"
        print(f"✓ OCR extracted {len(raw_text)} characters")
        
        # Verify the content is from the Solar PV Designer resume
        assert "ROHAN VERMA" in raw_text or "rohan" in raw_text.lower(), "Expected to find 'ROHAN VERMA' in resume"
        assert "Solar" in raw_text or "solar" in raw_text.lower(), "Expected to find 'Solar' in resume"
        print("✓ Resume content verified (Solar PV Designer)")
        
        # Verify skills extraction
        skills = resume_data.get("skills", [])
        assert isinstance(skills, list), "Skills should be a list"
        assert len(skills) > 0, "Expected at least some skills to be extracted"
        print(f"✓ Skills extracted: {skills}")
        
        # Verify expected skills from the Solar PV Designer resume
        expected_skills = ["python", "sql", "aws"]  # Common skills that should be found
        found_expected = [s for s in expected_skills if s in skills]
        assert len(found_expected) > 0, f"Expected to find at least one of {expected_skills} in {skills}"
        print(f"✓ Found expected skills: {found_expected}")
    
    def test_resume_parse_returns_all_fields(self):
        """Verify all expected fields are returned in resume_data"""
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'file': ('test_resume.pdf', f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/api/resume/parse", files=files)
        
        assert response.status_code == 200
        data = response.json()
        resume_data = data["resume_data"]
        
        # Check all expected fields exist
        expected_fields = ["raw_text", "current_role", "years_experience", "education", "skills", "certifications", "companies"]
        for field in expected_fields:
            assert field in resume_data, f"Missing field: {field}"
        
        print(f"✓ All expected fields present: {expected_fields}")
    
    def test_resume_parse_text_input(self):
        """Test POST /api/resume/parse with text input (not file)"""
        test_text = """
        John Doe
        Software Engineer with 5 years of experience
        Skills: Python, JavaScript, AWS, Docker, Kubernetes
        Education: Bachelor's in Computer Science
        """
        
        response = requests.post(
            f"{BASE_URL}/api/resume/parse",
            data={"text": test_text}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        resume_data = data["resume_data"]
        assert "python" in resume_data.get("skills", []), "Expected 'python' in skills"
        assert "javascript" in resume_data.get("skills", []), "Expected 'javascript' in skills"
        assert resume_data.get("years_experience") == 5, "Expected 5 years experience"
        print("✓ Text input parsing works correctly")
    
    def test_resume_parse_no_input_returns_400(self):
        """Test POST /api/resume/parse with no input returns 400"""
        response = requests.post(f"{BASE_URL}/api/resume/parse")
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("✓ No input returns 400 as expected")
    
    def test_ocr_extracts_meaningful_content(self):
        """Verify OCR extracts meaningful content from the Solar PV Designer resume"""
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'file': ('test_resume.pdf', f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/api/resume/parse", files=files)
        
        assert response.status_code == 200
        raw_text = response.json()["resume_data"]["raw_text"].lower()
        
        # Check for key content from the Solar PV Designer resume
        content_checks = [
            ("name", "rohan" in raw_text or "verma" in raw_text),
            ("role", "solar" in raw_text or "designer" in raw_text),
            ("location", "hyderabad" in raw_text or "india" in raw_text),
            ("skills_section", "python" in raw_text or "sql" in raw_text),
        ]
        
        passed = 0
        for check_name, result in content_checks:
            if result:
                passed += 1
                print(f"✓ Content check '{check_name}' passed")
            else:
                print(f"✗ Content check '{check_name}' failed")
        
        assert passed >= 3, f"Expected at least 3/4 content checks to pass, got {passed}/4"
        print(f"✓ OCR content verification: {passed}/4 checks passed")


class TestOCRAvailability:
    """Tests to verify OCR libraries are available"""
    
    def test_health_endpoint(self):
        """Verify backend is healthy"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print("✓ Backend is healthy")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
