#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_ai_endpoints():
    """Quick test of the 5 AI endpoints mentioned in review request"""
    
    base_url = "https://careershift-app.preview.emergentagent.com/api"
    
    # Register a new user first
    timestamp = datetime.now().strftime('%H%M%S')
    user_data = {
        "name": f"Quick Test User {timestamp}",
        "email": f"quicktest{timestamp}@example.com", 
        "password": "TestPass123!"
    }
    
    print("🔐 Registering test user...")
    response = requests.post(f"{base_url}/auth/register", json=user_data, timeout=30)
    if response.status_code != 200:
        print(f"❌ Registration failed: {response.status_code}")
        return
    
    token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    print(f"✅ User registered successfully")
    
    # Sample resume text
    resume_text = """John Smith - Senior Software Engineer with 5+ years experience in Python, machine learning, and cloud technologies.

EXPERIENCE:
• Senior Software Engineer at TechCorp (2020-2024)
  - Built ML pipelines using Python, TensorFlow, and PyTorch serving 1M+ users
  - Developed REST APIs with FastAPI and Django handling 10K+ requests/second
  - Deployed models on AWS using Docker, Kubernetes, and SageMaker
  - Led team of 4 engineers on machine learning projects
  - Improved model accuracy by 25% through advanced feature engineering

EDUCATION:
Master's in Computer Science, Stanford University (2018)

SKILLS: Python, JavaScript, TensorFlow, PyTorch, AWS, Docker, Kubernetes, FastAPI, Django, SQL, MongoDB, Machine Learning, Deep Learning, MLOps, Git, Linux"""

    results = {}
    
    # 1. CV Generation
    print(f"\n1️⃣ Testing CV Generation...")
    cv_data = {
        "resume_text": resume_text,
        "target_role_id": "ml_engineer",
        "target_region": "us"
    }
    
    try:
        response = requests.post(f"{base_url}/cv/generate", json=cv_data, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            versions = result.get('versions', [])
            if versions:
                ats_score = versions[0].get('ats_score', 0)
                human_score = versions[0].get('human_appeal_score', 0)
                print(f"   ✅ CV Generation: SUCCESS (ATS: {ats_score}, Human: {human_score})")
                results['cv_generation'] = {'success': True, 'ats_score': ats_score, 'human_score': human_score}
            else:
                print(f"   ❌ CV Generation: No versions returned")
                results['cv_generation'] = {'success': False, 'error': 'No versions'}
        else:
            print(f"   ❌ CV Generation: {response.status_code} - {response.text[:200]}")
            results['cv_generation'] = {'success': False, 'error': f"{response.status_code}"}
    except Exception as e:
        print(f"   ❌ CV Generation: {str(e)}")
        results['cv_generation'] = {'success': False, 'error': str(e)}
    
    # 2. Resume Scanner
    print(f"\n2️⃣ Testing Resume Scanner...")
    scan_data = {
        "resume_text": resume_text,
        "target_role_id": "ml_engineer"
    }
    
    try:
        response = requests.post(f"{base_url}/resume/scan", json=scan_data, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            ats_score = result.get('ats_score', 0)
            human_score = result.get('human_appeal_score', 0)
            print(f"   ✅ Resume Scanner: SUCCESS (ATS: {ats_score}, Human: {human_score})")
            results['resume_scanner'] = {'success': True, 'ats_score': ats_score, 'human_score': human_score}
        else:
            print(f"   ❌ Resume Scanner: {response.status_code} - {response.text[:200]}")
            results['resume_scanner'] = {'success': False, 'error': f"{response.status_code}"}
    except Exception as e:
        print(f"   ❌ Resume Scanner: {str(e)}")
        results['resume_scanner'] = {'success': False, 'error': str(e)}
    
    # 3. Learning Path Generation
    print(f"\n3️⃣ Testing Learning Path Generation...")
    learning_data = {
        "current_role": "Software Engineer",
        "years_experience": 3,
        "current_skills": ["Python"],
        "target_role_id": "ml_engineer",
        "location": "US"
    }
    
    try:
        response = requests.post(f"{base_url}/learning-path/generate", json=learning_data, headers=headers, timeout=90)
        if response.status_code == 200:
            result = response.json()
            target_role = result.get('target_role', '')
            path_id = result.get('path_id', '')
            print(f"   ✅ Learning Path: SUCCESS (Role: {target_role}, ID: {path_id[:8]}...)")
            results['learning_path'] = {'success': True, 'target_role': target_role}
        else:
            print(f"   ❌ Learning Path: {response.status_code} - {response.text[:200]}")
            results['learning_path'] = {'success': False, 'error': f"{response.status_code}"}
    except Exception as e:
        print(f"   ❌ Learning Path: {str(e)}")
        results['learning_path'] = {'success': False, 'error': str(e)}
    
    # 4. Cover Letter Generation
    print(f"\n4️⃣ Testing Cover Letter Generation...")
    cover_data = {
        "resume_text": resume_text,
        "job_description": "We are seeking a Senior ML Engineer to join our AI team. Requirements: 5+ years ML experience, Python, TensorFlow/PyTorch, AWS.",
        "company_name": "TechCorp",
        "target_role": "ML Engineer"
    }
    
    try:
        response = requests.post(f"{base_url}/cover-letter/generate", json=cover_data, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            cover_id = result.get('cover_letter_id', '')
            company = result.get('company_name', '')
            print(f"   ✅ Cover Letter: SUCCESS (Company: {company}, ID: {cover_id[:8]}...)")
            results['cover_letter'] = {'success': True, 'company': company}
        else:
            print(f"   ❌ Cover Letter: {response.status_code} - {response.text[:200]}")
            results['cover_letter'] = {'success': False, 'error': f"{response.status_code}"}
    except Exception as e:
        print(f"   ❌ Cover Letter: {str(e)}")
        results['cover_letter'] = {'success': False, 'error': str(e)}
    
    # 5. Career Analysis (correct endpoint: /api/analyze)
    print(f"\n5️⃣ Testing Career Analysis...")
    analysis_data = {
        "resume_data": {
            "raw_text": resume_text,
            "current_role": "Software Engineer",
            "years_experience": 5,
            "education": ["Master's in Computer Science"],  # Fixed: should be list
            "skills": ["Python", "TensorFlow", "PyTorch", "AWS", "Machine Learning"],
            "certifications": [],
            "companies": ["TechCorp"]
        },
        "target_role_id": "ml_engineer",
        "background_context": {
            "current_role": "Software Engineer",
            "years_experience": 5,
            "education_level": "Master's",
            "primary_skills": ["Python", "Machine Learning", "TensorFlow"],
            "career_goals": "Transition to ML Engineer role",
            "location": "US"
        }
    }
    
    try:
        response = requests.post(f"{base_url}/analyze", json=analysis_data, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            analysis_id = result.get('analysis_id', '')
            target_role = result.get('target_role', {}).get('name', '')
            print(f"   ✅ Career Analysis: SUCCESS (Role: {target_role}, ID: {analysis_id[:8]}...)")
            results['career_analysis'] = {'success': True, 'target_role': target_role}
        else:
            print(f"   ❌ Career Analysis: {response.status_code} - {response.text[:200]}")
            results['career_analysis'] = {'success': False, 'error': f"{response.status_code}"}
    except Exception as e:
        print(f"   ❌ Career Analysis: {str(e)}")
        results['career_analysis'] = {'success': False, 'error': str(e)}
    
    # Score Consistency Check
    print(f"\n🎯 Score Consistency Check...")
    if results.get('cv_generation', {}).get('success') and results.get('resume_scanner', {}).get('success'):
        cv_ats = results['cv_generation']['ats_score']
        cv_human = results['cv_generation']['human_score']
        scanner_ats = results['resume_scanner']['ats_score']
        scanner_human = results['resume_scanner']['human_score']
        
        ats_diff = abs(cv_ats - scanner_ats)
        human_diff = abs(cv_human - scanner_human)
        
        print(f"   CV Generator:    ATS={cv_ats}, Human={cv_human}")
        print(f"   Resume Scanner:  ATS={scanner_ats}, Human={scanner_human}")
        print(f"   Differences:     ATS={ats_diff}, Human={human_diff}")
        
        if ats_diff <= 2 and human_diff <= 2:
            print(f"   ✅ Score Consistency: PASSED (within 2 point tolerance)")
            results['score_consistency'] = {'success': True}
        else:
            print(f"   ❌ Score Consistency: FAILED (differences too large)")
            results['score_consistency'] = {'success': False}
    else:
        print(f"   ⚠️ Score Consistency: Cannot test (CV or Scanner failed)")
        results['score_consistency'] = {'success': False, 'error': 'Prerequisites failed'}
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 FINAL SUMMARY")
    print(f"=" * 60)
    
    success_count = sum(1 for r in results.values() if r.get('success', False))
    total_count = len(results)
    
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    print(f"📈 Success Rate: {(success_count/total_count)*100:.1f}%")
    
    print(f"\n📋 Individual Results:")
    for feature, result in results.items():
        status = "✅ PASS" if result.get('success') else "❌ FAIL"
        print(f"   {feature.replace('_', ' ').title()}: {status}")
    
    return results

if __name__ == "__main__":
    test_ai_endpoints()