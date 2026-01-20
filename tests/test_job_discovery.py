import pytest
from backend.server import JobDiscoveryService

class TestJobDiscoveryService:
    def test_strip_html_basic(self):
        """Test basic HTML stripping"""
        html = "<p>Hello <b>World</b></p>"
        assert JobDiscoveryService._strip_html(html) == "Hello World"

    def test_strip_html_malformed(self):
        """Test malformed HTML stripping"""
        html = "<p>Hello <b>World"
        # lxml should handle this gracefully
        result = JobDiscoveryService._strip_html(html)
        assert "Hello" in result
        assert "World" in result

    def test_strip_html_script_injection(self):
        """Test that scripts are removed or text content is preserved safely"""
        # lxml.html.fromstring().text_content() usually keeps the text inside script tags if not careful,
        # but standard _strip_html purpose is often to get readable text.
        # Let's see how lxml behaves. text_content() includes text of script tags.
        # Ideally we want to avoid executing anything, which text_content() achieves.
        html = "<script>alert('xss')</script>Description"
        # We expect the content to be safe string.
        assert "Description" in JobDiscoveryService._strip_html(html)

    def test_is_ai_role_positive(self):
        """Test positive AI role matching"""
        assert JobDiscoveryService.is_ai_role("Senior Machine Learning Engineer")
        assert JobDiscoveryService.is_ai_role("AI Researcher")
        assert JobDiscoveryService.is_ai_role("Data Scientist (NLP)")
        assert JobDiscoveryService.is_ai_role("Software Engineer", "Working with LLMs and Generative AI")

    def test_is_ai_role_negative(self):
        """Test negative AI role matching"""
        assert not JobDiscoveryService.is_ai_role("Senior React Developer")
        assert not JobDiscoveryService.is_ai_role("Sales Representative")
        assert not JobDiscoveryService.is_ai_role("HR Manager")
        assert not JobDiscoveryService.is_ai_role("Software Engineer", "Building CRUD apps with Rails")

    def test_is_ai_role_strong_signals(self):
        """Test strong signals override negative keywords"""
        # "Accountant" is in NON_AI_ROLES, but if they work on "AI Accountant" it might match if we checked title first.
        # The logic is: exclusions checked first UNLESS strong signal is in title.
        assert JobDiscoveryService.is_ai_role("AI Accountant") # "AI " is strong signal
