#!/usr/bin/env python3

import requests
import sys
import json

class ExistingUserTester:
    def __init__(self, base_url="https://careershift-app.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None

    def test_existing_user_login(self):
        """Test login with existing user that has analysis data"""
        login_data = {
            "email": "testuser1@example.com",
            "password": "Test123!"
        }
        
        url = f"{self.base_url}/auth/login"
        try:
            response = requests.post(url, json=login_data, timeout=30)
            print(f"Login Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get('access_token')
                self.user_id = result.get('user', {}).get('id')
                print(f"✅ Login successful - User ID: {self.user_id}")
                return True
            else:
                print(f"❌ Login failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False

    def test_get_existing_analyses(self):
        """Get existing analyses for the user"""
        if not self.token:
            print("❌ No token available")
            return False
        
        url = f"{self.base_url}/analyses"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Get Analyses Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                analyses = result.get('analyses', [])
                print(f"✅ Found {len(analyses)} existing analyses")
                
                if analyses:
                    # Print details of first analysis
                    first_analysis = analyses[0]
                    print(f"   Analysis ID: {first_analysis.get('id')}")
                    print(f"   Target Role: {first_analysis.get('target_role', {}).get('name', 'N/A')}")
                    print(f"   Created: {first_analysis.get('created_at', 'N/A')}")
                    
                    # Check if analysis has complete data
                    analysis_result = first_analysis.get('analysis_result', {})
                    career_fit = analysis_result.get('career_fit', {})
                    print(f"   Career Fit Score: {career_fit.get('score', 'N/A')}")
                    print(f"   Career Fit Rating: {career_fit.get('rating', 'N/A')}")
                    
                    return first_analysis.get('id')
                else:
                    print("   No analyses found for this user")
                    return None
            else:
                print(f"❌ Failed to get analyses: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error getting analyses: {str(e)}")
            return False

    def test_get_specific_analysis(self, analysis_id):
        """Get specific analysis by ID"""
        if not self.token or not analysis_id:
            print("❌ No token or analysis ID available")
            return False
        
        url = f"{self.base_url}/analyses/{analysis_id}"
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Get Specific Analysis Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Successfully retrieved analysis {analysis_id}")
                
                # Check completeness of analysis data
                analysis_result = result.get('analysis_result', {})
                sections = [
                    'career_fit', 'ats_score', 'transferable_skills', 
                    'skill_gaps', 'learning_path', 'cv_natural', 
                    'cv_ats_optimized', 'next_steps'
                ]
                
                print("   Analysis sections present:")
                for section in sections:
                    present = section in analysis_result
                    status = "✅" if present else "❌"
                    print(f"     {status} {section}")
                
                return True
            else:
                print(f"❌ Failed to get analysis: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error getting analysis: {str(e)}")
            return False

    def run_tests(self):
        """Run all tests for existing user"""
        print("🔍 Testing Existing User with Analysis Data")
        print("=" * 50)
        
        # Test login
        if self.test_existing_user_login():
            # Get analyses list
            analysis_id = self.test_get_existing_analyses()
            
            # Test specific analysis if found
            if analysis_id:
                self.test_get_specific_analysis(analysis_id)
                return analysis_id
        
        return None

def main():
    tester = ExistingUserTester()
    analysis_id = tester.run_tests()
    
    if analysis_id:
        print(f"\n✅ Existing user test successful - Analysis ID: {analysis_id}")
        return 0
    else:
        print("\n❌ Existing user test failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())